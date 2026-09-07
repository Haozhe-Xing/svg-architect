# Tech-Dark Visual Specification

## Palette (沉浸暗黑)
- **Background**: `#0A0A0B` (Deep Space)
- **Primary**: `#3B82F6` (Electric Blue)
- **Secondary**: `#8B5CF6` (Cyber Purple)
- **Text (Primary)**: `#F8FAFC`
- **Text (Secondary)**: `#94A3B8`

## Typography (现代排版)
- **Font Stack (中文内容)**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Font Stack (英文/数字标题)**: `Inter, PingFang SC, Noto Sans SC, system-ui, sans-serif`
- **Code / Monospace**: `JetBrains Mono, monospace`
- **Title Weight**: 800 (Extra Bold)
- **Letter Spacing**: 2px 仅适用于纯 Latin/ASCII 标题；中文标题 `letter-spacing` 设为 0 或省略，避免汉字间距异常

### 字号（参考 platform_profiles.md 基准）

tech_dark 偏大字号，H1 取基准上限或略超：

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| H1 主标题 | 96–120px | 72–88px |
| H2 副标题 | 44–56px | 36–44px |
| Body 节点文字 | 26–32px | 22–26px |
| Caption | ≥18px | ≥16px |

### 中英文混排规则

- 同一行中英文混排时，用 `<tspan>` 切换字体：中文片段用中文栈，英文/数字片段用英文栈
- 英文单词视觉偏小时，在同一 `<text>` 内对英文 `<tspan>` 设置 `font-size` 放大 5–10%
- 禁止对含中文的 `<text>` 整体设置 `letter-spacing > 0`；如需强调间距，仅对 Latin `<tspan>` 设置

## Effects (质感光影)
- **Glow**: Use `feGaussianBlur` with `stdDeviation="15"` for core nodes.
- **Grid**: 40x40px, `#1E293B`, opacity 0.3.
- **Lines**: Smooth Bezier curves with `#3B82F6` stroke and 2px width.

## Negative Constraints
- No pure black `#000000`.
- No high-saturation primary red/green.
