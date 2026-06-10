# 项目名称

多智能体交易竞技场：面向股票市场的语言驱动交易系统

## 项目简介

AgentStock 是一个面向股票市场的多智能体交易仿真系统。系统通过大语言模型驱动不同投资者 Agent 进行股票分析、市场传闻生成、买卖决策和策略反思，并在一个简化撮合市场中记录价格变化、订单成交、Agent 财富曲线和策略表现。项目提供 Django 后端 API 和 Vue 前端页面，用于配置仿真参数、启动仿真、查看股票行情和对比不同 Agent 的交易结果。

## 方向

Agentic AI 原生开发

## 技术栈

- 后端: Python, Django, SQLite
- 前端: Vue 3, Vite, TypeScript, Element Plus, ECharts
- 智能体与 LLM: OpenAI SDK 兼容接口、Qwen/DeepSeek/Llama 等模型调用封装
- 数据处理与可视化: pandas, numpy, matplotlib, mplfinance
- 缓存/外部服务: Redis 工具封装


## 核心功能

- 仿真参数配置：支持设置模拟天数、Agent 数量和股票数量。
- 多 Agent 交易：不同投资者 Agent 基于自身资产、持仓、策略、市场信息和传闻生成买卖决策。
- 市场撮合：系统维护买卖订单簿，按股票撮合买卖订单，并根据成交量和成交价格更新股价。
- 市场信息生成：维护股票价格、市场指数、Agent 记忆、市场传闻和交易记录。
- 策略反思：支持基于历史交易记忆和收益表现生成策略复盘与更新。
- 结果展示：前端展示 Agent 财富曲线、交易行为、股票 K 线/价格数据和 Agent 表现对比。

## 系统模块

### 后端服务模块

后端位于 `src/AgentStock`，使用 Django 提供 API 服务。

- `AgentStock/urls.py`: 后端路由配置，注册仿真初始化、结果查询、股票数据查询和 Agent 对比接口。
- `AgentStock/views.py`: API 入口层，负责接收前端参数、调用仿真主流程、读取 SQLite 仿真结果并返回 JSON。
- `AgentStock/settings.py`: Django 工程配置，包含 SQLite、CORS、本地缓存等配置。
- `AgentStock/utils/redis_service.py`: Redis String、Hash、Set、List、SortedSet 的简单封装，用于缓存或外部状态测试。

主要 API：

- `GET /api/paraminit`: 初始化并启动一次仿真。参数包括 `No_Days`、`Num_Person`、`Num_Stock`。
- `GET /api/simulation_results`: 获取 Agent 财富曲线与已完成交易记录。
- `GET /api/stock_data`: 获取股票开盘价、收盘价、最高价、最低价等价格序列。
- `GET /api/agent_comparison`: 获取 Agent 之间的收益曲线和最终资产对比数据。
- `GET /redis_test`: Redis 连接与数据结构测试接口。

### 仿真核心模块

仿真核心位于 `src/AgentStock/AgentStock/Stockagent`。

- `main.py`: 仿真主流程。负责初始化数据库、股票、Agent、Broker 和 Market，并按虚拟日期推进交易。
- `constant.py`: 仿真参数与路径配置，例如模拟天数、每日迭代次数、Agent 数量、股票数量、保存目录等。
- `Person.py`: 定义投资者 Agent 和 Broker。Agent 维护现金、持仓、财富、策略和记忆，并负责创建订单和结算资产。
- `Stock.py`: 定义股票和市场指数。负责股票基础信息、价格历史、日内涨跌幅、K 线数据和市场指数计算。
- `Market.py`: 市场撮合引擎。负责读取活跃订单、撮合买卖双方、更新订单状态、结算资产并推动价格变化。
- `behavior.py`: Agent 行为逻辑。包括股票分析、买卖决策解析、传闻生成和策略反思。
- `database_utils.py`: SQLite 表结构、查询解析、订单提交、收益计算和图表生成工具。
- `load_json.py`: 读取和保存 persona、stocks 以及仿真对象快照。
- `content/`: Prompt 模板和 LLM 请求封装，用于分析、买入、卖出、传闻和反思等语言驱动决策。

### 前端展示模块

前端位于 `src/AgentStock/Fronted`，使用 Vue 3 + Vite 构建。

- `src/views/Dashboard.vue`: 首页参数面板，提交模拟天数、Agent 数量、股票数量并启动仿真。
- `src/views/SimulationView.vue`: 仿真详情页，展示各 Agent 的策略描述、财富曲线和交易动作。
- `src/views/ComparisonView.vue`: Agent 对比页，用于比较不同 Agent 的收益曲线和最终资产。
- `src/views/StockmarketView.vue`: 股票市场页，用于展示股票价格走势。
- `src/components/AgentPanel.vue`: 单个 Agent 的结果展示组件。
- `src/components/StockPanel.vue`: 单只股票的行情展示组件。
- `src/utils/http.ts`: Axios 实例，默认连接 `http://localhost:8000` 后端服务。
- `src/router/index.ts`: 前端路由配置，包含首页、仿真详情、Agent 对比、股票市场和 About 页面。

