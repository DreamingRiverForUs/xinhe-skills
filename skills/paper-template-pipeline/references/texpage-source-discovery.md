# TeXPage 模板源检查清单

当拿到一个新的 TeXPage 模板时，按以下顺序检查源可用性。每个层级失败后才进入下一层。

## 第 1 层：页面 HTML（秒级，无需登录）

**Pitfall**：TeXPage 使用阿里云 ESA（Edge Security Acceleration）进行反爬保护。curl 不带浏览器特征 headers 会返回 403 `Denied by http_custom`。必须携带完整的 Chrome 浏览器 headers（包括 Sec-Ch-Ua、Sec-Fetch-* 系列），仅设 `-A` 不够。

```bash
curl -sL \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  -H "Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7" \
  -H "Sec-Ch-Ua: \"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"" \
  -H "Sec-Ch-Ua-Mobile: ?0" \
  -H "Sec-Ch-Ua-Platform: \"macOS\"" \
  -H "Sec-Fetch-Dest: document" \
  -H "Sec-Fetch-Mode: navigate" \
  -H "Sec-Fetch-Site: none" \
  -H "Sec-Fetch-User: ?1" \
  -H "Upgrade-Insecure-Requests: 1" \
  "https://www.texpage.com/template/<id>" 2>&1
```

检查项：
- `grep -oE 'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+'` → 提取 GitHub URL
- meta description 中是否有作者/项目链接（如 `<meta name='description' content='CSPC CCS Thesis / Capstone Template | ...'>`）
- 是否有 `__NEXT_DATA__` 内嵌 JSON

**SSR HTML 可提取的结构化数据**（无需登录、无需 JS 渲染）：
页面虽然是 React SPA，但模板详情信息在服务端渲染（SSR）的 `<div class="detail-info-item">` 中。可用以下模式提取：

```bash
curl ... | python3 -c "
import sys, re
html = sys.stdin.read()
for m in re.finditer(r'<div class=.detail-info-label.>(.*?)</div>\s*<div class=.detail-info-value.>(.*?)</div>', html, re.DOTALL):
    label = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    value = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    print(f'{label}: {value}')
"
```

SSR HTML 中会出现的字段：
- **Author** — 模板作者全名（可用于后续 GitHub 用户搜索）
- **Last Modified** — 模板最后修改日期
- **Abstract** — 模板描述/摘要
- **License** — 许可证（如 Creative Commons CC BY 4.0）
- **PDF 预览 URL** — `latex-static.texpage.com/<uuid>?x-content-type=application/pdf`（可下载 PDF 预览）
- **模板截图** — `latex-static.texpage.com/<uuid>_full`

**注意**：GitHub 源仓库 URL（如果有）是 JS 渲染的，不出现在 SSR HTML 中。必须走后续层级的搜索。

**Pitfall：Abstract 中的 GitHub 链接可能是作者个人主页，不是模板源仓库**。部分作者在 Abstract 中链接个人主页/作品集（如 "可以访问个人主页https://github.com/xxx/yyy"），`grep` 会命中这些 URL 但与模板源码无关。判定方法：阅读 URL 周围的上下文文字，若含"个人主页""homepage""personal"等词 → 忽略，继续下层搜索。只有独立于描述文字的、明确标注"项目地址""source""仓库"的链接才是模板源。

## 第 2 层：作者 GitHub 用户搜索（秒级，接 Layer 1 的作者字段）

当 Layer 1 从 SSR HTML 中提取到 Author 全名后，可尝试将作者映射到 GitHub 用户名，进而查找其仓库：

```bash
# 作者全名搜索 GitHub 用户
gh api "search/users?q=<Author全名>" --jq '.items[].login'
```

然后检查每个候选用户的仓库列表：
```bash
gh repo list <login> --limit 50 | grep -i "thesis\|template\|latex\|tex"
```

**Pitfall**：TeXPage 作者名可能与 GitHub 用户名无直接关联（如作者使用机构名或笔名发布模板）。不要仅靠作者名匹配，优先下层的仓库关键词搜索。

## 第 3 层：GitHub 关键词搜索（秒级）

```bash
# 按模板名称关键词搜索
gh search repos "<学校名> latex" --limit 10
gh search repos "<学校名> <模板类型>" --limit 10
# 按 TeXPage 描述中的关键词搜索
gh search repos "<描述关键词>" --limit 10
```

## 第 4 层：TeXPage API（需区分是否需要登录）

