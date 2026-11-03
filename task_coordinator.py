import os
import json

class MilyarTaskCoordinator:
    def __init__(self, config_path="config_v2.json"):
        self.config_path = config_path
        self.active_tasks = []

    def initialize_system_checks(self):
        """تنسيق استدعاء ملفات الفحص والتقييم والترجمة المحددة في النظام"""
        print("[+] جاري بدء تشغيل منسق المهام المركزي...")
        
        # مصفوفة التحقق من وجود المكونات الأساسية للـ AI
        components = {
            "Evaluator": "ai/model_evaluator.py",
            "Multi-Translator": "ai/translators/multi_translator.py"
        }
        
        for name, path in components.items():
            if os.path.exists(path):
                print(f"    - تم فحص وتأكيد جاهزية المكون: {name}")
                self.active_tasks.append(name)
            else:
                print(f"    - تنبيه: المكون {name} غير متوفر في المسار المحدد.")
                
        return {"status": "READY", "tasks_coordinated": self.active_tasks}

if __name__ == "__main__":
    coordinator = MilyarTaskCoordinator()
    result = coordinator.initialize_system_checks()
    print("[+] تم تهيئة نظام منسق المهام الأولي للمشروع بنجاح.")