## 目录结构

```text
AgentStock_V3/
├── README.md
├── LICENSE
└── src/
    └── AgentStock/
        ├── manage.py
        ├── db.sqlite3
        ├── readme.txt
        ├── AgentStock/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── views.py
        │   ├── utils/
        │   │   └── redis_service.py
        │   └── Stockagent/
        │       ├── main.py
        │       ├── constant.py
        │       ├── Person.py
        │       ├── Stock.py
        │       ├── Market.py
        │       ├── behavior.py
        │       ├── database_utils.py
        │       ├── load_json.py
        │       ├── content/
        │       └── save/
        ├── save/
        │   └── sim01/
        └── Fronted/
            ├── package.json
            ├── vite.config.ts
            └── src/
                ├── views/
                ├── components/
                ├── router/
                └── utils/
```

## 环境搭建

### 1. 后端环境

进入后端目录：

```sh
cd src/AgentStock
```

创建并启用 Python 虚拟环境：

```sh
python -m venv .venv
.\.venv\Scripts\activate
```

安装后端依赖。当前仓库未提供 `requirements.txt`，可先按代码导入安装基础依赖：

```sh
pip install django django-cors-headers redis openai timeout-decorator pillow google-generativeai pandas numpy matplotlib mplfinance openpyxl
```

如需运行完整 LLM 仿真，需要配置对应模型服务的 API Key。可参考以下变量：

```text
DJANGO_SECRET_KEY=
OPENAI_API_KEY=
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DEEPINFRA_API_KEY=
DEEPINFRA_BASE_URL=https://api.deepinfra.com/v1/openai
GOOGLE_API_KEY=
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

在 PowerShell 中可以这样临时设置环境变量：

```sh
$env:DASHSCOPE_API_KEY="your_api_key"
$env:DEEPINFRA_API_KEY="your_api_key"
$env:REDIS_HOST="localhost"
```

### 2. 前端环境

进入前端目录：

```sh
cd src/AgentStock/Fronted
```

安装依赖：

```sh
npm install
```

## 启动步骤

### 1. 启动后端

在 `src/AgentStock` 目录运行：

```sh
python manage.py runserver
```

默认后端地址：

```text
http://localhost:8000
```

### 2. 启动前端

在 `src/AgentStock/Fronted` 目录运行：

```sh
npm run dev
```

默认前端地址通常为：

```text
http://localhost:5173
```

如果 5173 端口被占用，Vite 会自动切换到其他端口。后端 CORS 当前允许 `5173` 和 `5174`。

## 使用流程

1. 启动 Django 后端。
2. 启动 Vue 前端。
3. 打开前端首页，设置模拟天数、Agent 数量和股票数量。
4. 点击“开始模拟”，前端调用 `/api/paraminit`，后端执行仿真。
5. 仿真完成后进入结果页，查看 Agent 财富变化和交易记录。
6. 在股票市场页查看股票价格走势，在对比页查看 Agent 表现差异。

## 数据与输出

- 默认仿真数据位于 `src/AgentStock/save/sim01` 或 `src/AgentStock/AgentStock/Stockagent/save`。
- 新仿真会按时间戳创建 `save/sim_YYYYMMDD_HHMMSS` 目录。
- 主要输出文件包括：
  - `data.db`: SQLite 仿真数据库。
  - `persona.json`: Agent 初始画像与投资策略。
  - `stocks.json`: 股票初始数据。
  - `classes/*.pkl`: 仿真对象快照。
  - `stock_*_price.jpg`, `plot_order.jpg`, `plot_person*_order.jpg`: 可视化图表。

## 开发备注

- 当前 `SimulationView.vue` 默认读取 `simulation_id=sim01`，如果要展示最新一次仿真，需要把后端返回的 `simulation_id` 保存到前端状态或路由参数中。
- 当前仓库没有统一的 Python 依赖锁文件，建议后续补充 `requirements.txt` 或 `pyproject.toml`。
- 模型调用和 Redis 连接已改为环境变量读取；如果历史提交曾包含真实凭据，仍应在对应平台轮换旧 Key。
- 当前 `database_utils.py` 中部分图表与查询逻辑固定读取 `save/sim01/data.db`，如需支持多次仿真对比，应统一传入 `simulation_id` 或数据库路径。

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final
