#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import os
import argparse
import sys
import re

ERR_CODES = {
    "E_VIEWBOX_MISSING": "缺失 viewBox 属性",
    "E_VIEWBOX_INVALID": "viewBox 格式错误",
    "E_GEOMETRY_OUT_OF_BOUNDS": "坐标超出 viewBox 范围",
    "E_CONTRAST_LOW": "对比度不足 (要求 4.5:1)",
    "E_CONTRAST_UNRESOLVED": "关键文本颜色无法解析，对比度未知",
    "E_CONTRAST_GRADIENT_TEXT": "strict 模式下文字 fill 为渐变/pattern，对比度无法验证",
    "E_SECURITY_TAG": "检测到危险标签 (script/foreignobject/iframe/use)",
    "E_SECURITY_STYLE_CONTENT": "检测到危险的样式内容 (@import/外部url/data/js)",
    "E_SECURITY_EXTERNAL": "检测到非法外链或脚本协议",
    "E_A11Y_MISSING": "缺少 title 或 desc 标签",
    "E_ID_PREFIX_MISSING": "id 属性未使用规定前缀",
    "E_FONT_FAMILY_MISSING": "文本元素缺少 font-family（含祖先继承）",
    "E_FONT_FALLBACK_MISSING": "font-family 缺少 sans-serif 或 monospace fallback",
    "E_FONT_EXTERNAL": "检测到 @font-face 或外部字体 url",
    "E_FONT_SIZE_TOO_SMALL": "文字字号低于平台 Caption 下限",
    "E_XML_PARSE_FAIL": "XML 解析失败",
    "E_VALIDATOR_CRASH": "校验器运行时异常",
}

SVG_NS = "http://www.w3.org/2000/svg"

def log_stderr(msg):
    print(msg, file=sys.stderr)

def parse_length(length_str, viewBox_size=1000):
    if not length_str:
        return 0
    length_str = str(length_str).strip().lower()
    if length_str.endswith('%'):
        try:
            return (float(length_str[:-1]) / 100.0) * viewBox_size
        except:
            return 0
    if length_str.endswith('px'):
        try:
            return float(length_str[:-2])
        except:
            return 0
    try:
        return float(re.sub(r'[a-z%]+', '', length_str))
    except:
        return 0

_CSS_NAMED_COLORS = {
    'black': '000000', 'white': 'ffffff', 'red': 'ff0000', 'green': '008000',
    'blue': '0000ff', 'yellow': 'ffff00', 'cyan': '00ffff', 'magenta': 'ff00ff',
    'orange': 'ffa500', 'purple': '800080', 'pink': 'ffc0cb', 'gray': '808080',
    'grey': '808080', 'silver': 'c0c0c0', 'navy': '000080', 'teal': '008080',
    'maroon': '800000', 'olive': '808000', 'lime': '00ff00', 'aqua': '00ffff',
    'fuchsia': 'ff00ff', 'coral': 'ff7f50', 'salmon': 'fa8072', 'gold': 'ffd700',
    'indigo': '4b0082', 'violet': 'ee82ee', 'brown': 'a52a2a', 'crimson': 'dc143c',
    'darkblue': '00008b', 'darkgray': 'a9a9a9', 'darkgreen': '006400',
    'lightblue': 'add8e6', 'lightgray': 'd3d3d3', 'lightyellow': 'ffffe0',
    'whitesmoke': 'f5f5f5', 'ghostwhite': 'f8f8ff',
}

def parse_color(color_str):
    if not color_str or color_str in ('none', 'transparent'):
        return None
    color_str = color_str.strip().lower()
    if color_str in _CSS_NAMED_COLORS:
        return _CSS_NAMED_COLORS[color_str]
    if color_str.startswith('#'):
        c = color_str.lstrip('#')
        if len(c) == 3:
            c = ''.join([ch * 2 for ch in c])
        if len(c) == 6:
            return c
        return None
    if color_str.startswith('rgb'):
        nums = re.findall(r'\d+', color_str)
        if len(nums) >= 3:
            return '{:02x}{:02x}{:02x}'.format(int(nums[0]), int(nums[1]), int(nums[2]))
        return None
    return None

def get_luminance(hex_color):
    if not hex_color:
        return 0.5
    try:
        r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    except:
        return 0.5

def check_contrast_ratio(c1_hex, c2_hex):
    if not c1_hex or not c2_hex:
        return None
    l1, l2 = get_luminance(c1_hex), get_luminance(c2_hex)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def parse_rect(rect_str):
    if not rect_str:
        return None
    parts = re.split(r'[,\s]+', rect_str.strip())
    if len(parts) != 4:
        return None
    try:
        return [float(p) for p in parts]
    except:
        return None

