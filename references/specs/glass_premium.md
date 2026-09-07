# Glass Premium Visual Specification（玻璃高级感）

适用场景：技术/SaaS/AI 产品封面、金融科技配图、高端品牌场景。

## Palette

- **Background**: `#0D1117` (Deep Void，深背景打底)
- **Glass Layer**: `rgba(255,255,255,0.06)` (半透明玻璃面板)
- **Glass Border**: `rgba(255,255,255,0.12)` (微高光边框)
- **Primary Text**: `#F0F6FF` (Ice White)
- **Secondary Text**: `#8B9EC8` (Muted Blue-Gray)
- **Accent**: `#60A5FA` (Sky Blue 强调)
- **Accent Glow**: `rgba(96,165,250,0.25)` (光晕用)

## Typography（SVG 适配）

- **Font Stack (中文内容)**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Font Stack (英文标题)**: `Inter, PingFang SC, Noto Sans SC, system-ui, sans-serif`
- **Title Weight**: 700
- **Letter Spacing (Title)**: 1px 仅适用于纯 Latin 标题；中文标题 `letter-spacing` 设为 0
- **Body Weight**: 400
- SVG 中文字必须放在有不透明底托或足够深色背景上，禁止直接悬浮在纯模糊层

### 字号（参考 platform_profiles.md 基准）

glass_premium 强调高级感，字号克制但留足呼吸空间：

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| H1 主标题 | 80–108px | 60–80px |
| H2 副标题 | 40–52px | 32–42px |
| Body 注释 | 24–30px | 20–24px |
| Caption | ≥18px | ≥16px |

### 中英文混排规则

- 中英混排时用 `<tspan>` 切换字体；英文片段优先 Inter
- 不对含中文的 `<text>` 整体设置 `letter-spacing > 0`
- 英文片段视觉偏小时，在 `<tspan>` 上单独放大 5%

## Layout（SVG 构图规则）

- **层次**：深色背景 → 玻璃面板（中景，半透明 rect） → 文字/图标前景，三层
- **玻璃面板**：用 `<rect>` + `fill="rgba(255,255,255,0.06)"` + `stroke="rgba(255,255,255,0.12)"` 实现；不依赖 CSS backdrop-filter（SVG 不支持）
- **光晕点缀**：背景层可放 1-2 个大半径模糊圆（`feGaussianBlur stdDeviation="60"`）作为氛围光
- **边框圆角**：玻璃面板 `rx="16"`

## Effects（SVG 原语）

- **背景光晕**：`<circle>` + `<filter><feGaussianBlur stdDeviation="60"/></filter>`，opacity 0.3-0.5
- **玻璃面板实现**：独立 SVG **无法实现真正的 backdrop blur**（`backdrop-filter` 是 CSS 属性，`feImage` 引用外部背景层也不可控）。
  正确做法：用半透明 `<rect fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.12)"/>` 叠加在深色背景上，通过透明度和边框模拟玻璃质感，**禁止尝试 feImage 或 backdrop 方案**。
- **光效线**：1px 渐变线（`linearGradient` from Accent to transparent）模拟玻璃折射

## Negative Constraints

- 禁止超过 3 层玻璃面板叠加（可读性崩溃）
- 禁止文字直接放在无底托的纯模糊层上（对比度不达标）
- 禁止浅色背景版本（本风格强依赖深色打底，浅色用 minimal_clean）
