# AgentStock 架构说明

## 1. 系统定位

AgentStock 是一个面向股票市场的多智能体交易仿真系统。系统用大语言模型驱动不同投资者 Agent 完成信息分析、传闻生成、买卖决策和策略反思，并在一个简化的撮合市场中记录股票价格、订单成交、账户资产、Agent 记忆和仿真快照。

当前工程由三部分组成：

- 前端展示层：`src/AgentStock/Fronted`，基于 Vue 3、Vite、TypeScript、Element Plus、ECharts。
- 后端 API 层：`src/AgentStock/AgentStock`，基于 Django，提供仿真启动、结果查询、股票行情查询和 Agent 对比接口。
- 仿真核心层：`src/AgentStock/AgentStock/Stockagent`，负责 Agent、股票、市场、数据库、Prompt 和 LLM 调用。

## 2. 顶层目录

```text
AgentStock_V3/
|-- README.md
|-- LICENSE
|-- docs/
|   |-- architecture.md
|   |-- agent.mp4
|   `-- CS599_大作业报告.pdf
`-- src/
    `-- AgentStock/
        |-- manage.py
        |-- db.sqlite3
        |-- AgentStock/
        |   |-- settings.py
        |   |-- urls.py
        |   |-- views.py
        |   |-- utils/
        |   |   `-- redis_service.py
        |   `-- Stockagent/
        |       |-- main.py
        |       |-- constant.py
        |       |-- Person.py
        |       |-- Stock.py
        |       |-- Market.py
        |       |-- behavior.py
        |       |-- database_utils.py
        |       |-- load_json.py
        |       `-- content/
        |           |-- gpt_structure.py
        |           |-- our_run_gpt_prompt.py
        |           |-- our_prompt_template/
        |           `-- our_prompt_without_price/
        |-- save/
        `-- Fronted/
            |-- package.json
            |-- vite.config.ts
            `-- src/
                |-- main.ts
                |-- App.vue
                |-- router/
                |-- views/
                |-- components/
                `-- utils/
```

## 3. 分层架构

```text
Browser
  |
  | HTTP / Axios
  v
Vue 3 Frontend
  |-- Dashboard: 参数输入与启动仿真
  |-- SimulationView: Agent 收益曲线与交易动作
  |-- StockmarketView: 股票 K 线与价格表
  `-- ComparisonView: Agent 收益对比与排行
  |
  | REST API
  v
Django Backend
  |-- urls.py: API 路由
  |-- views.py: 参数校验、调用仿真、读取 SQLite、返回 JSON
  `-- utils/redis_service.py: Redis 辅助封装
  |
  | Python function call / SQLite file access
  v
Simulation Core
  |-- main.py: 仿真生命周期编排
  |-- Person.py: Agent 与 Broker 账户、下单、结算
  |-- Stock.py: 股票与市场指数
  |-- Market.py: 订单撮合与价格更新
  |-- behavior.py: LLM 行为逻辑、决策解析、反思
  |-- database_utils.py: SQLite 表、查询、订单提交、绘图
  |-- load_json.py: 初始 JSON 与对象快照读写
  `-- content/: Prompt 模板和模型请求封装
  |
  | persistence
  v
SQLite + JSON + Pickle + Images
```

## 4. 运行时主流程

### 4.1 从前端启动仿真

1. 用户打开前端首页 `/`，在 `Dashboard.vue` 中配置模拟天数、Agent 数量和股票数量。
2. 前端通过 `src/utils/http.ts` 中的 Axios 实例请求 Django：

```text
GET /api/paraminit?No_Days=...&Num_Person=...&Num_Stock=...
```

3. `views.paraminit` 校验参数范围：

- `No_Days >= 1`
- `1 <= Num_Person <= 12`
- `1 <= Num_Stock <= 10`

4. 后端按股票数量生成股票名称，例如 `A, B, C`。
5. 后端动态修改 `Stockagent.constant` 中的运行参数：

- `No_Days`
- `Num_Person`
- `Num_Stock`
- `STOCK_NAME`
- `SAVE_NAME`
- `Save_Path`
- `persona_path`
- `stock_path`

6. 后端创建新的保存目录 `save/sim_YYYYMMDD_HHMMSS`。
7. 后端同步调用 `overall_test()` 执行完整仿真。
8. 仿真结束后，后端返回 `status=success`，前端跳转到 `/simulation`。

注意：当前 `/api/paraminit` 是同步长任务接口。前端设置了 5 分钟超时，但后端没有任务队列、后台 Job、进度查询或取消机制。

### 4.2 仿真核心循环

核心入口在 `Stockagent/main.py`：

```text
overall_test()
  -> init_all(False)
     -> 创建 Database_operate(save/.../data)
     -> 删除旧表并初始化 SQLite 表
     -> 创建 Stock 列表
     -> 创建 Market_index
     -> 创建 Broker
     -> 创建 Person Agent 列表
     -> 创建 Market
  -> for virtual_date in range(No_Days)
     -> 第 0 天由 Broker 执行 IPO 挂卖单
     -> 更新市场指数
     -> generate_gossip()
     -> for iter in range(Iterations_Daily)
        -> stock_ops(): LLM 分析并生成买/卖/持有动作
        -> Person.create_order(): 将动作转换为订单
        -> Market.match_order(): 撮合 Agent 间订单
        -> Market.end_of_market(): 剩余订单由 Broker 参与处理
        -> 更新市场指数
        -> Person.end_of_iteration(): 更新 Agent 资产
        -> save_all(): 保存对象快照
     -> Market.end_of_day(): 关闭剩余 active 订单
     -> Person.end_of_day(): 结算现金、资产、费用、股息
     -> Stock.end_of_day(): 写入下一日股票开盘状态
     -> Market_index.end_of_day(): 写入下一日指数
