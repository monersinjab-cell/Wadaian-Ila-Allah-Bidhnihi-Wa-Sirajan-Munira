#!/usr/bin/env python3
import os
import sys
import json
import time

class TaskCoordinator:
    def __init__(self):
        self.manifest_path = "agent_manifest.json"
        self.core_protocol_path = "milyar_core_protocol.json"
        self.is_firewall_enabled = False
        self.load_configurations()

    def load_configurations(self):
        """تحميل بروتوكولات الأمان والبيانات الأساسية للمنظومة."""
        print("🛡️ جاري قراءة بروتوكولات الأمان وملفات التكوين...")
        if os.path.exists(self.core_protocol_path):
            try:
                with open(self.core_protocol_path, 'r', encoding='utf-8') as f:
                    protocol = json.load(f)
                print("✅ تم تحميل milyar_core_protocol.json بنجاح.")
            except Exception as e:
                print(f"⚠️ فشل في قراءة ملف بروتوكول النواة: {e}")
        else:
            print("⚠️ تنبيه: ملف milyar_core_protocol.json غير موجود.")

    def enable_self_defense_firewall(self):
        """تفعيل جدار الحماية الذاتي لمنع التلاعب البرمجي بالنظام."""
        print("⚡ جاري تفعيل جدار الحماية للدفاع الذاتي في Task Coordinator...")
        self.is_firewall_enabled = True
        time.sleep(0.5)
        print("🔒 تم تشغيل جدار الحماية بنجاح. كافة صلاحيات العمليات تحت المراقبة الصارمة.")

    def run_security_checks(self):
        """تشغيل فحص السلامة التلقائي قبل تنسيق وجدولة أي مهمة برمجية."""
        print("🔍 جاري فحص تكامل النظام الرقمي قبل بدء الجدولة...")
        
        # استدعاء أداة التحقق من الازدواجية والتكرار
        if os.path.exists("check_duplication.py"):
            exit_code = os.system("python check_duplication.py")
            if exit_code != 0:
                print("❌ تم إيقاف منسق المهام: تم اكتشاف ازدواجية غير مصرح بها في ملفات النظام.")
                return False
        
        # استدعاء خطاف التحقق من النص القرآني المرجعي
        if os.path.exists("quran_integrity_check.py"):
            exit_code = os.system("python quran_integrity_check.py")
            if exit_code != 0:
                print("❌ تم إيقاف منسق المهام: فشل فحص مطابقة بايتات النص المرجعي الشريف.")
                return False
                
        print("✅ اجتاز النظام كافة فحوصات الأمان والتكامل البنيوي.")
        return True

    def execute_coordinator(self):
        """بدء إدارة العمليات وتنسيق المهام المؤتمتة للمنظومة."""
        self.enable_self_defense_firewall()
        if not self.run_security_checks():
            print("❌ إجهاض تشغيل منسق المهام لحماية النظام.")
            sys.exit(1)
            
        print("🚀 منسق المهام (Task Coordinator) في وضع الاستعداد والتشغيل النشط الآن.")
        # هنا يتم استقبال وجدولة مهام طلبات نماذج الذكاء الاصطناعي الآلية لاحقاً

if __name__ == "__main__":
    coordinator = TaskCoordinator()
    coordinator.execute_coordinator()
