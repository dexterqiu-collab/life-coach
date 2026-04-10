# GitHub 上传指南

## 📤 手动上传到GitHub

### 方法1：通过GitHub网页创建（推荐）

1. **创建新仓库**
   - 访问 https://github.com/new
   - 仓库名称：`life-coach`
   - 描述：`Elite Life Coach Skill - 综合全球顶级教练方法论的AI教练`
   - 选择 `Public` 或 `Private`
   - **不要**勾选 "Add a README file"（我们已经有了）
   - 点击 "Create repository"

2. **推送现有仓库**
   创建仓库后，GitHub会显示类似下面的命令：
   ```bash
   cd /Users/dexter/life-coach-perspective
   git remote add origin https://github.com/YOUR_USERNAME/life-coach.git
   git branch -M main
   git push -u origin main
   ```

### 方法2：使用GitHub CLI（如果安装）

```bash
# 安装GitHub CLI（如果未安装）
brew install gh

# 登录GitHub
gh auth login

# 创建仓库并推送
cd /Users/dexter/life-coach-perspective
gh repo create life-coach --public --source=. --remote=origin --push
```

## ✅ 上传后验证

1. 访问你的GitHub仓库：`https://github.com/YOUR_USERNAME/life-coach`
2. 检查文件是否正确上传
3. 确认README.md显示正常
4. 测试安装命令

## 🔗 安装链接提供

### Claude Code 用户
```bash
git clone https://github.com/YOUR_USERNAME/life-coach.git
cd life-coach
cp SKILL.md ~/.claude/skills/life-coach.md
```

### OpenClaw 用户
```bash
git clone https://github.com/YOUR_USERNAME/life-coach.git
cd life-coach
cp SKILL.md ~/.openclaw/skills/life-coach.md
```

## 📝 添加仓库信息

上传成功后，请更新README.md中的仓库链接：
- 第32行：`git clone https://github.com/YOUR_USERNAME/life-coach.git`
- 第38行：`git clone https://github.com/YOUR_USERNAME/life-coach.git`

将 `YOUR_USERNAME` 替换为你的GitHub用户名。

---

**准备好了吗？** 按照方法1的步骤开始上传吧！
