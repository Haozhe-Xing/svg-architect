# SVG Architect Error & Exit Codes

## 1. Error Codes (`E_*`)

| Code | Meaning | Repair Responsibility |
| :--- | :--- | :--- |
| `E_VIEWBOX_MISSING` | Missing `viewBox` attribute | `svg_fixer.py` (auto) |
| `E_VIEWBOX_INVALID` | Malformed `viewBox` format | `svg_fixer.py` (auto) |
| `E_GEOMETRY_OUT_OF_BOUNDS` | Safe area or slots exceed viewBox | `repair-cmd` / Manual |
| `E_CONTRAST_LOW` | Contrast ratio < 4.5:1 | `repair-cmd` / Manual |
| `E_CONTRAST_UNRESOLVED` | Text color cannot be resolved (strict) | `repair-cmd` / Manual |
| `E_SECURITY_TAG` | Dangerous tag (`script`, `iframe`, etc.) | `repair-cmd` / Manual |
| `E_SECURITY_STYLE_CONTENT` | Unsafe CSS (`@import`, external `url()`) | `svg_fixer.py` (auto) |
| `E_SECURITY_EXTERNAL` | External `href` or `src` detected | `repair-cmd` / Manual |
| `E_A11Y_MISSING` | Missing `<title>` or `<desc>` | `svg_fixer.py` (auto) |
| `E_ID_PREFIX_MISSING` | 有 `id` 属性但未使用允许前缀（默认 `svga-`）；修复：重命名 id 并同步所有 `url(#id)`、`href="#id"`、`xlink:href="#id"` 引用 | Manual |
| `E_FONT_FAMILY_MISSING` | 文本元素缺少 `font-family`，且祖先也未提供可继承字体栈 | Manual |
| `E_FONT_FALLBACK_MISSING` | `font-family` 缺少最终 fallback：`sans-serif` 或 `monospace` | Manual |
| `E_FONT_EXTERNAL` | 检测到 `@font-face` 或外部字体 `url(...)` | Manual |
| `E_FONT_SIZE_TOO_SMALL` | 文本字号低于当前平台 Caption 下限（`wechat_cover` < 18px，`wechat_article` < 16px，`doc_figure` < 12px） | Manual |
| `E_CONTRAST_GRADIENT_TEXT` | strict 模式下关键文字使用 `url(#...)` 渐变/pattern fill，对比度无法计算；需改为 solid fill 或人工确认 | Manual |
| `E_XML_PARSE_FAIL` | SVG is not a valid XML | Manual |
| `E_VALIDATOR_CRASH` | Internal validator logic error | Developer |
| `E_PIPELINE_STALLED` | No progress made after retry | Manual |
| `E_PIPELINE_REPORT_PARSE_FAIL` | Failed to parse JSON report | Developer |

---

## 2. Pipeline Exit Codes

| Code | Meaning | Action |
| :--- | :--- | :--- |
| **0** | **Success** | Pipeline completed, assets ready. |
| **1** | **Failed (Logic/Stalled)** | Max retries reached or `E_PIPELINE_STALLED`. |
| **2** | **Failed (Infrastructure)** | `E_PIPELINE_REPORT_PARSE_FAIL` or validator crash. |
| **3** | **Repair Required** | Non-auto-fixable error detected (when no `--repair-cmd`). |
| **4** | **Post-processing Warning** | SVG ready but PNG export failed. |
