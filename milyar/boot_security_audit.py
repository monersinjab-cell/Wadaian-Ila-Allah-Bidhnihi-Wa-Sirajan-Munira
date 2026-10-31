# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from milyar.army_agents.agent_integrity import verify_seed_integrity
from milyar.army_agents.agent_syntax import run_syntax_patrol
from milyar.army_agents.agent_security import run_security_shield

def execute_boot_audit():
    print("=== 🔐 بدء التدقيق الأمني التلقائي وإقلاع المنظومة ===")
    print(verify_seed_integrity())
    print(run_syntax_patrol())
    print(run_security_shield())
    print("=== 🎉 انتهى فحص الإقلاع، والمنظومة آمنة ومحكومة بالحق ===")

if __name__ == '__main__':
    execute_boot_audit()
