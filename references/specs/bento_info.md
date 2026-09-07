# Bento Info Visual Specification（信息格栅）

适用场景：多要素配图、架构图、功能对比、技术全景图、信息密集型流程图。

## Palette（深色版，默认）

- **Background**: `#111418` (Dark Base)
- **Card Background**: `#1A1D24` (Card Surface)
- **Card Border**: `#2A2D35` (Subtle Border)
- **Primary Text**: `#F1F5F9` (Near White)
- **Secondary Text**: `#64748B` (Muted)
- **Accent A**: `#3B82F6` (Blue，主要连接/强调)
- **Accent B**: `#10B981` (Green，正向/成功状态)
- **Accent C**: `#F59E0B` (Amber，警告/重点)

## Palette（浅色版，可选）

- **Background**: `#F2F4F8`，**Card**: `#FFFFFF`，**Border**: `#D1D5DB`
- 文字、强调色同深色版

## Typography（SVG 适配）

- **Font Stack**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Card Title Weight**: 600（字号见下方字号表）
- **Card Body Weight**: 400（字号见下方字号表）
- **全局标题 Weight**: 700（字号见下方字号表）
- 每个格子内容独立，不跨格放文字

### 字号（参考 platform_profiles.md 基准）

bento_info 以信息密度为优先，全局标题可适度克制：

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| 全局标题 H1 | 56–80px | 44–64px |
| 卡片标题 | 28–36px | 24–32px |
| 卡片正文 | 20–26px | 18–22px |
| 数值大字（强调格） | 48–72px | 36–56px |
| Caption / 小标签 | ≥18px | ≥16px |

> 卡片内字号不受 H1 基准约束，但单格内所有文字必须 ≥ Caption 下限。

### 中英文混排规则

- 卡片标题常见中英混排，用 `<tspan>` 切换字体：英文/数字片段用 `Inter, system-ui`
- 数值大字（强调格）优先 Inter 字体栈，并设置 `font-variant-numeric: tabular-nums` 保证数字列对齐；若需要严格等宽（如计数器、代码量对比），对数字 `<tspan>` 改用 `JetBrains Mono, monospace`
- 不对含中文的 `<text>` 整体设置 `letter-spacing`
- 全局标题的混排规则同 tech_dark

## Layout（SVG 构图规则）

- **格栅划分**：画布显式划分为 N 个矩形格（N 通常 4-9 个），每格有独立背景 rect
- **格子比例**：支持大小混排，但最大格不超过最小格面积的 4 倍
- **间距**：格间距统一 12px，格内 padding 统一 16px
- **圆角**：每个格子 `rx="12"`
- **层次**：深色背景底板 → 格子卡片 → 格内内容（图标/文字/数值）

## Effects（SVG 原语）

- **卡片阴影**：`filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3))`（深色版），轻量即可
- **强调格**：部分格子可用 Accent 色作为背景（`fill="#3B82F6"`），形成视觉节奏
- **连接线**：格子间关系用 1-2px Accent 色折线表达，搭配小箭头
- **数值标注**：大数字用 `font-weight:800` 撑开格子视觉重心

## Negative Constraints

- 禁止非格栅的自由浮动元素超过画布面积 20%
- 禁止格子间距不统一（视觉凌乱来源）
- 禁止同一张图混用深色版和浅色版格子
