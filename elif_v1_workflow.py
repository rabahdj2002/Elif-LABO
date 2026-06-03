import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_workflow():
    parser = argparse.ArgumentParser(description="ELIF V1 One-Command Workflow")
    parser.add_argument("--case", required=True, help="Case directory name in cases/")
    parser.add_argument("--condition", default="c", help="Procedure condition (default: c)")
    parser.add_argument("--out-dir", type=Path, help="Directory for output artifacts (default: results/<case_id>/<timestamp>)")
    parser.add_argument("--api-key", help="Anthropic API Key (bypasses environment variable)")
    
    args = parser.parse_args()
    
    case_id = args.case
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = args.out_dir or Path(f"results/{case_id}/{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = out_dir / "run_report.json"
    
    print(f"--- Starting ELIF V1 Workflow for Case: {case_id} ---")
    
    # 1. Run the procedure
    print(f"[*] Step 1: Executing 11-step reasoning procedure...")
    # We use subprocess to call the CLI module
    env = os.environ.copy()
    
    # If API key is provided via argument, set it in the internal environment
    if args.api_key:
        env["ELIF_ANTHROPIC_API_KEY"] = args.api_key
    
    # Ensure ELIF_CASES_DIR is passed through if not already in env
    if "ELIF_CASES_DIR" not in env:
        # Fallback to the local workspace-relative path
        env["ELIF_CASES_DIR"] = str(Path(__file__).parent / "cases")
        
    # Ensure PYTHONPATH is set so src is discoverable
    src_path = str(Path(__file__).parent / "src")
    env["PYTHONPATH"] = src_path
    
    cmd_run = [
        sys.executable, "-m", "elif_v0_1.cli", "run",
        "--case", case_id,
        "--condition", args.condition,
        "--results-dir", str(out_dir)
    ]
    
    try:
        # We capture output and write to file to avoid PowerShell encoding issues in the future
        result = subprocess.run(cmd_run, capture_output=True, text=True, env=env, check=True)
        report_path.write_text(result.stdout, encoding="utf-8")
        print(f"    [+] Run complete. Report saved to {report_path}")
    except subprocess.CalledProcessError as e:
        print(f"    [!] Error during execution (Exit code {e.returncode}):")
        print(e.stderr)
        return e.returncode

    # 2. Generate Viewers
    print(f"[*] Step 2: Generating visual reasoning surfaces...")
    
    viewers = [
        ("decision-room", "decision_room.md"),
        ("exploration", "exploration_lens.md"),
        ("object-drift", "object_drift_panel.md")
    ]
    
    for cmd, filename in viewers:
        viewer_out = out_dir / filename
        cmd_viewer = [
            sys.executable, "-m", "elif_v0_1.viewers.cli", cmd,
            "--run-report", str(report_path),
            "--out", str(viewer_out)
        ]
        # Object drift needs the input frame anchor if available
        if cmd == "object-drift":
            cases_dir = env.get("ELIF_CASES_DIR")
            if cases_dir:
                frame_path = Path(cases_dir) / case_id / "input_frame.md"
                if frame_path.exists():
                    cmd_viewer.extend(["--input-frame", str(frame_path)])
        
        try:
            subprocess.run(cmd_viewer, env=env, check=True)
            print(f"    [+] Generated {filename}")
        except subprocess.CalledProcessError as e:
            print(f"    [!] Failed to generate {filename}")

    print(f"\n--- Workflow Complete ---")
    print(f"Artifacts available in: {out_dir}")
    print(f"Final Verdict can be found in: {out_dir / 'decision_room_md'}")
    return 0

if __name__ == "__main__":
    sys.exit(run_workflow())
