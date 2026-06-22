#!/usr/bin/env python3
"""
打板策略 —— 首板早盘板选股器
================================
只做首板（第一个涨停），要求早盘封板、有换手、有资金、属热点。

规则
----
✅ 首板（连板数 = 1）
✅ 首次封板时间 < 10:00
✅ 封单额 > 5000 万
✅ 换手率 5% ~ 15%
✅ 流通市值 30 ~ 100 亿
✅ 所属板块为当前热点（涨停家数 Top 8）
✅ 最新价 < 40 元
✅ 主板 A 股（60/00 开头）
❌ ST / *ST / 尾盘板 / 一字板

使用
----
    python3 daban_scanner.py                    # 当天扫描（终端输出）
    python3 daban_scanner.py 20260617           # 指定日期
    python3 daban_scanner.py --ci               # CI 模式：输出 scan_results.json
    python3 daban_scanner.py --near-miss        # 额外输出近失名单
"""

import argparse
import json
import os
import sys
import warnings
from datetime import date, datetime

import akshare as ak
import pandas as pd

warnings.filterwarnings("ignore")

# ============================================================
# 策略参数
# ============================================================
SEAL_TIME_LIMIT = "103000"
MIN_SEAL_AMOUNT = 50_000_000
MIN_TURNOVER = 3.0
MAX_TURNOVER = 20.0
MIN_MCAP = 3_000_000_000
MAX_MCAP = 30_000_000_000
MAX_PRICE = 40.0
BOARD_NUM = 1
HOT_SECTOR_TOP_N = 12

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(SCRIPT_DIR, "scan_results.json")

# ============================================================
# 工具函数
# ============================================================
def is_main_board(code: str) -> bool:
    return str(code).startswith("60") or str(code).startswith("00")


def is_st(name: str) -> bool:
    return "ST" in str(name).upper().strip()


def parse_seal_time(val) -> str:
    if pd.isna(val):
        return "999999"
    s = str(val).strip().replace(":", "").replace(".", "")
    return s.zfill(6)[:6]


def identify_hot_sectors(df: pd.DataFrame, top_n: int = HOT_SECTOR_TOP_N) -> set:
    if "所属行业" not in df.columns:
        return set()
    sector_counts = df.groupby("所属行业").size().sort_values(ascending=False)
    return set(sector_counts.head(top_n).index.tolist())


