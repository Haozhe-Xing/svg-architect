# Neubrutalism Visual Specification（新粗野主义）

适用场景：强冲击力封面、Z 世代品牌传播、活动宣传、醒目社交媒体配图。

## Palette

- **Background**: `#FFFBE6` (Warm Off-White，主背景) 或 `#F5F5F5` (Cool Off-White)
- **Primary Text**: `#0A0A0A` (Near Black)
- **Border / Shadow**: `#000000` (Pure Black，硬边框和投影唯一颜色)
- **Accent A**: `#FF3B30` (Saturated Red) — 科技/警示/冲突
- **Accent B**: `#FFD60A` (Saturated Yellow) — 活力/重点标注
- **Accent C**: `#0A84FF` (Saturated Blue) — 信息/品牌
- 每张图选其中 **1 个强调色**，不混用多个

## Typography（SVG 适配）

- **Font Stack (英文/数字标题，高冲击)**: `Arial Black, PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Font Stack (中文内容)**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Title Weight**: 900（Black，必须极粗）
- **Letter Spacing (Title)**: 0（紧凑贴合）
- **Body Weight**: 700
- 标题字号要足够大，保证视觉冲击（封面图标题 ≥ 96px，配图 ≥ 72px）
- 英文/数字标题用 `Arial Black` 开头栈，确保 Latin 字符命中极粗字体；中文内容切换到中文栈

### 字号（参考 platform_profiles.md 基准，neubrutalism 取上限）

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| H1 主标题 | **96–120px**（硬下限 96px） | **72–88px**（硬下限 72px） |
| H2 副标题 | 48–56px | 40–48px |
| Body 正文 | 28–32px | 24–28px |
| Caption | ≥20px | ≥18px |

### 中英文混排规则

- 英文/数字大标题：用 `Arial Black` 开头字体栈的独立 `<text>` 或 `<tspan>`
- 中文内容或中英混排正文：切换为中文栈 `<tspan>`
- neubrutalism 标题通常纯英文或纯中文，**尽量避免中英文在同一行混排**（破坏冲击感）
- 如必须混排，英文片段字号放大 8–10%，保证视觉等高

## Layout（SVG 构图规则）

- **层次**：暖白背景 → 强调色色块（中景） → 黑色边框文字前景
- **硬投影**：所有卡片/面板用 `<rect>` 偏移复制模拟硬投影，颜色 `#000000`，偏移 4-6px
  - 实现：先画偏移黑色 rect（shadow），再画原色 rect（front），最后放内容
- **边框**：2-3px 纯黑 stroke，所有矩形边框可见
- **非对称布局**：刻意打破中心对称，强调色块偏向一侧

## Effects（SVG 原语）

- **硬投影**（核心效果）：位移复制 `<rect>` 实现，**不用 drop-shadow filter**（filter 会产生柔和感）
  ```
  <!-- 投影层 -->
  <rect x="54" y="54" width="200" height="80" fill="#000000"/>
  <!-- 主色层 -->
  <rect x="50" y="50" width="200" height="80" fill="#FFD60A" stroke="#000000" stroke-width="2"/>
  ```
- **纹理**：可选在背景加极细斜线网格（opacity 0.05），增加手工感

## Negative Constraints

- 禁止圆角（所有 rect rx="0"，这是新粗野主义的核心原则）
- 禁止柔和阴影（drop-shadow filter），只用硬偏移投影
- 禁止低饱和配色和渐变色块（强调色必须高饱和实色）
