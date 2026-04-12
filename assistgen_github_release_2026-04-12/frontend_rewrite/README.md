# frontend_rewrite

合规原创改版前端，使用 Vue 3 + Vite + TypeScript。

## 模块结构

- `src/pages/`：页面编排层
- `src/features/`：按业务能力拆分的组件
- `src/composables/`：状态与交互逻辑
- `src/services/`：HTTP 与业务 API 封装
- `src/shared/`：环境配置与通用类型

## 当前功能

- 后端健康检查
- 会话列表查看
- 会话创建 / 重命名 / 删除
- 会话历史消息查看
- 流式聊天
- 流式聊天会自动携带当前选中的 `user_id` / `conversation_id`

## 推荐目录说明

- `docs/DEPLOYMENT.md`：部署与联调说明
- `docs/SCREENSHOTS.md`：截图清单与素材占位
- `docs/ARCHITECTURE.md`：架构说明
- `docs/CHANGELOG_REWRITE.md`：改版记录

## 运行

```powershell
npm install
$env:VITE_API_BASE_URL='http://localhost:8100'
npm run dev
```

## Docker 运行

```powershell
Set-Location "G:\智能客服Agent\Agent\code\code\assistgen_original_rewrite_v1"
docker compose up -d --build
```

前端开发访问地址：`http://localhost:5176`

Docker 版本由 Nginx 提供静态托管，并将 `/api/*`、`/health` 反代到后端容器。

## 构建验证

```powershell
npm run build
```


