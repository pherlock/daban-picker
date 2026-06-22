#!/usr/bin/env python3
"""
daban_vt_enhance.py — Vibe-Trading 增强版打板扫描器
=====================================================
在原 daban_scanner.py 基础上增加三层分析：

Layer 1 — 集合竞价分析
  • 竞价量比（竞价总量 / 近5日均量）
  • 竞价价格趋势（9:15→9:25 价格走向）
  • 末段抢筹检测（9:20-9:25 量价齐升）

Layer 2 — 开盘5分钟量价分析
  • 开盘确认信号（高开高走 vs 高开低走）
  • 开盘量能确认（5分钟量 / 竞价量）
  • 开盘价格斜率

Layer 3 — Alpha Zoo 三因子评分
  • 动量因子 (Carhart UMD): 12月收益 - 1月收益 → 趋势强度
  • 价值因子 (FF HML proxy): -252日收益 → 反转深度
  • 质量因子 (FF RMW proxy): -60日波动率 → 稳健性
  • 组内横截面 z-score 排名

策略参数（优化版）
  • 流通市值 30-300亿（放宽上限）
  • 换手率 3-20%（放宽上下限）
  • 封板时间 < 10:30（放宽30分钟）
  • 热点板块 Top 12（扩大覆盖）

使用
----
    python3 daban_vt_enhance.py                        # 今天扫描
    python3 daban_vt_enhance.py 20260623               # 指定日期
    python3 daban_vt_enhance.py --no-factor            # 跳过因子计算（快）
    python3 daban_vt_enhance.py --auction-only         # 仅竞价分析
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from datetime import date, datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(SCRIPT_DIR, "scan_results.json")
ENHANCED_FILE = os.path.join(SCRIPT_DIR, "enhanced_results.json")

# ============================================================
# 优化后的策略参数（相比原版：放宽市值/换手/时间/板块）
# ============================================================
OPTIMIZED = {
    "seal_time_limit": "103000",       # < 10:30（原 10:00）
    "min_seal_amount": 50_000_000,     # > 5000万（不变）
    "min_turnover": 3.0,               # > 3%（原 5%）
    "max_turnover": 20.0,              # < 20%（原 15%）
    "min_mcap": 3_000_000_000,         # > 30亿（不变）
    "max_mcap": 30_000_000_000,        # < 300亿（原 100亿）
    "max_price": 40.0,                 # < 40元（不变）
    "board_num": 1,                    # 首板（不变）
    "hot_sector_top_n": 12,            # Top 12（原 8）
}

# ============================================================
# 集合竞价分析
# ============================================================

def fetch_auction_data(symbol: str, date_str: str) -> pd.DataFrame | None:
    """获取集合竞价逐分钟数据 (9:15-9:25)。"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist_pre_min_em(
            symbol=symbol,
            start_time="09:15:00",
            end_time="09:25:00",
        )
        if df is None or df.empty:
            return None
        # 标准化列名
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception:
        return None


def analyze_auction(auction_df: pd.DataFrame | None) -> dict[str, Any]:
    """分析集合竞价数据，返回评分和信号。"""
    if auction_df is None or auction_df.empty:
        return {"status": "no_data", "score": 0, "signals": []}

    result: dict[str, Any] = {"status": "ok", "signals": [], "score": 0}
    col_map = _find_columns(auction_df)

    # --- 1. 竞价量比 ---
    vol_col = col_map.get("volume")
    price_col = col_map.get("price")
    if vol_col and price_col:
        total_vol = auction_df[vol_col].sum()
        late = auction_df.tail(5)
        # 用每分钟平均量作为参考（近似）
        avg_per_min = auction_df[vol_col].mean()
        if avg_per_min > 0:
            # 末段5分钟量比（9:20-9:25）
            late = auction_df.tail(5)
            early = auction_df.head(6)  # 9:15-9:20
            late_vol = late[vol_col].sum()
            early_vol = early[vol_col].sum()
            if early_vol > 0:
                vol_ratio = late_vol / early_vol
                result["vol_ratio_late_vs_early"] = round(vol_ratio, 2)
                if vol_ratio > 1.5:
                    result["signals"].append("末段放量抢筹")
                    result["score"] += 2
                elif vol_ratio > 1.0:
                    result["signals"].append("竞价量平稳")
                    result["score"] += 1

        # --- 2. 竞价价格趋势 ---
        first_price = auction_df[price_col].iloc[0]
        last_price = auction_df[price_col].iloc[-1]
        if first_price > 0:
            price_change = (last_price - first_price) / first_price
            result["price_trend_pct"] = round(price_change * 100, 2)
            if price_change > 0.005:
                result["signals"].append("竞价价格上行")
                result["score"] += 2
            elif price_change < -0.01:
                result["signals"].append("竞价价格回落⚠️")
                result["score"] -= 1

        # --- 3. 末段抢筹（9:20后量价齐升）---
        if len(late) >= 3:
            late_prices = late[price_col].values
            late_vols = late[vol_col].values
            price_up = late_prices[-1] > late_prices[0]
            vol_up = late_vols[-1] > late_vols[0] * 1.2
            if price_up and vol_up:
                result["signals"].append("末段量价齐升🔥")
                result["score"] += 3

        # --- 4. 竞价总量评分 ---
        result["total_auction_vol"] = int(total_vol)

    return result


