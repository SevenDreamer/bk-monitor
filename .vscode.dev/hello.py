import os
import shutil
import sys
from pathlib import Path

import django
from dotenv import load_dotenv

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent.parent.parent
BKMONITOR_DIR = BASE_DIR / "bkmonitor"

print(f"BASE_DIR \t:{BASE_DIR}")
print(f"BKMONITOR_DIR\t:{BKMONITOR_DIR}")

# 添加 bk-monitor 到 sys.path
# sys.path.insert(0,str(BKMONITOR_DIR))


# 添加 bk-monitor/bkmoniotr 到 sys.path
sys.path.insert(0, str(BKMONITOR_DIR))

# 添加 bk-monitor/bkmonitor/packages 到 sys.path
sys.path.insert(0, str(BKMONITOR_DIR / "packages"))


def fix_ai_agent():
    """
    添加对 ai_agent 引用报错的防御性修复
    先删除 /bkmonitor/ai_agent
    通过将 /ai_agent 复制到 /bkmonitor/ai_agent 来解决
    """
    # 先判断 /bkmonitor/ai_agent 是否存在, 如果存在则删除
    ai_agent_path = BKMONITOR_DIR / "ai_agent"
    if ai_agent_path.exists():
        shutil.rmtree(ai_agent_path)

    os.system(f"cp -r {BASE_DIR/ 'ai_agent' } {ai_agent_path}")

def setup_django():
    """
    启动 django 服务

    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    load_dotenv(str(BASE_DIR / ".env"))

    django.setup()


'''
使用方法
请把我放在这里 .venv/share/jupyter/hello.py

from hello import fix_ai_agent, setup_django
fix_ai_agent()
setup_django()
'''
