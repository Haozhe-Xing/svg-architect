#!/usr/bin/env python3
import subprocess
import json
import os
import argparse
import sys
import hashlib
import shlex
import shutil
from datetime import datetime
from pathlib import Path

# Skill Root deduction
SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"

AUTO_FIXABLE = ["E_VIEWBOX_MISSING", "E_VIEWBOX_INVALID", "E_A11Y_MISSING", "E_SECURITY_STYLE_CONTENT"]

def get_file_hash(path):
    try:
        with open(path, 'rb') as f: return hashlib.md5(f.read()).hexdigest()
    except: return None

def run_cmd(cmd, env=None):
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return res.returncode, res.stdout, res.stderr

def main():
    parser = argparse.ArgumentParser(description="Industrial SVG Orchestrator v14 (Hard Reporting)")
    parser.add_argument("--svg", required=True)
    parser.add_argument("--plan")
    parser.add_argument("--slug", default="asset")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--repair-cmd", help="External command to fix errors")
    parser.add_argument("--export-format", default="svg", choices=["svg", "png", "all"])
    parser.add_argument("--output-dir", default=os.environ.get("SVG_ARCHITECT_WORKSPACE", os.path.join(os.path.expanduser("~"), "Documents", "workspace", "svg-architect")))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_filename = f"{timestamp}_{args.slug}"
    target_svg = out_dir / f"{target_filename}.svg"
    target_png = out_dir / f"{target_filename}.png"
    
    shutil.copy(args.svg, target_svg)
    working_svg = str(target_svg.resolve())

    print(f"[*] Pipeline Init: {working_svg}")
    attempt = 0
    attempt_history = set()

    while attempt <= args.max_retries:
        val_cmd = ['python3', str(SCRIPTS_DIR / "svg_validator.py"), '--svg', working_svg, '--json']
        if args.plan: val_cmd.extend(['--plan', args.plan])
        if args.strict: val_cmd.append('--strict')
        
        _, stdout, stderr = run_cmd(val_cmd)
        try:
            report = json.loads(stdout.strip())
        except:
            sys.exit(2)
            
        if report['status'] == 'PASS':
            break
            
        errors = [e['code'] for e in report['errors']]
        file_hash = get_file_hash(working_svg)
        state_id = hashlib.md5(f"{sorted(errors)}_{file_hash}".encode()).hexdigest()
        if state_id in attempt_history:
            sys.exit(1)
        attempt_history.add(state_id)

        fixable = [e for e in errors if e in AUTO_FIXABLE]
        non_fixable = [e for e in errors if e not in AUTO_FIXABLE]
        
        if fixable:
            fix_cmd = ['python3', str(SCRIPTS_DIR / "svg_fixer.py"), '--svg', working_svg, '--errors', ','.join(fixable)]
            if args.plan: fix_cmd.extend(['--plan', args.plan])
            run_cmd(fix_cmd)
            attempt += 1
            continue
            
        if non_fixable:
            if args.repair_cmd:
                env = os.environ.copy()
                env['SVG_ERRORS'] = ','.join(non_fixable)
                ret, _, r_err = run_cmd(shlex.split(args.repair_cmd), env=env)
                if ret != 0:
                    attempt += 1
                    continue
                attempt += 1
                continue
            else:
                sys.exit(3)
        attempt += 1

    # Final Gate: Post-processing (Hard Logic Fix)
    pp_cmd = ['python3', str(SCRIPTS_DIR / "optimize_and_convert.py"), working_svg, 
              '--output', working_svg, '--png', str(target_png.resolve()),
              '--format', args.export_format, '--json']
    
    ret, pp_out, pp_err = run_cmd(pp_cmd)
    
    # 核心修复：先解析，后打印
    try:
        pp_report = json.loads(pp_out.strip())
        svg_abs = str(Path(working_svg).resolve())
        
        if pp_report['status'] == 'SUCCESS':
            print(f"svg_abs_path: {svg_abs}")
            if args.export_format in ["png", "all"]:
                print(f"png_abs_path: {target_png.resolve()}")
            print("status: SUCCESS")
            sys.exit(0)
        elif pp_report['status'] == 'PARTIAL_SUCCESS':
            print(f"svg_abs_path: {svg_abs}")
            print("status: PARTIAL_SUCCESS")
            print("reason: Bitmap conversion failed.")
            sys.exit(4)
        else:
            print("status: FAILED")
            print(f"reason: {pp_report}")
            sys.exit(4)
    except Exception:
        # 强制：解析失败绝不输出 SUCCESS
        print("status: FAILED")
        print("[💥] Post-processing report malformed or empty.")
        sys.exit(4)

if __name__ == "__main__": main()
