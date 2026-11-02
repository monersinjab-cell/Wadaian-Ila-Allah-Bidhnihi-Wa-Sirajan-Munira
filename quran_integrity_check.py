#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""فحص بصمة ملف مرجعي مع توثيق المعايير البنيوية دون تعديل النص القرآني."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REFERENCE = Path("quran/quran.txt")
DEFAULT_MANIFEST = Path("quran/quran_integrity_manifest.json")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_reference(path):
    # قراءة UTF-8 صارمة؛ دون تغيير التشكيل أو المسافات أو الأسطر.
    return path.read_bytes().decode("utf-8", errors="strict")


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="فحص سلامة الملف المرجعي دون تعديل محتواه مع توثيق معايير الأسطر والكلمات والحروف."
    )
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--create-baseline", action="store_true",
        help="إنشاء بصمة أولية بعد مراجعة مصدر الملف."
    )
    args = parser.parse_args()

    try:
        ref = args.reference
        manifest_path = args.manifest

        if not ref.is_file():
            raise FileNotFoundError(f"ملف المرجع غير موجود: {ref}")

        content = read_reference(ref)
        digest = sha256(ref)
        
        # حساب المعايير البنيوية الثانوية بدقة
        lines = content.splitlines()
        line_count = len(lines)
        word_count = len(content.split())
        char_count = len(content)

        if args.create_baseline:
            if manifest_path.exists():
                raise FileExistsError(
                    f"البصمة موجودة مسبقًا ولن تُستبدل: {manifest_path}"
                )

            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "schema_version": 2,
                "purpose": "byte_and_structural_integrity",
                "reference_file": str(ref),
                "encoding": "UTF-8",
                "byte_length": ref.stat().st_size,
                "metrics": {
                    "line_count": line_count,
                    "word_count": word_count,
                    "character_count": char_count
                },
                "sha256": digest,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "warning": (
                    "البصمة لا تثبت أصالة المصدر أو صحة النص من الناحية التفسيرية. "
                    "راجع المصدر قبل اعتماد خط الأساس."
                )
            }

            with manifest_path.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(data, stream, ensure_ascii=False, indent=2)
                stream.write("\n")

            output({
                "status": "BASELINE_CREATED",
                "sha256": digest,
                "metrics": data["metrics"],
                "manifest": str(manifest_path),
                "reference_modified": False
            })
            return 0

        if not manifest_path.is_file():
            output({
                "status": "NO_BASELINE",
                "message": "لم يُنشأ خط أساس. استخدم --create-baseline عند الموافقة على المصدر.",
                "reference_modified": False
            })
            return 3

        baseline = json.loads(read_reference(manifest_path))
        expected = baseline.get("sha256", "")

        if (baseline.get("schema_version") != 2
                or not isinstance(expected, str)
                or len(expected) != 64
                or any(c not in "0123456789abcdef" for c in expected)):
            raise ValueError("ملف البصمة غير صالح أو يتبع إصداراً قديماً.")

        matched = digest == expected
        
        # فحص إضافي للمطابقة البنيوية
        metrics_match = True
        if "metrics" in baseline:
            m = baseline["metrics"]
            if (m.get("line_count") != line_count or 
                m.get("word_count") != word_count or 
                m.get("character_count") != char_count):
                metrics_match = False

        final_match = matched and metrics_match

        output({
            "status": "MATCH" if final_match else "MISMATCH",
            "sha256_match": matched,
            "metrics_match": metrics_match,
            "expected_sha256": expected,
            "actual_sha256": digest,
            "current_metrics": {
                "line_count": line_count,
                "word_count": word_count,
                "character_count": char_count
            },
            "reference_modified": False,
            "message_ar": "تطابقت البصمة والمعايير البنيوية تماماً." if final_match else "فشل التحقق؛ هناك اختلاف في البصمة أو بنية النص."
        })
        return 0 if final_match else 2

    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        output({
            "status": "ERROR",
            "error_type": type(exc).__name__,
            "message": str(exc)
        })
        return 1


if __name__ == "__main__":
    sys.exit(main())
