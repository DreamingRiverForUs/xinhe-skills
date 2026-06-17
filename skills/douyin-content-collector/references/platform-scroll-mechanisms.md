# 各平台滚动/翻页机制对比

| 平台 | 机制 | 滚动目标 | 翻页方式 | 每批数量 |
|------|------|----------|----------|----------|
| 抖音 | 虚拟滚动 | `document.scrollingElement` | `scrollTo(0, scrollTop+700)` 反复到底，顶+底两次采集合并 | ~12 |
| B站 | 标准翻页 | 无滚动 | `click .bcc-pagination-next` | 10 |
| 知乎 | 虚拟滚动 | `document.scrollingElement` | `scrollTo(0, scrollTop+800)` | ~15 |
| 小红书 | 容器滚动 | `div.content` | `el.scrollTo(0, el.scrollTop+400)` | ~10 |
| 视频号 | 待验证 | 待验证 | 待验证 | ~5(首页) |
| CSDN | 无 | 无 | 列表直接可见 | — |

## 通用流程

1. 先找滚动容器：遍历 `div`，找 `scrollHeight > clientHeight + 10` 的
2. 虚拟滚动需顶+底两次采集合并去重（key=标题前40字符）
3. 标准翻页用 `.click()` 触发
