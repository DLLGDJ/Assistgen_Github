# AssistGen 合规原创改版（淘宝商家智能客服）

一个面向 GitHub 展示与简历讲解的重写项目：在保持原有能力边界的前提下，对后端、前端、部署与文档进行工程化重构。

## 项目亮点

- FastAPI 后端重写，按 `api/services/domain/infra/core` 分层组织
- Vue 3 + Vite + TypeScript 前端重构，按 `pages/features/composables/services/shared` 模块化拆分
- 支持会话中心、历史消息、流式聊天、知识上传与检索、LangGraph 占位入口
- 引入 SQLite 持久化与 Alembic 迁移，便于后续演进
- 提供 Docker Compose（前后端编排）与 Nginx 静态托管方案
- 配套文档、变更记录、发布清单与合规说明，适合公开仓库展示

## 功能概览

- `GET /health`：服务健康检查
- `POST /api/chat`：聊天（支持 `stream=true/false`）
- `POST /api/reason`：推理步骤返回（含证据片段）
- `POST /api/search`：知识检索
- `POST /api/upload`、`POST /api/upload/image`：上传入口
- 会话管理：创建 / 列表 / 重命名 / 删除 / 历史消息
- `POST /api/langgraph/query`、`POST /api/langgraph/resume`：工作流预留接口

## 技术栈

- 后端：FastAPI、Uvicorn、Pydantic、SQLAlchemy、Alembic、SQLite
- 前端：Vue 3、Vite、TypeScript、Nginx
- 运行环境：Windows + PowerShell（已提供启动脚本）

## 项目结构

- `backend_rewrite/`：后端源码、迁移、测试、容器配置
- `frontend_rewrite/`：前端源码、构建配置、Nginx 配置
- `docs/`：架构、部署、截图规范、改版说明、发布清单
- `evidence/`：接口映射、依赖许可证清单
- `scripts/`：本地启动与回滚脚本

## 快速开始（本地开发）

### 1) 启动后端

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\scripts"
.\start_backend.ps1 -PrepareOnly
.\start_backend.ps1
```

默认后端地址：`http://localhost:8100`

> 脚本会在项目内准备 `backend_rewrite/.python-base/` 与 `backend_rewrite/.venv/`，不依赖全局 Python。

### 2) 启动前端

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\scripts"
.\start_frontend.ps1
```

默认前端开发地址：`http://localhost:5176`

## Docker Compose（一条命令前后端全起）

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose up -d --build
```

按当前编排配置：

- 前端入口：`http://localhost:8080`
- 后端接口：`http://localhost:8100`
- 持久化目录：`backend_rewrite/data/`

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose logs -f backend
```

## LLM 配置（环境变量）

后端支持 `mock / ollama / deepseek / openai` 兼容调用，常用变量如下：

- `ASSISTGEN_LLM_PROVIDER`：`mock` / `ollama` / `deepseek` / `openai`
- `ASSISTGEN_LLM_BASE_URL`：模型服务地址
- `ASSISTGEN_LLM_API_KEY`：API Key（请只放环境变量，不要写入仓库）
- `ASSISTGEN_LLM_DEFAULT_MODEL`：默认模型名
- `ASSISTGEN_LLM_TIMEOUT_SECONDS`：请求超时秒数

## GitHub 首页截图位

建议截图放入 `docs/images/`：

- `01-dashboard-overview.png`：页面总览（健康检查 + 会话 + 聊天）
- `02-conversation-list.png`：会话列表与历史消息
- `03-streaming-chat.png`：流式回复过程
- `04-deployment-terminal.png`：启动与部署终端画面

可在 README 中按需插入：

```markdown
![dashboard](docs/images/01-dashboard-overview.png)
![conversation](docs/images/02-conversation-list.png)
![streaming](docs/images/03-streaming-chat.png)
```

## 文档入口

- `docs/ARCHITECTURE.md`：架构设计说明
- `docs/DEPLOYMENT.md`：本地与容器部署说明
- `docs/DEPLOYMENT_TAOBAO_SELLER_NOTES.md`：淘宝商家场景部署与运营注意事项
- `docs/REWRITE_IMPROVEMENTS.md`：改版点与实现原理详解
- `docs/GITHUB_RELEASE_FILES.md`：GitHub 发布文件清单
- `docs/SCREENSHOTS.md`：截图命名规范
- `CHANGELOG.md`：发布向变更记录
- `docs/CHANGELOG_REWRITE.md`：详细改版记录
- `docs/NOTICE.md`：来源与许可证说明
- `evidence/third_party_licenses.md`：第三方依赖许可证清单

## 路线图

- 完善登录 / 权限 / 用户体系
- 增强多店铺隔离（如 `shop_id`）
- 完善知识库索引与检索策略
- 增加调用监控、限流与成本治理
- 补充生产级 HTTPS、反向代理和观测能力



## License

本仓库许可证见 `LICENSE`。
