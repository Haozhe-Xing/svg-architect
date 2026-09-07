# Layout Planning Reference

Phase 2 布局规划的示例输出，供参考。

## 布局计划示例（tech_dark + wechat_cover）

```json
{
  "canvas": {
    "viewBox": "0 0 1800 766",
    "safe_area": { "x": 150, "y": 80, "width": 1500, "height": 606 }
  },
  "metadata": {
    "theme": "tech_dark",
    "platform": "wechat_cover",
    "language": "zh"
  },
  "slots": [
    { "slot_id": "background",  "rect": { "x": 0,    "y": 0,   "w": 1800, "h": 766 } },
    { "slot_id": "title_area",  "rect": { "x": 150,  "y": 180, "w": 900,  "h": 280 } },
    { "slot_id": "info_area",   "rect": { "x": 150,  "y": 480, "w": 900,  "h": 160 } },
    { "slot_id": "brand_mark",  "rect": { "x": 1500, "y": 80,  "w": 200,  "h": 200 } }
  ],
  "creative_zone": {
    "allowed_area": "right half (x: 900-1800)",
    "visual_language": "floating nodes with glow lines",
    "focal_point": "center-right"
  },
  "palette": {
    "background": "#0A0A0B",
    "primary": "#3B82F6",
    "text": "#F8FAFC"
  }
}
```

## Self-Check 示例（Phase 4）

对照 `references/quality_checklist.md` 逐项核查，输出格式：

| ID | 检查项 | 状态 | 备注 |
|----|--------|------|------|
| tech-1 | viewBox 正确 | ✅ | `0 0 1800 766` |
| tech-3 | 无外部资源链接 | ✅ | 无外链 |
| acc-2 | 对比度 ≥ 4.5:1 | ✅ | #F8FAFC on #0A0A0B ≈ 17:1 |
| comp-1 | 核心信息在 safe_area 内 | ✅ | 标题 y=180，在 80-686 范围内 |
