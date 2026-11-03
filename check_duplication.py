#!/usr/bin/env python3
import os
import json

def check_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            seen = set()
            duplicates = 0
            for item in data:
                serialized = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if serialized in seen:
                    duplicates += 1
                else:
                    seen.add(serialized)
            return duplicates
        return 0
    except Exception:
        return 0

def check_json_file_lines(file_path):
    try:
        seen = set()
        duplicates = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    parsed = json.loads(clean_line)
                    serialized = json.dumps(parsed, sort_keys=True, ensure_ascii=False)
                    if serialized in seen:
                        duplicates += 1
                    else:
                        seen.add(serialized)
                except json.JSONDecodeError:
                    pass
        return duplicates
    except Exception:
        return 0

def main():
    print("🔍 جاري فحص ملفات JSON و JSONL لمنع تكرار البيانات وازدواجيتها...")
    total_duplicates = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json') and not file.endswith('integrity_manifest.json'):
                dups = check_json_file(file_path)
                if dups > 0:
                    print(f"⚠️ تم العثور على {dups} عناصر مكررة في الملف: {file_path}")
                    total_duplicates += dups
            elif file.endswith('.jsonl'):
                dups = check_json_file_lines(file_path)
                if dups > 0:
                    print(f"⚠️ تم العثور على {dups} أسطر مكررة في الملف: {file_path}")
                    total_duplicates += dups

    if total_duplicates == 0:
        print("✅ المنظومة سليمة تماماً: لم يتم العثور على أي بيانات مكررة.")
        return 0
    else:
        print(f"❌ تم حظر العملية: إجمالي التكرارات المكتشفة هو {total_duplicates}")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
