import json, re, subprocess, hashlib
from pathlib import Path
from datetime import datetime, timezone

root = Path.cwd()
base = root / "milyar"
base.mkdir(exist_ok=True)
evidence_dir = base / "evidence"
evidence_dir.mkdir(exist_ok=True)
now = datetime.now(timezone.utc).isoformat()
checks = []

def record(task, status, detail, files=None):
    checks.append({
        "task": task,
        "status": status,
        "detail": detail,
        "files": files or [],
        "checked_at_utc": now
    })

def write(rel, content):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + "\n", encoding="utf-8")
    return rel

# M-001: Quran text integrity. Never rewrite Quran text.
quran_candidates = [
    root / "milyar/corpus/approved/quran_reference_seed.jsonl"
]
quran_file = next((p for p in quran_candidates if p.is_file()), None)
if quran_file:
    raw = quran_file.read_bytes()
    record("M-001", "قيد التحقق",
           "عُثر على ملف نصي؛ حُسبت بصمته فقط. لم تتم مطابقته مع مصدر معتمد.",
           [str(quran_file.relative_to(root))])
    quran_note = (
        "# M-001 — سلامة النص القرآني\n\n"
        f"- الملف الموجود: `{quran_file.relative_to(root)}`\n"
        f"- SHA-256: `{hashlib.sha256(raw).hexdigest()}`\n"
        "- نتيجة المطابقة مع مصدر قرآني معتمد: لم تُنفّذ.\n"
        "- لم يُعدّل هذا السكربت محتوى النص القرآني.\n"
        "- لا تعتبر البصمة وحدها إثباتاً لصحة النص.\n"
    )
else:
    record("M-001", "متعذرة مؤقتاً",
           "لم يُعثر على quran/quran.txt أو quran.txt؛ يلزم تحديد مصدر النص المعتمد.")
    quran_note = (
        "# M-001 — سلامة النص القرآني\n\n"
        "لم يُعثر على ملف النص المتوقع. لم يُنشأ نص بديل ولم يُخترع مصدر.\n"
        "يلزم توفير الملف ومصدره المعتمد ثم إجراء المطابقة.\n"
    )
write("milyar/evidence/M-001.md", quran_note)

# M-002: source registry template, no invented sources.
write("milyar/SOURCES_REGISTER.csv",
      "title,organization,url,accessed_date,source_type,verification_status\n")
write("milyar/evidence/M-002.md", """# M-002 — سجل المصادر العلمية

تم إنشاء سجل فارغ. لم تُضف مصادر مختلقة.
لكل مصدر لاحقاً: العنوان، الجهة، الرابط، تاريخ الاطلاع، نوع المصدر،
وما تم التحقق منه فعلياً.
الحالة: قيد التنفيذ؛ السجل يحتاج مصادر موثقة.
""")
record("M-002", "قيد التنفيذ",
       "أُنشئ سجل المصادر الفارغ؛ لم تُضف مصادر خارجية قبل التحقق.",
       ["milyar/SOURCES_REGISTER.csv"])

# M-003: reproducible research log template.
write("milyar/EXPERIMENT_TEMPLATE.md", """# نموذج تسجيل بحث أو تجربة

- رقم السجل:
- تاريخ التسجيل:
- السؤال:
- الفرضية (غير مثبتة حتى اختبارها):
- الطريقة والأدوات:
- البيانات ومصدرها:
- خطوات إعادة الاختبار:
- النتيجة الفعلية:
- حدود التجربة ومصادر الخطأ:
- هل هي محاكاة أم قياس واقعي؟
- رابط الأدلة:
- المراجع:
- المراجع المستقل ونتيجة مراجعته:
""")
write("milyar/evidence/M-003.md", """# M-003 — البحث والتجارب

تم إنشاء نموذج للتوثيق وإعادة الاختبار.
لم تُسجل نتيجة تجريبية مختلقة؛ يلزم تنفيذ تجربة وتسجيل بياناتها الفعلية.
""")
record("M-003", "قيد التنفيذ",
       "أُنشئ نموذج البحث والتجربة؛ لا توجد تجربة جديدة مثبتة.")