# ============================================================
# 核心扫描
# ============================================================
def scan(date_str: str | None = None, near_miss: bool = False, ci_mode: bool = False):
    if date_str is None:
        date_str = date.today().strftime("%Y%m%d")

    if not ci_mode:
        print(f"📡 正在获取 {date_str} 涨停池数据 ...")

    try:
        raw = ak.stock_zt_pool_em(date=date_str)
    except Exception as e:
        err = {"error": str(e), "date": date_str}
        if ci_mode:
            json.dump(err, open(RESULTS_FILE, "w"), ensure_ascii=False, indent=2)
        else:
            print(f"❌ 获取涨停池失败: {e}")
        sys.exit(1)

    if raw.empty:
        err = {"error": "empty", "date": date_str, "message": "无涨停数据（可能非交易日）"}
        if ci_mode:
            json.dump(err, open(RESULTS_FILE, "w"), ensure_ascii=False, indent=2)
        else:
            print("⚠️ 当日无涨停数据（可能非交易日）。")
        sys.exit(0 if ci_mode else 0)

    df = raw.copy()
    total = len(df)

    # 热点板块
    hot_sectors = identify_hot_sectors(df)

    # 过滤管道
    mask_st     = ~df["名称"].apply(is_st)
    mask_main   = df["代码"].apply(is_main_board)
    mask_first  = df["连板数"] == BOARD_NUM
    df["_st"]   = df["首次封板时间"].apply(parse_seal_time)
    mask_seal   = df["_st"] < SEAL_TIME_LIMIT
    df["封板资金"] = pd.to_numeric(df["封板资金"], errors="coerce").fillna(0)
    mask_amount = df["封板资金"] >= MIN_SEAL_AMOUNT
    df["换手率"]   = pd.to_numeric(df["换手率"], errors="coerce").fillna(0)
    mask_to     = (df["换手率"] >= MIN_TURNOVER) & (df["换手率"] <= MAX_TURNOVER)
    df["流通市值"] = pd.to_numeric(df["流通市值"], errors="coerce").fillna(0)
    mask_mcap   = (df["流通市值"] >= MIN_MCAP) & (df["流通市值"] <= MAX_MCAP)
    df["最新价"]   = pd.to_numeric(df["最新价"], errors="coerce").fillna(999)
    mask_price  = df["最新价"] <= MAX_PRICE
    mask_sector = df["所属行业"].isin(hot_sectors) if hot_sectors else pd.Series([True] * len(df), index=df.index)

    stages = {
        "total": total,
        "excl_st": int((~mask_st).sum()),
        "excl_board": int((~mask_main).sum()),
        "excl_not_first": int((~mask_first).sum()),
        "excl_late_seal": int((~mask_seal).sum()),
        "excl_low_seal": int((~mask_amount).sum()),
        "excl_turnover": int((~mask_to).sum()),
        "excl_mcap": int((~mask_mcap).sum()),
        "excl_price": int((~mask_price).sum()),
        "excl_sector": int((~mask_sector).sum()),
    }
    stages["candidates"] = int((mask_st & mask_main & mask_first & mask_seal & mask_amount & mask_to & mask_mcap & mask_price & mask_sector).sum())

    # 候选结果
    passed_all = mask_st & mask_main & mask_first & mask_seal & mask_amount & mask_to & mask_mcap & mask_price & mask_sector
    candidates = df[passed_all].copy()

    candidates_list = []
    for _, row in candidates.sort_values("封板资金", ascending=False).iterrows():
        candidates_list.append({
            "code": str(row["代码"]),
            "name": str(row["名称"]),
            "price": round(float(row["最新价"]), 2),
            "change_pct": round(float(row["涨跌幅"]), 2),
            "turnover": round(float(row["换手率"]), 2),
            "seal_amount": int(row["封板资金"]),
            "seal_amount_str": f"{row['封板资金']/1e4:.0f}万",
            "first_seal_time": str(row["首次封板时间"]),
            "board_num": int(row["连板数"]),
            "float_mcap": int(row["流通市值"]),
            "float_mcap_str": f"{row['流通市值']/1e8:.1f}亿",
            "volume": int(row.get("成交额", 0)),
            "volume_str": f"{row.get('成交额', 0)/1e4:.0f}万",
            "sector": str(row["所属行业"]),
            "board_stat": str(row.get("涨停统计", "")),
            "is_hot_sector": str(row["所属行业"]) in hot_sectors,
        })

    # 热点板块统计
    sector_counts = raw.groupby("所属行业").size().sort_values(ascending=False)
    hot_sector_list = []
    for s, c in sector_counts.head(HOT_SECTOR_TOP_N).items():
        hot_sector_list.append({"sector": str(s), "count": int(c)})

    # 近失名单
    near_miss_list = []
    if near_miss or ci_mode:
        # 构建条件判定
        judges = [
            ("非ST", mask_st),
            ("主板", mask_main),
            ("首板", mask_first),
            ("<10:00", mask_seal),
            ("封单>5000万", mask_amount),
            ("换手5-15%", mask_to),
            ("市值30-100亿", mask_mcap),
            ("价<40", mask_price),
            ("热点板块", mask_sector),
        ]
        fail_counts = pd.Series(0, index=df.index)
        fail_reasons = pd.Series([[] for _ in range(len(df))], index=df.index)
        for label, mask in judges:
            failed = ~mask
            fail_counts += failed.astype(int)
            for idx in df[failed].index:
                fail_reasons[idx].append(label)

        near_mask = (fail_counts >= 1) & (fail_counts <= 2) & ~passed_all
        near = df[near_mask].copy()
        near = near.sort_values("封板资金", ascending=False)
        for _, row in near.iterrows():
            nm = {
                "code": str(row["代码"]),
                "name": str(row["名称"]),
                "price": round(float(row["最新价"]), 2),
                "change_pct": round(float(row["涨跌幅"]), 2),
                "turnover": round(float(row["换手率"]), 2),
                "seal_amount_str": f"{row['封板资金']/1e4:.0f}万",
                "seal_amount": int(row["封板资金"]),
                "first_seal_time": str(row["首次封板时间"]),
                "float_mcap_str": f"{row['流通市值']/1e8:.1f}亿",
                "sector": str(row["所属行业"]),
                "failed_rules": [r for r in fail_reasons.get(row.name, []) if isinstance(r, str)],
            }
            near_miss_list.append(nm)

    # 构建输出
    result = {
        "date": date_str,
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_limit_ups": total,
        "stages": stages,
        "hot_sectors": hot_sector_list,
        "candidates": candidates_list,
        "near_miss": near_miss_list,
    }

    # 保存 JSON
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Webhook notification (CI mode only, same bot as wyckoff-picker)
    if ci_mode:
        send_feishu_webhook(result)

    if not ci_mode:
        # 终端输出
        print(f"\n📊 筛选漏斗 (原始涨停: {total})")
        for label, key in [
            ("ST / *ST", "excl_st"),
            ("创业板/科创板/北证", "excl_board"),
            ("非首板", "excl_not_first"),
            ("尾盘板(≥10:00)", "excl_late_seal"),
            ("封单额不足5000万", "excl_low_seal"),
            ("换手率不达标", "excl_turnover"),
            ("流通市值不达标", "excl_mcap"),
            ("股价≥40元", "excl_price"),
            ("非热点板块", "excl_sector"),
        ]:
            print(f"   ├─ 排除 {label:16s}: {stages[key]}")

        print(f"   └─ ★ 最终候选:              {stages['candidates']}")

        if hot_sector_list:
            print(f"\n🔥 热点板块 (涨停家数 Top {HOT_SECTOR_TOP_N}):")
            for h in hot_sector_list:
                print(f"   {h['sector']}: {h['count']} 家 ★")

        if candidates_list:
            print("\n" + "=" * 80)
            print("  🎯 打板策略 · 首板早盘板 候选标的")
            print("=" * 80)
            for i, c in enumerate(candidates_list):
                print(f"\n  {i+1}. {c['code']} {c['name']}  ¥{c['price']}  {c['change_pct']:+.2f}%")
                print(f"     封板: {c['first_seal_time']} | 封单: {c['seal_amount_str']} | 换手: {c['turnover']:.2f}%")
                print(f"     市值: {c['float_mcap_str']} | 成交: {c['volume_str']} | 板块: {c['sector']}")
                print(f"     涨停统计: {c['board_stat']}")
        else:
            print("\n😔 当日无完全符合条件的打板标的。")

        if near_miss and near_miss_list:
            print("\n" + "=" * 80)
            print("  🔍 近失名单（差 1-2 个条件）")
            print("=" * 80)
            for i, nm in enumerate(near_miss_list[:15]):
                print(f"  {i+1:2d}. {nm['code']} {nm['name']:8s} ¥{nm['price']} | 封单{nm['seal_amount_str']} | "
                      f"封板{nm['first_seal_time']} | 市值{nm['float_mcap_str']} | {nm['sector']}")
                print(f"      未通过: {', '.join(nm['failed_rules'])}")

        print(f"\n💾 完整数据已保存至 {RESULTS_FILE}")
    else:
        # CI 模式：简洁输出
        print(f"✅ {date_str} 扫描完成")
        print(f"   涨停总数: {total} → 打板候选: {stages['candidates']}")
        if candidates_list:
            print(f"   候选标的:")
            for c in candidates_list:
                print(f"     {c['code']} {c['name']} ¥{c['price']} 封单{c['seal_amount_str']} 换手{c['turnover']:.1f}% 板块:{c['sector']}")
        else:
            print(f"   ⚠️ 无候选标的")
        if near_miss_list:
            print(f"   近失标的 ({len(near_miss_list)} 只):")
            for nm in near_miss_list[:10]:
                print(f"     {nm['code']} {nm['name']} 未通过: {', '.join(nm['failed_rules'])}")

    return result


