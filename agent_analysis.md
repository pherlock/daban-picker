
Preflight Check
 OK   │ LLM (deepseek)     │ deepseek-chat via https://api.deepseek.com |       
      │                    │ base=https://api.deepseek.com timeout=120s         
      │                    │ retries=2 proxy=none                               
 OK   │ OKX API            │ reachable                                          
 OK   │ yfinance           │ reachable                                          
 N/A  │ Tushare            │ TUSHARE_TOKEN not set (optional) (A-share data     
      │                    │ unavailable)                                       
 OK   │ akshare            │ installed                                          
 OK   │ ccxt               │ installed                                          

5/6 services ready

Prompt: 分析 /home/runner/work/daban-picker/daban-picker/enhanced_results.json 中综合评分 Top 3 的打板候选标的，结合竞价信号和 Alpha 因子评分，给出今日打板操作建议（买...

Let me start by reading the file to understand its structure.
  - read_file /home/runner/work/daban-picker/daban-picker/enhanced_results.json  FAIL 0.0s  {"status": "error", "error": "File not found or path escapes workspace: /home/ru
  - bash ls -la /home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "total 172\ndrwxr
  - read_file /home/runner/work/daban-picker/daban-picker/enhanced_results.json  FAIL 0.0s  {"status": "error", "error": "File not found or path escapes workspace: /home/ru
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | head -20  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "{\n  \"date\": \
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== Summary ===\
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
现在让我获取这些标的的实时行情和基本面数据，以便给出更精准的建议。
  - get_market_data   - get_financial_statements 002354.SZ  - get_financial_statements 000700.SZ  - get_financial_statements 600156.SH..  OK 3.0s
  OK 0.7s
  OK 1.7s
  OK 3.1s
Now let me get the full JSON data to see the complete picture including the score breakdowns and auction signals.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== SUMMARY ===\
Now let me get the near_miss items to understand the broader context, and also check the sector info for these stocks.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "", "stderr": ""}
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "Total near_miss:
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "Keys: ['date', '
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== SUMMARY ===\
Now let me get the sector info and recent news for these stocks.
  - get_sector_info 002354.SZ  - get_sector_info 000700.SZ  - get_sector_info 600156.SH  - get_stock_news 002354.SZ  - get_stock_news 000700.SZ  - get_stock_news 600156.SH....eastmoney news fetch failed for 002354.SZ: Expecting value: line 1 column 1 (char 0)
eastmoney news fetch failed for 000700.SZ: Expecting value: line 1 column 1 (char 0)
.eastmoney news fetch failed for 600156.SH: Expecting value: line 1 column 1 (char 0)
Blocked duplicate call: get_sector_info (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_financial_statements (already succeeded)
Blocked duplicate call: get_market_data (already succeeded)
Blocked duplicate call: get_sector_info (already succeeded)
  OK 2.1s
  OK 2.7s
  OK 3.2s
  OK 4.3s
  OK 5.0s
  OK 6.2s
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
Now let me get the full list of top_picks to see how many there are and check the rest.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   FAIL 0.0s  {"status": "error", "exit_code": 1, "stdout": "Total top_picks: 10\n#1 002354 天娱
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "Total top_picks:
Now let me get the sector info for the top 3 to understand the industry context.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
Now let me get the financial indicators for these three stocks to understand their fundamentals.
Let me try to get the data again since the previous results were cleared.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "Total top_picks:
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
Now let me get the financial indicators for these three stocks.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "Total top_picks:
Now let me get the detailed score breakdowns and auction signals for the top 3.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
Now let me get the full details for all 10 top picks to understand the broader picture.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "#1 002354 天娱数科 评
Now let me also check the market data for these stocks to see their recent price action.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== #1 002354 天娱
Now I have all the data. Let me also check the sector ranking for today to understand the broader market context.
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== SUMMARY ===\
Now I have a comprehensive picture. Let me compile the analysis.

---

## 📊 打板候选标的分析报告 — 2026年7月3日

### 市场概况

今日全市场共 **93 只涨停**，系统筛选出 **3 只候选标的**（另有 57 只 near-miss 被规则过滤）。整体打板环境较好，但需注意分化。

---

### 🥇 Top 1：天娱数科（002354）— 广告营销

| 指标 | 数值 |
|---|---|
| 价格 | 10.34 元 |
| 涨幅 | **+10.00%**（涨停） |
| 换手率 | **6.32%**（适中） |
| 封单额 | **5.02 亿**（封单极强） |
| 首封时间 | **09:30:03**（秒板） |
| 板数 | 首板 |
| 流通市值 | 168.1 亿（中大盘） |
| 板块热度 | ✅ 热点板块（广告营销，板块内 10 涨 5 跌） |

**评分明细：** 竞价信号 0 / 开盘信号 0 / Alpha 因子 0（系统未获取到竞价数据）

**分析：**
- ✅ **封单极强**：5.02 亿封单，远超其 6.32% 的换手，封板质量高
- ✅ **秒板**：09:30:03 即封死，说明资金抢筹意愿极强
- ✅ **板块效应**：广告营销板块有 10 只上涨，板块热度确认
- ⚠️ 流通市值 168 亿偏大，次日连板需要更多资金接力
- ⚠️ 换手 6.32% 偏低，说明筹码交换不充分，次日抛压可能集中释放

---

### 🥈 Top 2：模塑科技（000700）— 汽车零部件

| 指标 | 数值 |
|---|---|
| 价格 | 16.87 元 |
| 涨幅 | **+9.97%**（涨停） |
| 换手率 | **12.39%**（充分换手） |
| 封单额 | **1.08 亿** |
| 首封时间 | **10:09:30**（换手板） |
| 板数 | 首板 |
| 流通市值 | 154.9 亿（中大盘） |
| 板块热度 | ✅ 热点板块（汽车零部件） |

**分析：**
- ✅ **换手充分**：12.39% 换手，筹码交换健康，次日抛压相对分散
- ✅ **板块热度**：汽车零部件板块为近期主线之一
- ⚠️ 封单 1.08 亿相对其 155 亿市值偏弱，封板质量一般
- ⚠️ 10:09 才封板，属于盘中换手板，强度不如秒板
- ⚠️ 流通市值 155 亿偏大，连板难度较高

---

### 🥉 Top 3：华升股份（600156）— 纺织制造

| 指标 | 数值 |
|---|---|
| 价格 | 9.53 元 |
| 涨幅 | **+10.05%**（涨停） |
| 换手率 | **3.91%**（偏低） |
| 封单额 | **6,953 万** |
| 首封时间 | **09:59:26** |
| 板数 | 首板 |
| 流通市值 | **38.3 亿**（小盘） |
| 板块热度 | ✅ 热点板块（纺织制造） |

**分析：**
- ✅ **小盘优势**：仅 38.3 亿流通市值，连板所需资金少，弹性大
- ✅ 换手 3.91% 偏低但封板时间较早（09:59），说明抛压不大
- ⚠️ 封单 6,953 万相对市值不算小，但绝对值偏低
- ⚠️ 纺织制造板块持续性一般，非当前市场主线

---

## 🎯 今日打板操作建议

### 综合排序

| 排名 | 标的 | 封板质量 | 板块持续性 | 接力难度 | 综合评级 |
|---|---|---|---|---|---|
| **1** | **天娱数科** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | **优先关注** |
| **2** | **华升股份** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **次选** |
| **3** | **模塑科技** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | **谨慎** |

### 买入时机

**天娱数科（002354）— 首选**
- **打板买入**：如果明天高开 3%-6% 且开盘后承接有力（分时均线上方运行），可在换手率到 5%-8% 时分批介入
- **排板买入**：如果一字板开盘，观察封单是否持续增加，排板需谨慎（秒板次日容易高开低走）
- **放弃条件**：高开 >8% 后快速下杀破分时均线，放弃

**华升股份（600156）— 次选**
- **打板买入**：如果高开 2%-5%，开盘后放量换手（换手率到 8%+）后封板，可打板介入
- **低吸机会**：小盘股弹性大，如果开盘小幅低开或平开，可轻仓试错
- **放弃条件**：高开 >7% 缩量秒板，放弃（容易炸板）

**模塑科技（000700）— 谨慎**
- 仅作为板块轮动备选，如果前两个都买不到且汽车零部件板块当日强势，可考虑轻仓打板
- 封单偏弱，建议等二封确认后再介入

### 仓位建议（假设总仓位 10 成）

| 标的 | 仓位 | 说明 |
|---|---|---|
| 天娱数科 | **3 成** | 核心仓位，封单质量最高 |
| 华升股份 | **2 成** | 小盘弹性标的 |
| 模塑科技 | **1 成** | 观察仓，确认后加 |
| 现金 | **4 成** | 留足子弹应对炸板或次日补仓 |

### 止损纪律

| 标的 | 止损线 | 逻辑 |
|---|---|---|
| 天娱数科 | **买入价 -5%** | 中大盘首板，跌破 5% 说明资金出逃 |
| 华升股份 | **买入价 -7%** | 小盘股波动大，适当放宽 |
| 模塑科技 | **买入价 -5%** | 同中大盘标准 |

### ⚠️ 风险提示

1. **今日 93 只涨停**，市场情绪偏热，次日分化概率大，切忌追高后排跟风股
2. **三只标的均为首板**，首板次日溢价率取决于大盘情绪和板块持续性
3. **竞价数据缺失**（系统显示 auction/opening 信号为 0），建议明日 09:20-09:25 观察集合竞价量能和价格走势再做最终决策
4. **天娱数科秒板换手低**，次日如果缩量高开，炸板风险较大，务必等换手充分后再考虑
5. **打板有风险**，以上仅为量化分析参考，不构成投资建议，请根据自身风险承受能力操作
Status: SUCCESS
Elapsed: 2m 02s
Run ID: 20260703_065929_75_9d533f
Run dir: /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/runs/20260703_065929_75_9d533f

Now I have a comprehensive picture. Let me compile the analysis.

---

## 📊 打板候选标的分析报告 — 2026年7月3日

### 市场概况

今日全市场共 **93 只涨停**，系统筛选出 **3 只候选标的**（另有 57 只 near-miss 被规则过滤）。整体打板环境较好，但需注意分化。

---

### 🥇 Top 1：天娱数科（002354）— 广告营销

| 指标 | 数值 |
|---|---|
| 价格 | 10.34 元 |
| 涨幅 | **+10.00%**（涨停） |
| 换手率 | **6.32%**（适中） |
| 封单额 | **5.02 亿**（封单极强） |
| 首封时间 | **09:30:03**（秒板） |
| 板数 | 首板 |
| 流通市值 | 168.1 亿（中大盘） |
| 板块热度 | ✅ 热点板块（广告营销，板块内 10 涨 5 跌） |

**评分明细：** 竞价信号 0 / 开盘信号 0 / Alpha 因子 0（系统未获取到竞价数据）

**分析：**
- ✅ **封单极强**：5.02 亿封单，远超其 6.32% 的换手，封板质量高
- ✅ **秒板**：09:30:03 即封死，说明资金抢筹意愿极强
- ✅ **板块效应**：广告营销板块有 10 只上涨，板块热度确认
- ⚠️ 流通市值 168 亿偏大，次日连板需要更多资金接力
- ⚠️ 换手 6.32% 偏低，说明筹码交换不充分，次日抛压可能集中释放

---

### 🥈 Top 2：模塑科技（000700）— 汽车零部件

| 指标 | 数值 |
|---|---|
| 价格 | 16.87 元 |
| 涨幅 | **+9.97%**（涨停） |
| 换手率 | **12.39%**（充分换手） |
| 封单额 | **1.08 亿** |
| 首封时间 | **10:09:30**（换手板） |
| 板数 | 首板 |
| 流通市值 | 154.9 亿（中大盘） |
| 板块热度 | ✅ 热点板块（汽车零部件） |

**分析：**
- ✅ **换手充分**：12.39% 换手，筹码交换健康，次日抛压相对分散
- ✅ **板块热度**：汽车零部件板块为近期主线之一
- ⚠️ 封单 1.08 亿相对其 155 亿市值偏弱，封板质量一般
- ⚠️ 10:09 才封板，属于盘中换手板，强度不如秒板
- ⚠️ 流通市值 155 亿偏大，连板难度较高

---

### 🥉 Top 3：华升股份（600156）— 纺织制造

| 指标 | 数值 |
|---|---|
| 价格 | 9.53 元 |
| 涨幅 | **+10.05%**（涨停） |
| 换手率 | **3.91%**（偏低） |
| 封单额 | **6,953 万** |
| 首封时间 | **09:59:26** |
| 板数 | 首板 |
| 流通市值 | **38.3 亿**（小盘） |
| 板块热度 | ✅ 热点板块（纺织制造） |

**分析：**
- ✅ **小盘优势**：仅 38.3 亿流通市值，连板所需资金少，弹性大
- ✅ 换手 3.91% 偏低但封板时间较早（09:59），说明抛压不大
- ⚠️ 封单 6,953 万相对市值不算小，但绝对值偏低
- ⚠️ 纺织制造板块持续性一般，非当前市场主线

---

## 🎯 今日打板操作建议

### 综合排序

| 排名 | 标的 | 封板质量 | 板块持续性 | 接力难度 | 综合评级 |
|---|---|---|---|---|---|
| **1** | **天娱数科** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | **优先关注** |
| **2** | **华升股份** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **次选** |
| **3** | **模塑科技** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | **谨慎** |

### 买入时机

**天娱数科（002354）— 首选**
- **打板买入**：如果明天高开 3%-6% 且开盘后承接有力（分时均线上方运行），可在换手率到 5%-8% 时分批介入
- **排板买入**：如果一字板开盘，观察封单是否持续增加，排板需谨慎（秒板次日容易高开低走）
- **放弃条件**：高开 >8% 后快速下杀破分时均线，放弃

**华升股份（600156）— 次选**
- **打板买入**：如果高开 2%-5%，开盘后放量换手（换手率到 8%+）后封板，可打板介入
- **低吸机会**：小盘股弹性大，如果开盘小幅低开或平开，可轻仓试错
- **放弃条件**：高开 >7% 缩量秒板，放弃（容易炸板）

**模塑科技（000700）— 谨慎**
- 仅作为板块轮动备选，如果前两个都买不到且汽车零部件板块当日强势，可考虑轻仓打板
- 封单偏弱，建议等二封确认后再介入

### 仓位建议（假设总仓位 10 成）

| 标的 | 仓位 | 说明 |
|---|---|---|
| 天娱数科 | **3 成** | 核心仓位，封单质量最高 |
| 华升股份 | **2 成** | 小盘弹性标的 |
| 模塑科技 | **1 成** | 观察仓，确认后加 |
| 现金 | **4 成** | 留足子弹应对炸板或次日补仓 |

### 止损纪律

| 标的 | 止损线 | 逻辑 |
|---|---|---|
| 天娱数科 | **买入价 -5%** | 中大盘首板，跌破 5% 说明资金出逃 |
| 华升股份 | **买入价 -7%** | 小盘股波动大，适当放宽 |
| 模塑科技 | **买入价 -5%** | 同中大盘标准 |

### ⚠️ 风险提示

1. **今日 93 只涨停**，市场情绪偏热，次日分化概率大，切忌追高后排跟风股
2. **三只标的均为首板**，首板次日溢价率取决于大盘情绪和板块持续性
3. **竞价数据缺失**（系统显示 auction/opening 信号为 0），建议明日 09:20-09:25 观察集合竞价量能和价格走势再做最终决策
4. **天娱数科秒板换手低**，次日如果缩量高开，炸板风险较大，务必等换手充分后再考虑
5. **打板有风险**，以上仅为量化分析参考，不构成投资建议，请根据自身风险承受能力操作
--show 20260703_065929_75_9d533f  |  --continue 20260703_065929_75_9d533f "..."  |  --code 20260703_065929_75_9d533f  |  --pine 20260703_065929_75_9d533f
