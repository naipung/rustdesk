import sys
import os
import re

def inject():
    # 从命令行获取 GitHub Secrets 传进来的值
    server_addr = sys.argv[1] if len(sys.argv) > 1 else ""
    pub_key = sys.argv[2] if len(sys.argv) > 2 else ""

    # 参数检查
    if not server_addr or not pub_key:
        print("❌ 错误: 缺失服务器地址或公钥参数")
        sys.exit(1)

    # 子模块配置文件的相对路径
    file_path = 'libs/hbb_common/src/config.rs'

    if not os.path.exists(file_path):
        print(f"❌ 错误: 没找到子模块文件 {file_path}")
        print("💡 请确保 checkout 时开启了 submodules: recursive")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 统计替换次数
        count_addr = 0
        count_key = 0

        # 1. 替换所有 Rendezvous 服务器地址（使用 re.subn 获取次数）
        content, count_addr = re.subn(
            r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
            f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server_addr}"];',
            content
        )

        # 2. 替换所有公钥
        content, count_key = re.subn(
            r'pub const RS_PUB_KEY: &str = "[^"]*";',
            f'pub const RS_PUB_KEY: &str = "{pub_key}";',
            content
        )

        # 检查是否替换成功
        if count_addr == 0:
            print("⚠️ 警告: 未找到 RENDEZVOUS_SERVERS 配置")
        if count_key == 0:
            print("⚠️ 警告: 未找到 RS_PUB_KEY 配置")

        # 写入修改
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 配置注入成功！")
        print(f"📍 服务器地址已更新: {count_addr} 处")
        print(f"🔑 公钥已更新: {count_key} 处")
        print(f"📁 文件: {file_path}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inject()