# ============================================================
# 开盘5分钟量价分析
# ============================================================

def fetch_opening_data(symbol: str, date_str: str) -> pd.DataFrame | None:
    """获取开盘后5分钟 K 线数据 (9:30-9:35, 1分钟周期)。"""
    try:
        import akshare as ak
        start_dt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} 09:30:00"
        end_dt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} 09:35:00"
        df = ak.stock_zh_a_hist_min_em(
            symbol=symbol,
            start_date=start_dt,
            end_date=end_dt,
            period="1",
            adjust="",
        )
        if df is None or df.empty:
            return None
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception:
        return None


def analyze_opening(opening_df: pd.DataFrame | None) -> dict[str, Any]:
    """分析开盘5分钟量价，返回确认信号。"""
    if opening_df is None or opening_df.empty:
        return {"status": "no_data", "score": 0, "signals": []}

    result: dict[str, Any] = {"status": "ok", "signals": [], "score": 0}
    col_map = _find_columns(opening_df)

    open_col = col_map.get("open")
    close_col = col_map.get("close")
    vol_col = col_map.get("volume")
    high_col = col_map.get("high")

    if open_col and close_col and vol_col:
        # --- 开盘方向 ---
        first_open = opening_df[open_col].iloc[0]
        last_close = opening_df[close_col].iloc[-1]
        if first_open > 0:
            open_ret = (last_close - first_open) / first_open
            result["open_return_pct"] = round(open_ret * 100, 2)

        # --- 高开幅度 ---
        if high_col and close_col:
            max_price = opening_df[high_col].max()
            if first_open > 0:
                gap = (max_price - first_open) / first_open
                result["max_gap_pct"] = round(gap * 100, 2)
                if gap > 0.02:
                    result["signals"].append("开盘强势上攻")
                    result["score"] += 2

        # --- 量能确认（5分钟总量）---
        total_vol = opening_df[vol_col].sum()
        result["opening_5min_vol"] = int(total_vol)

        # --- 分时形态 ---
        if len(opening_df) >= 4:
            first_half = opening_df.head(3)
            second_half = opening_df.tail(2)
            if close_col in opening_df.columns:
                trend_up = (
                    opening_df[close_col].iloc[-1]
                    > opening_df[open_col].iloc[0]
                )
                vol_healthy = second_half[vol_col].mean() > first_half[vol_col].mean()
                if trend_up:
                    result["signals"].append("分时上行")
                    result["score"] += 1
                if vol_healthy:
                    result["signals"].append("量能持续")
                    result["score"] += 1
                if trend_up and vol_healthy:
                    result["signals"].append("量价配合良好✅")
                    result["score"] += 2

    return result


# ============================================================
# Alpha Zoo 三因子计算
# ============================================================

def fetch_daily_history(symbol: str, lookback: int = 252) -> pd.DataFrame | None:
    """拉取日线 OHLCV 数据用于因子计算。"""
    try:
        import akshare as ak
        end_date = date.today().strftime("%Y%m%d")
        start_date = (date.today() - timedelta(days=lookback * 2)).strftime("%Y%m%d")
        code = symbol.replace(".SH", "").replace(".SZ", "")
        df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                start_date=start_date, end_date=end_date,
                                adjust="qfq")
        if df is None or df.empty:
            return None
        df.columns = [c.lower() for c in df.columns]
        if "收盘" in df.columns:
            df = df.rename(columns={"收盘": "close"})
        elif "close" not in df.columns:
            for c in df.columns:
                if "close" in c.lower() or "收盘" in c:
                    df = df.rename(columns={c: "close"})
                    break
        if "close" not in df.columns:
            return None
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        return df.dropna(subset=["close"])
    except Exception:
        return None


