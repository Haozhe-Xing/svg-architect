# Quality Checklist

SVG 交付前必须逐项核查。High severity 项不通过禁止交付，Medium/Low 项须在 Self-Check 报告中说明。

## Accessibility

| ID | 检查项 | 严重度 |
|----|--------|--------|
| acc-1 | 包含 `<title>` 和 `<desc>` 标签 | Medium |
| acc-2 | 文字与背景对比度 ≥ 4.5:1 | **High** |
| acc-3 | 必要时提供 `aria-label` | Low |

## Technical

| ID | 检查项 | 严重度 |
|----|--------|--------|
| tech-1 | 包含正确的 `viewBox` 属性 | **High** |
| tech-2 | 明确定义 `preserveAspectRatio` | Medium |
| tech-3 | 无外部资源链接（字体/脚本/图片均须内嵌） | **High** |
| tech-4 | 所有 ID 唯一且带 `svga-<slug>-` 前缀（防多图内联冲突） | **High** |
| tech-5 | 所有文本必须有明确 `font-family`，且字体栈末尾包含 `sans-serif` 或 `monospace` | **High** |
| tech-6 | 禁止外部字体资源，包括 `@font-face src: url(...)` | **High** |
| tech-7 | 文字字号不得低于平台 Caption 下限：`wechat_cover` ≥ 18px，`wechat_article` ≥ 16px | **High** |
| tech-8 | 中英混排使用 `<tspan>` 或独立 `<text>` 分层，不对含中文文本整体设置正/负 `letter-spacing` | Medium |

## Composition

| ID | 检查项 | 严重度 |
|----|--------|--------|
| comp-1 | 关键信息位于 Safe Area 内 | **High** |
| comp-2 | 视觉焦点明确，无过度拥挤 | Medium |
| comp-3 | 连线平滑（贝塞尔或圆角），无穿模 | Medium |

## Branding

| ID | 检查项 | 严重度 |
|----|--------|--------|
| brand-1 | 符合所选风格规范（tech_dark / minimal_clean / glass_premium / neubrutalism / bento_info / clay_soft） | Medium |
| brand-2 | 配色方案与所选风格 spec 一致 | Medium |
