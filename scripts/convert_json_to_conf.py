import json
import os
import sys

# 任务配置
TASKS_MAP = {
    'rules/route/skip_proxy.json': 'skip_proxy',
    'rules/route/always_direct.json': 'always_direct',
    'rules/route/through_proxy.json': 'through_proxy'
}

def convert(json_rel_path, conf_name):
    # 路径解析：
    # source 指向检出的 main 副本
    # target 指向检出的 surge 副本下的 custom 目录
    source = f'main_files/{json_rel_path}'
    target = f'surge_files/custom/{conf_name}.conf'
    
    if not os.path.exists(source):
        print(f"跳过: {json_rel_path} 不存在")
        return

    print(f"正在精准转换: {json_rel_path}")
    
    with open(source, 'r', encoding='utf-8') as f:
        data = json.load(f)

    surge_rules = []
    # 提取规则逻辑
    for rule_obj in data.get('rules', []):
        for sb_key, surge_key in {
            'domain': 'DOMAIN', 
            'domain_suffix': 'DOMAIN-SUFFIX', 
            'domain_keyword': 'DOMAIN-KEYWORD', 
            'ip_cidr': 'IP-CIDR'
        }.items():
            if sb_key in rule_obj:
                for val in rule_obj[sb_key]:
                    if sb_key == 'domain_suffix' and val.startswith('.'):
                        val = val[1:]
                    surge_rules.append(f"{surge_key},{val}")

    # 核心：这里是在操作 surge_files/custom/ 目录
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(f"# Surge Rule-Set: {conf_name}\n\n")
        f.write("\n".join(surge_rules))

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    # 如果没传参数（手动运行），则检查所有任务
    files_to_process = changed_files if changed_files else TASKS_MAP.keys()
    
    for file_path in files_to_process:
        if file_path in TASKS_MAP:
            convert(file_path, TASKS_MAP[file_path])
