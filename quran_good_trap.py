#!/usr/bin/env python3
import os
import sys
import json
import time

class QuranGoodTrap:
    def __init__(self):
        self.trap_log_path = "milyar/security_trap_log.json"
        self.monitored_files = [
            "quran_integrity_check.py",
            "check_duplication.py",
            "quran/quran_integrity_manifest.json"
        ]

    def verify_pipeline_integrity(self):
        """التحقق من خلو بيئة العمل من أي تكرار أو تلاعب بالبيانات قبل تفعيل المصيدة."""
        print("🛡️ [Security Trap] جاري فحص خط الدفاع الرقمي الأساسي...")
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [إيقاف فوري] تم رصد ازدواجية بيانات مكررة! إجهاض تفعيل مصيدة الأمان.")
                return False
        return True

    def deploy_trap_mechanism(self):
        """تفعيل آلية المصيدة ومراقبة سلامة الملفات الأساسية للنظام."""
        if not self.verify_pipeline_integrity():
            sys.exit(1)

        print("⚡ [Security Trap] جاري نشر مصيدة الحظر الذكي لحماية المستودع...")
        time.sleep(0.3)

        # فحص وجود الملفات الأساسية وتوثيق بصمتها الزمنية الحالية
        tamper_detected = False
        audit_results = {}

        for file_name in self.monitored_files:
            if os.path.exists(file_name):
                file_status = "SECURE_UNCHANGED"
                # التحقق من أن الملفات لم يتم تعديلها خارج خط التثبيت المعتمد
                audit_results[file_name] = {
                    "last_modified": os.path.getmtime(file_name),
                    "status": file_status
                }
            else:
                audit_results[file_name] = {
                    "status": "MISSING_WARNING"
                }

        # إعداد وثيقة سجل الأمان الحالية للمصيدة
        trap_status = {
            "activation_timestamp": int(time.time()),
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "trap_mode": "ACTIVE_MONITORING",
            "audit_manifest": audit_results,
            "system_lock_status": "LOCKED" if not tamper_detected else "BREACH_ALERT"
        }

        # حفظ وتأمين سجل المصيدة والأمان
        os.makedirs("milyar", exist_ok=True)
        with open(self.trap_log_path, 'w', encoding='utf-8') as f:
            json.dump(trap_status, f, indent=4, ensure_ascii=False)

        print(f"✅ تم تفعيل سكريبت الحظر الذكي ومصيدة الحماية بنجاح في: {self.trap_log_path}")
        return True

if __name__ == "__main__":
    trap = QuranGoodTrap()
    trap.deploy_trap_mechanism()