# M-004: safe static checks; do not execute project scripts.
py_files = list(root.rglob("*.py"))
json_files = list(root.rglob("*.json"))
skip_parts = {".git", ".venv", "venv", "__pycache__", "node_modules"}
py_files = [p for p in py_files if not (set(p.parts) & skip_parts)]
json_files = [p for p in json_files if not (set(p.parts) & skip_parts)]
py_ok, py_bad = [], []
for p in py_files:
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec")
        py_ok.append(str(p.relative_to(root)))
    except Exception as e:
        py_bad.append((str(p.relative_to(root)), type(e).__name__))

json_ok, json_bad = [], []
for p in json_files:
    try:
        json.loads(p.read_text(encoding="utf-8"))
        json_ok.append(str(p.relative_to(root)))
    except Exception as e:
        json_bad.append((str(p.relative_to(root)), type(e).__name__))

software_report = [
    "# M-004 — نتائج الفحص المحلي",
    "",
    f"- ملفات Python التي اجتازت فحص الصياغة: {len(py_ok)}",
    f"- ملفات Python التي فشل فحصها: {len(py_bad)}",
    f"- ملفات JSON الصحيحة: {len(json_ok)}",
    f"- ملفات JSON غير الصحيحة: {len(json_bad)}",
    "- هذا فحص صياغة فقط؛ لا يثبت صحة الوظائف ولا يشغّل البرامج.",
    "",
    "## أخطاء Python"
]
software_report += [f"- `{p}` — {err}" for p, err in py_bad] or ["- لا أخطاء صياغة مكتشفة."]
software_report += ["", "## أخطاء JSON"]
software_report += [f"- `{p}` — {err}" for p, err in json_bad] or ["- لا أخطاء JSON مكتشفة."]
write("milyar/evidence/M-004.md", "\n".join(software_report))
record("M-004", "قيد التنفيذ" if py_bad or json_bad else "فحص أولي ناجح",
       f"Python: {len(py_ok)} ناجح و{len(py_bad)} أخطاء؛ JSON: {len(json_ok)} صحيح و{len(json_bad)} أخطاء.",
       ["milyar/evidence/M-004.md"])

# M-005: scan tracked public files for likely secret patterns.
# Report only file and line number, never print the matched secret.
patterns = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token_like", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key_like", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("generic_secret_assignment", re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"))
]
try:
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
except Exception:
    tracked = []

findings = []
for name in tracked:
    p = root / name
    try:
        if not p.is_file() or p.stat().st_size > 2_000_000:
            continue
    except (OSError, ValueError):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in patterns:
            if pattern.search(line):
                findings.append({"file": name, "line": lineno, "pattern": label})
                break

audit_lines = [
    "# M-005 — فحص مؤشرات الأسرار",
    "",
    f"- الملفات المتتبعة التي فُحصت: {len(tracked)}",
    f"- الأسطر التي تطابق أنماطاً محتملة: {len(findings)}",
    "- هذا فحص آلي محدود؛ قد ينتج إنذارات كاذبة أو يفوّت أسراراً.",
    "- لم تُطبع أي قيمة سرية في التقرير.",
    ""
]
audit_lines += [
    f"- `{x['file']}`، سطر {x['line']}: `{x['pattern']}`"
    for x in findings
] or ["لم تُكتشف مؤشرات مطابقة للأنماط المحددة."]
write("milyar/evidence/M-005.md", "\n".join(audit_lines))
record("M-005", "مراجعة مطلوبة" if findings else "فحص آلي أولي",
       f"عُثر على {len(findings)} تطابقات محتملة. راجع الملفات يدوياً دون نسخ الأسرار.",
       ["milyar/evidence/M-005.md"])

