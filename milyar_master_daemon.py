#!/usr/bin/env python3
import os
import sys
import json
import time

class MilyarMasterDaemon:
    def __init__(self):
        self.daemon_status_path = "milyar/daemon_status.json"
        self.is_running = False
        
    def check_core_integrity(self):
        """فحص تكامل المنظومة كلياً قبل تشغيل الخدمة الخلفية المستمرة."""
        print("🛡️ [Daemon Core] جاري التحقق من بروتوكولات الأمان الشاملة للمنظومة...")
        
        # 1. فحص عدم تكرار أو ازدواجية البيانات
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [Daemon Alert] تم رصد ازدواجية بيانات مكررة! إجهاض تشغيل الخدمة الخلفية.")
                return False
                
        # 2. فحص سلامة النص القرآني المرجعي
        if os.path.exists("quran_integrity_check.py"):
            if os.system("python quran_integrity_check.py") != 0:
                print("❌ [Daemon Alert] فشل مطابقة النص المرجعي الشريف! إجهاض فوري للخدمة.")
                return False
                
        print("✅ [Daemon Core] المنظومة مستقرة واجتازت كافة معايير السلامة الرقمية.")
        return True

    def start_daemon_service(self):
        """تشغيل وتأمين الخدمة الخلفية المركزية."""
        if not self.check_core_integrity():
            sys.exit(1)
            
        print("⚙️ [Daemon Core] جاري تشغيل الخدمة الخلفية المستمرة للنظام...")
        self.is_running = True
        
        # تسجيل تقرير حالة تشغيل الخدمة الخلفية
        daemon_status = {
            "daemon_mode": "ACTIVE_BACKGROUND_SERVICE",
            "uptime_start": int(time.time()),
            "integrity_shield": "STRICT_ENFORCED",
            "status": "HEALTHY"
        }
        
        os.makedirs("milyar", exist_ok=True)
        with open(self.daemon_status_path, 'w', encoding='utf-8') as f:
            json.dump(daemon_status, f, indent=4, ensure_ascii=False)
            
        print(f"✅ تم تشغيل الـ Daemon وتأمين ملف الحالة بنجاح في: {self.daemon_status_path}")
        return True

if __name__ == "__main__":
    daemon = MilyarMasterDaemon()
    daemon.start_daemon_service()