def _get_style_prop(style_str, prop):
    """从 style="..." 字符串中提取属性值。"""
    if not style_str:
        return None
    for part in style_str.split(';'):
        part = part.strip()
        if ':' in part:
            k, _, v = part.partition(':')
            if k.strip().lower() == prop:
                return v.strip()
    return None

def _resolve_attr(elem, attr, ancestors):
    """从元素自身 attr/style 或祖先链查找继承值，返回字符串或 None。"""
    # 自身属性
    val = elem.attrib.get(attr)
    if not val:
        val = _get_style_prop(elem.attrib.get('style', ''), attr)
    if val:
        return val
    # 祖先继承（从近到远）
    for anc in reversed(ancestors):
        val = anc.attrib.get(attr)
        if not val:
            val = _get_style_prop(anc.attrib.get('style', ''), attr)
        if val:
            return val
    return None

def _has_generic_fallback(font_family_str):
    """检查 font-family 末尾是否包含 sans-serif 或 monospace。"""
    families = [f.strip().strip('"\'').lower() for f in font_family_str.split(',')]
    if not families:
        return False
    last = families[-1]
    return last in ('sans-serif', 'monospace', 'serif', 'cursive', 'fantasy')

def _is_gradient_fill(fill_str):
    """检查 fill 是否指向渐变/pattern（url(#...)）。"""
    if not fill_str:
        return False
    return bool(re.match(r'url\s*\(', fill_str.strip().lower()))

def _build_ancestor_map(root):
    """构建每个元素的祖先列表 {id(elem): [anc, ...]}（从根到父）。"""
    parent_map = {}
    for parent in root.iter():
        for child in parent:
            parent_map[id(child)] = parent
    ancestors = {}
    for elem in root.iter():
        chain = []
        cur = elem
        while id(cur) in parent_map:
            cur = parent_map[id(cur)]
            chain.insert(0, cur)
        ancestors[id(elem)] = chain
    return ancestors

def detect_platform(vb_parts):
    """根据 viewBox 自动识别平台，返回 (platform_name, min_font_size)。

    doc_figure 高度按内容弹性（360–1200），仅按宽度识别。
    """
    if not vb_parts:
        return None, None
    _, _, w, h = vb_parts
    if abs(w - 1800) <= 20 and abs(h - 766) <= 20:
        return 'wechat_cover', 18
    if abs(w - 1200) <= 20 and abs(h - 500) <= 20:
        return 'wechat_article', 16
    if abs(w - 680) <= 16 and 360 <= h <= 1200:
        return 'doc_figure', 12
    return None, None

