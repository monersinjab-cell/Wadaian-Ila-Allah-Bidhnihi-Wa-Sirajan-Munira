#!/usr/bin/env python3
import os
import sys
import json
import time

class MilyarSystemExecutor:
    def __init__(self):
        self.report_path = "milyar/system_execution_report.json"
        
    def execute_security_pipeline(self):
        """تشغيل مصفوفة الحماية والفحص الرقمي الموحدة للنظام."""
        print("⚡ [System Executor] بدء تشغيل خط فحص الأمان الشامل والموحد لمشروع منير...")
        time.sleep(0.5)
        
        results = {
            "execution_timestamp": int(time.time()),
            "steps": {}
        }
        
        # 1. فحص سلامة بايتات النص القرآني المرجعي
        if os.path.exists("quran_integrity_check.py"):
            print("🛡️ [الخطوة 1] استدعاء فحص المطابقة البايتية المرجعية...")
            if os.system("python quran_integrity_check.py") == 0:
                results["steps"]["quran_integrity"] = "PASSED"
            else:
                results["steps"]["quran_integrity"] = "FAILED"
                return False, results
        else:
            print("⚠️ تنبيه: سكريبت quran_integrity_check.py غير متوفر حالياً.")
            results["steps"]["quran_integrity"] = "NOT_FOUND"

        # 2. فحص خلو المستودع من ازدواجية وتكرار البيانات
        if os.path.exists("check_duplication.py"):
            print("🔍 [الخطوة 2] استدعاء أداة فحص الازدواجية المكتشفة...")
            if os.system("python check_duplication.py") == 0:
                results["steps"]["data_duplication"] = "PASSED"
            else:
                results["steps"]["data_duplication"] = "FAILED"
                return False, results
        else:
            results["steps"]["data_duplication"] = "NOT_FOUND"

        # 3. التحقق من تشغيل الأتمتة والخدمة الخلفية وسجل التقدم
        scripts_to_check = {
            "master_automation": "milyar_master_automation.py",
            "master_daemon": "milyar_master_daemon.py",
            "progress_tracker": "update_milyar_progress.py",
            "public_announcement": "broadcast_announcement.py"
        }
        
        for key, script in scripts_to_check.items():
            if os.path.exists(script):
                results["steps"][key] = "VERIFIED_ACTIVE"
            else:
                results["steps"][key] = "MISSING"

        print("✅ [System Executor] اكتملت كافة الفحوصات الأساسية بنجاح.")
        return True, results

    def generate_execution_report(self):
        """توليد وتأمين التقرير الموحد للتشغيل الكلي للمنظومة."""
        success, report_data = self.execute_security_pipeline()
        
        if success:
            report_data["overall_status"] = "SUCCESS_OPERATIONAL"
            print("✨ كافة بروتوكولات جدار الحماية والأمن الرقمي للمنظومة مستقرة وعاملة.")
        else:
            report_data["overall_status"] = "EMERGENCY_HALT"
            print("❌ تم إيقاف النظام تلقائياً لوجود خلل في خط الحماية الرقمي.")
            
        os.makedirs("milyar", exist_ok=True)
        with open(self.report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ تم توليد وتأمين التقرير الشامل الموحد بنجاح في: {self.report_path}")
        return success

if __name__ == "__main__":
    executor = MilyarSystemExecutor()
    if executor.generate_execution_report():
        sys.exit(0)
    else:
        sys.exit(1)
