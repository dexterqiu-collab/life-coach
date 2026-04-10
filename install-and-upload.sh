#!/bin/bash

# Life Coach Skill - GitHub 上传脚本
# 使用方法：./install-and-upload.sh

set -e

echo "🚀 Life Coach Skill - GitHub 上传工具"
echo "======================================"
echo ""

# 1. 检查是否已安装 gh
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI 已安装"
else
    echo "📦 正在安装 GitHub CLI..."

    # 下载并解压到用户目录（不需要 sudo）
    if [ ! -f /tmp/gh.tar.gz ]; then
        echo "下载中..."
        curl -L https://github.com/cli/cli/releases/download/v2.57.0/gh_2.57.0_macOS_arm64.tar.gz -o /tmp/gh.tar.gz
    fi

    echo "解压中..."
    mkdir -p ~/.local/bin
    tar -xzf /tmp/gh.tar.gz -C /tmp/
    cp /tmp/gh_2.57.0_macOS_arm64/bin/gh ~/.local/bin/
    chmod +x ~/.local/bin/gh

    # 添加到 PATH（如果还没有）
    if ! grep -q '~/.local/bin' ~/.zshrc 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        export PATH="$HOME/.local/bin:$PATH"
    fi

    echo "✅ GitHub CLI 安装完成"
fi

# 2. 验证安装
echo ""
echo "🔍 验证安装..."
~/.local/bin/gh --version || echo "⚠️  请先运行: source ~/.zshrc"

# 3. 检查登录状态
echo ""
echo "🔐 检查 GitHub 登录状态..."
if ~/.local/bin/gh auth status &> /dev/null; then
    echo "✅ 已登录 GitHub"
else
    echo "⚠️  需要先登录 GitHub"
    echo "请运行: ~/.local/bin/gh auth login"
    echo "然后选择：GitHub.com -> HTTPS -> Login with a web browser"
    echo ""
    read -p "登录完成后按回车继续..."
fi

# 4. 创建仓库并推送
echo ""
echo "📤 正在创建 GitHub 仓库并推送..."
echo ""

cd "$(dirname "$0")"

# 检查是否已有 remote
if git remote get-url origin &> /dev/null; then
    echo "Git remote 已存在，跳过创建"
    read -p "请输入你的 GitHub 仓库 URL (https://github.com/USERNAME/life-coach.git): " repo_url
    git remote set-url origin "$repo_url"
    git push -u origin main
else
    echo "请选择方式："
    echo "1. 使用 GitHub CLI 自动创建（推荐）"
    echo "2. 手动输入仓库 URL"
    read -p "选择 (1 或 2): " choice

    if [ "$choice" = "1" ]; then
        ~/.local/bin/gh repo create life-coach --public --source=. --remote=origin --push
    else
        read -p "请输入你的 GitHub 仓库 URL (https://github.com/USERNAME/life-coach.git): " repo_url
        git remote add origin "$repo_url"
        git branch -M main
        git push -u origin main
    fi
fi

echo ""
echo "✅ 完成！你的 Life Coach Skill 已上传到 GitHub"
echo "🔗 仓库地址："
git remote get-url origin
echo ""
echo "📝 下一步："
echo "1. 访问你的 GitHub 仓库"
echo "2. 更新 README.md 中的链接"
echo "3. 在 Claude Code 中测试：cp SKILL.md ~/.claude/skills/life-coach.md"