def _safe_div(a, b):
    """安全除法，除数为0返回NaN。"""
    b = b.where(b != 0, np.nan)
    return a / b


def _delta(series: pd.Series, lag: int) -> pd.Series:
    """计算滞后差分。"""
    return series - series.shift(lag)


def compute_carhart_mom(close: pd.Series) -> float:
    """Carhart 动量因子：252日收益 - 21日收益。正值=强趋势。"""
    if len(close) < 252:
        return float("nan")
    ret_252 = (close.iloc[-1] - close.iloc[-252]) / close.iloc[-252]
    ret_21 = (close.iloc[-1] - close.iloc[-21]) / close.iloc[-21]
    return float(ret_252 - ret_21)


def compute_hml_value(close: pd.Series) -> float:
    """HML 价值因子（价格代理）：-252日收益。正值=深跌（价值）。"""
    if len(close) < 252:
        return float("nan")
    ret_252 = (close.iloc[-1] - close.iloc[-252]) / close.iloc[-252]
    return float(-ret_252)


def compute_rmw_quality(close: pd.Series) -> float:
    """RMW 质量因子（价格代理）：-60日波动率。正值=低波（高质量）。"""
    if len(close) < 60:
        return float("nan")
    rets = close.pct_change().dropna().tail(60)
    return float(-rets.std())


def _find_columns(df: pd.DataFrame) -> dict[str, str]:
    """在 DataFrame 中自动识别量、价列。"""
    cols = {c.lower(): c for c in df.columns}
    result = {}
    for key in ["volume", "vol", "成交量", "成交额"]:
        if key in cols:
            result["volume"] = cols[key]
            break
    for key in ["price", "close", "最新价", "收盘"]:
        if key in cols:
            result["price"] = cols[key]
            break
    for key in ["open", "开盘"]:
        if key in cols:
            result["open"] = cols[key]
            break
    for key in ["high", "最高"]:
        if key in cols:
            result["high"] = cols[key]
            break
    for key in ["close", "收盘"]:
        if key in cols:
            result["close"] = cols[key]
            break
    return result


def compute_factor_scores(tickers: list[dict]) -> dict[str, dict[str, float]]:
    """
    对所有候选+近失标的计算 Alpha Zoo 三因子，
    然后在组内做横截面 z-score 排名。
    """
    scores: dict[str, dict[str, float]] = {}
    raw_values: dict[str, dict[str, float]] = {}

    print(f"\n📊 计算 Alpha Zoo 三因子（{len(tickers)} 只标的）...")

    for i, t in enumerate(tickers):
        code = t.get("code", "")
        name = t.get("name", "")
        sym = f"sh{code}" if code.startswith("6") else f"sz{code}"
        print(f"  [{i+1}/{len(tickers)}] {code} {name} ...", end=" ")

        df = fetch_daily_history(sym, lookback=300)
        if df is None or df.empty or "close" not in df.columns:
            print("❌ 无日线数据")
            scores[f"{code}_{name}"] = {
                "carhart_mom": float("nan"),
                "hml_value": float("nan"),
                "rmw_quality": float("nan"),
                "composite": float("nan"),
            }
            continue

        close = df["close"]
        carhart = compute_carhart_mom(close)
        hml = compute_hml_value(close)
        rmw = compute_rmw_quality(close)

        print(f"OK (mom={carhart:.4f}, val={hml:.4f}, qual={rmw:.6f})")

        key = f"{code}_{name}"
        raw_values[key] = {"carhart_mom": carhart, "hml_value": hml, "rmw_quality": rmw}

    # --- 横截面 z-score ---
    if len(raw_values) >= 3:
        for factor in ["carhart_mom", "hml_value", "rmw_quality"]:
            vals = [v[factor] for v in raw_values.values() if not np.isnan(v[factor])]
            if len(vals) < 3:
                continue
            mu = np.mean(vals)
            sigma = np.std(vals, ddof=1)
            if sigma == 0:
                continue
            for key in raw_values:
                if not np.isnan(raw_values[key][factor]):
                    raw_values[key][f"{factor}_z"] = (raw_values[key][factor] - mu) / sigma
                else:
                    raw_values[key][f"{factor}_z"] = float("nan")

        # --- 复合评分 ---
        for key in raw_values:
            zs = [
                raw_values[key].get("carhart_mom_z", float("nan")),
                raw_values[key].get("hml_value_z", float("nan")),
                raw_values[key].get("rmw_quality_z", float("nan")),
            ]
            valid = [z for z in zs if not np.isnan(z)]
            composite = float(np.mean(valid)) if valid else float("nan")
            raw_values[key]["composite"] = composite
    else:
        for key in raw_values:
            raw_values[key]["composite"] = float("nan")

    return raw_values


