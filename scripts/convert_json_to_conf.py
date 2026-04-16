import json
import os
import sys

# 任务配置表
TASKS_MAP = {
    'rules/route/skip_proxy.json': 'skip_proxy',
    'rules/route/always_direct.json': 'always_direct',
    'rules/route/through_proxy.json': 'through_proxy',
    'rules/route/steam@cn.json': 'steam@cn',
}

def convert(json_rel_path, conf_name):
    source = f'main_files/{json_rel_path}'
    target = f'surge_files/custom/{conf_name}.conf'
    
    if not os.path.exists(source):
        print(f"--- 跳过: {json_rel_path} (源文件不存在) ---")
        return

    print(f">>> 正在转换: {json_rel_path} -> {conf_name}.conf")
    
    with open(source, 'r', encoding='utf-8') as f:
        data = json.load(f)

    surge_rules = []
    mapping = {'domain': 'DOMAIN', 'domain_suffix': 'DOMAIN-SUFFIX', 'domain_keyword': 'DOMAIN-KEYWORD', 'ip_cidr': 'IP-CIDR'}

    for rule_obj in data.get('rules', []):
        for sb_key, surge_key in mapping.items():
            if sb_key in rule_obj:
                for val in rule_obj[sb_key]:
                    # 转换 domain_suffix: .google.com -> google.com
                    if sb_key == 'domain_suffix' and val.startswith('.'):
                        val = val[1:]
                    surge_rules.append(f"{surge_key},{val}")

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(f"# Surge Rule-Set: {conf_name}\n\n")
        f.write("\n".join(surge_rules))

if __name__ == "__main__":
    # 获取参数列表
    changed_files = sys.argv[1:]
    
    # 【核心逻辑修改】
    if not changed_files:
        # 如果没有任何参数（手动触发或列表为空），处理所有任务
        print("提示: 未检测到特定变动文件，启动全量转换模式...")
        for json_path, conf_name in TASKS_MAP.items():
            convert(json_path, conf_name)
    else:
        # 如果有名单，则只处理名单内的文件
        print(f"提示: 检测到变动名单，启动定向转换模式...")
        for file_path in changed_files:
            if file_path in TASKS_MAP:
                convert(file_path, TASKS_MAP[file_path])
            else:
                print(f"--- 忽略无关文件: {file_path} ---")
