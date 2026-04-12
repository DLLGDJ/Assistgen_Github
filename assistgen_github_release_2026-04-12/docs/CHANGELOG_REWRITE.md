# CHANGELOG_REWRITE

## v0.8.1 - 2026-04-11

### 文档

- 新增根目录 `CHANGELOG.md`（GitHub 首页友好）。
- 新增根目录 `LICENSE`（MIT）。
- 更新根 `README.md`：
  - 文档入口增加 `CHANGELOG.md` 与 `LICENSE`
  - 补充运行验证状态（health/build/test）
- 更新 `docs/NOTICE.md`：
  - 去除 `TODO_*` 占位表达
  - 改为“维护者填充上游真实信息”的发布前清单模板

### 验证

- 后端测试：`8 passed`
- 前端构建：`npm run build` 通过
- 后端健康检查：`/health` 返回 `{"status":"ok","service":"assistgen-rewrite"}`

## v0.8.0 - 2026-04-09

### 新增

- 后端会话存储升级为 SQLite 持久化：
  - 新增 `backend_rewrite/app/core/settings.py`
  - 新增 `backend_rewrite/app/infra/sqlite.py`
  - 新增 `backend_rewrite/app/infra/repositories/sqlite_conversation_repository.py`
- 容器默认装配 SQLite 仓储，继续保留 `memory` 回退开关。
- 新增持久化回归测试：
  - `backend_rewrite/tests/test_sqlite_conversation_repository.py`
  - `backend_rewrite/tests/contract_test.py` 增加跨应用实例持久化验证
- 新增项目忽略/占位文件：`.gitignore`、`backend_rewrite/data/.gitkeep`

### 变更

- `backend_rewrite/app/core/container.py`：默认使用 SQLite 仓储
- `backend_rewrite/app/store.py`：兼容别名指向 SQLite 仓储
- `backend_rewrite/README.md`、`README.md`：补充 SQLite 路径与环境变量说明

### 验证

- 后端 `.venv` 测试：`8 passed`
- SQLite 持久化：已通过“新建应用实例后仍可读取历史消息”的回归测试

## v0.7.0 - 2026-04-09

### 变更

- 完成“无全局 Python”回退：卸载全局 `Python.Python.3.12`。
- 后端改为项目内运行时：`backend_rewrite/.python-base/`。
- 更新 `scripts/start_backend.ps1`：
  - 自动下载并解压项目内 Python（NuGet 包）
  - 自动创建 `backend_rewrite/.venv`
  - 全程使用项目内解释器，不依赖系统 `python` 命令
- 更新 `README.md` 与 `backend_rewrite/README.md` 的启动说明。

### 验证

- `python --version`：系统不可用（符合“无全局 Python”目标）
- `backend_rewrite/.venv` 测试：`5 passed`

## v0.6.0 - 2026-04-09

### 变更

- 回退为“项目虚拟环境优先”策略，避免依赖全局 Python PATH。
- 更新 `scripts/start_backend.ps1`：
  - 支持自动准备 `.venv`
  - 支持 `-PrepareOnly` 模式
  - 使用 `.venv/Scripts/python.exe` 启动后端
- 更新 `backend_rewrite/README.md` 与根 `README.md` 的运行说明，补充 PyCharm 2025.3 解释器设置建议。

### 验证

- 后端虚拟环境测试：`5 passed`（`backend_rewrite/.venv`）。

## v0.5.0 - 2026-04-09

### 新增

- 后端从单文件骨架迁移为分层结构：
  - `backend_rewrite/app/api/`（路由层）
  - `backend_rewrite/app/services/`（业务编排层）
  - `backend_rewrite/app/domain/`（领域模型/仓储协议）
  - `backend_rewrite/app/infra/`（内存仓储实现）
  - `backend_rewrite/app/core/`（容器装配）
- 新增后端容器和路由聚合：
  - `backend_rewrite/app/core/container.py`
  - `backend_rewrite/app/api/router.py`
  - `backend_rewrite/app/main.py` 改为 `create_app()` 工厂
- 新增后端契约测试：`backend_rewrite/tests/contract_test.py`
  - 校验 SSE `data: [DONE]`
  - 校验会话上下文聊天可写入历史消息
  - 校验 LangGraph query/resume 路径
- 保留兼容层：`backend_rewrite/app/store.py` 继续导出兼容别名

### 变更

- `backend_rewrite/requirements.txt` 增加 `pytest`
- `backend_rewrite/README.md` 更新为分层架构说明

