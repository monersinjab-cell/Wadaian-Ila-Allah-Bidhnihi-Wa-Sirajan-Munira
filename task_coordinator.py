#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""منسق المهام (Task Coordinator) لإدارة وتنسيق العمليات البرمجية مع نظام النسخ الاحتياطي التلقائي."""

import argparse
import json
import sys
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_FILE = Path("logs/coordinator_history.jsonl")
BACKUP_DIR = Path("backups")


def run_task(command):
    """تنفيذ المهمة البرمجية والتقاط حالتها ومخرجاتها."""
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


def trigger_auto_backup(target_file_or_dir):
    """إنشاء نسخة احتياطية مؤرشفة وتلقائية للملفات أو المجلدات الهامة."""
    try:
        path_to_backup = Path(target_file_or_dir)
        if not path_to_backup.exists():
            return {"status": "SKIPPED", "message": "المسار المستهدف للنسخ الاحتياطي غير موجود."}
            
        # حظر أمني لمنع تعديل أو إعادة كتابة مخرجات خط الأساس القرآني
        if "quran" in str(path_to_backup).lower():
            return {"status": "BLOCKED", "message": "ملفات المرجع القرآني محمية برمجياً ضد عمليات التعديل أو التكرار الخارجي."}

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{path_to_backup.name}_{timestamp}"
        
        if path_to_backup.is_file():
            dest = BACKUP_DIR / backup_name
            shutil.copy2(path_to_backup, dest)
        elif path_to_backup.is_dir():
            dest = BACKUP_DIR / backup_name
            shutil.copytree(path_to_backup, dest)
            
        return {
            "status": "BACKUP_SUCCESS",
            "destination": str(dest),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    except Exception as exc:
        return {"status": "BACKUP_ERROR", "message": str(exc)}


def log_event(log_path, event_data):
    """تسجيل العمليات بنمط JSONL لحفظ السجلات التراكمية."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event_data, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Task Coordinator - منسق المهام للتحكم بالعمليات المؤتمتة مع النسخ الاحتياطي التلقائي."
    )
    parser.add_argument("cmd", help="الأمر البرمجي المراد تنفيذه وتنسيقه.")
    parser.add_argument("--backup-target", help="مسار ملف أو مجلد لأخذ نسخة احتياطية تلقائية له عند نجاح المهمة.")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG_FILE, help="مسار ملف السجلات التراكمي.")
    args = parser.parse_args()

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "requested_command": args.cmd,
        "execution_result": {},
        "backup_result": None
    }

    # الفحص الوقائي وحماية المكونات المرجعية الأساسية
    if "quran" in args.cmd.lower() and "check" not in args.cmd.lower():
         print("⚠️ [تحذير أمني] العمليات المباشرة على ملف المرجع محظورة عبر المنسق.")
         event["execution_result"] = {
             "status": "BLOCKED",
             "message": "تم حظر العملية وقائياً لحماية المكونات المرجعية."
         }
         log_event(args.log, event)
         return 1

    # تشغيل المهمة وتوثيق المخرجات
    result = run_task(args.cmd)
    event["execution_result"] = result

    # تنفيذ النسخ الاحتياطي التلقائي إذا طُلب وكانت العملية ناجحة
    if result["status"] == "SUCCESS" and args.backup_target:
        print(f"⏳ جاري تفعيل النسخ الاحتياطي التلقائي لـ: {args.backup_target}...")
        backup_res = trigger_auto_backup(args.backup_target)
        event["backup_result"] = backup_res
        print(f"📦 نتيجة النسخ الاحتياطي: {backup_res['status']}")

    # كتابة السجل الكلي
    log_event(args.log, event)

    # طباعة ملخص العملية للطرفية
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
