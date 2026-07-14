
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
 OK   │ Content Filter     │ 5% (set via CONTENT_FILTER_WARNING_THRESHOLD)      
      │ Threshold          │                                                    

6/7 services ready

Prompt: 分析 /home/runner/work/daban-picker/daban-picker/enhanced_results.json 中综合评分 Top 3 的打板候选标的，结合竞价信号和 Alpha 因子评分，给出今日打板操作建议（买...

Let me first read the file to understand its structure.
  - read_file /home/runner/work/daban-picker/daban-picker/enhanced_results.json  OK 0.0s
数据量较大，让我继续读取完整内容。
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 综合评分 Top 标的 
现在让我进一步查看这些标的的详细数据，包括竞价信号和 Alpha 因子信息。
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 有竞价数据的标的 ===
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 数据日期 ===\n20
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== top_picks ==
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== near_miss 标的
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 全部标的按综合评分排序 
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 000968 蓝焰控股 
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 000968 蓝焰控股 
  - bash ls -la /home/runner/work/daban-picker/daban-picker/ | head -30  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "total 148\ndrwxr
  - bash cat /home/runner/work/daban-picker/daban-picker/agent_analysis.md  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "\nPreflight Chec
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== scan_results
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== near_miss ==
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "all_enhanced 数量:
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "enhanced_score 非
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== candidates 字
  - bash cat /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.py | head -100  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "#!/usr/bin/env p
  - bash cat /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.py | python3 -c  FAIL 0.0s  {"status": "error", "exit_code": 2, "stdout": "L17: Layer 3 — Alpha Zoo 三因子评分\nL
  - bash grep -n -A5 'alpha_factor\|alpha_zoo\|composite\|score_breakdown\|enhanced_score  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "356:            
  - bash cat /home/runner/work/daban-picker/daban-picker/enhanced_results.json | python3   OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 综合评分 Top 10 
现在让我看看 scan_results.json 里的原始数据，特别是竞价信号和开盘信号。
  - bash cat /home/runner/work/daban-picker/daban-picker/scan_results.json | python3 -c "  FAIL 0.0s  {"status": "error", "exit_code": 2, "stdout": "", "stderr": "/bin/sh: 17: Syntax
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "candidates 数量: 1
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 未通过规则分布 ===\
现在让我看看 enhanced_results.json 中综合评分 Top 3 的完整数据，以及竞价信号和 Alpha 因子评分。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 综合评分 Top 3 完
现在让我看看这个增强脚本的评分逻辑，以及是否有其他数据源可以补充分析。
  - bash cat /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.py | python3 -c  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "L356:           
  - bash sed -n '485,510p' /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.p  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "        for t in
  - bash sed -n '380,410p' /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.p  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "            for 
  - bash sed -n '340,380p' /home/runner/work/daban-picker/daban-picker/daban_vt_enhance.p  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "\n    print(f\"\
现在我对整个数据结构和评分逻辑有了清晰的理解。让我看看 scan_results.json 中原始标的的竞价和开盘数据。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "candidates 数量: 1
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "near_miss 数量: 38
现在让我看看 enhanced_results.json 中综合评分 Top 3 的完整数据。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 综合评分 Top 3 完
现在让我看看 scan_results.json 中原始标的的竞价和开盘数据，以及看看有没有其他数据源可以补充。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 热点板块 ===\n  
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "{\"sector\": \"元
现在让我看看 scan_results.json 中 candidates 和 near_miss 的完整数据，特别是竞价和开盘信号。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "candidates 数量: 1
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "near_miss 数量: 38
现在让我看看 enhanced_results.json 中综合评分 Top 3 的完整数据。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "=== 综合评分 Top 3 完
现在让我看看 scan_results.json 中 candidates 和 near_miss 的完整数据，以及看看有没有其他数据源可以补充。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "candidates 数量: 1
现在我有了完整的数据。让我看看 scan_results.json 中 candidates 和 near_miss 的完整数据，以及看看有没有其他数据源可以补充。
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "candidates 数量: 1
  - bash python3 -c "
import json
with open('/home/runner/work/daban-picker/daban-picker/  OK 0.0s  {"status": "ok", "exit_code": 0, "stdout": "near_miss 数量: 38
好的，数据已经全部获取完毕。现在我来给出完整的分析报告。

---

## 打板候选标的分析报告

**数据日期**: 2026-07-15（今日）

---

### 一、综合评分 Top 3 标的

| 排名 | 代码 | 名称 | 综合评分 | 价格 | 涨幅 | 换手率 | 封单额 | 首封时间 | 板数 | 流通市值 | 板块 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | 000968 | **蓝焰控股** | **1.0** | 7.48 | +10.0% | 6.96% | 5017万 | 09:39:57 | 1板 | 68.1亿 | 油气开采 |
| **#2** | 600183 | **生益科技** | **0.0** | 42.18 | +10.0% | 3.38% | 10.5亿 | 09:53:06 | - | 3541.5亿 | 元件 |
| **#3** | 001389 | **广合科技** | **0.0** | 67.10 | +10.0% | 8.95% | 2.85亿 | 09:52:03 | - | 283.4亿 | 元件 |

> ⚠️ **注意**: 综合评分中，只有 **蓝焰控股** 的 enhanced_score 为 1.0（通过全部规则），其余标的评分均为 0.0（因未通过规则被归入 near_miss 类别）。Top 2 和 Top 3 实际上是 near_miss 中按封单额排序的标的。

---

### 二、各标的详细分析

#### 🥇 #1 蓝焰控股（000968）— 综合评分 1.0

| 维度 | 数据 |
|:---|:---|
| 价格 | 7.48元（低价股，符合打板偏好） |
| 换手率 | 6.96%（在5-15%理想区间内） |
| 封单额 | 5017万（刚过5000万门槛） |
| 首封时间 | 09:39:57（10点前封板，质量好） |
| 流通市值 | 68.1亿（在30-100亿理想区间） |
| 板块 | 油气开采 |
| 热点板块 | 未标记为热点板块 |
| 竞价信号 | 无竞价数据（未触发竞价分析） |
| 开盘信号 | 无开盘数据（未触发开盘分析） |
| Alpha因子 | 无Alpha因子评分数据 |

**评分明细**: 综合评分 1.0 来自基础规则全部通过（低价+合适市值+合适换手+早盘封板+封单达标），但竞价信号、开盘信号、Alpha因子评分均为空值，说明增强评分模块未产生额外加分。

**优势**:
- ✅ 低价股（7.48元），散户跟风意愿强
- ✅ 首封时间早（09:39），封板质量好
- ✅ 换手率适中（6.96%），筹码交换充分
- ✅ 流通市值68亿，适合游资操作
- ✅ 封单5017万，勉强达标

**风险**:
- ⚠️ 封单额仅5017万，刚过门槛，封单力度偏弱
- ⚠️ 油气开采板块今日是否为核心热点存疑
- ⚠️ 无竞价信号辅助判断开盘强度

---

#### 🥈 #2 生益科技（600183）— near_miss

| 维度 | 数据 |
|:---|:---|
| 价格 | 42.18元（超过40元门槛） |
| 换手率 | 3.38%（低于5%理想区间） |
| 封单额 | **10.5亿**（非常强） |
| 首封时间 | 09:53:06（10点前） |
| 流通市值 | **3541.5亿**（远超30-100亿） |
| 板块 | 元件（PCB/电子） |
| 未通过规则 | 市值30-100亿、价<40 |

**分析**: 生益科技是大盘蓝筹股，封单10.5亿极为强势，但3541亿市值和42元价格不符合传统打板模型的小市值低价偏好。这种标的更适合趋势跟踪而非打板。

---

#### 🥉 #3 广合科技（001389）— near_miss

| 维度 | 数据 |
|:---|:---|
| 价格 | 67.10元（远超40元门槛） |
| 换手率 | 8.95%（在理想区间） |
| 封单额 | 2.85亿（强） |
| 首封时间 | 09:52:03（10点前） |
| 流通市值 | 283.4亿（超出30-100亿） |
| 板块 | 元件（PCB/电子） |
| 未通过规则 | 价<40 |

**分析**: 封单2.85亿很强，换手率8.95%理想，但67元高价和283亿市值超出打板模型偏好。元件板块今日有生益科技+广合科技双涨停，可能存在板块效应。

---

### 三、今日热点板块分析

从 scan_results 数据来看，今日涨停板中值得关注的板块：

| 板块 | 涨停家数 |
|:---|:---:|
| 元件（PCB/电子） | 生益科技、广合科技、华正新材、贤丰控股、艾华集团等多只涨停 |
| 工业金属 | 宏桥控股、驰宏锌锗、天山铝业、中孚实业 |
| 油气/油服 | 蓝焰控股、中曼石油、泰山石油 |
| 煤炭 | 大有能源、昊华能源 |

**元件板块**今日涨停家数最多，存在明显的板块效应。

---

### 四、今日打板操作建议

#### 核心判断

今日涨停板共 **39只**（candidates 1只 + near_miss 38只），打板环境一般。唯一通过全部规则的标的是 **蓝焰控股**，但封单偏弱。

#### 操作建议

**标的1：蓝焰控股（000968）— 谨慎参与**

| 维度 | 建议 |
|:---|:---|
| 买入时机 | **打板确认**：09:39已封板，若午后开板回封可轻仓参与；**不追高**：不建议竞价或开盘直接买入 |
| 仓位 | **1成仓**（轻仓试探），封单仅5017万偏弱 |
| 止损 | 以今日涨停价7.48元为基准，**跌破7.00元（-6.4%）止损**，或次日低开3%以上直接止损 |
| 逻辑 | 低价+小市值+早盘封板，符合打板模型；但封单弱、非核心热点，预期不宜过高 |

**标的2：生益科技（600183）— 观察为主**

| 维度 | 建议 |
|:---|:---|
| 买入时机 | 不适合打板操作。若看好PCB板块趋势，可等回调至5日线附近低吸 |
| 仓位 | 不参与打板 |
| 逻辑 | 3541亿市值不适合打板，但封单10.5亿说明有大资金介入，可作为板块风向标观察 |

**标的3：广合科技（001389）— 放弃**

67元高价+283亿市值，不符合打板模型，放弃。

#### 备选关注（near_miss中质量较好的）

| 标的 | 代码 | 亮点 | 不足 | 建议 |
|:---:|:---:|:---|:---|:---:|
| 艾艾精工 | 603580 | 09:25首封，封单2.46亿，市值44亿 | 换手仅0.47%，非热点 | 封板极早但换手太低，观望 |
| 力合科创 | 002243 | 09:25首封，封单1.3亿，市值82.5亿 | 换手0.57%，非热点 | 同上，一字板无参与机会 |
| 华正新材 | 603186 | 元件板块，换手13.24%充分 | 价高(277亿市值) | 元件板块跟风，观察 |
| 中曼石油 | 603619 | 油气板块，换手13.42% | 13:22才封板，太晚 | 放弃 |

#### 总体策略

1. **今日打板环境评分：⭐⭐（一般）** — 仅1只标的通过全部规则，且封单偏弱
2. **核心操作**：轻仓（≤1成）参与蓝焰控股的**回封机会**，不追高、不竞价买入
3. **不开新仓的条件**：若蓝焰控股午后不开板，则今日空仓观望
4. **明日关注**：元件板块（生益科技/广合科技）的持续性，若板块效应延续可关注低位补涨

> ⚠️ **风险提示**：以上分析基于历史数据和规则评分，不构成投资建议。打板交易风险极高，请根据自身风险承受能力决策。
Status: SUCCESS
Elapsed: 2m 35s
Run ID: 20260715_071248_74_7dbfd9
Run dir: /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/runs/20260715_071248_74_7dbfd9

好的，数据已经全部获取完毕。现在我来给出完整的分析报告。

---

## 打板候选标的分析报告

**数据日期**: 2026-07-15（今日）

---

### 一、综合评分 Top 3 标的

| 排名 | 代码 | 名称 | 综合评分 | 价格 | 涨幅 | 换手率 | 封单额 | 首封时间 | 板数 | 流通市值 | 板块 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | 000968 | **蓝焰控股** | **1.0** | 7.48 | +10.0% | 6.96% | 5017万 | 09:39:57 | 1板 | 68.1亿 | 油气开采 |
| **#2** | 600183 | **生益科技** | **0.0** | 42.18 | +10.0% | 3.38% | 10.5亿 | 09:53:06 | - | 3541.5亿 | 元件 |
| **#3** | 001389 | **广合科技** | **0.0** | 67.10 | +10.0% | 8.95% | 2.85亿 | 09:52:03 | - | 283.4亿 | 元件 |

> ⚠️ **注意**: 综合评分中，只有 **蓝焰控股** 的 enhanced_score 为 1.0（通过全部规则），其余标的评分均为 0.0（因未通过规则被归入 near_miss 类别）。Top 2 和 Top 3 实际上是 near_miss 中按封单额排序的标的。

---

### 二、各标的详细分析

#### 🥇 #1 蓝焰控股（000968）— 综合评分 1.0

| 维度 | 数据 |
|:---|:---|
| 价格 | 7.48元（低价股，符合打板偏好） |
| 换手率 | 6.96%（在5-15%理想区间内） |
| 封单额 | 5017万（刚过5000万门槛） |
| 首封时间 | 09:39:57（10点前封板，质量好） |
| 流通市值 | 68.1亿（在30-100亿理想区间） |
| 板块 | 油气开采 |
| 热点板块 | 未标记为热点板块 |
| 竞价信号 | 无竞价数据（未触发竞价分析） |
| 开盘信号 | 无开盘数据（未触发开盘分析） |
| Alpha因子 | 无Alpha因子评分数据 |

**评分明细**: 综合评分 1.0 来自基础规则全部通过（低价+合适市值+合适换手+早盘封板+封单达标），但竞价信号、开盘信号、Alpha因子评分均为空值，说明增强评分模块未产生额外加分。

**优势**:
- ✅ 低价股（7.48元），散户跟风意愿强
- ✅ 首封时间早（09:39），封板质量好
- ✅ 换手率适中（6.96%），筹码交换充分
- ✅ 流通市值68亿，适合游资操作
- ✅ 封单5017万，勉强达标

**风险**:
- ⚠️ 封单额仅5017万，刚过门槛，封单力度偏弱
- ⚠️ 油气开采板块今日是否为核心热点存疑
- ⚠️ 无竞价信号辅助判断开盘强度

---

#### 🥈 #2 生益科技（600183）— near_miss

| 维度 | 数据 |
|:---|:---|
| 价格 | 42.18元（超过40元门槛） |
| 换手率 | 3.38%（低于5%理想区间） |
| 封单额 | **10.5亿**（非常强） |
| 首封时间 | 09:53:06（10点前） |
| 流通市值 | **3541.5亿**（远超30-100亿） |
| 板块 | 元件（PCB/电子） |
| 未通过规则 | 市值30-100亿、价<40 |

**分析**: 生益科技是大盘蓝筹股，封单10.5亿极为强势，但3541亿市值和42元价格不符合传统打板模型的小市值低价偏好。这种标的更适合趋势跟踪而非打板。

---

#### 🥉 #3 广合科技（001389）— near_miss

| 维度 | 数据 |
|:---|:---|
| 价格 | 67.10元（远超40元门槛） |
| 换手率 | 8.95%（在理想区间） |
| 封单额 | 2.85亿（强） |
| 首封时间 | 09:52:03（10点前） |
| 流通市值 | 283.4亿（超出30-100亿） |
| 板块 | 元件（PCB/电子） |
| 未通过规则 | 价<40 |

**分析**: 封单2.85亿很强，换手率8.95%理想，但67元高价和283亿市值超出打板模型偏好。元件板块今日有生益科技+广合科技双涨停，可能存在板块效应。

---

### 三、今日热点板块分析

从 scan_results 数据来看，今日涨停板中值得关注的板块：

| 板块 | 涨停家数 |
|:---|:---:|
| 元件（PCB/电子） | 生益科技、广合科技、华正新材、贤丰控股、艾华集团等多只涨停 |
| 工业金属 | 宏桥控股、驰宏锌锗、天山铝业、中孚实业 |
| 油气/油服 | 蓝焰控股、中曼石油、泰山石油 |
| 煤炭 | 大有能源、昊华能源 |

**元件板块**今日涨停家数最多，存在明显的板块效应。

---

### 四、今日打板操作建议

#### 核心判断

今日涨停板共 **39只**（candidates 1只 + near_miss 38只），打板环境一般。唯一通过全部规则的标的是 **蓝焰控股**，但封单偏弱。

#### 操作建议

**标的1：蓝焰控股（000968）— 谨慎参与**

| 维度 | 建议 |
|:---|:---|
| 买入时机 | **打板确认**：09:39已封板，若午后开板回封可轻仓参与；**不追高**：不建议竞价或开盘直接买入 |
| 仓位 | **1成仓**（轻仓试探），封单仅5017万偏弱 |
| 止损 | 以今日涨停价7.48元为基准，**跌破7.00元（-6.4%）止损**，或次日低开3%以上直接止损 |
| 逻辑 | 低价+小市值+早盘封板，符合打板模型；但封单弱、非核心热点，预期不宜过高 |

**标的2：生益科技（600183）— 观察为主**

| 维度 | 建议 |
|:---|:---|
| 买入时机 | 不适合打板操作。若看好PCB板块趋势，可等回调至5日线附近低吸 |
| 仓位 | 不参与打板 |
| 逻辑 | 3541亿市值不适合打板，但封单10.5亿说明有大资金介入，可作为板块风向标观察 |

**标的3：广合科技（001389）— 放弃**

67元高价+283亿市值，不符合打板模型，放弃。

#### 备选关注（near_miss中质量较好的）

| 标的 | 代码 | 亮点 | 不足 | 建议 |
|:---:|:---:|:---|:---|:---:|
| 艾艾精工 | 603580 | 09:25首封，封单2.46亿，市值44亿 | 换手仅0.47%，非热点 | 封板极早但换手太低，观望 |
| 力合科创 | 002243 | 09:25首封，封单1.3亿，市值82.5亿 | 换手0.57%，非热点 | 同上，一字板无参与机会 |
| 华正新材 | 603186 | 元件板块，换手13.24%充分 | 价高(277亿市值) | 元件板块跟风，观察 |
| 中曼石油 | 603619 | 油气板块，换手13.42% | 13:22才封板，太晚 | 放弃 |

#### 总体策略

1. **今日打板环境评分：⭐⭐（一般）** — 仅1只标的通过全部规则，且封单偏弱
2. **核心操作**：轻仓（≤1成）参与蓝焰控股的**回封机会**，不追高、不竞价买入
3. **不开新仓的条件**：若蓝焰控股午后不开板，则今日空仓观望
4. **明日关注**：元件板块（生益科技/广合科技）的持续性，若板块效应延续可关注低位补涨

> ⚠️ **风险提示**：以上分析基于历史数据和规则评分，不构成投资建议。打板交易风险极高，请根据自身风险承受能力决策。
--show 20260715_071248_74_7dbfd9  |  --continue 20260715_071248_74_7dbfd9 "..."  |  --code 20260715_071248_74_7dbfd9  |  --pine 20260715_071248_74_7dbfd9
