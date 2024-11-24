with open('data_entity.json', 'r', encoding='utf-8') as f:  ##change
   pass
import os

# 获取当前脚本文件所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "data_entity.json")
print("Resolved Path:", filepath)