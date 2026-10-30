import json
from pathlib import Path
from datetime import datetime, timezone

root = Path.cwd()
data_file = root / "milyar/tasks.json"
index_file = root / "index.html"

if not data_file.exists() or not index_file.exists():
    raise SystemExit("توقف: ملف tasks.json أو index.html غير موجود.")

data = json.loads(data_file.read_text(encoding="utf-8"))
tasks = data if isinstance(data, list) else data.get("tasks", [])

if not tasks:
    raise SystemExit("توقف: لم أجد قائمة المهام.")

def field(task, *names):
    for name in names:
        if name in task:
            return task[name]
    return ""

def evidence_exists(value):
    if isinstance(value, dict):
        value = value.get("url") or value.get("path") or value.get("description") or ""
    if isinstance(value, list):
        return any(evidence_exists(x) for x in value)
    return str(value).strip().lower() not in {
        "", "لم يرفق بعد", "لم يُرفق بعد", "لا يوجد", "none", "null"
    }

rows = []
for task in tasks:
    if not isinstance(task, dict):
        continue
    status = str(field(task, "status", "state", "الحالة") or "بانتظار التنفيذ")
    evidence = field(task, "evidence", "proof", "الدليل", "evidence_url")
    complete = ("مكتمل" in status or "complete" in status.lower()) and evidence_exists(evidence)
    rows.append({
        "id": str(field(task, "id", "task_id", "code") or "غير محدد"),
        "title": str(field(task, "title", "name", "المهمة") or "مهمة"),
        "status": "مكتملة موثقة" if complete else status,
        "evidence_provided": evidence_exists(evidence),
        "counted_complete": complete
    })

if not rows:
    raise SystemExit("توقف: لا توجد مهام قابلة للقراءة.")

done = sum(r["counted_complete"] for r in rows)
total = len(rows)
percent = round(done * 100 / total, 1)

result = {
    "project": "قمرا منيرا بإذن ربه — المليار",
    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    "completed_verified": done,
    "total_tasks": total,
    "progress_percent": percent,
    "tasks": rows,
    "rule": "لا تحتسب المهمة مكتملة إلا إذا وُجد دليل وحالة مكتملة."
}
Path("milyar/progress.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

lines = [
    "# لوحة تقدم المليار", "",
    f"- الإنجاز الموثق: **{done} من {total} ({percent}%)**", "",
    "| المعرف | المهمة | الحالة | الدليل مرفق |",
    "|---|---|---|---|"
]
for r in rows:
    lines.append(
        f"| {r['id']} | {r['title'].replace('|', '/')} | "
        f"{r['status'].replace('|', '/')} | "
        f"{'نعم' if r['evidence_provided'] else 'لا'} |"
    )
Path("milyar/PROGRESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

start = "<!-- MILYAR_PROGRESS_START -->"
end = "<!-- MILYAR_PROGRESS_END -->"
section = f"""{start}
<section id="milyar-progress" dir="rtl" style="margin:24px auto;padding:20px;max-width:900px;border:1px solid #b99a52;border-radius:14px">
<h2>لوحة تقدم المليار</h2>
<p>المهام المكتملة الموثقة: <strong>{done} / {total}</strong></p>
<p>نسبة الإنجاز الموثق: <strong>{percent}%</strong></p>
<progress value="{done}" max="{total}" style="width:100%;height:18px"></progress>
<p>لا تُحتسب المهمة مكتملة إلا بوجود دليل قابل للتحقق.</p>
<p><a href="milyar/PROGRESS.md">سجل التقدم</a> · <a href="milyar/progress.json">بيانات التقدم</a> · <a href="milyar/TASK_BOARD.md">سجل المهام</a></p>
</section>
{end}"""

html = index_file.read_text(encoding="utf-8")
if start in html and end in html:
    a = html.index(start)
    b = html.index(end, a) + len(end)
    html = html[:a] + section + html[b:]
else:
    pos = html.lower().rfind("</body>")
    if pos >= 0:
        html = html[:pos] + "\n" + section + "\n" + html[pos:]
    else:
        html += "\n" + section + "\n"

index_file.write_text(html, encoding="utf-8")
print(f"نجح الإنشاء محليًا: {done}/{total} — {percent}%")
