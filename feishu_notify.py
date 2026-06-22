#!/usr/bin/env python3
"""
feishu_notify.py — 飞书打板扫描通知
====================================
从 enhanced_results.json 提取 Top 3 摘要，通过飞书 Webhook 发送文本消息。

使用:
    python3 feishu_notify.py                         # 使用默认 enhanced_results.json
    python3 feishu_notify.py enhanced_results.json    # 指定文件
    python3 feishu_notify.py --dry-run               # 打印消息但不发送

环境变量:
    FEISHU_WEBHOOK    飞书机器人 Webhook URL
"""

import json
import os
import sys


def load_data(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def build_summary(data: dict) -> str:
    s = data.get("summary", {})
    lines = [
        "📊 " + data["date"] + " 打板扫描",
        "",
        f"{s.get('total_limit_ups', 0)}涨停 → "
        f"{s.get('candidates', 0)}候选/{s.get('near_miss', 0)}近失",
        f"竞价数据: {s.get('auction_ok', 0)}  开盘数据: {s.get('opening_ok', 0)}",
        "",
    ]

    top = data.get("top_picks", [])[:3]
    if not top:
        lines.append("😔 今日无高分候选")
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, t in enumerate(top):
            code = t.get("code", "")
            name = t.get("name", "")
            price = t.get("price", "-")
            pct = t.get("change_pct", "-")
            score = t.get("enhanced_score", 0)
            sigs = t.get("auction", {}).get("signals", [])
            lines.append(
                f"{medals[i]} {code} {name}  ¥{price}  +{pct}%  综合{score}分"
            )
            if sigs:
                lines.append(f"  {', '.join(sigs[:3])}")
            lines.append("")

    return "\n".join(lines)


def send_to_feishu(webhook_url: str, text: str) -> tuple[int, str]:
    import urllib.request
    payload = json.dumps({
        "msg_type": "text",
        "content": {"text": text},
    }, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="飞书打板扫描通知")
    parser.add_argument("input_file", nargs="?", default="enhanced_results.json",
                        help="增强结果 JSON 文件")
    parser.add_argument("--dry-run", action="store_true",
                        help="只打印消息，不发送")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"❌ 文件不存在: {args.input_file}")
        sys.exit(1)

    data = load_data(args.input_file)
    text = build_summary(data)

    print("=== 飞书通知 ===")
    print(text)
    print("================")

    if args.dry_run:
        print("\n🔍 Dry run — 未发送")
        return

    webhook = os.environ.get("FEISHU_WEBHOOK", "")
    if not webhook:
        print("\n❌ FEISHU_WEBHOOK 环境变量未设置")
        sys.exit(1)

    print(f"\n📤 发送到飞书...")
    code, resp = send_to_feishu(webhook, text)

    if code == 200:
        print(f"✅ 发送成功 (HTTP {code})")
    else:
        print(f"❌ 发送失败 (HTTP {code}): {resp}")
        sys.exit(1)


if __name__ == "__main__":
    main()
