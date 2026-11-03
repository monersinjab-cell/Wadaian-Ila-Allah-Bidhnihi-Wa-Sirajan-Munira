#!/usr/bin/env python3
import os
import sys
import urllib.parse
import json

class FastSocialPublisher:
    def __init__(self):
        self.facebook_post_path = "milyar/social_campaign/facebook_x_post.txt"
        self.repo_url = "https://github.com"
        
    def check_security(self):
        """التحقق من سلامة البيئة وعدم التكرار قبل إطلاق حملة النشر السريع."""
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [حظر فوري] تم رصد ازدواجية بيانات مكررة في المستودع! تم إلغاء حملة النشر.")
                return False
        return True

    def launch_broadcast(self):
        if not self.check_security():
            sys.exit(1)

        # قراءة النص الرسمي المعتمد المرفوع في المستودع
        if os.path.exists(self.facebook_post_path):
            with open(self.facebook_post_path, 'r', encoding='utf-8') as f:
                post_text = f.read()
        else:
            post_text = f"إشهار رسمي لمنظومة المليار الخيرية وجيش المليار بقيادة منير محمد نذير سنجاب. {self.repo_url}"

        # ترميز النص ليتوافق مع روابط الويب الآمنة (URL Encoding)
        encoded_text = urllib.parse.quote(post_text)

        print("\n🚀 [إطلاق النشر القوي والسريع] جاري فتح بوابات النشر الفوري على المنصات العالمية...")

        # توليد روابط النشر الفوري (Web Intents)
        platforms = {
            "𝕏 (تويتر سابقاً)": f"https://twitter.com{encoded_text}",
            "فيسبوك (Facebook)": f"https://facebook.com{urllib.parse.quote(self.repo_url)}",
            "لينكد إن (LinkedIn)": f"https://linkedin.com{urllib.parse.quote(self.repo_url)}"
        }

        for name, url in platforms.items():
            print(f"📡 جاري فتح بوابة النشر على {name}...")
            # استخدام أمر Termux لفتح الروابط مباشرة في المتصفح أو التطبيق الرسمي للمنصة على الهاتف
            os.system(f"termux-open '{url}'")
            
        print("\n📸 [تنويه للمنصات المرئية - تيك توك، إنستغرام، سناب شات]:")
        print("💡 تم نسخ الروابط بنجاح. يرجى فتح التطبيق ونشر الفيديو المخصص للمنظومة مع النص الجاهز في مجلد Campaign.")
        return True

if __name__ == "__main__":
    publisher = FastSocialPublisher()
    publisher.launch_broadcast()
