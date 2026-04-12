# third_party_licenses

以下清单基于当前改版工程依赖文件：

- 后端：`backend_rewrite/requirements.txt`
- 前端：`frontend_rewrite/package.json`

## Backend

| 包名 | 版本 | 许可证 | 官方仓库/主页 |
|---|---|---|---|
| fastapi | 0.116.1 | MIT | https://github.com/fastapi/fastapi |
| uvicorn | 0.35.0 | BSD-3-Clause | https://github.com/encode/uvicorn |
| pydantic | 2.11.7 | MIT | https://github.com/pydantic/pydantic |
| python-multipart | 0.0.20 | Apache-2.0 | https://github.com/Kludex/python-multipart |

## Frontend

| 包名 | 版本 | 许可证 | 官方仓库/主页 |
|---|---|---|---|
| vue | ^3.5.22 | MIT | https://github.com/vuejs/core |
| vite | ^7.1.10 | MIT | https://github.com/vitejs/vite |
| typescript | ^5.9.3 | Apache-2.0 | https://github.com/microsoft/TypeScript |
| @vitejs/plugin-vue | ^6.0.1 | MIT | https://github.com/vitejs/vite-plugin-vue |

## 说明

- 许可证信息来自各官方仓库常见 SPDX 声明，发布前建议再次核验依赖锁文件与上游 LICENSE。
- 若后续新增依赖，请同步更新该文档并在 PR 中附上来源链接。