```

## 5. 核心模块职责

### 5.1 Django 后端

`AgentStock/settings.py`

- 使用 SQLite 作为 Django 默认数据库：`src/AgentStock/db.sqlite3`。
- 启用 `corsheaders`，允许 `http://localhost:5173` 和 `http://localhost:5174`。
- 使用本地内存缓存 `LocMemCache`。
- `DEBUG=True`、`ALLOWED_HOSTS=['*']`，更适合开发环境。

`AgentStock/urls.py`

| 路径 | 视图 | 作用 |
| --- | --- | --- |
| `/api/paraminit` | `paraminit` | 初始化参数并启动一次仿真 |
| `/api/simulation_results` | `get_simulation_results` | 查询 Agent 收益曲线和成交动作 |
| `/api/stock_data` | `get_stock_data` | 查询股票 OHLC 价格序列 |
| `/api/agent_comparison` | `get_agent_comparison` | 查询 Agent 收益曲线和最终资产 |
| `/testcache` | `testcache` | 本地缓存测试 |
| `/redis_test` | `redis_test_view` | Redis 数据结构测试 |

`AgentStock/views.py`

- 接收前端参数。
- 更新仿真全局常量。
- 调用 `overall_test()`。
- 直接读取 `save/{simulation_id}/data.db`。
- 将 SQLite 查询结果整理为前端所需 JSON。

### 5.2 仿真编排

`Stockagent/main.py`

- 是仿真的总入口。
- `init_all(load=False)` 负责初始化或加载仿真对象。
- `overall_test()` 负责按天和日内迭代推进仿真。
- 当前默认使用 `Iterations_Daily=1`。

`Stockagent/constant.py`

- 保存仿真超参数和路径。
- 关键参数包括：

| 参数 | 含义 |
| --- | --- |
| `No_Days` | 仿真天数 |
| `Iterations_Daily` | 每个虚拟日的交易迭代次数 |
| `Num_Person` | 投资者 Agent 数量 |
| `Num_Stock` | 股票数量 |
| `STOCK_NAME` | 股票名称列表 |
| `Daily_Price_Limit` | 单次成交价格相对当前价的涨跌限制 |
| `expense_ratio` | Agent 日常费用计算比例 |
| `Fluctuation_Constant` | 交易量影响价格变化的权重 |
| `Save_Path` | 当前仿真输出目录 |

### 5.3 Agent 与账户

`Stockagent/Person.py`

包含两个主要类：

- `Person`：普通投资者 Agent。
- `Broker`：市场发行方/兜底交易方，`person_id = -1`。

`Person` 维护：

- 现金 `cash`
- 股票资产 `asset`
- 总财富 `wealth`
- 投资原则 `principle`
- 人设信息 `identity`
- 最低生活成本 `minimum_living_expense`
- 反思频率 `reflect_frequency`
- 持仓账户
- 交易记忆
- 市场传闻

核心方法：

| 方法 | 作用 |
| --- | --- |
| `initialize_person()` | 从 `persona.json` 读取 Agent 初始资金、收入、策略等 |
| `create_order()` | 将 LLM 行为结果转换为买/卖订单 |
| `settlement()` | 成交后更新现金、持仓、成本价和资产 |
| `end_of_iteration()` | 每轮交易后按最新股价更新资产 |
| `end_of_day()` | 每日结算股息、生活成本、资产和下一日账户记录 |
| `query_prompt()` | 生成持仓摘要，供 Prompt 使用 |
| `add_memory()` | 记录每次分析、交易、反思上下文 |
| `add_gossip()` | 记录 Agent 生成的市场传闻 |

