# GitHub Release Files

> 目的：给 GitHub 仓库维护者一份“哪些文件应提交、哪些文件应忽略、哪些文件建议保留”的清单。

## 1. 必须提交的核心文件

### 根目录

- `README.md`
- `CHANGELOG.md`
- `LICENSE`
- `.gitignore`
- `docker-compose.yml`

### 后端

- `backend_rewrite/README.md`
- `backend_rewrite/requirements.txt`
- `backend_rewrite/alembic.ini`
- `backend_rewrite/alembic/`
- `backend_rewrite/app/`
- `backend_rewrite/tests/`
- `backend_rewrite/docker-entrypoint.sh`
- `backend_rewrite/Dockerfile`
- `backend_rewrite/.env.example`

### 前端

- `frontend_rewrite/README.md`
- `frontend_rewrite/package.json`
- `frontend_rewrite/package-lock.json`
- `frontend_rewrite/tsconfig.json`
- `frontend_rewrite/vite.config.ts`
- `frontend_rewrite/index.html`
- `frontend_rewrite/src/`
- `frontend_rewrite/Dockerfile`
- `frontend_rewrite/nginx.conf`

### 文档

- `docs/ARCHITECTURE.md`
- `docs/DEPLOYMENT.md`
- `docs/DEPLOYMENT_TAOBAO_SELLER_NOTES.md`
- `docs/SCREENSHOTS.md`
- `docs/CHANGELOG_REWRITE.md`
- `docs/NOTICE.md`
- `docs/GITHUB_RELEASE_FILES.md`
- `docs/REWRITE_IMPROVEMENTS.md`

### 证据与说明

- `evidence/interface_mapping.md`
- `evidence/third_party_licenses.md`
- `evidence/` 下的必要说明文件

### 启动脚本

- `scripts/start_backend.ps1`
- `scripts/start_frontend.ps1`
- `scripts/rollback.ps1`

## 2. 建议提交的素材文件

### 截图

建议提交到：`docs/images/`

- `01-dashboard-overview.png`
- `02-conversation-list.png`
- `03-streaming-chat.png`
- `04-deployment-terminal.png`

这些图片用于：
- GitHub 首页展示
- README 图文说明
- 面试讲解时展示“项目完成度”

### 说明占位

- `backend_rewrite/data/.gitkeep`
- `frontend_rewrite/.gitkeep`（如有需要）

## 3. 不建议提交的内容

### 后端运行产物

- `backend_rewrite/.python-base/`
- `backend_rewrite/.venv/`
- `backend_rewrite/.pytest_cache/`
- `backend_rewrite/__pycache__/`
- `backend_rewrite/data/*.sqlite3`
- `backend_rewrite/data/*.db`
- `backend_rewrite/data/*.sqlite3-wal`
- `backend_rewrite/data/*.sqlite3-shm`
- `backend_rewrite/python.3.12.10.nupkg`

### 前端运行产物

- `frontend_rewrite/node_modules/`
- `frontend_rewrite/dist/`
- `frontend_rewrite/.vite/`（如存在）
- `frontend_rewrite/.cache/`（如存在）

### 本地化与编辑器文件

- `.idea/`
- `.vscode/`（如仅本地使用）
- `*.log`
- `.DS_Store`
- `Thumbs.db`

### 敏感信息

- `.env`
- `.env.*`（保留 `!.env.example`）
- `*.secret`
- `*.key`
- `*.pem`

## 4. 发布前核对建议

1. 确认 `README.md` 中的运行地址与真实端口一致。
2. 确认 `docs/DEPLOYMENT.md` 里的命令能直接复制执行。
3. 确认 `package-lock.json` 已提交，以保证前端安装结果可复现。
4. 确认数据库密钥、LLM Key、私有地址没有写进仓库。
5. 确认 `docs/images/` 至少放入一张首页总览图。

## 5. 建议的 GitHub 仓库首页结构

仓库首页建议呈现顺序：

1. 项目简介
2. 核心功能
3. 技术栈
4. 页面截图
5. 启动方式
6. 文档入口
7. 改进说明
8. 许可证与合规说明

这样读者能先看懂“做了什么”，再看到“怎么跑”，最后理解“为什么这样改”。

