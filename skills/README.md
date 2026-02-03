# Skills for Claude Code

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is a command-line tool that lets you work with Claude directly in your terminal. **Skills** are pre-written workflows that Claude Code can execute — think of them as macros or recipes. You type a slash command (like `/split-pdf`), and Claude follows a detailed set of instructions to carry out a complex, multi-step task automatically.

This directory documents the skills included in this repo. The actual skill files that Claude reads live in `.claude/skills/` (a hidden directory that doesn't show up on GitHub). This visible `skills/` directory exists so you can browse what's available, see examples of real output, and learn how to install them in your own projects.

---

## Available Skills

| Skill | Command | What it does |
|-------|---------|--------------|
| [**Split-PDF**](split-pdf/) | `/split-pdf` | You give Claude a paper (local file or search query). It downloads the PDF, saves it locally, splits it into 4-page chunks, reads them in small batches, and writes detailed structured notes — preserving the original PDF throughout. [See the full walkthrough and example output →](split-pdf/) |

---

## How to Use These Skills in Your Own Projects

1. **Clone this repo** (or just copy the `.claude/skills/` directory)
2. Place the `.claude/skills/` folder in your project root
3. Open Claude Code in that project
4. Type the slash command (e.g., `/split-pdf "Gentzkow Shapiro 2014 competition newspapers"`)

Claude Code automatically discovers skills in `.claude/skills/`. No configuration needed beyond having the files in the right place.

---

## How Skills Work (Under the Hood)

A skill is a markdown file at `.claude/skills/<name>/SKILL.md` with YAML frontmatter. The frontmatter tells Claude Code the skill's name, what tools it's allowed to use, and a hint for what arguments the user should provide. The body of the file is imperative instructions — a prompt that Claude follows step by step when the skill is invoked.

```yaml
---
name: your-skill-name
description: What the skill does (one sentence)
allowed-tools: Bash(python*), Read, Write
argument-hint: [what-the-user-provides]
---

# Instructions for Claude

Step 1: Do this.
Step 2: Then do that.
Step 3: Write the output here.
```

The SKILL.md is written *for Claude*, not for humans. That's why this `skills/` directory exists — to provide human-readable documentation, methodology explanations, and example output for each skill.

---

## Adding New Skills

To create a new skill:

1. Add a directory under `.claude/skills/` with a `SKILL.md` file
2. Optionally add a matching directory under `skills/` with a human-readable `README.md`

```
.claude/skills/
└── your-skill-name/
    └── SKILL.md              # Instructions Claude follows

skills/
└── your-skill-name/
    └── README.md             # Documentation for humans
```

If you develop a useful skill, PRs are welcome.