`Broker` 维护所有股票初始库存。第 0 天通过 `ipo()` 将股票挂为卖单，为市场提供初始供给。

### 5.4 股票与市场指数

`Stockagent/Stock.py`

`Stock` 表示单只股票，负责：

- 从 `stocks.json` 初始化数量、名称、价格、每股股息。
- 写入历史价格。
- 更新日内价格、成交量、最高价、最低价。
- 为 LLM Prompt 提供近期价格序列和当日价格变化。

`Market_index` 表示市场指数，`stock_id = -1`。它根据各股票初始账面价值权重计算加权指数，并写入同一张 `stock` 表。

### 5.5 市场撮合

`Stockagent/Market.py`

市场撮合逻辑围绕 `active_orders` 表运行：

1. `_fetch_orders("buy", stock_id)` 查询某股票 active 买单。
2. `_fetch_orders("sell", stock_id)` 查询某股票 active 卖单。
3. `match_order(today)` 对每只股票撮合买卖双方。
4. 成交价取买卖报价均值，再按交易量和 `Fluctuation_Constant` 调整股票当前价。
5. `_update_order()` 将订单更新为：

- `finished`
- `partially fulfilled`
- `update`

6. 成交后调用对应 `Person.settlement()` 更新 Agent 账户。
7. `end_of_market()` 会尝试让 Broker 处理剩余 active 订单。
8. `end_of_day()` 将仍未完成的 active 订单关闭为 `closed`。

价格更新简化模型：

```text
new_price =
  (deal_price * trade_quantity * Fluctuation_Constant + current_price * total_quantity)
  / (trade_quantity * Fluctuation_Constant + total_quantity)
```

如果成交价相对当前价的偏离超过 `Daily_Price_Limit`，该轮撮合会跳过。

### 5.6 LLM 行为层

`Stockagent/behavior.py`

负责把 LLM 输出转换成可执行行为：

- `generate_gossip()`：为每个 Agent 生成市场传闻。
- `stock_ops()`：为每个 Agent 生成买入、卖出或持有决策。
- `reflection()`：按反思频率生成策略复盘和新策略。
- `extract_for_choose_buy()`：用正则解析买入响应。
- `extract_for_choose_sell()`：用正则解析卖出响应。
- `extract_analysis_for_reflect()`：解析策略优缺点。
- `extract_strategy()`：解析新策略。

`Stockagent/content/our_run_gpt_prompt.py`

负责组合 Prompt 输入：

- 股票信息：`integrate_stock_info()`
- 持仓信息：`integrate_hold_info()`
- 传闻信息：`integrate_gossip()`
- 历史记忆：`integrate_reflect_info()`
- 买入决策：`run_gpt_prompt_choose_buy_stock()`
- 卖出决策：`run_gpt_prompt_choose_sell_stock()`
- 分析结果：`analysis()`
- 传闻生成：`run_gpt_generate_gossip()`
- 策略更新：`update_strategy()`

`Stockagent/content/gpt_structure.py`

封装不同模型提供方调用：

- OpenAI 兼容接口。
- DashScope/Qwen VL。
- DeepInfra Llama / DeepSeek。
- Gemini。
- 多图输入接口。

环境变量主要包括：

| 变量 | 用途 |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI 接口 |
| `DASHSCOPE_API_KEY` | DashScope/Qwen 接口 |
| `DASHSCOPE_BASE_URL` | DashScope OpenAI-compatible base URL |
| `DEEPINFRA_API_KEY` | DeepInfra 接口 |
| `DEEPINFRA_BASE_URL` | DeepInfra OpenAI-compatible base URL |
| `GOOGLE_API_KEY` | Gemini 接口 |

当前 `ChatGPT_safe_generate_response()` 中存在按 `person_id` 切换模型的逻辑，但后续又统一调用了一次 `qwenvl(prompt)`，实际效果以最后一次赋值为准。

## 6. 数据持久化

系统有两类 SQLite：

- Django 默认库：`src/AgentStock/db.sqlite3`，由 Django 配置使用。
- 仿真结果库：`src/AgentStock/save/{simulation_id}/data.db`，由 `Database_operate` 创建和读写。

前端展示主要依赖仿真结果库，而不是 Django ORM。

