# 账号摸底流程

工厂里的账号数据可能严重过时。做任何运营决策前，必须先浏览器验证。

## 创作者中心 URL（直接打开）

| 平台 | 创作者中心 URL | 登录态要求 |
|------|---------------|-----------|
| 知乎 | https://www.zhihu.com/creator | Chrome 已登录 |
| 小红书 | https://creator.xiaohongshu.com/new/home | Chrome 已登录 |
| 抖音 | https://creator.douyin.com/creator-micro/home | Chrome 已登录 |
| B站 | https://member.bilibili.com/platform/home | Chrome 已登录 |
| 视频号 | https://channels.weixin.qq.com/platform | Chrome 已登录（需扫码） |
| CSDN | https://mp.csdn.net/mp_blog/manage/article | Chrome 已登录 |

## 每次摸底读取的信息

1. **账号名/昵称** — 与工厂记录对比，可能已改名
2. **粉丝数** — 首页直接显示
3. **关注数/获赞数** — 如有
4. **平台账号ID**（抖音号、小红书号、BV号等）
5. **简介/个签** — 判断账号定位

## 历史摸底记录

### 2026-06-16

| 平台 | 工厂记录 | 浏览器实际 | 修正 |
|------|---------|-----------|------|
| 知乎 | 小河的论文日常 (999粉) | 论文不会鸭 (Lv5) | 完全不同账号，新增 |
| 小红书 | Ai个锤子 (36粉) | Ai个锤子🔨 (73粉, ID:676462433) | 粉丝翻倍，更新 |
| 抖音 | 心河Paper (227粉) | 心河Paper (1218粉, ID:922714934) | 5倍差距，更新 |
| B站 | 绘梦心河 (29粉) | 是小小河呀 (70粉, UP主1365天) | 完全不同账号，新增 |
| 视频号 | 绘梦心河 (20粉) | 绘梦心河 (50粉, ID:sphP1jBmOFIFHx6, 43视频) | 粉丝翻倍，更新 |
| CSDN | 无 | 论文不会鸭 (2篇文) | 新增 |

## 当前设备(Chrome)登录账号矩阵

这台 Chrome 同时登录了两个手机号的账号：
- **15700079382 (黄一鸣)**: 知乎「论文不会鸭」, 小红书「华农柒柒」
- **18772318183 (黄一鸣)**: 抖音「心河Paper」, 视频号「绘梦心河」, 小红书「Ai个锤子🔨」, B站「是小小河呀」

## 多设备/多账号注意事项

- Chrome 每个平台只能登录一个账号
- 切换账号需要登出再登入（触发风控风险）
- 用户偏好：多账号问题通过添加设备解决，不纠结复杂的多Profile方案
- 当前优先：这台设备上登录的账号全部走明白

## 数据更新 API

账号详情通过 `GET /api/v1/social-accounts` 获取（含 phone_number、device 关联）。
更新通过 `PUT /api/v1/social-accounts/{id}`。
CLI 的 `get-account` 和 `update-account` 返回 404（后端未实现），用直接 API。
