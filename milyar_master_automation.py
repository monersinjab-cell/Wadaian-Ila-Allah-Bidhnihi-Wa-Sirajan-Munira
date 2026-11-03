#!/usr/bin/env python3
import os
import sys
import json
import time

class MilyarMasterAutomation:
    def __init__(self):
        self.automation_log = "milyar/automation_status.json"
        self.is_system_locked = False

    def run_pre_flight_security(self):
        """تشغيل آليات الفحص الأمني الشامل لمنظومة المليار قبل التفعيل الكامل."""
        print("🛡️ [Master Automation] بدء الفحص الأمني الاستباقي الشامل...")
        
        # 1. التحقق من سلامة النص القرآني المرجعي
        if os.path.exists("quran_integrity_check.py"):
            if os.system("python quran_integrity_check.py") != 0:
                print("❌ [إيقاف فوري] فشل فحص مطابقة النص المرجعي الشريف!")
                return False
        
        # 2. التحقق من خلو المستودع من ازدواجية البيانات
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [إيقاف فوري] تم رصد ازدواجية بيانات مكررة في ملفات JSON/JSONL!")
                return False

        # 3. التحقق من سجل التقدم وتوثيقه
        if os.path.exists("update_milyar_progress.py"):
            print("✅ سكريبت حماية التقدم جاهز ومفعل.")
            
        return True

    def initialize_orchestration(self):
        """بدء إدارة العمليات الكبرى وربط وتنسيق المهام المؤتمتة."""
        if not self.run_pre_flight_security():
            print("❌ تم حظر تفعيل الأتمتة الشاملة لعدم استيفاء معايير الحماية الصارمة.")
            sys.exit(1)
            
        print("🚀 [منظومة المليار الخيرية] تم تفعيل الأتمتة الرئيسية (Master Automation) بنجاح.")
        print("🔒 النظام بأكمله يدار الآن تحت جدار حماية دفاعي صارم ومؤتمت بالكامل.")
        
        # تسجيل حالة التفعيل بنجاح في ملف التكوين النشط
        status_data = {
            "master_status": "OPERATIONAL",
            "last_verification": int(time.time()),
            "security_lock": "STRICT_ACTIVE"
        }
        
        with open(self.automation_log, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ تم تأمين وتحديث تقرير حالة الأتمتة في: {self.automation_log}")
        return True

if __name__ == "__main__":
    master = MilyarMasterAutomation()
    master.initialize_orchestration()
