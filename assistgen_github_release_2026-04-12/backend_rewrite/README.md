# backend_rewrite

这是合规原创改版的后端实现，当前版本已从单文件骨架迁移为分层结构（api/services/domain/infra），并保持原有接口契约可用。

## 分层结构

- `app/api/`：路由与 HTTP 协议层
- `app/services/`：业务编排层
- `app/domain/`：领域模型与仓储协议
- `app/infra/`：基础设施实现（默认 SQLite，支持 memory 回退）
- `app/core/`：容器与依赖装配

## 当前已覆盖接口

- `GET /health`
- `POST /api/chat`（支持 SSE/非流式）
- `POST /api/reason`
- `POST /api/search`
- `POST /api/upload`
- `POST /api/upload/image`
- `POST /api/conversations`
- `GET /api/conversations/user/{user_id}`
- `GET /api/conversations/{conversation_id}/messages`
- `DELETE /api/conversations/{conversation_id}`
- `PUT /api/conversations/{conversation_id}/name`
- `POST /api/langgraph/query`
- `POST /api/langgraph/resume`

## 本轮后端增强（已完成）

- `POST /api/chat` 已接入可切换的 LLM 适配层（`mock` / `ollama` / `deepseek(openai兼容)`）
- `stream=false` 与 `stream=true` 都走统一模型调用链路
- 聊天写库语义保持一致：带 `conversation_id` 时保存 user/assistant 双消息
- 无效会话 ID 聊天请求返回 `404`
- `POST /api/upload` 上传文本会落库到 `knowledge_items`
- `POST /api/search` 从 SQLite 知识表检索，支持上传后立即命中
- `POST /api/reason` 返回推理步骤并附带检索证据片段

## LLM 配置（环境变量）

- `ASSISTGEN_LLM_PROVIDER`：`mock` / `ollama` / `deepseek` / `openai`
- `ASSISTGEN_LLM_BASE_URL`：
  - ollama 示例：`http://127.0.0.1:11434`
  - deepseek/openai 兼容示例：`https://api.deepseek.com`
- `ASSISTGEN_LLM_API_KEY`：DeepSeek/OpenAI 兼容接口所需
- `ASSISTGEN_LLM_DEFAULT_MODEL`：默认模型名（如 `deepseek-chat`）
- `ASSISTGEN_LLM_TIMEOUT_SECONDS`：请求超时（秒）

### API Key 使用注意（测试环境）

- 测试 key 仅用于本地联调，不要写入代码、README、截图或提交记录
- 建议仅在本地终端或 PyCharm Run Configuration 中注入 `ASSISTGEN_LLM_API_KEY`
- 发布到 GitHub 前，建议轮换为新 key，并确认仓库历史中不含旧 key

## 存储说明

- 默认使用 SQLite 持久化会话与消息历史
- 数据文件默认位置：`backend_rewrite/data/assistgen.sqlite3`
- 可通过环境变量 `ASSISTGEN_DB_PATH` 覆盖数据库路径
- 如需临时切换回内存仓储，可设置 `ASSISTGEN_CONVERSATION_STORE=memory`

## 运行（仅项目内 Python + 虚拟环境）

### 方式 A：用脚本自动准备并启动（推荐）

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\scripts"
.\start_backend.ps1 -PrepareOnly
.\start_backend.ps1
```

> 脚本会在 `backend_rewrite/.python-base/` 下准备项目内 Python 运行时，并创建 `backend_rewrite/.venv/`。

### 方式 B：手动使用项目内 Python + `.venv`

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\backend_rewrite"
.\.python-base\tools\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
```

## PyCharm 2025.3 设置建议

- `File -> Settings -> Project -> Python Interpreter`
- 选择 `Add Interpreter -> Existing` 或 `Add Local Interpreter`
- 指向：`backend_rewrite/.venv/Scripts/python.exe`
- 勾选当前项目专用解释器，避免使用全局 Python

## 测试

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\backend_rewrite"
.\.venv\Scripts\python.exe -m pytest -q
```

当前结果：`10 passed`

## Alembic 迁移

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\backend_rewrite"
.\.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
```

可选检查：

```powershell
.\.venv\Scripts\python.exe -m alembic -c alembic.ini current
```

## Docker 运行

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose up -d --build
```

后端日志：

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose logs -f backend
```

说明：容器启动会自动执行 `alembic upgrade head`，然后再启动 `uvicorn`。

## 契约测试重点

- SSE 终止帧包含 `data: [DONE]`
- 会话 CRUD 路径可用
- 带会话上下文的聊天请求会写入会话历史
- LangGraph 占位 query/resume 路径可用
- 无效会话 ID 的聊天请求返回 `404`
- 上传文本后，`/api/search` 可检索到对应知识项



