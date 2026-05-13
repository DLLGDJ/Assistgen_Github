# DEPLOYMENT

## Alembic 迁移（新增）

> 后端数据库结构由 Alembic 管理，建议每次发布前先执行迁移。

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\backend_rewrite"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
```

常用命令：

```powershell
# 查看当前迁移版本
.\.venv\Scripts\python.exe -m alembic -c alembic.ini current

# 回滚一个版本（谨慎）
.\.venv\Scripts\python.exe -m alembic -c alembic.ini downgrade -1
```

## 本地联调顺序

### 1. 启动后端

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\scripts"
.\start_backend.ps1
```

默认后端地址：`http://localhost:8100`

### 2. 启动前端

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\scripts"
.\start_frontend.ps1
```

默认前端地址：`http://localhost:5176`

### 3. 验证清单

- `GET /health` 返回 `ok`
- 会话中心可加载、创建、重命名、删除会话
- 点击某个会话后，右侧可显示历史消息
- 流式聊天区域会显示当前会话名称，并携带选中的 `user_id` / `conversation_id`

## 生产打包

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1\frontend_rewrite"
npm run build
```

## Docker Compose 启动（新增）

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose up -d --build
```

默认映射：

- 后端：`http://localhost:8100`
- 前端：`http://localhost:8080`
- 数据卷：`backend_rewrite/data`（SQLite 持久化）

说明：前端由 Nginx 托管，`/api/*` 和 `/health` 默认反代到后端容器。

查看日志：

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose logs -f backend
```

停止服务：

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose down
```

## 淘宝商家版注意事项

- 详见：`docs/DEPLOYMENT_TAOBAO_SELLER_NOTES.md`

## 备注

- 当前已支持本地启动与 Docker Compose 两种方式。
- 若前端部署到不同域名，请配置 `VITE_API_BASE_URL` 指向后端地址。




