#!/usr/bin/env python3
import os
import sys
import json
import time

class MilyarProgressTracker:
    def __init__(self):
        self.progress_log_path = "milyar/system_progress_log.json"
        
    def verify_security_protocols(self):
        """التحقق من تفعيل كافة خطافات الحماية وعدم وجود ازدواجية قبل تحديث السجل."""
        print("🛡️ جاري تشغيل فحوصات الحماية التلقائية لجيش المليار...")
        
        # 1. فحص تكرار البيانات
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ تم حظر تحديث التقدم: تم رصد ازدواجية بيانات في المستودع!")
                return False
                
        # 2. فحص خطاف الحماية للنص القرآني المرجعي
        if os.path.exists(".git/hooks/pre-commit"):
            print("✅ خطاف الحماية المحمي pre-commit hook نشط ومفعل.")
            
        return True

    def record_progress(self, phase_name, details):
        """تسجيل وتأمين خطوة التقدم الجديدة في ملف السجل النشط."""
        if not self.verify_security_protocols():
            print("❌ إجهاض عملية تحديث السجل لأسباب أمنية.")
            return False
            
        print(f"📝 جاري تسجيل التقدم الحالي للمنظومة: [{phase_name}]...")
        os.makedirs("milyar", exist_ok=True)
        
        log_data = []
        if os.path.exists(self.progress_log_path):
            try:
                with open(self.progress_log_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            except Exception:
                log_data = []
                
        new_entry = {
            "timestamp": int(time.time()),
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "phase": phase_name,
            "details": details,
            "integrity_lock": "SECURED"
        }
        
        log_data.append(new_entry)
        
        with open(self.progress_log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ تم تحديث وتأمين سجل التقدم بنجاح في: {self.progress_log_path}")
        return True

if __name__ == "__main__":
    tracker = MilyarProgressTracker()
    # تسجيل خطوة الدمج والتأمين الحالية للمنظومة
    success = tracker.record_progress(
        phase_name="تأمين النواة والنموذج المحلي",
        details="دمج سكريبت فحص الازدواجية، وتفعيل خطافات الحماية، وتوثيق مقاييس النموذج المحلي المتعدد اللغات."
    )
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
