# My Claude Code Workflow for Empirical Research

> **What follows is my approach to using Claude Code for empirical economics research.** It may be different from how you use it or how others recommend using it. This is what works for me.

---

## The Core Philosophy: Thinking Partner, Not Code Monkey

I don't use Claude Code the way most programmers do. Most users treat AI assistants as "code generators"—they describe what they want, the AI writes it, done. I treat Claude Code as a **thinking partner** who happens to be able to write code.

The key difference:
- **Typical use**: "Write me a function that does X"
- **My use**: "I'm seeing Y in the data. What could explain this? Let's investigate together."

This distinction matters enormously for empirical research, where the hard part isn't writing code—it's figuring out what code to write and whether the results mean what you think they mean.

---

## The Fundamental Problem: Claude Has Amnesia

Claude Code forgets everything between sessions. Most people treat AI tools as stateless—ask a question, get an answer, done. I treat Claude Code as a **collaborator who has amnesia**. Every session, I re-orient Claude by pointing it to markdown files that contain:

1. **What we're working on** (README.md, CLAUDE.md)
2. **What problems we've hit and how we solved them** (CLAUDE.md)
3. **What we did last time and what's next** (session logs)
4. **Reference materials** (documentation/)

This builds **institutional memory** that persists even though Claude's memory doesn't.

---

## The Workflow in Practice

### 1. Exploratory Dialogue Before Action

I rarely start with a specific coding request. I start with an observation or puzzle:

> "The treatment and control groups look almost identical in the pre-period. That seems weird given how different the policies are. Can you look at the summary statistics and tell me what's going on?"

This forces Claude to engage with the **substance** of the problem, not just the mechanics. The output isn't code—it's understanding.

### 2. Socratic Method for Alignment

I frequently ask Claude to guess what I'm about to ask, or to explain back what it understands:

> "Do you see the issue with this specification?"
> "That's not it. The problem is the standard errors."
> "Guess at what I'm about to ask you to do."

This isn't about testing Claude—it's about ensuring alignment. If Claude guesses wrong, that reveals a misunderstanding that needs correcting before proceeding. This prevents hours of wasted work going in the wrong direction.

**Why this matters for research**: In product development, a wrong turn wastes time. In research, a wrong turn can lead to **incorrect conclusions in a published paper**. The cost of misunderstanding is much higher.

### 3. Persistent Documentation

I maintain running documentation that records:
- What was done
- Why it was done
- What was discovered
- What problems were encountered and how they were solved

This serves multiple purposes:
- **Continuity across sessions**: Claude Code sessions have context limits. The logs let a new session pick up where the last one left off.
- **Audit trail**: Months later, you can understand why a particular decision was made.
- **Team communication**: Collaborators can read the documentation to understand project status without a meeting.
- **Error correction**: When Claude misunderstands something, updating the documentation ensures future Claudes don't repeat the mistake.

### 4. Verification Through Visualization

I constantly ask for figures, tables, and visual outputs rather than just trusting numerical results:

> "Make a figure showing this relationship"
> "Put it in a slide so I can see it"
> "Let's review this visually"

This isn't about aesthetics (though I do care about presentation). It's about **catching errors**. A table that says "ATT = -0.73" is easy to accept uncritically. A visualization that shows the wrong pattern makes the error visible.

### 5. Beautiful Decks for Communication

I regularly create Beamer decks to communicate with coauthors and my future self. This is a regular practice, not an occasional one.

**Why beauty matters**: The rhetoric of decks is fundamentally about competing for attention. People are busy. Attention is scarce. A deck that looks like a wall of text will be skimmed or ignored. A beautiful deck makes people *want* to look at the slides.

> "Efficient communication requires beauty so that people stare at the slides and want more."

This isn't vanity. It's strategic: if you want someone to understand something, you first have to get them to *look* at it. Beautiful design lowers the friction of attention.

---

## Session Startup Routine

Every time I open Claude Code in a project directory, I give instructions like:

1. **"Read all the markdowns."**
   This gives Claude context on what we're doing, what problems we've hit, and where we left off.

2. **"Read the key programs."**
   So Claude knows the current state of the codebase.

3. **"State the goals of this session."**
   Forces Claude to articulate what we're working on before diving in.

4. **"Document problems into CLAUDE.md."**
   Any issues encountered get logged.

5. **"Document solutions in CLAUDE.md."**
   Whether they worked or not—this builds institutional memory.

This routine takes a minute or two but means Claude starts each session informed rather than ignorant.

---

## Cross-Software Replication: Catching Bugs Through Redundancy

One of my most effective bug-catching strategies is **implementing the same analysis in multiple statistical software packages**—typically R and Stata, sometimes Python. This isn't about needing multiple languages; it's about exploiting orthogonal error structures.

### The Core Insight

When Claude writes code, it can make mistakes:
- Misunderstanding variable definitions
- Off-by-one errors in indexing
- Incorrect handling of missing values
- Wrong function syntax
- Logical errors in conditional statements

Here's the key observation: **the mistakes Claude makes in R and the mistakes Claude makes in Stata are largely independent.** They're orthogonal error vectors. A bug that Claude introduces when writing `dplyr` code is unlikely to be the same bug Claude introduces when writing equivalent Stata code.

### Why This Works

1. **Syntax errors are language-specific.** An R script that runs without errors proves nothing about whether the Stata script is correct, and vice versa. If both produce the same answer, both had to navigate their own syntax correctly.

2. **Default behaviors differ.** R and Stata handle edge cases differently (NA propagation, factor ordering, floating point precision). If both arrive at the same answer, neither relied on a problematic default.

3. **The implementation path is different.** In R, you might use `group_by() %>% summarize()`. In Stata, you might use `collapse`. These are conceptually equivalent but mechanically different. Same answer = same concept.

### The Practice

For any non-trivial data transformation or analysis:

