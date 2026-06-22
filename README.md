# Daban Picker 🎯 打板策略选股器

A-share 首板早盘板量化筛选工具。每天自动扫描涨停池，按打板策略规则筛选候选标的。

## 策略规则

| 条件 | 阈值 |
|------|------|
| 连板数 | = 1（首板） |
| 首次封板时间 | < 10:00（早盘板） |
| 封单额 | > 5000 万 |
| 换手率 | 5% ~ 15% |
| 流通市值 | 30 ~ 100 亿 |
| 最新价 | < 40 元 |
| 板块 | 当前热点（涨停家数 Top 8） |
| 股票类型 | 主板 A 股（60/00 开头） |
| 排除 | ST、一字板、尾盘板 |

## 使用

```bash
# 当天扫描
python3 daban_scanner.py

# 指定日期 + 近失名单
python3 daban_scanner.py 20260617 --near-miss

# 查看结果
python3 codex_analyze.py              # 候选摘要
python3 codex_analyze.py 600237       # 单票详情
python3 codex_analyze.py --near-miss  # 近失名单
```

## 自动化

GitHub Actions 每个交易日上午 10:30 自动运行扫描，结果写入 `scan_results.json`。