### 6.1 仿真表结构

`active_orders`

| 字段 | 含义 |
| --- | --- |
| `timestamp` | 订单时间戳，作为订单标识 |
| `virtual_date` | 虚拟日期 |
| `weekday` | 虚拟星期 |
| `iteration` | 当日迭代轮次 |
| `stock_id` | 股票 ID |
| `person_id` | Agent ID，Broker 为 -1 |
| `type` | `buy` 或 `sell` |
| `price` | 报价或成交价 |
| `quantity` | 数量 |
| `status` | `active`、`closed`、`finished` |

`stock`

| 字段 | 含义 |
| --- | --- |
| `stock_id` | 股票 ID，市场指数为 -1 |
| `virtual_date` | 虚拟日期 |
| `weekday` | 虚拟星期 |
| `volume` | 成交额 |
| `quantity` | 成交数量 |
| `last_price` | 最新价/收盘价 |
| `begin_price` | 开盘价 |
| `highest_price` | 最高价 |
| `lowest_price` | 最低价 |

`person`

| 字段 | 含义 |
| --- | --- |
| `person_id` | Agent ID，Broker 为 -1 |
| `virtual_date` | 虚拟日期 |
| `cash` | 现金 |
| `asset` | 股票资产 |
| `wealth` | 总财富 |
| `work_income` | 工作收入 |
| `capital_gain` | 资本收益 |
| `daily_expense` | 当日支出 |
| `principle` | 投资原则/策略 |

`account`

| 字段 | 含义 |
| --- | --- |
| `person_id` | Agent ID |
| `stock_id` | 股票 ID |
| `virtual_date` | 虚拟日期 |
| `weekday` | 虚拟星期 |
| `quantity` | 持仓数量 |
| `cost_price` | 持仓成本价 |
| `current_price` | 当前价 |
| `profit` | 收益率 |
| `start_date` | 建仓日期 |

`memory`

记录 Agent 决策上下文，包括交易动作、策略、传闻、股票分析、策略分析、价格信息、市场变化和财务状况。

`gossip`

记录 Agent 在某个虚拟日期生成的市场传闻。

### 6.2 文件输出

每次仿真会保存到 `save/{simulation_id}`：

```text
save/sim_YYYYMMDD_HHMMSS/
|-- data.db
|-- persona.json
|-- stocks.json
|-- information.json
`-- classes/
    |-- STOCK_0.pkl
    |-- PERSON_0.pkl
    |-- Market_index.pkl
    `-- MARKET.pkl
```

另外，绘图工具可能在当前工作目录生成：

- `stock_A_price.jpg`
- `stock_B_price.jpg`
- `stock_C_price.jpg`
- `plot_order.jpg`
- `plot_person{n}_order.jpg`

这些图片可被多模态模型调用逻辑转为 base64 image URL。

## 7. API 说明

### 7.1 启动仿真

```text
GET /api/paraminit
```

Query 参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `No_Days` | `11` | 仿真天数 |
| `Num_Person` | `4` | Agent 数量 |
| `Num_Stock` | `3` | 股票数量 |

成功响应：

```json
{
  "status": "success",
  "message": "...",
  "data": {
    "No_Days": 3,
    "Num_Person": 4,
    "Num_Stock": 3,
    "save_path": "sim_YYYYMMDD_HHMMSS",
    "simulation_id": "YYYYMMDD_HHMMSS"
  }
}
```

注意：`save_path` 带 `sim_` 前缀，`simulation_id` 当前只返回时间戳。后续查询接口默认读取 `save/{simulation_id}/data.db`，因此前后端需要统一使用 `save_path` 或统一拼接规则。

### 7.2 查询仿真结果

```text
GET /api/simulation_results?simulation_id=sim01
```

返回每个 Agent：

- `id`
- `prompt`
- `profitCurve`
- `actions`

当前 `SimulationView.vue` 固定传入 `simulation_id=sim01`。

### 7.3 查询股票数据

```text
GET /api/stock_data?simulation_id=sim01
```

返回每只股票：

- `id`
- `name`
- `prices[]`
  - `day`
  - `open`
  - `close`
  - `high`
  - `low`

`StockmarketView.vue` 当前传了 `stock_id`，后端实际主要按 `simulation_id` 查询全部股票，再由前端按 `id` 过滤。

### 7.4 查询 Agent 对比

```text
GET /api/agent_comparison?simulation_id=sim01
```

返回：

- `agents[]`
  - `id`
  - `profitCurve`
  - `finalValue`
- `dayLabels[]`
- `simulation_id`