1. **Implement in R first** (or Stata—doesn't matter which is primary)
2. **Implement the same logic in the secondary language**
3. **Export comparable outputs** (CSV tables, summary statistics)
4. **Create a validation comparison** that shows:
   - Row counts match
   - Variable means/SDs match
   - Key computed values match to floating-point tolerance

If they don't match, something is wrong. Find it before proceeding.

### When to Use Cross-Software Validation

**Always use it for:**
- Sample construction (who's in, who's out)
- Variable construction (especially computed variables)
- Any transformation that changes the unit of analysis
- Final results tables

**Optional for:**
- Simple data loads
- Obvious subsetting (e.g., `age >= 25`)
- Intermediate exploratory analysis

---

## The Referee 2 Protocol: Adversarial Review

One of my most powerful techniques is invoking **Referee 2**—a fresh Claude instance whose job is to audit and challenge the work. This isn't adversarial in a hostile sense; it's collaborative stress-testing.

### Why Separation Matters

If you ask the same Claude that wrote code to review that code, you're asking a student to grade their own exam. The "review" will rationalize existing choices rather than challenge them.

True adversarial review requires:
- A **new terminal** (fresh context)
- **No prior commitments** to the existing code
- A **formal protocol** with specific checks

### How It Works

1. Complete your analysis in your main Claude session (the "author")
2. Open a **new terminal** with a fresh Claude
3. Load the Referee 2 protocol (`personas/referee2.md`)
4. Point it at your project
5. Referee 2 performs five systematic audits:
   - **Code Audit**: Coding errors, missing values, merge diagnostics
   - **Cross-Language Replication**: Creates scripts in 2 other languages, compares to 6 decimals
   - **Directory Audit**: Is this replication-package ready?
   - **Output Automation Audit**: Are outputs generated by code or manual?
   - **Econometrics Audit**: Specification coherence, standard errors, identification
6. Referee 2 files a formal **referee report** with findings
7. You respond to each concern (fix or justify)
8. Iterate until the verdict is "Accept"

### What This Catches

- **Unstated assumptions**: "Did you actually verify X, or just assume it?"
- **Alternative explanations**: "Could the pattern come from something else?"
- **Documentation gaps**: "Where does it explicitly say this?"
- **Logical leaps**: "You concluded A, but the evidence only supports B"
- **Missing verification steps**: "Have you actually checked the raw data?"

### The Philosophy

Referee 2 isn't about being negative. It's about **earning confidence**. A conclusion that survives rigorous challenge is stronger than one that was never questioned. The goal isn't to find reasons to abandon your work—it's to find the weak points and either fix them or accept them knowingly.

---

## How This Differs From Product Development

| Aspect | Product Development | My Research Workflow |
|--------|---------------------|----------------------|
| **Goal** | Ship working code | Understand phenomena correctly |
| **Error cost** | Bug in production | Wrong conclusion in paper |
| **Iteration** | Fast shipping, fix later | Slow, careful, get it right |
| **Documentation** | API docs, READMEs | Session logs, rationale files |
| **Testing** | Unit tests, CI/CD | Visual inspection, cross-software validation |
| **Success metric** | Does it run? | Does it mean what we think? |

A product developer would see code working and move on. I notice when results are similar when they "shouldn't" be, dig into why, discover the underlying issue, quantify it, and document it.

This is the difference between "the code runs" and "the code is correct."

---

## Why This Works for Empirical Economics

### 1. The Stakes Are Different

A bug in a web app causes user frustration. A bug in an empirical analysis can lead to:
- Incorrect policy recommendations
- Wasted research effort by others who build on your work
- Reputational damage when errors are discovered
- Retraction of published papers

The careful, verification-heavy workflow is appropriate for these stakes.

### 2. Understanding > Speed

In product development, shipping fast matters. In research, shipping fast but wrong is worse than shipping slow but right. The Socratic approach—constantly checking that Claude understands the problem correctly—prioritizes correctness over speed.

### 3. Reproducibility Requirements

Academic research must be reproducible. The documentation practices (session logs, rationale files, archived scripts with explanations) create an audit trail that allows others to understand and verify the work.

### 4. Complex, Interconnected Decisions

Research involves many decisions that interact:
- Which sample to use
- Which covariates to include
- How to handle missing data
- What robustness checks to run

Each decision affects the others. The exploratory dialogue approach helps surface these interactions before they become problems.

---

## Practical Tips

### Starting a Session
1. Ask Claude to read the markdown files first
2. Summarize where you left off
3. State what you want to accomplish

### During a Session
1. If something seems wrong, stop and investigate
2. Ask Claude to explain its understanding before proceeding
3. Request visualizations when possible
4. Update the documentation as you go

### Ending a Session
1. Ensure CLAUDE.md is updated with what was done
2. Note any unresolved issues or next steps
3. Commit important changes

### When Things Go Wrong
1. Don't just "fix" the output—understand why it was wrong
2. Document the error and the correct understanding
3. Check if similar errors exist elsewhere

---

## Summary

| Dimension | My Approach |
|-----------|-------------|
| **Philosophy** | Thinking partner, not code generator |
| **Memory** | External via markdown (Claude has amnesia) |
| **Verification** | Cross-software replication (R = Stata = Python) |
| **Review** | Referee 2 protocol in fresh terminal |
| **Documentation** | First-class output, not afterthought |
| **Visualization** | Trust pictures over numbers |
| **Speed** | Correctness over velocity |

The key insight is that Claude Code isn't just a code generator—it's a thinking partner. Treat it like a research assistant who needs to understand the problem, not a compiler that just needs syntactically correct instructions. Ask it questions. Make it explain its understanding. Verify its outputs visually. Document everything.

And when the stakes are high, spawn Referee 2 to challenge what you think you know. Then validate across software to catch the bugs that slip through.

That's how I use AI for research.

---

*Scott Cunningham — Professor of Economics, Baylor University*
*[scunning.com](https://www.scunning.com) | [causalinf.substack.com](https://causalinf.substack.com)*
