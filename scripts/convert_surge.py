import json
import requests
import os

# 配置资源列表
# type: 'dns' 存入 rules/dns/, 'route' 存入 rules/route/
sources = {
    # --- DNS 分流 (直接下载) ---
    "dns/alibaba": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/alibaba.conf", "type": "dns"},
    "dns/tencent": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/tencent.conf", "type": "dns"},
    "dns/bilibili": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/bilibili.conf", "type": "dns"},
    "dns/xiaomi": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/xiaomi.conf", "type": "dns"},
    "dns/bytedance": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/bytedance.conf", "type": "dns"},
    "dns/baidu": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/baidu.conf", "type": "dns"},
    "dns/qihoo360": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/qihoo360.conf", "type": "dns"},
    "dns/hostpot_captive_portal": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/hotspot_captive_portal.conf", "type": "dns"},
    "dns/lan_without_real_ip": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/lan_without_real_ip.conf", "type": "dns"},
    "dns/lan_with_realip": {"url": "https://ruleset.skk.moe/Modules/Rules/sukka_local_dns_mapping/lan_with_realip.conf", "type": "dns"},    
    # --- 流量分流 (直接下载) ---
    "domainset/speedtest": {"url": "https://ruleset.skk.moe/List/domainset/speedtest.conf", "type": "domainset"},
    "domainset/cdn": {"url": "https://ruleset.skk.moe/List/domainset/cdn.conf", "type": "domainset"},
    "non_ip/cdn": {"url": "https://ruleset.skk.moe/List/non_ip/cdn.conf", "type": "non_ip"},
    "non_ip/stream_us": {"url": "https://ruleset.skk.moe/List/non_ip/stream_us.conf", "type": "non_ip"},
    "ip/stream_us": {"url": "https://ruleset.skk.moe/List/ip/stream_us.conf", "type": "ip"},
    "non_ip/stream_hk": {"url": "https://ruleset.skk.moe/List/non_ip/stream_hk.conf", "type": "non_ip"},
    "ip/stream_hk": {"url": "https://ruleset.skk.moe/List/ip/stream_hk.conf", "type": "ip"},
    "non_ip/stream_jp": {"url": "https://ruleset.skk.moe/List/non_ip/stream_jp.conf", "type": "non_ip"},
    "ip/stream_jp": {"url": "https://ruleset.skk.moe/List/ip/stream_jp.conf", "type": "ip"},
    "/non_ip/stream_tw": {"url": "https://ruleset.skk.moe/List/non_ip/stream_tw.conf", "type": "non_ip"},
    "ip/stream_tw": {"url": "https://ruleset.skk.moe/List/ip/stream_tw.conf", "type": "ip"},
    "non_ip/stream_eu": {"url": "https://ruleset.skk.moe/List/non_ip/stream_eu.conf", "type": "non_ip"},
    "ip/stream_eu": {"url": "https://ruleset.skk.moe/List/ip/stream_eu.conf", "type": "ip"},
    "non_ip/stream": {"url": "https://ruleset.skk.moe/List/non_ip/stream.conf", "type": "non_ip"},
    "ip/stream": {"url": "https://ruleset.skk.moe/List/ip/stream.conf", "type": "ip"},
    "non_ip/ai": {"url": "https://ruleset.skk.moe/List/non_ip/ai.conf", "type": "non_ip"},
    "non_ip/apple_intelligence": {"url": "https://ruleset.skk.moe/List/non_ip/apple_intelligence.conf", "type": "non_ip"},
    "non_ip/telegram": {"url": "https://ruleset.skk.moe/List/non_ip/telegram.conf", "type": "non_ip"},
    "ip/telegram": {"url": "https://ruleset.skk.moe/List/ip/telegram.conf", "type": "ip"},
    "domainset/apple_cdn": {"url": "https://ruleset.skk.moe/List/domainset/apple_cdn.conf", "type": "domainset"},
    "non_ip/apple_cn": {"url": "https://ruleset.skk.moe/List/non_ip/apple_cn.conf", "type": "non_ip"},
    "non_ip/apple_services": {"url": "https://ruleset.skk.moe/List/non_ip/apple_services.conf", "type": "non_ip"},
    "non_ip/my_git": {"url": "https://ruleset.skk.moe/List/non_ip/my_git.conf", "type": "non_ip"},
    "non_ip/microsoft_cdn": {"url": "https://ruleset.skk.moe/List/non_ip/microsoft_cdn.conf", "type": "non_ip"},
    "non_ip/microsoft": {"url": "https://ruleset.skk.moe/List/non_ip/microsoft.conf", "type": "non_ip"},
    "domainset/download": {"url": "https://ruleset.skk.moe/List/domainset/download.conf", "type": "domainset"},
    "non_ip/download": {"url": "https://ruleset.skk.moe/List/non_ip/download.conf", "type": "non_ip"},
    "non_ip/lan": {"url": "https://ruleset.skk.moe/List/non_ip/lan.conf", "type": "non_ip"},
    "ip/lan": {"url": "https://ruleset.skk.moe/List/ip/lan.conf", "type": "ip"},
    "non_ip/domestic": {"url": "https://ruleset.skk.moe/List/non_ip/domestic.conf", "type": "non_ip"},
    "non_ip/direct": {"url": "https://ruleset.skk.moe/List/non_ip/direct.conf", "type": "non_ip"},
    "non_ip/global": {"url": "https://ruleset.skk.moe/List/non_ip/global.conf", "type": "non_ip"},
    "ip/domestic": {"url": "https://ruleset.skk.moe/List/ip/domestic.conf", "type": "ip"},
    "ip/china_ip": {"url": "https://ruleset.skk.moe/List/ip/china_ip.conf", "type": "ip"},
    "geosite/steam@cn": {"url": "https://surge.bojin.co/geosite/balanced/steam@cn", "type": "geosite"},
    "geosite/game_download": {"url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Game/GameDownload/GameDownload.list", "type": "geosite"},
    "geosite/category-games@cn": {"url": "https://surge.bojin.co/geosite/balanced/category-games@cn", "type": "geosite"},
    "geosite/category-games": {"url": "https://surge.bojin.co/geosite/balanced/category-games", "type": "geosite"},
    "geosite/geolocation-cn": {"url": "https://surge.bojin.co/geosite/balanced/geolocation-cn", "type": "geosite"},
    "geosite/geolocation-!cn": {"url": "https://surge.bojin.co/geosite/balanced/geolocation-!cn", "type": "geosite"},
    "geosite/gfw": {"url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/ruleset/gfw.txt", "type": "geosite"},
}

def process_source(name, info):
    url = info["url"]
    folder = f"surge/{info['type']}"
    os.makedirs(folder, exist_ok=True)
    
    # 自动获取后缀名 (.conf 或 .json)
    ext = '.conf'
    save_path = f"surge/{name}{ext}"

    print(f"Processing {name} from {url}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # 不再进行解析和转换，直接保存原始文本/二进制内容
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
    except Exception as e:
        print(f"Failed to process surge/{name}: {e}")

if __name__ == "__main__":
    for name, info in sources.items():
        process_source(name, info)
