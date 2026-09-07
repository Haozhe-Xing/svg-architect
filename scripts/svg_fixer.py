#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import os
import argparse
import re

def fix_svg(svg_path, error_codes, plan_path=None):
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except: return False
    
    fixed_any = False
    plan = {}
    if plan_path and os.path.exists(plan_path):
        with open(plan_path, 'r') as f: plan = json.load(f)

    for code in error_codes:
        # 1. ViewBox Fix
        if code in ["E_VIEWBOX_MISSING", "E_VIEWBOX_INVALID"] and plan.get('canvas'):
            root.attrib['viewBox'] = plan['canvas']['viewBox']
            fixed_any = True
        
        # 2. A11y Fix
        if code == "E_A11Y_MISSING":
            if not any(c.tag.split('}')[-1] == 'title' for c in root):
                title = ET.Element('{http://www.w3.org/2000/svg}title')
                title.text = plan.get('metadata', {}).get('platform', 'SVG Architect')
                root.insert(0, title)
            if not any(c.tag.split('}')[-1] == 'desc' for c in root):
                desc = ET.Element('{http://www.w3.org/2000/svg}desc')
                desc.text = "Verified industrial SVG asset."
                root.insert(1, desc)
            fixed_any = True

        # 3. Security Style Content Fix (P1-5: 强化清理，不误伤本地 URL)
        if code == "E_SECURITY_STYLE_CONTENT":
            for elem in root.iter():
                tag = elem.tag.split('}')[-1]
                if tag == 'style' and elem.text:
                    # 使用正则中和非本地引用
                    elem.text = re.sub(r'url\(\s*[\'"]?(?!#)[^)]*\)', 'url(#removed)', elem.text, flags=re.I)
                    elem.text = re.sub(r'@import|data:|javascript:', '/* removed */', elem.text, flags=re.I)
                    fixed_any = True
                if 'style' in elem.attrib:
                    s = elem.attrib['style']
                    s = re.sub(r'url\(\s*[\'"]?(?!#)[^)]*\)', 'url(#removed)', s, flags=re.I)
                    s = re.sub(r'data:|javascript:', '/* unsafe */', s, flags=re.I)
                    elem.attrib['style'] = s
                    fixed_any = True

    if fixed_any:
        tree.write(svg_path, encoding='utf-8', xml_declaration=True)
    return fixed_any

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", required=True)
    parser.add_argument("--errors", required=True)
    parser.add_argument("--plan")
    args = parser.parse_args()
    error_list = args.errors.split(',')
    success = fix_svg(args.svg, error_list, args.plan)
    print(f"Fix status: {'SUCCESS' if success else 'NO_CHANGE'}")

if __name__ == "__main__": main()