```bash
# 公开 API — 无需登录
curl -sL "https://www.texpage.com/api/template/get?templateId=<id>" \
  -H "Accept: application/json" -A "Mozilla/5.0"
curl -sL "https://www.texpage.com/api/template/download?templateId=<id>" \
  -A "Mozilla/5.0"
```

**Pitfall**：download 端点返回 HTTP 200 但 body 是 JSON 错误 `{"status":{"code":1003,"message":"Not logged in"}}`。需要 `file` 命令或检查内容前几个字节来区分真实 zip 和 JSON 错误。

## 第 4 层：TeXPage OSS 静态资源

```bash
for path in "main.tex" "readme.md" "template.zip"; do
  curl -sL "https://latex-static.texpage.com/template/<id>/$path"
  curl -sL "https://upload.texpage.com/template/<id>"
done
```

## 第 5 层：TeXPage Git 服务器

```bash
git clone https://git.texpage.com/<id>.git /tmp/test-clone
```

## 第 5 层：TeXPage OSS 静态资源

```bash
for path in "main.tex" "readme.md" "template.zip"; do
  curl -sL "https://latex-static.texpage.com/template/<id>/$path"
  curl -sL "https://upload.texpage.com/template/<id>"
done
```

## 第 6 层：TeXPage Git 服务器

```bash
git clone https://git.texpage.com/<id>.git /tmp/test-clone
```

需要认证，通常不可用。

## 第 7 层：外部搜索引擎

```bash
curl -sL "https://html.duckduckgo.com/html/?q=<学校名>+<模板类型>+latex+github" \
  -A "Mozilla/5.0" | grep -oE 'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+'
```

## 第 8 层：TeXPage 模板 ID 直接搜索

```bash
gh search code "<template-id>" --limit 10
```

检查模板 ID 是否出现在任何 GitHub 仓库的注释/README 中。

## 判定

- **第 1-4 层任一命中** → 方式 A（有源，gh repo clone）
- **全部 8 层均失败** → 方式 B（无源，需浏览器 Open as Template 提取）

## 已知方式 B 模板

| TeXPage ID | 名称 | 目标仓库 |
|------------|------|----------|
| `d2016614-0b7b-48ea-b4ed-47a8d2f3933a` | 内蒙古科技大学微型计算机实训模版 | iftaken/imust-microcomputer |
| `dc8b63ce-6699-4a1e-a2f7-fa6a1009da7b` | CSPC CCS Thesis / Capstone Template | iftaken/cspc-ccs-thesis |
| `ff0fcb27-114b-42e4-b9b2-3aa430cadfea` | Modelo de Artigo Acadêmico - IFPI | iftaken/ifpi-academic |
| `0bf98e2a-c7a6-42f6-960d-30c6c1ab82d9` | 江苏第二师范学院本科毕业论文 | iftaken/jsie-thesis |
| `3d62c7e2-8c94-478d-95b1-82a3fec336c4` | 浙江传媒学院数字电视原理实验报告 | iftaken/zjicmv-exp-report |
| `4c847050-151c-4c7e-8db7-e2dd71e3d465` | 全国大学生数学建模比赛通用模板 | iftaken/cumcm-general |
| `28f0e715-da1d-49e3-b589-609b08142293` | 韶关学院本科毕业论文 LaTeX 模板 v1.1 | iftaken/sgu-thesis |
| `745b795d-ef6b-408e-be3f-ab173124f4ae` | 郑州轻工业大学学位论文模板 | iftaken/zzuli-thesis |
| `9a50297f-089e-4f11-a7cf-240f0254534b` | 科学出版社 LaTeX 模板 | iftaken/sciencepress-template |
| `d0d9a74e-8d88-42f4-bf2b-49f532a4ef97` | 西南林业大学本科毕业论文（2025） | iftaken/southwest-forestry-university-thesis |
| `c478376a-ae91-479e-9b45-6b5eee743a36` | 实验报告 - 模版（上海交通大学物理实验） | iftaken/experiment-report-template |

**CSPC CCS 备注**：作者 Joseph Jessie S. Oñate（Camarines Sur Polytechnic Colleges — College of Computer Studies, Philippines），License CC BY 4.0，仅存在于 TeXPage 无 GitHub 源。通过 `gh api search/users?q=Joseph+Jessie+Onate` 找到候选用户 `iamjcoo` 和 `jessonate`，均无此模板仓库。需走方式 B 浏览器提取。
