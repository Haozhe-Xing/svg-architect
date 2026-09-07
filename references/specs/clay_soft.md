# Clay Soft Visual Specification（粘土软萌）

适用场景：教育类配图、产品介绍、轻松话题、亲子/健康/生活方式、非技术受众内容。

## Palette

- **Background**: `#FFF8F0` (Cream White，奶油底色)
- **Surface**: `#FFFFFF` (卡片/形体主色，配合投影呈现膨胀感)
- **Primary Text**: `#2D2D2D` (Soft Black，避免纯黑)
- **Secondary Text**: `#9CA3AF`
- 主题色三选一（每张图只选一个，形成色调统一感）：
  - **Coral**: `#FF6B6B` (活力珊瑚红)
  - **Teal**: `#4ECDC4` (清新蓝绿)
  - **Sunny**: `#FFE66D` (明亮柠檬黄)
- **Shadow Base**: 主题色深 20%（用于多层膨胀投影）

## Typography（SVG 适配）

- **Font Stack**: `PingFang SC, Noto Sans SC, Microsoft YaHei, system-ui, sans-serif`
- **Title Weight**: 700（圆润粗体，不用 900）
- **Letter Spacing**: 0（自然间距，中英文均不调整）
- **字号**：标题相对宽松，留出与内容的视觉呼吸

### 字号（参考 platform_profiles.md 基准）

clay_soft 轻松，字号适中，不追求极大极小：

| 层级 | wechat_cover | wechat_article |
|------|-------------|----------------|
| H1 主标题 | 72–96px | 56–72px |
| H2 副标题 | 40–52px | 32–40px |
| Body 说明文字 | 24–30px | 20–26px |
| Caption | ≥18px | ≥16px |

### 中英文混排规则

- clay_soft 以中文内容为主，混入少量英文单词时，用同一字体栈即可（PingFang SC 对 ASCII 的渲染不差）
- 如需区分中英字体，用 `<tspan>` 切换；英文片段字号保持与中文一致，不放大
- 禁止在 clay_soft 中使用等宽或无衬线黑体风格的英文字体（破坏软萌气质）

## Layout（SVG 构图规则）

- **层次**：奶油背景 → 主题色大圆/色块（中景装饰） → 白色膨胀形体 → 文字前景
- **形体特征**：所有矩形 `rx ≥ 20`，圆形和圆角矩形为主，避免任何尖锐角
- **膨胀感**：核心元素用多层同色系投影叠加，模拟 3D 粘土膨胀效果（见 Effects）
- **构图**：居中或轻微偏心，不做大面积非对称布局（软萌风不适合粗野感构图）

## Effects（SVG 原语）

- **多层膨胀投影**（核心效果）：3-4 层 `drop-shadow`，颜色从浅到深，逐层偏移：
  ```
  filter="drop-shadow(0 2px 0 #FFB3B3) drop-shadow(0 4px 0 #FF9090) drop-shadow(0 6px 0 #FF6B6B)"
  ```
  使用 `<filter>` + 多个 `feDropShadow` 叠加实现
- **背景装饰**：大半径圆形（主题色 opacity 0.15-0.2）作为背景色调气氛
- **点缀元素**：小圆点、弧线用主题色 opacity 0.4，增加手作感

## Negative Constraints

- 禁止尖锐边角（所有形体 `rx ≥ 20px`）
- 禁止纯黑描边（用深色系投影代替边框）
- 禁止写实方向的阴影（不模拟真实光源，只做装饰性膨胀投影）
