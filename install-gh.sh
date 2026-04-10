#!/bin/bash

echo "🚀 正在安装 GitHub CLI..."
echo "⚠️  需要输入一次密码（你电脑的登录密码）"
echo ""

# 下载
echo "📥 下载中..."
curl -L https://github.com/cli/cli/releases/download/v2.57.0/gh_2.57.0_macOS_arm64.tar.gz -o /tmp/gh.tar.gz

# 检查下载
if [ ! -s /tmp/gh.tar.gz ]; then
    echo "❌ 下载失败，请检查网络连接"
    exit 1
fi

# 解压并安装到系统目录（需要 sudo）
echo "📦 安装中（需要输入密码）..."
echo "请输入你的 macOS 登录密码："

# 解压
tar -xzf /tmp/gh.tar.gz -C /tmp/

# 复制到 /usr/local/bin（需要 sudo）
sudo cp /tmp/gh_2.57.0_macOS_arm64/bin/gh /usr/local/bin/
sudo chmod +x /usr/local/bin/gh

# 清理
rm -rf /tmp/gh_2.57.0_macOS_arm64 /tmp/gh.tar.gz

echo ""
echo "✅ GitHub CLI 安装完成！"
echo "验证安装："
gh --version
echo ""
echo "下一步：登录 GitHub"
echo "运行: gh auth login"
