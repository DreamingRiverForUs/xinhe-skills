# PII 清洗指南 — 心河Paper 模板上线前必做步骤

在模板完成编译适配后、推送上线前，必须对非官方来源（个人开发者）的模板进行 PII 清洗。

## 触发条件

模板来源为「方式2:LaTeX平台整合」且非官方出版商提供（非 Elsevier/Springer/IEEE/ACM 等）。

## 扫描模式

### 必扫字段

```bash
# 中文姓名（在 author/thanks/contact 上下文中）
grep -rn '作者\|author\|Author\|姓名\|\\author{' *.tex *.cls *.md 2>/dev/null

# 邮箱地址
grep -rnE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' *.tex *.cls *.sty *.bib *.md *.cfg *.def 2>/dev/null

# 手机号码（11位或国际格式）
grep -rnE '[0-9]{11}|[0-9]{3}[-. ][0-9]{4}[-. ][0-9]{4}' *.tex *.cls *.sty *.bib *.md 2>/dev/null

# QQ/微信号
grep -rniE '(qq|wechat|微信|扣扣)[:：]?\s*[0-9]{5,}' *.tex *.cls *.sty *.bib *.md 2>/dev/null

# 二维码引用
grep -rniE '(qr|二维码|扫码|加微信|加群)' *.tex *.cls *.sty *.bib *.md 2>/dev/null

# 个人 GitHub/Gitee 链接
grep -rniE '(github\.com/[^/]+/|gitee\.com/[^/]+/|zhihu\.com/people/|blog\.|个人主页|主页)' *.tex *.cls *.sty *.bib *.md 2>/dev/null

# 开发者署名
grep -rn '作者\|原作者\|维护者\|author\|maintainer' *.cls *.sty *.tex *.md 2>/dev/null

# 参考文献中的真实姓名（.bib 文件）
grep -rn 'author\s*=' *.bib 2>/dev/null
```

## 替换规则

### 姓名
- **中文姓名** → 张三, 李四, 王五, 赵六, 孙七, 周八（轮换使用，同一仓库内保持一致）
- **英文姓名** → Tom Smith, Jerry Johnson, King Williams, Mary Brown, Jane Doe
- 参考文献作者名同样替换（使用拼音化名：Zhang San, Li Si, Wang Wu）

### 联系方式
- **邮箱** → example@example.com
- **手机** → 13800138000 / +86-13800138000
- **QQ/微信/二维码引用** → 删除整行
- **社交媒体链接（CSDN/Bilibili/博客园/知乎等）** → 删除整行

### 代码与仓库
- **个人 GitHub/Gitee 链接** → 改为 `iftaken/<repo>` 或删除
- **cls/sty 文件头部的开发者署名** → 改为「模板维护者」
- **LICENSE 中的个人名** → 改为 iftaken

### 图片
- **二维码/收款码/人物照片** → 替换为 1×1 透明 PNG
- **大学校徽/官方标识** → 保留原样
- **通用示例图** → 保留原样

创建占位 PNG 的命令：
```bash
python3 -c "
import struct,zlib
w=h=1
raw=b''.join([b'\\x00\\xff\\xff\\xff\\xff'*w for _ in range(h)])
ihdr=struct.pack('>IIBBBBB',w,h,8,6,0,0,0)
crc=lambda d:struct.pack('>I',zlib.crc32(d)&0xffffffff)
png=b'\\x89PNG\\r\\n\\x1a\\n'+b'IHDR'+ihdr+crc(b'IHDR'+ihdr)+b'IDAT'+zlib.compress(raw)+crc(b'IDAT'+zlib.compress(raw))+b'IEND'+crc(b'IEND')
open('placeholder.png','wb').write(png)
"
```

### 不可修改的内容
- 大学名称（这是产品标识）
- LaTeX 宏包名称和版本
- 模板技术结构（cls/sty/def）
- 官方校徽等标识图片

## 批量处理流程

```
1. 分类：官方期刊 → 跳过；非官方 → 清洗
2. 分批：每 8 个模板一组，使用 delegate_task 并行处理
3. 每批子 Agent 执行：clone → PII scan → replace → compile test → push
4. 子 Agent toolsets: ["terminal", "file", "skills"]
5. 单批 timeout ≥ 600s
```

### 子 Agent 指令模板

```
You are batch-processing LaTeX template repos for 心河Paper. 
USER-CREATED templates needing PII scrubbing.

Repos: [list 8 repos]

For each repo:
1. Clone: cd /tmp && git clone git@github.com:iftaken/<repo>.git <repo>-work && cd <repo>-work
2. PII scan: grep for emails, phones, QQ/WeChat, QR codes, personal GitHub/social links, names
3. Replace per rules above
4. Compile: docker run --rm --platform linux/amd64 -v $(pwd):/app -v ~/.cache/paper-tectonic:/root/.cache/Tectonic <image> tectonic -X compile main.tex
5. Push: git add -A && git commit -m "scrub: remove PII" && git push origin main

Process one by one. Report per-repo: [OK/SKIP/FAIL] changes=[N] compile=[PASS/FAIL] notes=[brief].
```

## 已验证的高频 PII 模式

| 模板类型 | 常见 PII 位置 | 处理方式 |
|----------|--------------|----------|
| ElegantLaTeX 系列 | .cls 头部署名 + 邮箱, references.bib 作者名 | 统一替换 |
| 高校论文模板 | main.tex 作者名, .cls 维护者信息, QQ群 | 作者→张三, QQ→删除 |
| 数模竞赛模板 | QQ群号, 公众号二维码图, 邮箱 | 全部删除/替换 |
| 期刊模板 | .cls 授权信息, 示例中的真实邮箱 | 邮箱→example |
| thuthesis 派生 | .cls 原作者署名, bib 中特殊名 | 作者→张三 |

## 常见陷阱

- **不要并行编译**：多个 Docker tectonic 共用 ~/.cache/paper-tectonic 会导致缓存竞争
- **先 scan 再 clone**：空仓库快速跳过，不耗费编译时间
- **bib 文件中的作者名最容易遗漏**：参考文献往往有几十个真实姓名
- **.dtx 文件也要扫**：WHU 等模板的文档注释中可能包含真人姓名
- **README.md 也要扫**：常包含开发者的 GitHub 链接和联系方式
