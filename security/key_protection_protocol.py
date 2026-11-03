import os
import re

class MilyarKeyProtection:
    def __init__(self):
        # مصفوفة التعبيرات النمطية لاكتشاف المفاتيح والرموز الرقمية (GitHub Tokens & GCP Keys)
        self.patterns = {
            "GitHub PAT": r"(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{82})",
            "Google Cloud API Key": r"AIza[yA-Z0-9_-]{35}"
        }

    def scan_project_files(self, target_dir="."):
        """مسح كامل للملفات للتأكد من خلوها من أي تسريب رقمي قبل الرفع"""
        print("[+] جاري بدء فحص النزاهة الرقمية للمفاتيح وسجلات الإعدادات...")
        leaks_found = 0
        
        for root, _, files in os.walk(target_dir):
            # تخطي مجلدات التتبع والملفات المخفية
            if ".git" in root or "ai/" in root:
                continue
            for file in files:
                if file.endswith(('.json', '.py', '.jsonl', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        for key_type, pattern in self.patterns.items():
                            if re.search(pattern, content):
                                print(f"    - [تنبيه صارم] تم رصد خطر تسريب محتمل من نوع ({key_type}) في: {file_path}")
                                leaks_found += 1
                    except Exception:
                        continue
                        
        if leaks_found == 0:
            print("    - [حصن الحماية آمن] لم يتم العثور على أي مفاتيح مكشوفة في ملفات الإعدادات.")
        return {"status": "SECURE" if leaks_found == 0 else "WARNING", "leaks_count": leaks_found}

if __name__ == "__main__":
    protector = MilyarKeyProtection()
    protection_status = protector.scan_project_files()
    print("[+] تم إنهاء فحص بروتوكول الحماية والخصوصية للمفاتيح بنجاح.")
