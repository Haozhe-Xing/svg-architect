#!/usr/bin/env python3
import argparse
import os
import subprocess
import shutil
import re
import sys
import xml.etree.ElementTree as ET
import json

def prefix_svg_ids_xml(svg_path, prefix):
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        id_map = {}
        for elem in root.iter():
            if 'id' in elem.attrib:
                old_id = elem.attrib['id']
                new_id = f"{prefix}_{old_id}"
                id_map[old_id] = new_id
                elem.attrib['id'] = new_id
        for elem in root.iter():
            for attr, value in elem.attrib.items():
                if 'url(#' in value:
                    for old_id, new_id in id_map.items():
                        value = value.replace(f'url(#{old_id})', f'url(#{new_id})')
                    elem.attrib[attr] = value
                if value.startswith('#'):
                    old_id = value[1:]
                    if old_id in id_map:
                        elem.attrib[attr] = f"#{id_map[old_id]}"
        tree.write(svg_path, encoding='utf-8', xml_declaration=True)
        return True
    except: return False

def optimize_with_svgo(input_path, output_path):
    if shutil.which('svgo'):
        try:
            subprocess.run(['svgo', input_path, '-o', output_path], check=True, capture_output=True)
            return True
        except: return False
    return False

def convert_to_png(svg_path, png_path, width=None, height=None):
    for tool in ['cairosvg', 'resvg-js']:
        if shutil.which(tool):
            try:
                cmd = [tool, svg_path, '-o', png_path] if tool == 'cairosvg' else ['resvg-js', svg_path, png_path]
                if width and tool == 'cairosvg': cmd.extend(['-w', str(width)])
                subprocess.run(cmd, check=True, capture_output=True)
                return True
            except: continue
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output")
    parser.add_argument("--png")
    parser.add_argument("--prefix")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=630)
    parser.add_argument("--format", default="svg", choices=["svg", "png", "all"], help="Export format")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    report = {"status": "SUCCESS", "details": {}}
    if not os.path.exists(args.input):
        report["status"] = "FAILED"
        if args.json: print(json.dumps(report))
        sys.exit(1)
        
    output_svg = args.output if args.output else args.input
    output_png = args.png if args.png else args.input.replace('.svg', '.png')
    if args.output and args.output != args.input: shutil.copy(args.input, args.output)

    if args.prefix: report["details"]["prefix"] = "SUCCESS" if prefix_svg_ids_xml(output_svg, args.prefix) else "FAILED"
    report["details"]["svgo"] = "SUCCESS" if optimize_with_svgo(output_svg, output_svg) else "SKIPPED"
    
    # New Logic: Bitmap conversion only if requested
    if args.format in ["png", "all"]:
        if convert_to_png(output_svg, output_png, args.width, args.height):
            report["details"]["png"] = "SUCCESS"
        else:
            report["details"]["png"] = "FAILED"
            report["status"] = "PARTIAL_SUCCESS"
    else:
        report["details"]["png"] = "NOT_REQUESTED"

    if args.json:
        print(json.dumps(report))
    else:
        print(f"Status: {report['status']}")
        print(f"Details: {report['details']}")
        
    sys.exit(0 if report["status"] == "SUCCESS" else (4 if report["status"] == "PARTIAL_SUCCESS" else 1))

if __name__ == "__main__": main()