# ============================================================
# 核心增强扫描
# ============================================================

def load_scan_results(date_str: str) -> dict | None:
    """加载原始扫描结果，如果不存在则运行 daban_scanner。"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            data = json.load(f)
        if data.get("date") == date_str:
            return data

    # 扫描结果不存在或日期不匹配，运行原始扫描器
    print(f"⚠️ 未找到 {date_str} 的扫描结果，运行 daban_scanner ...")
    import subprocess
    subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "daban_scanner.py"), date_str, "--near-miss", "--ci"],
        cwd=SCRIPT_DIR, check=False,
    )
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return None


def enhance(scan_data: dict, skip_factor: bool = False,
            auction_only: bool = False) -> dict:
    """
    主增强流程：
    1. 对候选+近失标的做集合竞价分析
    2. 开盘5分钟量价分析
    3. Alpha Zoo 三因子评分
    """
    date_str = scan_data["date"]
    candidates = scan_data.get("candidates", [])
    near_miss = scan_data.get("near_miss", [])
    all_tickers = candidates + near_miss

    if not all_tickers:
        print("⚠️ 无候选或近失标的，跳过增强分析。")
        return {"status": "empty", "date": date_str}

    print(f"\n{'='*60}")
    print(f"  Vibe-Trading 增强分析 — {date_str}")
    print(f"  候选: {len(candidates)} | 近失: {len(near_miss)} | 合计: {len(all_tickers)}")
    print(f"{'='*60}")

    # --- Layer 1 & 2: 竞价 + 开盘分析 ---
    print(f"\n🔍 Layer 1+2: 集合竞价 & 开盘5分钟量价分析 ...")
    auction_ok = 0
    opening_ok = 0

    for i, t in enumerate(all_tickers):
        code = t.get("code", "")
        name = t.get("name", "")
        sym = f"sh{code}" if code.startswith("6") else f"sz{code}"

        # 集合竞价
        auction_df = fetch_auction_data(code, date_str)
        auction_result = analyze_auction(auction_df)
        t["auction"] = auction_result
        if auction_result.get("status") == "ok":
            auction_ok += 1

        # 开盘5分钟
        if not auction_only:
            opening_df = fetch_opening_data(code, date_str)
            opening_result = analyze_opening(opening_df)
            t["opening"] = opening_result
            if opening_result.get("status") == "ok":
                opening_ok += 1

        # 进度
        print(f"  [{i+1}/{len(all_tickers)}] {code} {name} "
              f"竞价={auction_result.get('score',0)} "
              f"开盘={t.get('opening',{}).get('score',0)}")

    print(f"\n  竞价数据: {auction_ok}/{len(all_tickers)} | 开盘数据: {opening_ok}/{len(all_tickers)}")

    # --- Layer 3: Alpha Zoo 因子 ---
    if not skip_factor and not auction_only:
        factor_scores = compute_factor_scores(all_tickers)
        for t in all_tickers:
            key = f"{t['code']}_{t['name']}"
            t["alpha_zoo"] = factor_scores.get(key, {})

    # --- 综合评分 ---
    for t in all_tickers:
        auction_score = t.get("auction", {}).get("score", 0)
        opening_score = t.get("opening", {}).get("score", 0)
        factor_score = 0
        if not skip_factor and not auction_only:
            comp = t.get("alpha_zoo", {}).get("composite", float("nan"))
            if not np.isnan(comp):
                factor_score = round(comp * 3)  # z-score → 整数分（3倍缩放）

        t["enhanced_score"] = auction_score + opening_score + factor_score
        t["score_breakdown"] = {
            "auction": auction_score,
            "opening": opening_score,
            "alpha_factor": factor_score,
        }

    # 按综合评分排序
    all_tickers.sort(key=lambda x: x.get("enhanced_score", 0), reverse=True)

    result = {
        "date": date_str,
        "enhanced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_limit_ups": scan_data.get("total_limit_ups", 0),
            "candidates": len(candidates),
            "near_miss": len(near_miss),
            "auction_ok": auction_ok,
            "opening_ok": opening_ok,
        },
        "top_picks": all_tickers[:10],
        "all_enhanced": all_tickers,
    }

    # 保存
    with open(ENHANCED_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 增强结果已保存: {ENHANCED_FILE}")

    return result


def print_report(result: dict):
    """打印增强分析报告。"""
    print(f"\n{'='*60}")
    print(f"  📋 Vibe-Trading 增强分析报告")
    print(f"  {result['date']} | {result['enhanced_at']}")
    print(f"{'='*60}")

    s = result["summary"]
    print(f"\n  总涨停: {s['total_limit_ups']} | 候选: {s['candidates']} | 近失: {s['near_miss']}")
    print(f"  竞价数据: {s['auction_ok']} | 开盘数据: {s['opening_ok']}")

    top = result.get("top_picks", [])
    if not top:
        print("\n  😔 无增强候选")
        return

    print(f"\n  🏆 Top {min(len(top), 8)} 增强候选:\n")
    print(f"  {'排名':<4} {'代码':<8} {'名称':<10} {'价格':>6} {'涨幅':>7} "
          f"{'竞价分':>5} {'开盘分':>5} {'因子分':>5} {'综合分':>5}")
    print(f"  {'-'*72}")

    for i, t in enumerate(top[:8]):
        score = t.get("enhanced_score", 0)
        bd = t.get("score_breakdown", {})
        print(f"  {i+1:<4} {t['code']:<8} {t['name']:<10} "
              f"{t.get('price','-'):>6} {t.get('change_pct','-'):>6}% "
              f"{bd.get('auction',0):>5} {bd.get('opening',0):>5} "
              f"{bd.get('alpha_factor',0):>5} {score:>5}")

        # Alpha 因子详情
        alpha = t.get("alpha_zoo", {})
        if alpha and not all(np.isnan(v) for v in alpha.values() if isinstance(v, float)):
            mom = alpha.get("carhart_mom", float("nan"))
            val = alpha.get("hml_value", float("nan"))
            qual = alpha.get("rmw_quality", float("nan"))
            print(f"       Alpha: 动量={mom:.4f} | 价值={val:.4f} | 质量={qual:.6f}")

        # 竞价信号
        auction_sigs = t.get("auction", {}).get("signals", [])
        if auction_sigs:
            print(f"       竞价信号: {', '.join(auction_sigs)}")

        # 开盘信号
        opening_sigs = t.get("opening", {}).get("signals", [])
        if opening_sigs:
            print(f"       开盘信号: {', '.join(opening_sigs)}")

    print()


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Vibe-Trading 增强版打板扫描器"
    )
    parser.add_argument("date", nargs="?", default=None,
                       help="扫描日期 YYYYMMDD（默认今天）")
    parser.add_argument("--no-factor", action="store_true",
                       help="跳过 Alpha Zoo 因子计算")
    parser.add_argument("--auction-only", action="store_true",
                       help="仅做竞价分析")
    args = parser.parse_args()

    date_str = args.date or date.today().strftime("%Y%m%d")

    # 加载原始扫描结果
    scan_data = load_scan_results(date_str)
    if scan_data is None:
        print(f"❌ 无法加载 {date_str} 的扫描结果")
        sys.exit(1)

    if "error" in scan_data:
        print(f"❌ 扫描错误: {scan_data['error']}")
        sys.exit(1)

    # 增强分析
    result = enhance(
        scan_data,
        skip_factor=args.no_factor,
        auction_only=args.auction_only,
    )

    # 打印报告
    print_report(result)

    # 提示下一步
    if result.get("top_picks"):
        print("💡 下一4: cd /path/to/vibe-trading && vibe-trading run -p")
        print("   \"分析 enhanced_results.json 中的 Top 打板候选，给出操作建议\"")


if __name__ == "__main__":
    main()
