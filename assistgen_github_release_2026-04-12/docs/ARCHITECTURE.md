# ARCHITECTURE

## 1. 架构原则

- **契约先行**：以原系统已暴露 API 路径作为兼容边界。
- **实现重写**：服务层、数据层、前端状态层全部重新组织。
- **可追踪**：每一次改版在 `CHANGELOG_REWRITE.md` 与 `evidence/` 记录。

## 2. 目标架构

```text
frontend_rewrite (Vue3)
  -> services/api.ts
  -> calls backend_rewrite

backend_rewrite (FastAPI)
  -> app/main.py (router)
  -> app/schemas.py (DTO)
  -> app/store.py (repository placeholder)
```

## 3. 后续分层（下一阶段）

- `app/api/`：路由与协议转换
- `app/domain/`：业务对象与规则
- `app/services/`：编排层
- `app/infra/`：模型客户端、数据库、向量库

## 4. 行为对齐范围

- 对话接口（普通/流式）
- 会话增删改查
- 上传与多模态入口
- LangGraph query/resume 工作流入口

