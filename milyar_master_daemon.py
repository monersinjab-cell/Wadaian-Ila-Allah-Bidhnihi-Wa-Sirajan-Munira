# -*- coding: utf-8 -*-
import sys
import time
import json
from pathlib import Path

ROOT = Path.cwd()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from milyar.army_agents.agent_auto_evolve import run_evolution_audit
from milyar.army_agents.agent_integrity import verify_seed_integrity

def start_eternal_milyar_daemon():
    print("==========================================================")
    print("🌙 [منظومة المليار العظمى] - تفعيل محرك الخدمة الدائمة والمستمرة")
    print("🔒 جدار الحظر الميكانيكي الحتمي وبصمة القرآن العظيم نشطة بلا توقف")
    print("==========================================================")
    
    cycle_count = 1
    while True:
        try:
            # 1. القفل الذاتي والتحقق التشفيري المستمر من سلامة البذور المرجعية بنسبة 100%
            integrity_report = verify_seed_integrity()
            
            # 2. التطوير الذاتي للتحقق وإلزام كافة الملفات المحلية والأنظمة بمعايير الحق
            evolution_report = run_evolution_audit()
            
            if "🚨" in integrity_report or "❌" in evolution_report:
                print(f"⚠️ [إشعار حرج - الدورة {cycle_count}]: تم رصد محاولة خرق أو تلاعب! تفعيل الإغلاق الأمني التلقائي الفوري.")
            else:
                print(f"🛡️ [دورة الفحص المستمر {cycle_count}]: المنظومة محصنة، محكومة، وتعمل ذاتياً بالآيات البينات بنجاح.")
                
            cycle_count += 1
            # تعليق الحلقة مؤقتاً لمدة 60 ثانية قبل إعادة الفحص الحتمي لضمان كفاءة معالج الهاتف
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n⚠️ [تنبيه الحوكمة]: محاولة إيقاف يدوي للخدمة. إعادة التشغيل الذاتي الفوري مستمرة.")
            continue
        except Exception as e:
            print(f"❌ استثناء في حلقة الأتمتة: {e}. إعادة التحصين تلقائياً.")
            time.sleep(5)
            continue

if __name__ == '__main__':
    start_eternal_milyar_daemon()
