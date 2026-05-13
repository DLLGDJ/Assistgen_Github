# SCREENSHOTS

本文件用于规范 GitHub 仓库中的截图素材与 README 引用方式。

## 建议放置目录

统一放到：`docs/images/`

## 推荐文件命名

按展示顺序命名，方便 README 和目录排序：

1. `01-dashboard-overview.png`
   - 展示：健康检查、会话中心、流式聊天总览
2. `02-conversation-list.png`
   - 展示：会话列表、当前选中会话、历史消息
3. `03-streaming-chat.png`
   - 展示：流式输出内容与当前会话名称
4. `04-deployment-terminal.png`
   - 展示：后端与前端启动命令窗口

## 建议截图标准

- 尽量使用 16:9 或接近 16:10 的比例
- 画面保持清晰，避免过多浏览器边框干扰
- 若涉及终端，建议展示命令与关键输出，不要截取过多空白区域
- 文件名统一使用英文小写、数字前缀和短横线

## README 引用模板

建议在根 `README.md` 中使用如下方式：

```md
![Dashboard Overview](docs/images/01-dashboard-overview.png)
![Conversation List](docs/images/02-conversation-list.png)
![Streaming Chat](docs/images/03-streaming-chat.png)
![Deployment Terminal](docs/images/04-deployment-terminal.png)
```

## 维护建议

- 新增截图时，优先沿用当前编号，不要随意改动已有文件名
- 如果截图内容大改，再考虑新增编号，而不是覆盖旧版本
- README 中的截图区建议和 `docs/images/` 目录保持一一对应

## 当前状态

- 目前仓库已准备好截图引用位置
- 后续只需要把实际截图放入 `docs/images/` 并保持命名一致即可