# M-006: translation and accessibility policy.
write("milyar/LANGUAGE_POLICY.md", """# سياسة اللغات وإمكانية الوصول

1. يُحفظ النص القرآني الأصلي منفصلاً ولا يُعدّل بغرض الترجمة.
2. تُعرض كل ترجمة في ملف مستقل مع اسم المترجم والمصدر والتاريخ.
3. لا تُنسب الترجمة إلى النص القرآني الأصلي.
4. يُوسم المحتوى غير المراجع بأنه مسودة.
5. تُراعى قابلية القراءة على الهاتف، والتباين، والنص البديل للصور.
6. تُخطط اللغات والإتاحة بالتدريج؛ لا يُدّعى اكتمال ترجمة غير موجودة.
""")
write("milyar/evidence/M-006.md",
      "# M-006 — اللغات وإمكانية الوصول\n\nتم إعداد سياسة فصل النص الأصلي عن الترجمة. لم تُدّعَ ترجمة مكتملة.\n")
record("M-006", "قيد التنفيذ",
       "أُنشئت سياسة للترجمة والإتاحة؛ يلزم تطبيقها ومراجعة المحتوى.")

# M-007: measurable, civilian service proposal.
write("milyar/COMMUNITY_SERVICE_PLAN.md", """# M-007 — مبادرة خدمة معرفية مدنية

## المبادرة
إعداد دليل رقمي مجاني يعلّم توثيق المصادر والتحقق من الادعاءات.

## تجربة أولية مقترحة
- إعداد صفحة واحدة تشرح طريقة التحقق من مصدر.
- إرفاق مصدر عام موثوق وتاريخ الاطلاع.
- طلب مراجعة متطوعين بموافقتهم، دون جمع بيانات شخصية غير لازمة.
- قياس عدد المواد المنشورة والمراجعات المكتملة والأخطاء المصححة.
- نشر النتائج الفعلية فقط؛ لا يُسجل مشاركون أو أثر قبل حدوثه.

## الحالة
اقتراح للتنفيذ، وليس نشاطاً منفذاً أو نتيجة مثبتة.
""")
write("milyar/evidence/M-007.md",
      "# M-007 — خدمة المجتمع\n\nتم إعداد اقتراح مدني قابل للقياس. التنفيذ الميداني لم يحدث بعد.\n")
record("M-007", "خطة جاهزة للتجربة",
       "اقتُرحت مبادرة معرفية مدنية؛ لم يُدّع تنفيذها.")

# Consolidated status. No task is automatically declared completed.
report = {
    "project": "قمرا منيرا بإذن ربه — المليار",
    "updated_at_utc": now,
    "tasks": checks,
    "completed_verified": 0,
    "total_tasks": 7,
    "progress_percent": 0,
    "note": "الملفات والفحوص الأولية ليست بديلاً عن مراجعة الأدلة والتحقق المستقل."
}
write("milyar/EXECUTION_REPORT.json",
      json.dumps(report, ensure_ascii=False, indent=2))
summary = [
    "# تقرير التنفيذ الموحد",
    "",
    f"- تاريخ التقرير (UTC): {now}",
    "- المهام: 7",
    "- المهام المكتملة الموثقة: 0",
    "- الإنجاز الموثق: 0%",
    "- السبب: لا تُعد القوالب أو الفحوص الأولية وحدها دليلاً على إكمال المهمة.",
    ""
]
for item in checks:
    summary += [
        f"## {item['task']} — {item['status']}",
        item["detail"], ""
    ]
write("milyar/EXECUTION_REPORT.md", "\n".join(summary))

print("اكتمل إعداد ملفات المهام والفحوص الأولية.")
print("تقرير التنفيذ: milyar/EXECUTION_REPORT.md")
print("الأدلة: milyar/evidence/")
print("الإنجاز الموثق يبقى 0% إلى حين التحقق الفعلي.")
