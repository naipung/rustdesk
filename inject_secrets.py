#!/usr/bin/env python3
import sys
import re
import os

def main():
    server = sys.argv[1] if len(sys.argv) > 1 else ""
    key = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if not server or not key:
        print("❌ 缺少参数")
        sys.exit(1)
    
    path = "libs/hbb_common/src/config.rs"
    
    if not os.path.exists(path):
        print(f"❌ 找不到 {path}")
        sys.exit(1)
    
    with open(path, 'r') as f:
        content = f.read()
    
    content = re.sub(
        r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[.*?\];',
        f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server}"];',
        content
    )
    content = re.sub(
        r'pub const RS_PUB_KEY: &str = ".*?";',
        f'pub const RS_PUB_KEY: &str = "{key}";',
        content
    )
    
    with open(path, 'w') as f:
        f.write(content)
    
    print(f"✅ 配置注入成功: {server}")

if __name__ == "__main__":
    main()