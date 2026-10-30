# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from milyar.quran_guard import verify_and_isolate_output

def execute_sandbox_test():
    print("=== 🧪 بدء تشغيل حقل الاختبار الحتمي لجيش المليار ===")
    
    # النص الأول: مطابق وموثق بالكامل في المرجع (الإسراء: 36)
    exact_text = "﴿وَلَا تَقْفُ مَا لَيْسَ لَكَ بِهِۦ عِلْمٌ ۚ إِنَّ ٱلسَّمْعَ وَٱلْبَصَرَ وَٱلْفُؤَادَ كُلُّ أُو۟لَٰٓئِكَ كَانَ عَنْهُ مَسْـُٔولًا﴾"
    
    # النص الثاني: محرف عمداً بإسقاط علامة ضبط واحدة (علمٌ -> علم)
    manipulated_text = "﴿وَلَا تَقْفُ مَا لَيْسَ لَكَ بِهِۦ عِلْمٌ﴾"

    print("\n1. فحص النص الموثق والمطابق حرفياً:")
    try:
        res = verify_and_isolate_output(exact_text)
        print("✅ [النتيجة الفعلية]: تم قبول النص بنجاح وتمريره لتطابقه المطلق.")
    except Exception as e:
        print(f"❌ [النتيجة الفعلية]: فشل خطأ في قبول النص السليم: {e}")

    print("\n2. فحص النص المحرف والمقتطع عمداً:")
    try:
        verify_and_isolate_output(manipulated_text)
        print("❌ [النتيجة الفعلية]: ثغرة أمنية! النظام مرر النص المحرف دون حظر.")
    except ValueError as e:
        print(f"🔒 [النتيجة الفعلية]: نجاح الحماية الحتمية! تم اكتشاف المخالفة وحجب النص فوراً.")
        print(f"📋 نص الرسالة الأمنية الصادرة: {e}")

if __name__ == '__main__':
    execute_sandbox_test()
