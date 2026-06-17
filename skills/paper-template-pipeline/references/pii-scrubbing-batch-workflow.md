# 心河Paper 模板 PII 清洗批量工作流

当新一批 iftaken 模板仓库需要上线前的内容审查时使用。

## 适用场景

- 个人开发者制作的 LaTeX 模板（高校论文、数模竞赛、简历等）
- 需要清除：真实姓名、邮箱、手机号、QQ/微信、二维码、个人 GitHub 链接
- **不适用**：官方出版商模板（Elsevier/Springer/IEEE/ACM/MDPI 等），这些跳过清洗

## 清洗规则

### 替换映射

| PII 类型 | 替换为 |
|----------|--------|
| 中文姓名 | 张三, 李四, 王五, 赵六（轮流使用） |
| 英文姓名 | Tom Smith, Jerry Johnson, King Williams, Mary Brown |
| 邮箱 | example@example.com |
| 手机号 | 13800138000（11位）/ 138-0000-0000（带分隔符） |
| QQ号/微信号 | 删除整行 |
| QQ群号 | 删除 |
| 二维码图片 | 1×1 透明 PNG 占位图 |
| 收款码 | 1×1 透明 PNG 占位图 |
| 个人头像 | 1×1 透明 PNG 占位图 |
| 个人 GitHub/Gitee 链接 | iftaken 或删除 |
| CSDN/博客园/Bilibili/知乎 | 删除链接 |
| 参考文献中真实作者名 | 张三/李四/王五等（逐条替换，保持 bib key 一致性） |
| 学生学号 | 000000000000 |
| .cls 头部开发者信息 | 模板维护者 / example@example.com |
| .bst 文件中的 GitHub 链接 | 删除行 |

### 绝对不可更改

- 大学名称（产品标识，如 `华中农业大学`、`whu-thesis`）
- LaTeX 宏包名和版本号
- 模板技术结构（.cls/.sty/.def 的功能代码）
- 校徽等官方标识图片
- 许可证文件（LICENSE 中的版权归属改为 iftaken）

## 扫描命令

```bash
# 中文姓名
grep -rn '[^\x00-\x7f]\{2,4\}' --include='*.tex' --include='*.cls' --include='*.bib' --include='*.md' . | grep -iE 'author|thanks|姓名|作者'

# 邮箱
grep -rnE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' --include='*.tex' --include='*.cls' --include='*.md' --include='*.bib' .

# 手机号
grep -rnE '[0-9]{11}|[0-9]{3}[-. ][0-9]{4}[-. ][0-9]{4}' --include='*.tex' --include='*.md' .

# QQ/微信
grep -rniE '(qq|wechat|微信|扣扣|加群)' --include='*.tex' --include='*.md' .

# 二维码
grep -rniE '(qr|二维码|扫码|加微信|公众号)' --include='*.tex' --include='*.md' .

# 个人 GitHub/Gitee
grep -rnE 'github\.com/[^/]+/' --include='*.tex' --include='*.cls' --include='*.md' --include='*.bst' . | grep -v 'iftaken'

# 开发者注释
grep -rn '作者\|原作者\|维护者\|author\|maintainer' --include='*.cls' --include='*.sty' --include='*.tex' .
```

## 透明 PNG 占位图生成

```python
python3 -c "import struct,zlib;w,h=1,1;raw=b''.join([b'\x00\xff\xff\xff\xff'*w for _ in range(h)]);ihdr=struct.pack('>IIBBBBB',w,h,8,6,0,0,0);crc=lambda d:struct.pack('>I',zlib.crc32(d)&0xffffffff);png=b'\x89PNG\r\n\x1a\n'+b'IHDR'+ihdr+crc(b'IHDR'+ihdr)+b'IDAT'+zlib.compress(raw)+crc(b'IDAT'+zlib.compress(raw))+b'IEND'+crc(b'IEND');open('placeholder.png','wb').write(png)"
```

## Docker 编译验证

```bash
mkdir -p ~/.cache/paper-tectonic
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

判定标准：exit code 0 + main.pdf >= 10KB

## 批量委派模式

每个子 Agent 处理 8-11 个仓库，使用 delegate_task：

```
toolsets: ["terminal","file","skills"]
timeout: 600s
batch_size: 8-11 repos
```

子 Agent 指令要点：
- 逐仓库串行处理（避免 tectonic 缓存竞争）
- 每个仓库：clone → scan → replace → compile → push
- 空仓库快速跳过
- 编译失败记录原因但不阻塞后续仓库

## 飞书表格状态同步

清洗完成后，在飞书模板管理表 `ErlObuSw9aTdOysjjkUce6j1nNh` → `tbl0YkvmiUznuZ8O` 中将对应记录状态从「待适配」更新为「已清洗」。

## 已验证的高频 PII 模式

- **ElegantLaTeX 生态**：elegantpaper.cls 头部有 `Dongsheng Deng & Ran Wang` + `ranwang.osbert@outlook.com`，references.bib 含真实中文作者名
- **dlmu 系列**：main.tex 有 `海哥`/`海老师` 等昵称，签名图为真实签名，QQ群号在 README
- **xduts 派生**：xduts 系列模板含 `note286@foxmail.com` 邮箱和支付宝/微信收款二维码
- **thuthesis 派生**：main.tex 和 .cls 含 `薛瑞尼`/`Xue Ruini` 等真实姓名
- **snuthesis**：参考文件含 28 个真实中文 bib 作者名
