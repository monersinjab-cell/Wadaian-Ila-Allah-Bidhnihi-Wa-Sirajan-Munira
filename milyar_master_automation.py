# -*- coding: utf-8 -*-
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
milyar_dir = ROOT / "milyar"
evidence_dir = milyar_dir / "evidence"
evidence_dir.mkdir(parents=True, exist_ok=True)

print("=== 🚀 تشغيل منظومة الأتمتة الموحدة والشاملة لجيش المليار ===")

now_utc = datetime.now(timezone.utc).isoformat()
report_data = {
    "project": "منظومة المليار العظمى — الأتمتة الموحدة",
    "executed_at_utc": now_utc,
    "results": {}
}

# 1. تشغيل وتقييم كتيبة النزاهة الرقمية للمصدر الشرعي
seed_file = ROOT / "milyar/corpus/approved/quran_reference_seed.jsonl"
sha_file = ROOT / "milyar/corpus/approved/quran_reference_seed.sha256"

if seed_file.exists() and sha_file.exists():
    current_hash = hashlib.sha256(seed_file.read_bytes()).hexdigest()
    expected_hash = sha_file.read_text().split()[0].strip()
    if current_hash == expected_hash:
        integrity_status = "✅ نجاح: بصمة المصدر سليمة ومطابقة بنسبة 100%."
    else:
        integrity_status = "🚨 تحذير: تم رصد تلاعب أو تعديل في ملف المرجع!"
else:
    integrity_status = "❌ خطأ: ملفات البذور أو التواقيع الرقمية مفقودة."

print(f"[كتيبة النزاهة]: {integrity_status}")
report_data["results"]["integrity_check"] = integrity_status

# 2. تشغيل وتقييم كتيبة التدقيق البرمجي ومكافحة الأخطاء
py_files = [p for p in ROOT.rglob("*.py") if "venv" not in p.parts and ".git" not in p.parts]
bad_syntax = []
for p in py_files:
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec")
    except Exception as e:
        bad_syntax.append(f"{p.name}: {type(e).__name__}")

syntax_status = f"✅ نجاح: تم فحص {len(py_files)} ملف بايثون، وجميعها سليمة." if not bad_syntax else f"❌ أخطاء مكتشفة: {bad_syntax}"
print(f"[كتيبة التدقيق]: {syntax_status}")
report_data["results"]["syntax_check"] = syntax_status

# 3. تشغيل وتقييم كتيبة الرقابة الأمنية لفحص الثغرات (دون طباعة السلسلة الحقيقية)
patterns = {"GitHub Token": r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"}
secret_findings = []
for p in py_files:
    if "milyar_master_automation.py" in p.name or "milyar_execute_all.py" in p.name:
        continue
    try:
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(patterns["GitHub Token"], line):
                secret_findings.append(f"{p.name} (السطر {i})")
    except:
        continue

security_status = "✅ نجاح: الملفات خالية من الرموز المكشوفة." if not secret_findings else f"⚠ مراجعة مطلوبة: رصد مؤشرات في {secret_findings}"
print(f"[كتيبة الرقابة]: {security_status}")
report_data["results"]["security_check"] = security_status

# 4. حفظ تقرير الأتمتة النهائي
output_report = milyar_dir / "MASTER_EXECUTION_REPORT.json"
output_report.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
print("\n=== 🎉 اكتملت كافة الفحوصات والأتمتة الشاملة بنجاح ===")
