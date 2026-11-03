# -*- coding: utf-8 -*-
"""تدقيق إقلاع واضح؛ لا يمنح ضماناً مطلقاً للأمان."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from milyar.army_agents.agent_integrity import verify_seed_integrity
from milyar.army_agents.agent_syntax import run_syntax_patrol
from milyar.army_agents.agent_security import run_security_shield


def classify_result(message):
    text = str(message)
    lower = text.lower()

    if any(word in text for word in ("خطأ", "فشل", "غير صالح", "مفقودة")):
        return "FAIL", text

    if any(word in text for word in ("تحذير", "مراجعة مطلوبة", "لم يتمكن", "غير مكتمل")):
        return "WARNING", text

    if any(word in text for word in ("نجاح", "سليم", "خالية من أخطاء")):
        return "PASS", text

    return "INCOMPLETE", text


def execute_boot_audit():
    checks = (
        ("سلامة بصمة المرجع", verify_seed_integrity),
        ("الصياغة البرمجية", run_syntax_patrol),
        ("مؤشرات الأسرار", run_security_shield),
    )

    print("=== تدقيق إقلاع منظومة وداعيا إلى الله بإذنه. وسراجا منيرا ===")
    results = []

    for name, check in checks:
        try:
            status, detail = classify_result(check())
        except Exception as exc:
            status = "INCOMPLETE"
            detail = f"{type(exc).__name__}: تعذر إكمال الفحص"

        results.append(status)
        print(f"[{status}] {name}: {detail}")

    print("=== ملخص التدقيق ===")
    for status in ("PASS", "WARNING", "FAIL", "INCOMPLETE"):
        print(f"{status}: {results.count(status)}")

    if "FAIL" in results:
        print("القرار: فشل فحص واحد على الأقل؛ يلزم إيقاف الاعتماد.")
        return 1
    if "WARNING" in results or "INCOMPLETE" in results:
        print("القرار: توجد نتائج تحتاج مراجعة؛ لا يُعلن اكتمال التدقيق.")
        return 2

    print("القرار: اجتازت الفحوص المحددة فقط؛ هذا ليس ضماناً مطلقاً للأمان.")
    return 0


if __name__ == "__main__":
    raise SystemExit(execute_boot_audit())
