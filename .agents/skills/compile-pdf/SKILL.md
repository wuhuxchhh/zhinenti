---
name: compile-pdf
description: 编译光合日程AI技术文档 PDF（XeLaTeX 双遍交叉引用）。路径：technical_report.tex
---

# 编译技术文档 PDF

执行 XeLaTeX 双遍编译以正确处理交叉引用和目录。

## 使用方法

```bash
# 完整流程（推荐）
techpdf

# 手动执行
cd /c/zhinenti/competition
export PATH="/d/texlive/2026/bin/windows:$PATH"
xelatex -interaction=nonstopmode technical_report.tex
xelatex -interaction=nonstopmode technical_report.tex
```

## 验证清单（编译后检查）

- [ ] 中文显示正常（无乱码）
- [ ] 页数 = 25-27 页
- [ ] PDF 大小 < 50MB（当前 ~7.5MB）
- [ ] 25 张图全部显示
- [ ] 目录正确生成
- [ ] 页码连续

## 故障排除

| 问题 | 解决 |
|---|---|
| `xelatex` not found | `export PATH="/d/texlive/2026/bin/windows:$PATH"` |
| `! Undefined control sequence` for `\checkmark` | 确认 `\usepackage{amssymb}` 已加载 |
| 中文字体缺失 | TeX Live 2026 自带，无需额外配置 |
| PDF > 50MB | 检查 fig_data_protocol 之类的图是否分辨率过高 |

## 关键文件

- 源：`C:\zhinenti\competition\technical_report.tex`
- 产物：`C:\zhinenti\competition\technical_report.pdf`
- 图目录：`C:\zhinenti\competition\figs\`
- 参考图：`C:\zhinenti\competition\ref_imgs_view\`

## 快速打开

```bash
start C:/zhinenti/competition/technical_report.pdf
```
