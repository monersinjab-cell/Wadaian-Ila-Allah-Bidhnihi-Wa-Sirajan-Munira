import re
from pathlib import Path

def run_security_shield():
    root = Path.cwd()
    patterns = {
        "Private Key": re.compile(r"-----BEGIN .*PRIVATE KEY-----"),
        "GitHub Token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")
    }
    findings = []
    for p in root.rglob("*.py"):
        if ("venv" in p.parts or ".git" in p.parts or "army_agents" in p.parts or "tests" in p.parts or p.name.startswith("test_")):
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                # تجاهل تعريف قاعدة الكشف البرمجية نفسها فقط.
                if (p.name == "milyar_execute_all.py"
                    and "re.compile(" in line and "PRIVATE KEY" in line):
                    continue
                for label, pattern in patterns.items():
                    if pattern.search(line):
                        findings.append(f"{p.name} (السطر {i}): {label}")
        except:
            continue
    if not findings:
        return "✅ نجاح: لم يتم العثور على أي مفاتيح سرية أو توكنز مكشوفة في الأكواد."
    return f"⚠ مراجعة مطلوبة: تم رصد مؤشرات أسرار مكشوفة في: {findings}"

if __name__ == '__main__':
    print(run_security_shield())