当前 `ComparisonView.vue` 未显式传入 `simulation_id`，后端默认使用 `sim01`。

### 7.5 Redis 测试

```text
GET /redis_test
```

该接口通过 `RedisService` 测试 String、Hash、Set、List、Sorted Set。它是辅助测试接口，不参与主仿真链路。

## 8. 前端架构

`Fronted/src/main.ts` 启动 Vue 应用，并挂载路由和 UI 组件库。

`Fronted/src/router/index.ts` 定义页面：

| 路径 | 组件 | 作用 |
| --- | --- | --- |
| `/` | `Dashboard.vue` | 参数配置与启动 |
| `/simulation` | `SimulationView.vue` | 单个 Agent 结果展示 |
| `/compare` | `ComparisonView.vue` | 多 Agent 对比 |
| `/stock` | `StockmarketView.vue` | 股票行情 |
| `/about` | `AboutView.vue` | 项目信息 |

`Fronted/src/utils/http.ts`

- Axios `baseURL` 为 `http://localhost:8000`。
- 超时时间为 `300000ms`。

主要展示组件：

- `AgentPanel.vue`：展示 Agent 策略、收益曲线和交易动作。
- `StockPanel.vue`：展示股票数据。

图表层使用 ECharts / vue-echarts：

- 折线图：收益曲线、Agent 对比。
- K 线图：股票 OHLC。

## 9. 关键数据流

### 9.1 启动与结果展示

```text
Dashboard.vue
  -> GET /api/paraminit
     -> views.paraminit
        -> constant 参数更新
        -> overall_test()
           -> SQLite data.db 写入
           -> JSON/Pickle/图片输出
  -> router.push('/simulation')
     -> SimulationView.vue
        -> GET /api/simulation_results?simulation_id=sim01
           -> SQLite 查询 person / active_orders / memory
           -> AgentPanel 展示
```

### 9.2 LLM 决策链路

```text
Person 当前状态 + Stock 当前状态 + Market_index + Gossip + Memory
  -> our_run_gpt_prompt.py 组装 Prompt
  -> gpt_structure.py 调用模型
  -> behavior.py 正则解析模型输出
  -> Person.create_order()
  -> active_orders
  -> Market.match_order()
  -> Person.settlement()
  -> person/account/stock/memory 表更新
```

### 9.3 股票价格链路

```text
订单成交
  -> 计算 deal_price
  -> 结合 trade_quantity 和 Fluctuation_Constant 更新 Stock.current_price
  -> Stock.update_trade_data()
  -> stock 表更新 last/begin/high/low/volume/quantity
  -> Market_index.update_market_index()
  -> /api/stock_data
  -> StockmarketView K 线图
```

## 10. 当前实现约束与改进点

1. 仿真启动是同步阻塞接口，长仿真会占用 Django 请求线程。更稳妥的做法是引入后台任务、任务状态表和轮询接口。
2. 前端启动仿真后没有保存新返回的 `save_path`，结果页仍默认读取 `sim01`。这会导致最新仿真结果不一定被展示。
3. `simulation_id` 命名不统一：启动接口返回时间戳，但保存目录是 `sim_时间戳`。
4. 仿真大量依赖 `constant.py` 全局变量。并发请求时，不同仿真参数可能互相覆盖。
5. SQLite 查询多处直接拼接 SQL 字符串，建议逐步改为参数化查询。
6. `database_utils.py` 中部分图表和查询函数固定读取 `save/sim01/data.db`，与多次仿真目录机制不一致。
7. `active_orders.status` 表约束只允许 `active`、`closed`、`finished`，但代码中出现 `partially fulfilled` 作为逻辑状态；当前它通过插入 `finished` 记录和更新原订单规避，但表设计和业务语义仍不完全一致。
8. LLM 输出依赖严格正则格式，模型返回稍有偏差就可能解析失败。建议保留 JSON Schema 或结构化输出格式。
9. Prompt、模型选择和图片路径中仍有硬编码。建议抽离为配置。
10. Django 默认数据库与仿真数据库分离，当前没有 ORM 模型或统一 Repository 层。短期可接受，长期维护建议封装仿真数据访问层。

## 11. 开发运行关系

后端：

```sh
cd src/AgentStock
python manage.py runserver
```

前端：

```sh
cd src/AgentStock/Fronted
npm install
npm run dev
```

默认地址：

- 后端：`http://localhost:8000`
- 前端：`http://localhost:5173`

完整仿真需要配置对应模型服务的 API Key，否则 LLM 调用会失败并返回错误兜底结果。
