import hashlib
import json
from pathlib import Path

def verify_seed_integrity():
    seed = Path("milyar/corpus/approved/quran_reference_seed.jsonl")
    sha_file = Path("milyar/corpus/approved/quran_reference_seed.sha256")
    if not seed.exists() or not sha_file.exists():
        return "❌ خطأ: ملفات البذور أو التواقيع الرقمية مفقودة!"
    
    current_hash = hashlib.sha256(seed.read_bytes()).hexdigest()
    expected_hash = sha_file.read_text().split()[0].strip()
    
    if current_hash == expected_hash:
        return "✅ نجاح: بصمة المصدر سليمة ومطابقة بنسبة 100%."
    return "🚨 تحذير: تم اكتشاف تلاعب أو تعديل في ملف المرجع القرآني العظيم!"

if __name__ == '__main__':
    print(verify_seed_integrity())
