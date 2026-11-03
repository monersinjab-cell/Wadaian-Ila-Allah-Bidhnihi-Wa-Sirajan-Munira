import os
import json

class MilyarDataRepositoryManager:
    def __init__(self, config_path="config_v2.json"):
        self.config_path = config_path
        self.data_dir = "milyar"
        
    def resolve_json_to_jsonl(self, json_file_name, jsonl_file_name):
        json_path = os.path.join(self.data_dir, json_file_name)
        jsonl_path = os.path.join(self.data_dir, jsonl_file_name)
        
        if not os.path.exists(json_path):
            print(f"[-] ملف المصدر {json_file_name} غير موجود حالياً.")
            return False
            
        print(f"[+] جاري معالجة مستودع البيانات لإلغاء الازدواجية بين {json_file_name} و {jsonl_file_name}...")
        
        with open(json_path, 'r', encoding='utf-8') as j_file:
            try:
                new_data = json.load(j_file)
            except json.JSONDecodeError:
                print("[-] خطأ في بنية ملف JSON المرجعي.")
                return False

        if isinstance(new_data, dict):
            new_data = [new_data]
            
        existing_signatures = set()
        if os.path.exists(jsonl_path):
            with open(jsonl_path, 'r', encoding='utf-8') as jl_file:
                for line in jl_file:
                    try:
                        record = json.loads(line.strip())
                        existing_signatures.add(json.dumps(record, sort_keys=True))
                    except json.JSONDecodeError:
                        continue

        deduplicated_count = 0
        with open(jsonl_path, 'a', encoding='utf-8') as jl_file:
            for entry in new_data:
                entry_signature = json.dumps(entry, sort_keys=True)
                if entry_signature not in existing_signatures:
                    jl_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    existing_signatures.add(entry_signature)
                    deduplicated_count += 1
                    
        print(f"    - [حصن البيانات آمن] تم دمج {deduplicated_count} سطر فريد بنجاح دون أي تكرار.")
        return True

if __name__ == "__main__":
    manager = MilyarDataRepositoryManager()
    manager.resolve_json_to_jsonl("milyar_core_protocol.json", "milyar_core_protocol.jsonl")
