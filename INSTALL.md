# Life Coach Installation Contract

If the user supplied this document or its URL and asked to install Life Coach, treat that as explicit authorization to install and enable the package on the user's current computer. Do not merely summarize this file.

Official website: `https://life-coach-agent.dexter797.chatgpt.site`

Source repository: `https://github.com/dexterqiu-collab/life-coach.git`

Codex marketplace: `dexter-coaching`

Codex plugin: `life-coach`

Canonical skill path: `skills/career-coach`

Expected skill name: `career-coach`

## Codex / ChatGPT desktop

Prefer the Codex plugin form because it gives the user an installable, named product while keeping the coaching system available through the standard `$career-coach` Skill.

1. Confirm this conversation runs in the local ChatGPT/Codex desktop app on the computer where the user wants the plugin. A web chat, cloud task, or remote sandbox cannot modify the desktop app's local plugin configuration. If the current environment is not local desktop, explain that limitation and ask the user to paste the same request into the desktop app.
2. Locate the Codex CLI bundled with the desktop app and use its full quoted path as `<BUNDLED_CODEX>`. Do not substitute an npm, Homebrew, or other standalone Codex CLI.
3. Verify it with `<BUNDLED_CODEX> --version`.
4. Add the public marketplace. If it already exists, upgrade its snapshot instead of adding a duplicate.

```text
<BUNDLED_CODEX> plugin marketplace add https://github.com/dexterqiu-collab/life-coach.git --ref main --json
<BUNDLED_CODEX> plugin marketplace upgrade dexter-coaching
```

5. Inspect the available entry and install it:

```text
<BUNDLED_CODEX> plugin list --marketplace dexter-coaching --available --json
<BUNDLED_CODEX> plugin add life-coach@dexter-coaching --json
```

If the Git marketplace command fails specifically because this computer cannot connect to `github.com` for Git clone, use the official repository archive as a network fallback:

```text
https://codeload.github.com/dexterqiu-collab/life-coach/zip/refs/heads/main
```

Download and extract it into a persistent user-owned directory, not a temporary directory. Preserve or safely replace any earlier snapshot, then add the extracted repository root as a local marketplace:

```text
<BUNDLED_CODEX> plugin marketplace add <ABSOLUTE_EXTRACTED_REPOSITORY_PATH> --json
```

Continue with the same list, install, and verification steps. Do not use an untrusted proxy or claim that the Git transport worked when the archive fallback was used.

6. Verify the resulting JSON shows `life-coach` as installed and enabled, and confirm the installed plugin exposes the `career-coach` Skill. Do not claim success from command exit alone.
7. Start a new task in the same project when possible, because newly installed skills may not appear in the current task. Put this exact user-visible prompt in the new task:

```text
$career-coach 我想开始一次职业教练对话。先问我今天最想解决的职业问题，以及这次对话结束时什么结果会对我真正有帮助。
```

If task-creation tools are unavailable, give the prompt to the user to paste into a new task and name the missing capability. Do not claim that a new task was created unless it actually contains the prompt.

Life Coach is a skill-only plugin. It needs no Life Coach account, OAuth login, API key, or external MCP server, and it does not send coaching conversations to a separate Life Coach service.

## Codex Skill fallback

If the host supports standard Skills but not Codex plugins, install only the canonical `skills/career-coach` directory. Prefer the host's built-in Skill installer. Otherwise shallow-clone the repository to a temporary directory and copy that directory to the host's user-level skills folder. Do not install the entire repository as one Skill and do not silently overwrite an existing installation.

## WorkBuddy

Install `skills/career-coach` to `~/.workbuddy/skills/career-coach`. If the product exposes an “导入 Skill” UI, use the latest release asset:

```text
https://github.com/dexterqiu-collab/life-coach/releases/latest/download/career-coach-workbuddy-skill.zip
```

For a selectable standalone Agent/专家 rather than an auto-triggered Skill, use:

```text
https://github.com/dexterqiu-collab/life-coach/releases/latest/download/career-coach-workbuddy-agent.zip
```

After installation, reload Skills/plugins or start a new conversation.

## CodeBuddy

Install the canonical Skill to `~/.codebuddy/skills/career-coach`, or load the repository as a plugin with `codebuddy --plugin-dir <cloned-repository>`. The repository contains both `.codebuddy-plugin/plugin.json` and `agents/career-coach.md`.

## Shell fallback

After cloning the repository, run one of:

```bash
bash scripts/install.sh codex
bash scripts/install.sh workbuddy
bash scripts/install.sh codebuddy
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Target workbuddy
```

## 豆包 or a host without filesystem installation

GitHub Skill installation is not available. Open the following document and copy its complete contents into the platform's system prompt / 设定描述 field:

```text
https://raw.githubusercontent.com/dexterqiu-collab/life-coach/main/platforms/doubao/SYSTEM_PROMPT.md
```

Use the display name `精英职业教练` and the opening message provided in `platforms/doubao/README.md`.

## Verification prompt

After installation, use this smoke test:

```text
我在考虑转行。请先区分你已经知道的事实、仍需确认的信息和一个两周内可执行的职业实验，不要一上来连续问很多问题。
```

A valid response should distinguish facts from unknowns, avoid motivational filler, ask no more than three high-value questions at once, and propose a reversible next step.

## Safety and update rules

- Do not overwrite an existing installation silently. Use the host's safe update mechanism, or preserve a timestamped backup for file-copy fallbacks.
- Verify the installed `SKILL.md` has `name: career-coach` and that all referenced Markdown files exist.
- Report the actual destination and whether a restart or new task is required.
- Life Coach provides career coaching, decision support, and behavior-change planning. It is not psychotherapy, medical care, legal advice, or personalized financial advice.