def validate_svg(svg_file, layout_plan_file=None, strict=False, id_prefix='svga-', platform='auto'):
    report = {"status": "PASS", "errors": [], "warnings": [], "info": []}
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
        vb_raw = root.attrib.get('viewBox', '')
        vb_parts = parse_rect(vb_raw)

        v_w = 1200
        v_h = 500
        if vb_parts:
            v_w = vb_parts[2]
            v_h = vb_parts[3]

        # 确定平台与字号下限
        if platform == 'auto':
            detected_platform, min_font_size = detect_platform(vb_parts)
        else:
            detected_platform = platform
            if platform == 'wechat_cover':
                min_font_size = 18
            elif platform == 'wechat_article':
                min_font_size = 16
            elif platform == 'doc_figure':
                min_font_size = 12
            else:
                min_font_size = None

        if detected_platform is None and platform == 'auto':
            report["warnings"].append({"code": "W_PLATFORM_UNKNOWN", "msg": "无法识别平台，跳过字号下限检查"})

        # ── 1. Geometry ──────────────────────────────────────────────────────
        if not vb_raw:
            report["errors"].append({"code": "E_VIEWBOX_MISSING", "msg": ERR_CODES["E_VIEWBOX_MISSING"]})
        elif not vb_parts:
            report["errors"].append({"code": "E_VIEWBOX_INVALID", "msg": ERR_CODES["E_VIEWBOX_INVALID"]})
        else:
            v_x, v_y, v_w, v_h = vb_parts
            if layout_plan_file and os.path.exists(layout_plan_file):
                with open(layout_plan_file, 'r') as f:
                    plan = json.load(f)
                sa = plan['canvas']['safe_area']
                if (sa['x'] < v_x or sa['y'] < v_y
                        or (sa['x'] + sa['width']) > (v_x + v_w)
                        or (sa['y'] + sa['height']) > (v_y + v_h)):
                    report["errors"].append({"code": "E_GEOMETRY_OUT_OF_BOUNDS",
                                             "msg": f"Safe Area {sa} exceeds viewBox"})
                for slot in plan.get('slots', []):
                    r = slot['rect']
                    if (r['x'] < v_x or r['y'] < v_y
                            or (r['x'] + r['w']) > (v_x + v_w)
                            or (r['y'] + r['h']) > (v_y + v_h)):
                        report["errors"].append({"code": "E_GEOMETRY_OUT_OF_BOUNDS",
                                                 "msg": f"Slot {slot['slot_id']} exceeds viewBox"})

        # ── 2. Security ───────────────────────────────────────────────────────
        for elem in root.iter():
            tag = elem.tag.split('}')[-1].lower()
            if tag in ('script', 'foreignobject', 'iframe'):
                report["errors"].append({"code": "E_SECURITY_TAG",
                                         "msg": f"Dangerous tag <{tag}> detected."})

            if tag == 'use':
                href = elem.attrib.get('href',
                       elem.attrib.get('{http://www.w3.org/1999/xlink}href', ''))
                if href and not href.startswith('#'):
                    report["errors"].append({"code": "E_SECURITY_EXTERNAL",
                                             "msg": f"External use href detected: {href}"})

            style_text = elem.text if tag == 'style' else elem.attrib.get('style', '')
            if style_text:
                # 外部字体 @font-face
                if re.search(r'@font-face', style_text, re.I):
                    report["errors"].append({"code": "E_FONT_EXTERNAL",
                                             "msg": ERR_CODES["E_FONT_EXTERNAL"]})
                if re.search(r'url\(\s*[\'"]?(?!#)', style_text, re.I) or \
                        any(p in style_text.lower() for p in ['@import', 'data:', 'javascript:']):
                    report["errors"].append({"code": "E_SECURITY_STYLE_CONTENT",
                                             "msg": ERR_CODES["E_SECURITY_STYLE_CONTENT"]})

            for attr, value in elem.attrib.items():
                if (any(p in value.lower() for p in ['http:', 'https:', 'data:', 'javascript:'])
                        and not value.strip().startswith('#')):
                    report["errors"].append({"code": "E_SECURITY_EXTERNAL",
                                             "msg": f"Unsafe value in {attr}: {value}"})

        # ── 3. ID 前缀检查 ────────────────────────────────────────────────────
        if id_prefix:
            all_ids = set()
            for elem in root.iter():
                eid = elem.attrib.get('id')
                if eid is None:
                    continue
                # SVG 根节点允许无前缀
                if elem is root:
                    continue
                all_ids.add(eid)
                if not eid.startswith(id_prefix):
                    report["errors"].append({
                        "code": "E_ID_PREFIX_MISSING",
                        "msg": f"id=\"{eid}\" 未使用前缀 \"{id_prefix}\"",
                    })

            # 引用一致性警告（不存在的 id）
            for elem in root.iter():
                for attr in ('href', '{http://www.w3.org/1999/xlink}href'):
                    ref = elem.attrib.get(attr, '')
                    if ref.startswith('#'):
                        target = ref[1:]
                        if target not in all_ids and target != root.attrib.get('id', ''):
                            report["warnings"].append({
                                "code": "W_ID_REF_MISSING",
                                "msg": f"{attr}=\"{ref}\" 引用的 id 不存在",
                            })
                fill = elem.attrib.get('fill', '')
                m = re.match(r'url\(#([^)]+)\)', fill.strip())
                if m:
                    target = m.group(1)
                    if target not in all_ids and target != root.attrib.get('id', ''):
                        report["warnings"].append({
                            "code": "W_ID_REF_MISSING",
                            "msg": f"fill=\"{fill}\" 引用的 id 不存在",
                        })

        # ── 4. Contrast ───────────────────────────────────────────────────────
        bg_color_hex = "0a0a0b"
        max_area = 0
        for rect in root.iter(f'{{{SVG_NS}}}rect'):
            w = parse_length(rect.attrib.get('width', '0'), v_w)
            h = parse_length(rect.attrib.get('height', '0'), v_w)
            if w * h > max_area:
                max_area = w * h
                c = parse_color(rect.attrib.get('fill', '#000000'))
                if c:
                    bg_color_hex = c

        ancestor_map = _build_ancestor_map(root)

        for text in root.iter(f'{{{SVG_NS}}}text'):
            ancestors = ancestor_map.get(id(text), [])
            fill_val = _resolve_attr(text, 'fill', ancestors) or 'white'

            if _is_gradient_fill(fill_val):
                if strict:
                    report["errors"].append({
                        "code": "E_CONTRAST_GRADIENT_TEXT",
                        "msg": ERR_CODES["E_CONTRAST_GRADIENT_TEXT"],
                    })
                else:
                    report["warnings"].append({
                        "code": "W_CONTRAST_GRADIENT_TEXT",
                        "msg": "文字 fill 为渐变，对比度无法自动验证",
                    })
                continue

            txt_color_hex = parse_color(fill_val)
            ratio = check_contrast_ratio(bg_color_hex, txt_color_hex)
            if ratio is None:
                if strict:
                    report["errors"].append({"code": "E_CONTRAST_UNRESOLVED",
                                             "msg": "Text color unresolved."})
                else:
                    report["warnings"].append({"code": "W_COLOR_UNRESOLVED",
                                               "msg": "Text color unresolved."})
            elif ratio < 4.5:
                level = "errors" if strict else "warnings"
                report[level].append({"code": "E_CONTRAST_LOW",
                                      "msg": f"Contrast ratio {ratio:.2f}:1 low."})

        # ── 5. A11y ───────────────────────────────────────────────────────────
        has_title = any(c.tag.split('}')[-1].lower() == 'title' for c in root)
        has_desc = any(c.tag.split('}')[-1].lower() == 'desc' for c in root)
        if not (has_title and has_desc):
            report["errors"].append({"code": "E_A11Y_MISSING", "msg": ERR_CODES["E_A11Y_MISSING"]})

        # ── 6. 字体检查 ───────────────────────────────────────────────────────
        text_tags = (f'{{{SVG_NS}}}text', f'{{{SVG_NS}}}tspan')
        for elem in root.iter():
            if elem.tag not in text_tags:
                continue
            ancestors = ancestor_map.get(id(elem), [])
            ff = _resolve_attr(elem, 'font-family', ancestors)
            if not ff:
                report["errors"].append({
                    "code": "E_FONT_FAMILY_MISSING",
                    "msg": ERR_CODES["E_FONT_FAMILY_MISSING"],
                })
            elif not _has_generic_fallback(ff):
                report["errors"].append({
                    "code": "E_FONT_FALLBACK_MISSING",
                    "msg": f"font-family=\"{ff}\" 缺少 sans-serif/monospace fallback",
                })

        # ── 7. 字号检查 ───────────────────────────────────────────────────────
        if min_font_size is not None:
            for elem in root.iter():
                if elem.tag not in text_tags:
                    continue
                ancestors = ancestor_map.get(id(elem), [])
                fs_str = _resolve_attr(elem, 'font-size', ancestors)
                if fs_str is None:
                    if strict:
                        report["errors"].append({
                            "code": "E_FONT_SIZE_TOO_SMALL",
                            "msg": "font-size 无法解析（strict 模式视为违规）",
                        })
                    else:
                        report["warnings"].append({
                            "code": "W_FONT_SIZE_UNRESOLVED",
                            "msg": "font-size 无法解析",
                        })
                    continue
                fs = parse_length(fs_str)
                if fs < min_font_size:
                    report["errors"].append({
                        "code": "E_FONT_SIZE_TOO_SMALL",
                        "msg": f"font-size={fs}px 低于平台下限 {min_font_size}px",
                    })

    except ET.ParseError as e:
        report["errors"].append({"code": "E_XML_PARSE_FAIL", "msg": str(e)})
    except Exception as e:
        report["errors"].append({"code": "E_VALIDATOR_CRASH", "msg": str(e)})

    report["status"] = "ERROR" if report["errors"] else "PASS"
    return report


