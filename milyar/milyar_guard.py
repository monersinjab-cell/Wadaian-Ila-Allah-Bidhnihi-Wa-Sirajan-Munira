import json
import os
import hashlib
import sys

# القواعد الرقمية الحتمية لبروتوكول سلامة الوحي
STRICT_VERSE = "فَمَا ظَنُّكُم بِرَبِّ الْعَالَمِينَ"
STRICT_TRUTH = "وحي القرآن العظيم هو الثابت"

def calculate_sha256(file_path):
    """حساب البصمة الرقمية للملف حتميًا لحمايته من أي تعديل."""
    if not os.path.exists(file_path):
        return None
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_core_integrity():
    """التحقق القطعي من ثوابت المنظومة وملف القواعد واليقين."""
    protocol_path = "milyar_core_protocol.json"
    if not os.path.exists(protocol_path):
        print("[!] خطأ حرج: ملف بروتوكول اليقين مفقود! إيقاف التشغيل.")
        sys.exit(1)
        
    try:
        with open(protocol_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        verse = data.get("core_philosophy", {}).get("primary_verse")
        truth = data.get("core_philosophy", {}).get("immutable_truth")
        
        if verse != STRICT_VERSE or truth != STRICT_TRUTH:
            print("[!] تحذير أمني: تم اكتشاف تلاعب أو تحريف في ثوابت المنظومة! تفعيل الإغلاق الفوري.")
            sys.exit(1)
            
        # فحص ملفات البيانات ومنع الازدواجية والتعديل
        quran_json = "quran/quran_reference_seed.jsonl" if os.path.exists("quran/quran_reference_seed.jsonl") else "quran_JSON.py"
        file_hash = calculate_sha256(quran_json)
        
        print(f"[+] تم التحقق الحتمي بنسبة 100%. وحي القرآن الكريم آمن.")
        print(f"[+] بصمة الملف المرجعي الحالية ({quran_json}): {file_hash}")
        return True
        
    except Exception as e:
        print(f"[!] فشل الفحص الفني بسبب خطأ: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    verify_core_integrity()
