# Minimal Clean Visual Specification（极简清朗）

适用场景：品牌介绍、概念文章、产品说明、轻商业内容、白皮书配图。

## Palette

- **Background**: `#FAFAFA` (Soft White)
- **Surface**: `#FFFFFF` (Pure White，用于卡片/区块底色)
- **Primary Text**: `#1A1A1A` (Near Black)
- **Secondary Text**: `#6B7280` (Cool Gray)
- **Accent**: `#0071E3` (Precision Blue，唯一强调色)
- **Border**: `#E5E7EB` (Hairline)

## Typography（SVG 适配）

- **Font Stack (中文内容)**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Font Stack (英文标题)**: `SF Pro Display, PingFang SC, Noto Sans SC, system-ui, sans-serif`
- **Title Weight**: 600（Semibold，克制有力）
- **Body Weight**: 400
- **Letter Spacing (Title)**: -0.3px 仅适用于纯 Latin 标题；中文标题设为 0，紧凑汉字不需要负向压缩
- **Letter Spacing (Body)**: 0
- SVG 中用 `font-weight` 属性控制，`letter-spacing` 写在 `<text>` 的 style 属性

### 字号（参考 platform_profiles.md 基准）

minimal_clean 克制，H1 取基准中段，不追求大字冲击：

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| H1 主标题 | 72–96px | 56–72px |
| H2 副标题 | 40–48px | 32–40px |
| Body 正文 | 24–28px | 20–24px |
| Caption | ≥18px | ≥16px |

### 中英文混排规则

- 中英混排时用 `<tspan>` 切换字体；英文片段优先 SF Pro Display
- 不对含中文的 `<text>` 设置负向 `letter-spacing`；仅对纯 Latin 标题 `<tspan>` 可设 -0.3px
- 中英文混排行，英文字号可与中文保持一致，无需额外放大（SF Pro Display 视觉尺寸与 PingFang SC 接近）

## Layout（SVG 构图规则）

- **层次**：背景色块（Background） → 内容区白色 Surface → 文字/图形前景，三层明度递进
- **网格感**：所有元素对齐隐式 8px 网格，避免随意浮动定位
- **留白**：核心内容占画布面积 ≤ 60%，余量为呼吸空间
- **分区**：用细线（1px `#E5E7EB`）或色块（浅灰 `#F3F4F6`）划分区域，不用粗边框

## Effects（SVG 原语）

- **阴影**：`filter: drop-shadow(0 1px 3px rgba(0,0,0,0.08))`，仅用于卡片底托
- **强调线**：Accent 色 2px 水平线或竖线，不超过画布宽度 30%
- **渐变**：仅允许同色系 2 色渐变（如 `#FAFAFA` → `#F3F4F6`），禁止跨色相渐变

## Negative Constraints

- 禁止渐变超过 2 个色标
- 禁止大面积装饰性几何图形（≥ 画布面积 30% 的装饰色块）
- 禁止字重 > 700 的标题（这是极简风，不是粗野风）
