# interface_mapping

> 目的：记录“原接口 -> 改版接口”映射，作为行为对齐证据。

| 原接口 | 改版接口 | 状态 | 备注 |
|---|---|---|---|
| `GET /health` | `GET /health` | 已实现 | 完整可用 |
| `POST /api/chat` | `POST /api/chat` | 已实现 | 支持 SSE 占位流 |
| `POST /api/reason` | `POST /api/reason` | 已实现 | 返回推理步骤占位 |
| `POST /api/search` | `POST /api/search` | 已实现 | 返回候选结果占位 |
| `POST /api/upload` | `POST /api/upload` | 已实现 | 返回文件元信息 |
| `POST /api/upload/image` | `POST /api/upload/image` | 已实现 | 返回文件元信息 |
| `POST /api/conversations` | `POST /api/conversations` | 已实现 | 内存仓储 |
| `GET /api/conversations/user/{user_id}` | `GET /api/conversations/user/{user_id}` | 已实现 | 内存仓储 |
| `GET /api/conversations/{conversation_id}/messages` | `GET /api/conversations/{conversation_id}/messages` | 已实现 | 内存仓储 |
| `DELETE /api/conversations/{conversation_id}` | `DELETE /api/conversations/{conversation_id}` | 已实现 | 内存仓储 |
| `PUT /api/conversations/{conversation_id}/name` | `PUT /api/conversations/{conversation_id}/name` | 已实现 | 内存仓储 |
| `POST /api/langgraph/query` | `POST /api/langgraph/query` | 已实现 | 占位工作流 |
| `POST /api/langgraph/resume` | `POST /api/langgraph/resume` | 已实现 | 占位工作流 |

