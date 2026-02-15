import json
import requests
import os

# 配置资源列表
# type: 'dns' 存入 rules/dns/, 'route' 存入 rules/route/
sources = {
    # --- DNS 分流 (需要从 .conf 转换) ---
    "alibaba": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/alibaba.conf", "type": "dns"},
    "tencent": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/tencent.conf", "type": "dns"},
    "bilibili": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/bilibili.conf", "type": "dns"},
    "xiaomi": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/xiaomi.conf", "type": "dns"},
    "bytedance": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/bytedance.conf", "type": "dns"},
    "baidu": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/baidu.conf", "type": "dns"},
    "qihoo360": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/qihoo360.conf", "type": "dns"},
    "hostpot_captive_portal": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/hotspot_captive_portal.conf", "type": "dns"},
    "lan_without_real_ip": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/lan_without_real_ip.conf", "type": "dns"},
    "lan_with_realip": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/lan_with_realip.conf", "type": "dns"},    
    # --- 流量分流 (已有 JSON，直接下载) ---
    # 示例：假设这是 Sukka 或其他大佬提供的流量分流 JSON 链接
    "speedtest": {"url": "https://ruleset.skk.moe/sing-box/domainset/speedtest.json", "type": "route"},
    "domainset_cdn": {"url": "https://ruleset.skk.moe/sing-box/domainset/cdn.json", "type": "route"},
    "non_ip_cdn": {"url": "https://ruleset.skk.moe/sing-box/non_ip/cdn.json", "type": "route"},
    "stream_us": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream_us.json", "type": "route"},
    "ip_stream_us": {"url": "https://ruleset.skk.moe/sing-box/ip/stream_us.json", "type": "route"},
    "stream_hk": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream_hk.json", "type": "route"},
    "ip_stream_hk": {"url": "https://ruleset.skk.moe/sing-box/ip/stream_hk.json", "type": "route"},
    "stream_jp": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream_jp.json", "type": "route"},
    "ip_stream_jp": {"url": "https://ruleset.skk.moe/sing-box/ip/stream_jp.json", "type": "route"},
    "stream_tw": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream_tw.json", "type": "route"},
    "ip_stream_tw": {"url": "https://ruleset.skk.moe/sing-box/ip/stream_tw.json", "type": "route"},
    "stream_eu": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream_eu.json", "type": "route"},
    "ip_stream_eu": {"url": "https://ruleset.skk.moe/sing-box/ip/stream_eu.json", "type": "route"},
    "stream": {"url": "https://ruleset.skk.moe/sing-box/non_ip/stream.json", "type": "route"},
    "ip_stream": {"url": "https://ruleset.skk.moe/sing-box/ip/stream.json", "type": "route"},
    "non_ip_ai": {"url": "https://ruleset.skk.moe/sing-box/non_ip/ai.json", "type": "route"},
    "apple_intelligence": {"url": "https://ruleset.skk.moe/sing-box/non_ip/apple_intelligence.json", "type": "route"},
    "telegram": {"url": "https://ruleset.skk.moe/sing-box/non_ip/telegram.json", "type": "route"},
    "ip_telegram": {"url": "https://ruleset.skk.moe/sing-box/ip/telegram.json", "type": "route"},
    "cn_apple_cdn": {"url": "https://ruleset.skk.moe/sing-box/domainset/apple_cdn.json", "type": "route"},
    "apple_cn": {"url": "https://ruleset.skk.moe/sing-box/non_ip/apple_cn.json", "type": "route"},
    "apple_services": {"url": "https://ruleset.skk.moe/sing-box/non_ip/apple_services.json", "type": "route"},
    "github": {"url": "https://ruleset.skk.moe/sing-box/non_ip/my_git.json", "type": "route"},
    "microsoft_cdn": {"url": "https://ruleset.skk.moe/sing-box/non_ip/microsoft_cdn.json", "type": "route"},
    "microsoft": {"url": "https://ruleset.skk.moe/sing-box/non_ip/microsoft.json", "type": "route"},
    "domainset_download": {"url": "https://ruleset.skk.moe/sing-box/domainset/download.json", "type": "route"},
    "download": {"url": "https://ruleset.skk.moe/sing-box/non_ip/download.json", "type": "route"},
    "lan": {"url": "https://ruleset.skk.moe/sing-box/non_ip/lan.json", "type": "route"},
    "ip_lan": {"url": "https://ruleset.skk.moe/sing-box/ip/lan.json", "type": "route"},
    "domestic": {"url": "https://ruleset.skk.moe/sing-box/non_ip/domestic.json", "type": "route"},
    "non_ip_direct": {"url": "https://ruleset.skk.moe/sing-box/non_ip/direct.json", "type": "route"},
    "non_ip_global": {"url": "https://ruleset.skk.moe/sing-box/non_ip/global.json", "type": "route"},
    "ip_domestic": {"url": "https://ruleset.skk.moe/sing-box/ip/domestic.json", "type": "route"},
    "china_ip": {"url": "https://ruleset.skk.moe/sing-box/ip/china_ip.json", "type": "route"}
}


def process_source(name, info):
    url = info["url"]
    folder = f"rules/{info['type']}"
    os.makedirs(folder, exist_ok=True)
    
    print(f"Processing {name} from {url}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # 判断是直接下载 JSON 还是 转换 .conf
        if url.endswith('.json'):
            content = response.json() # 直接作为 JSON 处理
        else:
            # 执行转换逻辑
            lines = response.text.splitlines()
            domain, domain_suffix, ip_cidr = [], [], []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split(',')
                if len(parts) < 2: continue
                tag, value = parts[0].strip(), parts[1].strip()
                if tag == 'DOMAIN': domain.append(value)
                elif tag == 'DOMAIN-SUFFIX': domain_suffix.append(value)
                elif tag in ['IP-CIDR', 'IP-CIDR6']: ip_cidr.append(value)
            content = {"version": 1, "rules": [{"domain": domain, "domain_suffix": domain_suffix, "ip_cidr": ip_cidr}]}
        
        # 保存到对应文件夹
        with open(f"{folder}/{name}.json", 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Failed to process {name}: {e}")

if __name__ == "__main__":
    for name, info in sources.items():
        process_source(name, info)