def send_feishu_webhook(data: dict):
    """Send scan results via Feishu webhook (same bot as wyckoff-picker)."""
    webhook = os.environ.get("FEISHU_WEBHOOK", "").replace("/bot/v2/hook/", "/bot/hook/")
    if not webhook:
        print("[webhook] FEISHU_WEBHOOK not set, skipping notification")
        return

    candidates = data.get("candidates", [])
    near = data.get("near_miss", [])
    hot = data.get("hot_sectors", [])[:5]

    lines = []
    lines.append("\U0001f3af 打板策略 | {} 早盘扫描\n".format(data['date']))

    if candidates:
        lines.append("\u2705 候选: {} 只\n".format(len(candidates)))
        for c in candidates:
            lines.append("\U0001f3c6 **{} {}** \u00a5{} {:+.2f}%\n".format(
                c['code'], c['name'], c['price'], c['change_pct']))
            lines.append("   封板 {} | 封单 {} | 换手 {:.1f}%\n".format(
                c['first_seal_time'], c['seal_amount_str'], c['turnover']))
            lines.append("   市值 {} | 板块 {}\n\n".format(
                c['float_mcap_str'], c['sector']))
    else:
        lines.append("\u26a0\ufe0f 无候选标的 (共 {} 只涨停)\n\n".format(data['total_limit_ups']))

    if hot:
        lines.append("\U0001f525 热点板块:\n")
        for h in hot:
            lines.append("   {}: {} 家\n".format(h['sector'], h['count']))

    if near:
        lines.append("\n\U0001f50d 近失标的 ({} 只，差 1-2 条件):\n".format(len(near)))
        for nm in near[:5]:
            lines.append("   {} {} \u00a5{} | {}\n".format(
                nm['code'], nm['name'], nm['price'], nm['sector']))
            lines.append("   \u2192 {}\n".format(', '.join(nm['failed_rules'])))

    lines.append("\n\u23f0 {} | Daban Scanner | \u4ec5\u4f9b\u53c2\u8003\n".format(
        data.get('scanned_at', '')))

    payload = {"title": "\U0001f3af {} 打板策略选股".format(data['date']), "text": "".join(lines)}
    import requests
    r = requests.post(webhook, json=payload, timeout=10)
    print("[webhook] {} ({})".format('OK' if r.status_code == 200 else 'FAIL', r.status_code))


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="打板策略 · 首板早盘板选股器")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYYMMDD，默认当天")
    parser.add_argument("--ci", action="store_true", help="CI 模式：输出 JSON 结果文件")
    parser.add_argument("--near-miss", "-n", action="store_true", help="输出近失名单")
    args = parser.parse_args()

    scan(date_str=args.date, near_miss=args.near_miss, ci_mode=args.ci)