### 验证

- 代码静态检查：通过
- 后端测试命令 `python -m pytest -q`：未执行成功（当前环境未安装可用 Python 解释器）

## v0.4.0 - 2026-04-09

### 新增

- 打通“当前会话 -> 流式聊天”的联动：
  - `frontend_rewrite/src/features/conversations/components/ConversationPanel.vue` 会向父页面同步当前 `userId`、`conversationId`、`conversationName`
  - `frontend_rewrite/src/pages/ChatWorkbenchPage.vue` 保存当前会话上下文并传递给聊天卡片
  - `frontend_rewrite/src/features/chat/components/ChatStreamCard.vue` 将当前会话上下文注入流式请求
  - `frontend_rewrite/src/services/chat/chatService.ts` 支持携带 `user_id` / `conversation_id`
- 补充更正式的项目文档：
  - `README.md`
  - `docs/DEPLOYMENT.md`
  - `docs/SCREENSHOTS.md`

### 验证

- 前端构建：`npm run build` 通过（2026-04-09）。

## v0.3.0 - 2026-04-09

### 新增

- 前端继续扩展会话功能（与现有健康检查、流式聊天组合）：
  - 新增会话服务：`frontend_rewrite/src/services/conversations/conversationService.ts`
  - 新增会话状态编排：`frontend_rewrite/src/composables/useConversations.ts`
  - 新增会话面板：`frontend_rewrite/src/features/conversations/components/ConversationPanel.vue`
  - 更新工作台页面：`frontend_rewrite/src/pages/ChatWorkbenchPage.vue`
- 扩展共享类型与请求封装：
  - `frontend_rewrite/src/shared/types/api.ts`
  - `frontend_rewrite/src/services/http/apiClient.ts`
- 更新前端说明文档：`frontend_rewrite/README.md`

### 验证

- 前端构建：待在本轮修改后再次执行。

## v0.2.0 - 2026-04-09

### 新增

- 前端模块化重构完成（保持健康检查 + 流式聊天能力）：
  - 新增页面层：`frontend_rewrite/src/pages/ChatWorkbenchPage.vue`
  - 新增功能层：
    - `frontend_rewrite/src/features/health/components/HealthCard.vue`
    - `frontend_rewrite/src/features/chat/components/ChatStreamCard.vue`
  - 新增组合式逻辑层：
    - `frontend_rewrite/src/composables/useHealthCheck.ts`
    - `frontend_rewrite/src/composables/useChatStream.ts`
  - 新增服务层：
    - `frontend_rewrite/src/services/http/apiClient.ts`
    - `frontend_rewrite/src/services/health/healthService.ts`
    - `frontend_rewrite/src/services/chat/chatService.ts`
  - 新增共享层：
    - `frontend_rewrite/src/shared/config/env.ts`
    - `frontend_rewrite/src/shared/types/api.ts`
- 精简根组件：`frontend_rewrite/src/App.vue` 仅作为应用壳。
- 更新文档：`frontend_rewrite/README.md`。

### 验证

- 前端构建：`npm run build` 通过（2026-04-09）。

## v0.1.0 - 2026-04-09

### 新增

- 创建全新目录 `assistgen_original_rewrite_v1`，与原工程并行。
- 新建 `backend_rewrite`：
  - 采用 FastAPI 重建核心接口（health/chat/reason/search/upload/conversations/langgraph）。
  - 使用全新 `schemas.py` 和 `store.py`（内存仓储占位）。
  - 新增 `tests/smoke_test.py`。
- 新建 `frontend_rewrite`：
  - 使用 Vue3 + TS + Vite 创建新前端骨架。
  - 新建 `src/services/api.ts`，重写健康检查和 SSE 请求封装。
  - 新建 `App.vue` 用于最小联调页面。
- 新建文档体系：`README.md`、`docs/ARCHITECTURE.md`、`docs/NOTICE.md`、`evidence/interface_mapping.md`。
- 新增脚本：`scripts/start_backend.ps1`、`scripts/start_frontend.ps1`、`scripts/rollback.ps1`。
- 完成依赖许可证清单：`evidence/third_party_licenses.md`。

### 验证

- 前端构建：`npm run build` 通过（Vite 7.3.2，2026-04-09）。
- 后端测试：待执行（当前终端环境缺少 `python` / `py` 命令）。

### 说明

- 当前阶段目标是“契约起步 + 可运行骨架”，非最终业务版本。
- 下一阶段将接入真实 LLM、持久化存储与完整前端页面模块。

