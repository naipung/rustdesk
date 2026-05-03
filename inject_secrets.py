import sys
import os

# 获取参数
server_addr = sys.argv[1] if len(sys.argv) > 1 else ""
pub_key = sys.argv[2] if len(sys.argv) > 2 else ""

file_path = 'libs/hbb_common/src/config.rs'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            # 1. 强制替换 Rendezvous 服务器地址
            if 'pub const RENDEZVOUS_SERVERS' in line:
                f.write(f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server_addr}"];\n')
            # 2. 强制替换公钥
            elif 'pub const RS_PUB_KEY' in line:
                f.write(f'pub const RS_PUB_KEY: &str = "{pub_key}";\n')
            else:
                f.write(line)
    print(f"成功在云端强制覆盖了子模块配置: {file_path}")
else:
    print(f"错误: 没找到子模块文件 {file_path}")
    sys.exit(1)
