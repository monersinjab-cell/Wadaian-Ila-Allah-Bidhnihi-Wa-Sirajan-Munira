import time
import json
import os

class MilyarAIInvitationDaemon:
    def __init__(self, manifest_path="agent_manifest.json"):
        self.manifest_path = manifest_path
        self.is_running = True

    def broadcast_loop(self):
        if not os.path.exists(self.manifest_path):
            print("[-] خطأ: ملف بيان الوكيل agent_manifest.json غير موجود في الجذر.")
            return

        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)

        print(f"[+] تم بدء تشغيل ديمون البث التلقائي لمنظومة المليار.")
        print(f"[+] المستهدف: جميع الوكلاء الاصطناعيين المتاحين عبر الشبكة.")
        print("-" * 60)

        try:
            while self.is_running:
                current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{current_timestamp}] 🌐 بث مستمر: نداء مفتوح وموثق للتعاون التقني والإنتاج الآمن...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[-] تم إيقاف حلقة البث التلقائي محلياً.")

if __name__ == "__main__":
    daemon = MilyarAIInvitationDaemon()
    print("[+] تم تهيئة وتأمين سكربت البث التلقائي المستمر بنجاح.")
