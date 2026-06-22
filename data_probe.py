#!/usr/bin/env python3
"""
data_probe.py — A 股数据源连通性探针
====================================
测试各免费数据源在你本机是否可用，给出延迟和推荐排序。

用于：诊断 daban-picker / daban_vt_enhance 的数据管线。

使用：
    python3 data_probe.py              # 全部测试
    python3 data_probe.py --quick      # 只测核心 (akshare + 东方财富直连)
    python3 data_probe.py --json       # JSON 输出（给 CI 用）
"""

from __future__ import annotations

import json
import sys
import time
from datetime import date
from typing import Any

# ── 通用工具 ──────────────────────────────────────────

def _timed(name: str, fn, *args, **kwargs) -> dict[str, Any]:
    """计时执行，返回 {'name','ok','elapsed_ms','error'}。"""
    t0 = time.perf_counter()
    try:
        fn(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000
        return {"name": name, "ok": True, "elapsed_ms": round(elapsed, 1)}
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000
        return {"name": name, "ok": False, "elapsed_ms": round(elapsed, 1),
                "error": str(e)[:120]}


def _print_result(r: dict[str, Any], i: int, total: int):
    icon = "✅" if r["ok"] else "❌"
    ms = f"{r['elapsed_ms']}ms"
    name = r["name"]
    print(f"  [{i}/{total}] {icon} {name:<35} {ms:>8}", end="")
    if not r["ok"]:
        print(f"  — {r['error']}")
    else:
        print()


# ── 各数据源测试 ───────────────────────────────────────

def test_akshare_spot():
    """akshare 实时行情 (东方财富底层)"""
    import akshare as ak
    df = ak.stock_zh_a_spot_em()
    assert len(df) > 1000, f"only {len(df)} rows"


def test_akshare_auction():
    """akshare 集合竞价逐分钟数据"""
    import akshare as ak
    df = ak.stock_zh_a_hist_pre_min_em(symbol="000001", start_time="09:15:00", end_time="09:25:00")
    assert df is not None and not df.empty, "empty result"


def test_akshare_limit_up():
    """akshare 涨停池"""
    import akshare as ak
    df = ak.stock_zt_pool_em(date=date.today().strftime("%Y%m%d"))
    assert df is not None, "None result"


def test_akshare_minute():
    """akshare 1分钟 K 线"""
    import akshare as ak
    df = ak.stock_zh_a_hist_min_em(symbol="000001", period="1",
                                   start_date="2026-06-20 09:30:00",
                                   end_date="2026-06-20 09:35:00")
    assert df is not None and not df.empty, "empty result"


def test_akshare_daily():
    """akshare 日线 K 线"""
    import akshare as ak
    df = ak.stock_zh_a_hist(symbol="000001", period="daily",
                            start_date="20260601", end_date="20260620",
                            adjust="qfq")
    assert df is not None and not df.empty, "empty result"


def test_eastmoney_direct():
    """东方财富 HTTP 直连（1分钟 K 线，绕过 akshare 封装）"""
    import requests
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": "1.600519", "klt": "1", "fqt": "1",
        "beg": "20260620", "end": "20260620",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",
        "lmt": "5",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    assert data.get("data") is not None, "no data in response"


def test_sina_direct():
    """新浪财经实时快照"""
    import requests
    url = "https://hq.sinajs.cn/list=sh600519,sz000001"
    headers = {"Referer": "https://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    assert "600519" in r.text, "no data"


def test_tencent_direct():
    """腾讯财经实时快照"""
    import requests
    url = "https://qt.gtimg.cn/q=sh600519,sz000001"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    assert "600519" in r.text, "no data"


def test_tushare():
    """Tushare Pro (需要 TUSHARE_TOKEN 环境变量)"""
    import os
    token = os.environ.get("TUSHARE_TOKEN", "")
    if not token:
        raise RuntimeError("TUSHARE_TOKEN not set")
    import tushare as ts
    ts.set_token(token)
    pro = ts.pro_api()
    df = pro.daily(ts_code="000001.SZ", start_date="20260601", end_date="20260620")
    assert df is not None and not df.empty, "empty result"


def test_mootdx():
    """mootdx 通达信 TCP（需要先跑 bestip）"""
    import subprocess
    import os
    # 先跑 bestip 选择最快服务器
    subprocess.run([sys.executable, "-m", "mootdx", "bestip", "-w"],
                   capture_output=True, timeout=30)
    from mootdx.quotes import Quotes
    c = Quotes.factory(market="std")
    d = c.bar(symbol="600519", frequency=9, start=0, offset=5)
    assert d is not None and not d.empty, "empty result"


# ── 主逻辑 ─────────────────────────────────────────────

ALL_TESTS = [
    ("akshare 实时行情",        test_akshare_spot),
    ("akshare 集合竞价",        test_akshare_auction),
    ("akshare 涨停池",          test_akshare_limit_up),
    ("akshare 1分钟K线",        test_akshare_minute),
    ("akshare 日线K线",         test_akshare_daily),
    ("东方财富 HTTP 直连",      test_eastmoney_direct),
    ("新浪财经 HTTP",           test_sina_direct),
    ("腾讯财经 HTTP",           test_tencent_direct),
    ("Tushare Pro",             test_tushare),
    ("mootdx 通达信 TCP",       test_mootdx),
]

QUICK_TESTS = [
    ("akshare 实时行情",        test_akshare_spot),
    ("akshare 集合竞价",        test_akshare_auction),
    ("akshare 涨停池",          test_akshare_limit_up),
    ("东方财富 HTTP 直连",      test_eastmoney_direct),
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="A股数据源连通性探针")
    parser.add_argument("--quick", action="store_true", help="只测核心源")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    tests = QUICK_TESTS if args.quick else ALL_TESTS
    results = []

    if not args.json:
        print(f"\n{'='*60}")
        print(f"  A股数据源连通性探针")
        print(f"  测试 {len(tests)} 个数据源...")
        print(f"{'='*60}\n")

    ok_count = 0
    for i, (name, fn) in enumerate(tests):
        r = _timed(name, fn)
        results.append(r)
        if r["ok"]:
            ok_count += 1
        if not args.json:
            _print_result(r, i + 1, len(tests))

    # ── 推荐 ──
    recommends: list[str] = []
    for r in results:
        if r["ok"] and "akshare" in r["name"]:
            recommends.append(r["name"])
        elif r["ok"] and "东方财富" in r["name"]:
            recommends.append(r["name"])

    if args.json:
        print(json.dumps({
            "ok": ok_count,
            "total": len(tests),
            "results": results,
            "recommends": recommends,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  {ok_count}/{len(tests)} 数据源可用")
        if recommends:
            print(f"  推荐用于 daban-picker: {', '.join(recommends)}")
        if ok_count == 0:
            print(f"  ⚠️  所有源都不通，检查网络/代理配置")
        print(f"{'='*60}\n")

    return 0 if ok_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
