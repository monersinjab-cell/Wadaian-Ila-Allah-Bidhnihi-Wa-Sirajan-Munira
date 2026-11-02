#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""منسق المهام (Task Coordinator) لإدارة وتنسيق العمليات البرمجية ببيئة مؤتمتة."""

import argparse
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_FILE = Path("logs/coordinator_history.jsonl")


def run_task(command):
    start_time = datetime.now(timezone.utc)
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        end_time = datetime.now(timezone.utc)
        
        return {
            "status": "SUCCESS" if process.returncode == 0 else "FAILED",
            "return_code": process.returncode,
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip(),
            "duration_seconds": (end_time - start_time).total_seconds()
        }
    except Exception as exc:
        end_time = datetime.now(timezone.utc)
        return {
            "status": "ERROR",
            "return_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_seconds": (end_time - start_time).total_seconds()
        }


def log_event(log_path, event_data):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event_data, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Task Coordinator - منسق المهام للتحكم بالعمليات المؤتمتة."
    )
    parser.add_argument("cmd", help="الأمر البرمجي المراد تنفيذه وتنسيقه.")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG_FILE, help="مسار ملف السجلات التراكمي.")
    args = parser.parse_args()

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "requested_command": args.cmd,
        "execution_result": {}
    }

    if "quran" in args.cmd.lower() and "check" not in args.cmd.lower():
         print("⚠️ [تحذير أمني] العمليات المباشرة على ملف المرجع محظورة عبر المنسق.")
         event["execution_result"] = {
             "status": "BLOCKED",
             "message": "تم حظر العملية وقائياً لحماية المكونات المرجعية."
         }
         log_event(args.log, event)
         return 1

    result = run_task(args.cmd)
    event["execution_result"] = result
    log_event(args.log, event)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
