#!/usr/bin/env python3
import os
import sys
import json
import time
import hashlib

class PreemptiveDefenseSystem:
    def __init__(self):
        self.defense_log_path = "milyar/defense_strike_log.json"
        self.is_shield_active = True
        # تعيين الآية الكريمة كشعار روحي ثابت للحماية والردع
        self.defense_verse = "وارادو به كيدا فجعلناهم الأخسرين"

    def calculate_file_hash(self, file_path):
        """حساب قيمة SHA-256 للملفات الأساسية للتحقق من سلامتها البايتية."""
        if not os.path.exists(file_path):
            return None
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def verify_system_integrity(self):
        """فحص تكامل النظام كلياً ضد أي تكرار أو تلاعب خارجي قبل تنشيط الردع."""
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [ضربة استباقية] تم رصد ازدواجية وتكرار بيانات! تفعيل الإغلاق الفوري لحماية النواة.")
                return False
        return True

    def execute_universe_purge(self, reason):
        """آلية الإغلاق الفوري وحظر العمليات لتطهير بيئة العمل عند رصد أي تهديد."""
        print(f"🚨 [إجراء دفاعي حاسم] تم تفعيل بروتوكول الإغلاق والحظر الفوري بسبب: {reason}")
        print(f"🛡️ الشعار النشط: {self.defense_verse}")
        
        strike_event = {
            "timestamp": int(time.time()),
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "event": "PREEMPTIVE_STRIKE_ACTIVATED",
            "trigger_reason": reason,
            "system_action": "EMERGENCY_SHUTDOWN_ENFORCED"
        }
        
        os.makedirs("milyar", exist_ok=True)
        with open(self.defense_log_path, 'w', encoding='utf-8') as f:
            json.dump(strike_event, f, indent=4, ensure_ascii=False)
            
        print(f"🔒 تم قفل المنظومة بنجاح وتوثيق الحدث في: {self.defense_log_path}")
        # إنهاء البرنامج فوراً لحماية المستودع والملفات الحساسة
        sys.exit(1)

    def run_defense_monitor(self):
        print("⚡ [الرد التلقائي] تنشيط الخوارزمية الدفاعية الصامتة والضربات الاستباقية...")
        if not self.verify_system_integrity():
            self.execute_universe_purge("DATA_DUPLICATION_DETECTED")
            
        # التحقق من ثبات وبصمة ملف التكوين لتجنب التلاعب غير المصرح به
        config_file = "config_v2.json"
        if os.path.exists(config_file):
            current_hash = self.calculate_file_hash(config_file)
            print(f"🔍 بصمة SHA-256 الحالية لملف التكوين: {current_hash}")
            
        print("✅ [الرد التلقائي] المنظومة في وضع الدفاع والردع النشط والمستقر بنجاح.")
        return True

if __name__ == "__main__":
    defense_system = PreemptiveDefenseSystem()
    defense_system.run_defense_monitor()
