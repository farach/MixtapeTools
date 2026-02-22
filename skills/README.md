# Skills for Claude Code

## What is this?

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is a way to work with Claude directly on your computer — you type instructions, and Claude reads files, writes code, searches the web, and carries out tasks for you. If you've used Claude in the browser, Claude Code is the version that can actually *do things* on your machine.

**Skills** are pre-written workflows for Claude Code. Think of them as recipes. You type a short command (like `/split-pdf`), and Claude follows a detailed set of instructions to carry out a complex, multi-step task automatically. Without the skill, you'd have to explain every step yourself each time. With the skill, it's one command.

This directory contains documentation, methodology, and example output for the skills in this repo. Browse what's available below.

---

## Available Skills

| Skill | Command | What it does |
|-------|---------|--------------|
| [**Split-PDF**](split-pdf/) | `/split-pdf` | You give Claude a paper (a local file or a search query like "Gentzkow Shapiro 2014 competition newspapers"). It finds and downloads the PDF, saves it locally, splits it into small chunks, reads them carefully in batches, and writes detailed structured notes — extracting research questions, methods, data sources, findings, and more. The original PDF is always preserved. [See the full walkthrough with example output →](split-pdf/) |
| [**New Project**](newproject/) | `/newproject` | Scaffolds a new research project with a standard directory structure — `code/`, `data/raw/`, `data/clean/`, `output/`, `documents/`, `decks/`, `notes/`, and `progress_logs/`. Copies a CLAUDE.md template for persistent AI context, generates a documented README, and creates an initial progress log for session continuity. [See documentation →](newproject/) |

---

## How to Use These Skills

**Prerequisites:** You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed. If you haven't set it up yet, follow Anthropic's installation guide first.

**Then:**

1. **Clone this repo** (or just copy the `.claude/skills/` directory — that's the hidden folder where the actual skill instructions live)
2. Place the `.claude/skills/` folder in your project root
3. Open Claude Code in that project directory
4. Type the slash command: `/split-pdf "Gentzkow Shapiro 2014 competition newspapers"`

That's it. Claude Code automatically discovers skills in `.claude/skills/` and makes them available as slash commands. No configuration needed.

---

## Why are there two directories?

You might notice this repo has both a visible `skills/` folder (what you're reading now) and a hidden `.claude/skills/` folder. Here's why:

- **`.claude/skills/`** contains the actual skill files — the instructions Claude follows when you invoke a command. These are written *for Claude*, in a format it understands (step-by-step imperatives with metadata). This directory is hidden on GitHub because it starts with a dot.

- **`skills/`** (this directory) contains documentation *for you* — what each skill does, why it works, how to use it, and examples of real output. It's the human-readable companion to the machine-readable instructions.

When you clone the repo, you get both. Claude reads its instructions from `.claude/skills/`. You read the documentation here in `skills/`.

---

## How Skills Work (Under the Hood)

Each skill is a markdown file at `.claude/skills/<name>/SKILL.md`. It has a small header (metadata) that tells Claude Code the skill's name and what tools it's allowed to use, followed by step-by-step instructions that Claude follows when you invoke the command.

```
.claude/skills/
├── split-pdf/
│   ├── SKILL.md           # The instructions Claude follows
│   └── methodology.md     # Why this approach works (for humans)
└── newproject/
    └── SKILL.md           # The instructions Claude follows

skills/
├── split-pdf/
│   └── README.md          # Full documentation and examples (for humans)
└── newproject/
    └── README.md          # Philosophy, folder purposes, installation (for humans)
```

If you're curious what the actual instructions look like, you can read the [SKILL.md file directly](../.claude/skills/split-pdf/SKILL.md) — but you don't need to understand it to use the skill.

---

## Adding New Skills

To create your own skill:

1. Create a directory under `.claude/skills/` with a `SKILL.md` file
2. Optionally create a matching directory under `skills/` with a `README.md` for documentation

If you develop a useful skill for academic research, PRs are welcome.
