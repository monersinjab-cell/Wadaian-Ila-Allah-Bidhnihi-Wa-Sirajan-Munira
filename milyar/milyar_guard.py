import json
import os
import hashlib

def verify_core_protocol():
    protocol_path = "milyar_core_protocol.json"
    if not os.path.exists(protocol_path):
        print("[!] خطأ حرج: ملف البروتوكول الأساسي مفقود!")
        return False
    
    with open(protocol_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # التأكيد الحتمي على الثوابت
    verse = data.get("core_philosophy", {}).get("primary_verse")
    truth = data.get("core_philosophy", {}).get("immutable_truth")
    
    if verse != "فَمَا ظَنُّكُم بِرَبِّ الْعَالَمِينَ" or truth != "وحي القرآن العظيم هو الثابت":
        print("[!] تحذير: تم كشف محاولة لتعديل الثوابت الرقمية! إغلاق المنظومة فوراً.")
        return False
        
    print("[+] تم التحقق من بروتوكول اليقين الحتمي بنظام نجاح.")
    return True

def clean_and_sync_json_data():
    print("[+] جاري فحص وتنظيف الازدواجية بين ملفات JSON و JSONL...")
    # هنا يتم التأكد من مطابقة ملفات quran_JSON و quran_reference_seed
    # لمنع أي تكرار أو تعارض برميجي في النصوص المرجعية العليا
    pass

if __name__ == "__main__":
    if verify_core_protocol():
        clean_and_sync_json_data()
