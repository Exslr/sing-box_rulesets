import json
import sys
import os

def convert(src_path, dest_path):
    if not os.path.exists(src_path):
        print(f"Error: Source {src_path} not found")
        sys.exit(1)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # 判定策略
    policy = "PROXY" if "through_proxy" in src_path else "DIRECT"

    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 兼容嵌套和扁平结构
        rules_data = data.get("rules", [data])[0]
        
        output = [
            f"# Surge Rule-Set: {os.path.basename(dest_path)}",
            f"# Generated from {os.path.basename(src_path)}",
            f"# Policy: {policy}\n"
        ]

        # 1. Surge Rule-Set 支持的标准字段
        mapping = {
            "domain": "DOMAIN",
            "domain_suffix": "DOMAIN-SUFFIX",
            "domain_keyword": "DOMAIN-KEYWORD",
            "ip_cidr": "IP-CIDR"
        }

        for sb_key, surge_type in mapping.items():
            for item in rules_data.get(sb_key, []):
                if sb_key == "ip_cidr":
                    output.append(f"{surge_type},{item},{policy},no-resolve")
                else:
                    output.append(f"{surge_type},{item},{policy}")

        # 2. 处理 Surge Rule-Set 不支持的字段 (Regex & Process)
        unsupported_mapping = {
            "domain_regex": "REGEX",
            "process_name": "PROCESS-NAME",
            "process_path": "PROCESS-PATH"
        }

        has_unsupported = False
        for sb_key, label in unsupported_mapping.items():
            items = rules_data.get(sb_key, [])
            if items:
                if not has_unsupported:
                    output.append(f"\n# --- Unsupported Rules in Surge Rule-Set (Commented Out) ---")
                    has_unsupported = True
                for item in items:
                    output.append(f"# {label}: {item} (Move to Main Profile if needed)")

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(output))
        
        print(f"Success: {src_path} -> {dest_path}")

    except Exception as e:
        print(f"Failed to convert {src_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        convert(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 convert_to_surge.py <input_json> <output_conf>")
