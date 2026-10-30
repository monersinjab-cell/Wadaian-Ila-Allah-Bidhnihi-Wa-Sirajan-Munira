import sys
from pathlib import Path

def run_syntax_patrol():
    root = Path.cwd()
    py_files = [p for p in root.rglob("*.py") if "venv" not in p.parts and ".git" not in p.parts]
    bad_files = []
    for p in py_files:
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except Exception as e:
            bad_files.append(f"{p.name}: {type(e).__name__}")
    
    if not bad_files:
        return f"✅ نجاح: تم فحص {len(py_files)} ملف بايثون، وجميعها خالية من أخطاء الصياغة."
    return f"❌ خطأ: تم العثور على أخطاء صياغة في الملفات التالية: {bad_files}"

if __name__ == '__main__':
    print(run_syntax_patrol())