def main():
    parser = argparse.ArgumentParser(description="SVG Architect Validator")
    parser.add_argument("--svg", required=True, help="SVG 文件路径")
    parser.add_argument("--plan", help="layout_plan.json 路径")
    parser.add_argument("--strict", action="store_true", help="strict 模式（对比度/渐变文字等升为 error）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出报告")
    parser.add_argument("--id-prefix", default="svga-", dest="id_prefix",
                        help="ID 前缀规则（默认 svga-，设为空字符串可跳过检查）")
    parser.add_argument("--platform", default="auto",
                        choices=["auto", "wechat_cover", "wechat_article", "doc_figure"],
                        help="目标平台（auto 时从 viewBox 自动识别）")
    args = parser.parse_args()

    log_stderr(f"[*] Validating {args.svg}...")
    report = validate_svg(args.svg, args.plan, args.strict, args.id_prefix, args.platform)

    if args.json:
        print(json.dumps(report))
    else:
        print(f"Status: {report['status']}")
        for e in report["errors"]:
            print(f"  [ERR] {e['code']}: {e['msg']}")
        for w in report["warnings"]:
            print(f"  [WRN] {w['code']}: {w['msg']}")

    sys.exit(1 if report["status"] == "ERROR" else 0)


if __name__ == "__main__":
    main()
