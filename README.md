# SVG Architect

纯代码生成微信公众号 SVG 视觉与文档插图的 Agent Skill。输入一句需求，输出一张通过校验、可直接交付的 SVG 文件。

覆盖场景：公众号封面 / 配图 / 插图 / 架构图 / 流程图 / 示意图 / 时序图 / 设计海报，以及 **mdBook / 博客 / 教材中的技术文档插图**。

---

## ✨ 本次新增：`zh_dense` 风格 + `doc_figure` 平台

这是本版本的核心更新：在原有的 6 种公众号视觉风格之外，新增了面向**技术文档插图**的第七种风格 `zh_dense`（中文信息密集），并配套新增 `doc_figure` 平台规格。

### 为什么新增

公众号视觉追求"一眼冲击、情绪表达"，而文档插图追求的是**在 680px 宽度内、以 100% 原尺寸嵌入页面时仍清晰可读、信息自洽**。两者在构图、字号、色彩、密度上的要求完全不同，原有公众号规格无法直接复用，因此引入独立平台与风格。

### `doc_figure` 平台

| 项 | 值 |
|----|----|
| 画布宽度 | 固定 **680px** |
| 画布高度 | **400–1000px 弹性**，按内容伸缩，以 8px 为步长取整 |
| 安全区 | `24 24 632 (h−48)` |
| 字号下限 | **12px**（屏幕阅读绝对下限） |
| 缩略图约束 | 无（不经过公众号缩略图分发） |
| 底部留白 | 禁止 >40px 的整块空白，宁可收缩高度 |

### `zh_dense` 风格核心特征

**一句话定位**：一张图就是一小节内容，而不是配图点缀。

- **浅色体系 + 高信息密度**：`#F8FAFC` 画布底、`#1E293B` 正文墨色、`#2563EB` 主强调，绿红语义色（绿=正确/收敛，红=错误/发散）全图一致。
- **结论先行**：标题块下方紧跟一条带蓝色竖条的一句话结论，让读者扫一眼即得主旨。
- **版式三件套**：H1 标题 + 副标题 + 右上角图例，结构固定可预期。
- **信息主体 ≥3 信息块 / ≥8 元素**：流程步骤、公式框、对比表格、数据条组合编排，块间距 8–12px，不留大面积空白。
- **禁止单一焦点构图**：不允许"一个大图形 + 少量文字"的极简布局。
- **硬约束**（由校验器强制）：
  - 所有文字一律深色 —— 对比度按画布底色 `#F8FAFC` 计算，白色/浅色文字会判 `E_CONTRAST_LOW`，即使它压在彩色色块上。
  - 最小字号 ≥12px（`E_FONT_SIZE_TOO_SMALL`）。
  - 所有 `id` 带 `svga-<slug>-` 前缀。
  - `viewBox` 宽度固定 680。

### 新增的脚本 / 校验支持

- `scripts/svg_validator.py`：新增 `doc_figure` 平台识别（按宽度 680 判定），并应用 12px 字号下限。
- `scripts/render_svg_preview.py`：`--platform doc_figure` 支持，按 SVG 自身 `viewBox` 推导高度，缩略图裁切取水平中央 50%。
- `references/specs/zh_dense.md`：新增的完整风格规范。
- `references/platform_profiles.md`：新增 `doc_figure` 行与字号基准表。
- `references/error_codes.md`：补充 `doc_figure < 12px` 的字号下限说明。

---

## 支持的平台

| 类型标识 | 适用场景 | 宽 × 高 |
|----------|----------|---------|
| `wechat_cover` | 公众号封面图、头图 | 1800 × 766 |
| `wechat_article` | 公众号配图、插图、架构图、流程图、示意图、时序图、海报 | 1200 × 500 |
| `doc_figure` | 技术文档 / mdBook / 博客内嵌插图（`zh_dense` 风格专用） | 680 × (400–1000 弹性) |

---

## 七种风格

| Style ID | 中文名 | 触发关键词 |
|----------|--------|-----------|
| `tech_dark` | 科技暗黑 | 技术、AI、代码、架构、工作流、基础设施、数据、自动化、暗黑 |
| `minimal_clean` | 极简清朗 | 极简、品牌、概念、轻商业、白皮书、产品说明、清爽 |
| `glass_premium` | 玻璃高级感 | 玻璃、高级、质感、SaaS 封面、金融科技、高端 |
| `neubrutalism` | 新粗野主义 | 冲击、醒目、大字、粗野、Z 世代、活动、宣传 |
| `bento_info` | 信息格栅 | 信息密集、多要素、全景图、功能对比、格栅、架构全景 |
| `clay_soft` | 粘土软萌 | 教育、软萌、轻松、亲子、健康、生活方式、可爱 |
| `zh_dense` | 中文信息密集 | 文档插图、mdBook、教材、讲义、博客、原理图、推导、对比表（**新增**） |

---

## 目录结构

```
.
├── SKILL.md                         # 技能主文件（工作流与约束）
├── README.md
├── requirements.txt                 # 可选后处理依赖
├── references/
│   ├── platform_profiles.md         # 平台尺寸与字号基准（含 doc_figure）
│   ├── layout_plan.schema.json      # 布局计划 schema
│   ├── prompt_template.md           # 复杂布局提示模板
│   ├── fonts_whitelist.json         # 字体白名单
│   ├── error_codes.md               # 错误码与退出码
│   ├── quality_checklist.md         # 交付质检清单
│   └── specs/                       # 七种风格规范
│       ├── tech_dark.md
│       ├── minimal_clean.md
│       ├── glass_premium.md
│       ├── neubrutalism.md
│       ├── bento_info.md
│       ├── clay_soft.md
│       └── zh_dense.md              # 新增
└── scripts/
    ├── run_pipeline.py              # 全流程管道
    ├── svg_validator.py             # 校验器（含 doc_figure）
    ├── svg_fixer.py                 # 自动修复
    ├── render_svg_preview.py        # QA 预览（含 doc_figure）
    └── optimize_and_convert.py      # 优化与 PNG 导出
```

---

## 快速开始

```bash
# 可选：安装后处理依赖（QA 预览 / PNG 导出）
pip install -r requirements.txt
# 若使用 playwright 渲染后端
playwright install chromium
```

---

## 工作流概览

1. **识别输出类型**：映射到 `wechat_cover` / `wechat_article` / `doc_figure`。
2. **选择风格**：无指定时按关键词推断；文档/课程/博客密集内容 → `doc_figure` + `zh_dense`。
3. **规划布局**：生成 `<slug>.layout.json` 布局计划。
4. **生成 SVG**：完整文件，含 `<title>`/`<desc>`、`svga-` ID 前缀、安全区约束。
5. **校验与修复**：
   ```bash
   python3 scripts/run_pipeline.py --svg draft.svg --plan layout.json --slug <slug> --strict
   python3 scripts/svg_validator.py --svg <path> --json
   ```
6. **交付**：输出 SVG 绝对路径 + 校验命令与 PASS 状态 + 质检自检摘要。

---

## 版本

当前 `metadata.version` 为 **0.16**，本次在此基础上新增 `zh_dense` 风格与 `doc_figure` 平台能力。
