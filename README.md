# 多智能体交易竞技场：面向股票市场的语言驱动交易系统

## 项目简介

本项目是一个**基于大语言模型的多智能体股票交易竞技场**，旨在研究AI代理在虚拟股票市场中的自主交易决策能力。通过LLM驱动多个具有不同风险偏好和投资风格的AI代理，在实时市场环境中进行交易竞争，解决如何利用大语言模型实现智能化、自主化的投资交易策略问题。

## 项目方向

Agentic AI 原生开发——基于 AI 代理的多轮决策与协作

## 技术栈

**后端：**
- Python 3.x
- Django 5.2（Web 框架）
- SQLite 3（数据存储）
- Redis（缓存与消息队列）
- LLM 集成：DeepSeek API

**前端：**
- Vue.js 3
- TypeScript
- Vite（构建工具）
- Element Plus（UI 组件库）
- ECharts（数据可视化）
- Axios（HTTP 客户端）
- Pinia（状态管理）

**其他：**
- Docker（容器化）
- CORS 中间件

## 目录结构

```
src/AgentStock/
├── AgentStock/                    # Django 应用配置目录
│   ├── Stockagent/               # 核心多智能体交易引擎
│   │   ├── Person.py             # 投资者代理类（包含 Broker 经纪人）
│   │   ├── Stock.py              # 股票类与市场指数类
│   │   ├── Market.py             # 市场交易撮合引擎
│   │   ├── behavior.py           # 交易行为生成与决策逻辑
│   │   ├── database.py           # 数据库初始化
│   │   ├── database_utils.py     # 数据库操作工具函数
│   │   ├── constant.py           # 常量定义（天数、人数、股数等）
│   │   ├── load_json.py          # JSON 数据加载与保存
│   │   ├── main.py               # 主程序入口（完整交易流程）
│   │   └── content/              # LLM 提示词和生成模块
│   │       ├── our_run_gpt_prompt.py  # GPT API 调用与提示词工程
│   │       ├── gpt_structure.py       # GPT 响应解析结构
│   │       └── utils.py              # 辅助工具函数
│   ├── utils/                    # 通用工具模块
│   │   └── redis_service.py      # Redis 缓存服务
│   ├── settings.py               # Django 配置文件
│   ├── urls.py                   # URL 路由配置
│   ├── views.py                  # 视图处理器
│   ├── wsgi.py                   # WSGI 应用程序入口
│   └── asgi.py                   # ASGI 应用程序入口
├── Fronted/                       # 前端应用（Vue.js）
│   ├── src/
│   │   ├── views/               # 页面组件
│   │   │   ├── Dashboard.vue    # 仪表板主页
│   │   │   ├── SimulationView.vue   # 交易模拟视图
│   │   │   ├── StockmarketView.vue  # 股票市场实时行情
│   │   │   ├── ComparisonView.vue   # 代理性能对比
│   │   │   └── AboutView.vue        # 关于页面
│   │   ├── components/          # 可复用组件
│   │   │   ├── AgentPanel.vue   # 代理信息展示
│   │   │   └── StockPanel.vue   # 股票信息展示
│   │   ├── router/              # 路由配置
│   │   ├── stores/              # Pinia 状态管理
│   │   └── utils/               # 前端工具函数
│   ├── package.json             # 前端依赖配置
│   └── vite.config.ts           # Vite 构建配置
├── manage.py                     # Django 管理命令入口
├── db.sqlite3                    # SQLite 数据库文件
└── test_simple.py               # 简单测试脚本
```

### 核心模块职责说明

| 模块 | 职责 | 关键类/函数 |
|------|------|-----------|
| **Person.py** | 定义投资者代理与经纪人 | `Person`（代理）、`Broker`（经纪人） |
| **Stock.py** | 定义股票对象与市场指数 | `Stock`（股票）、`Market_index`（指数） |
| **Market.py** | 市场撮合与交易结算 | `Market`（交易引擎） |
| **behavior.py** | LLM 驱动的交易决策生成 | `stock_ops()`、`reflection()`、`generate_gossip()` |
| **database_utils.py** | 数据库 CRUD 操作 | `Database_operate`、各类查询函数 |
| **our_run_gpt_prompt.py** | LLM API 调用与提示词工程 | `run_gpt_prompt_choose_buy_stock()`、`run_gpt_prompt_choose_sell_stock()` |
| **main.py** | 完整交易流程编排 | `overall_test()`（8天交易模拟） |

## 环境搭建

### 1. 依赖安装

#### 后端依赖（Python 3.8+）

```bash
# 进入后端目录
cd src/AgentStock

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装 Django 和其他依赖
pip install django==5.2
pip install django-cors-headers
pip install redis
# 如使用 DeepSeek API，安装相应的 LLM 库（如 openai、langchain 等）
# pip install openai langchain
```

#### 前端依赖（Node.js 18+）

```bash
# 进入前端目录
cd src/AgentStock/Fronted

# 安装前端依赖
npm install
```

### 2. 环境变量配置

⚠️ **重要：不硬编码 API Key**

在项目根目录创建 `.env` 文件（**不要提交到版本控制**）：

```bash
# 后端环境变量
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DJANGO_SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 数据库路径
DATABASE_PATH=./db.sqlite3
```

在 Django 设置文件中读取环境变量：

```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-default-key')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### 3. 启动步骤

#### 方式一：分别启动前后端

**启动后端服务：**
```bash
cd src/AgentStock
python manage.py runserver 8000
```

后端 API 地址：`http://localhost:8000`

**启动前端开发服务器（新终端）：**
```bash
cd src/AgentStock/Fronted
npm run dev
```

前端应用地址：`http://localhost:5173`

#### 方式二：运行核心交易模拟

```bash
cd src/AgentStock
python -m AgentStock.Stockagent.main
```

此命令将执行 8 天的完整虚拟交易模拟，结果保存到数据库和本地文件。

#### 前端构建生产版本

```bash
cd src/AgentStock/Fronted
npm run build
```

输出目录：`dist/`

## 使用流程

1. **配置环境变量** → 设置 LLM API Key 和数据库路径
2. **安装依赖** → 后端 Python 包、前端 Node 包
3. **启动后端** → `python manage.py runserver`
4. **启动前端** → `npm run dev`
5. **访问应用** → 浏览器打开 `http://localhost:5173`

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final

## 联系方式

有问题？请提交 Issue 或 PR！
