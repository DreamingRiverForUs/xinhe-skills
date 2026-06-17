# 山东大学本科毕业论文（设计）模板 (sdu-thesis-design)

## 来源

- GitHub: `MonsterXia/Shandong-University-Undergraduate-Thesis-Design-Template`
- TeXPage: `https://www.texpage.com/template/aeea63dd-082f-4ef3-9524-a240d65fe195`
- 心河Paper repo: `iftaken/sdu-thesis-design`

## 与已有 sdu-thesis 的区别

| 特性 | sdu-thesis（已有） | sdu-thesis-design（本模板） |
|------|-------------------|---------------------------|
| 上游 | Karcen/sdu-undergrad-thesis-latex | MonsterXia/Shandong-University-Undergraduate-Thesis-Design-Template |
| 文档类 | ctexart（无独立 cls） | sduthesis.cls（基于 `\LoadClass{book}` + ctex） |
| 参考文献 | BibTeX + gbt7714-numerical.bst | biblatex + biber + gb7714-2015 |
| 封面/声明 | 由 main.tex 管理 | 独立 `.def` 文件（sduthesis-front-cover.def, sduthesis-statement.def） |
| 字体策略 | ctex Fandol auto-detect | ctex Fandol auto-detect + 封面自定义 `\kt` 楷体命令 |
| 年份 | 2026 版 | 2015 版（v1.0.5） |

## 关键文件结构

```
sduthesis.cls                  ← 文档类（book + ctex，kvoptions 选项管理）
sduthesis-front-cover.def      ← 封面（含 `\maketitlepage` 命令）
sduthesis-statement.def        ← 原创性声明页
main.tex                       ← SDUthesistemplate.tex 重命名
contents/
  titlepageinfo.tex            ← 封面元数据（\StuNum, \Ctitle, \Cauthor 等）
  usersettings.tex             ← 用户自定义宏包（listings, subfig, ccmap 等）
  abstract.tex                 ← 中英文摘要
  ch1.tex, ch2.tex, ch3.tex    ← 正文章节
  conclusions.tex              ← 结论
  acknowledgement.tex          ← 致谢
  appendix.tex                 ← 附录
  translation.tex              ← 译文
  reference.bib                ← 原始参考文献（被 references.bib 替代）
figures/
  SDUWords.pdf                 ← 山东大学校名 logo
  appd.pdf                     ← 附录装饰
  print.pdf                    ← 打印装饰
```

## 适配要点

### 1. 封面字体 `\kt` → ctex heiti

`sdu-thesis-front-cover.def` 第 16 行：
```latex
\newCJKfontfamily{\kt}[AutoFakeBold={2.17}]{KaiTiGB2312.ttf}
```

问题：`\newCJKfontfamily` 走 fontspec 系统字体搜索，找不到 TeX Live bundle 中的 FandolKai，也找不到 KaiTiGB2312.ttf（本地 ttf 未上传）。

修复：重定向到 ctex 的 `\heiti`（黑体）：
```latex
\newcommand{\kt}{\heiti}
```

同时第 52 行的 `\CJKfamily{kt}` 改为 `\kt`。

### 2. biblatex 参考文献路径

`sdu-thesis.cls` 第 227 行：
```latex
\addbibresource[location=local]{contents/reference.bib}
```

改为：
```latex
\addbibresource{references.bib}
```

同时将 `contents/reference.bib` 复制为项目根 `references.bib`。

### 3. main.tex 末尾垃圾行

`main.tex` 末尾有 `\input{sduthesis.cls}` —— 删除。

### 4. .gitignore 资源 PDF 例外

```gitignore
!figures/SDUWords.pdf
!figures/appd.pdf
!figures/print.pdf
```

### 5. 字体方案

ctex 在 Docker/Linux 上 auto-detect 到 **fandol** fontset，四体齐全。零外部字体下载。init.sh 仅创建 `font/` 目录。

### 6. tectonic-biber 自动处理

`biblatex` + `biber` 后端由 tectonic-biber 自动调用，无需手动干预。编译会触发 2 次 biber re-run（正常）。

## 编译验证

编译成功，1.14 MiB PDF。仅有 cosmetic warnings：
- Underfull hbox（封面 makebox 宽度不足）
- Missing Roman numeral chars ⅠⅡⅢ in appendix（lmroman 无这些字符，不影响正文）
- PDF version mismatch（内嵌 PDF 版本略高，降级为 1.5）
