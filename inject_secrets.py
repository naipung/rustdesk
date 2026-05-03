import sys
import os

# 从命令行获取 GitHub Secrets 传进来的值
server_addr = sys.argv[1] if len(sys.argv) > 1 else ""
pub_key = sys.argv[2] if len(sys.argv) > 2 else ""

# 子模块配置文件的相对路径
file_path = 'libs/hbb_common/src/config.rs'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录替换前的状态用于统计
    old_content = content
    
    # 1. 替换所有 Rendezvous 服务器地址 (支持 11 处或更多)
    import re
    # 正则匹配 pub const RENDEZVOUS_SERVERS...; 结构
    content = re.sub(
        r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[.*?\];', 
        f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server_addr}"];', 
        content
    )
    
    # 2. 替换所有公钥
    content = re.sub(
        r'pub const RS_PUB_KEY: &str = ".*?";', 
        f'pub const RS_PUB_KEY: &str = "{pub_key}";', 
        content
    )

    # 写入修改
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 统计大概替换了多少行（简单通过内容差异判断）
    print(f"✅ 成功：已在地毯式扫描中更新了子模块配置！")
    print(f"目标文件: {file_path}")
else:
    print(f"❌ 错误: 没找到子模块文件 {file_path}。请确保 checkout 时开启了 submodules。")
    sys.exit(1)
