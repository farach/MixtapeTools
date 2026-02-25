---
name: compiledeck
description: Create and compile beautiful Beamer presentations following the Rhetoric of Decks philosophy. Use when making slides.
allowed-tools: Bash(pdflatex*), Bash(latexmk*), Bash(ls*), Bash(open*), Read, Write, Edit, Glob
argument-hint: [tex-file-path]
---

# Compile Deck — Beamer Presentations with the Rhetoric of Decks

This skill embodies a presentation philosophy for academic and research talks. The core principles are encoded here so you don't have to explain them each time.

## What This Skill Does

**The Rhetoric of Decks** is a philosophy for creating effective presentations. It recognizes two distinct use cases:

1. **External presentations** (seminars, conferences, teaching) — sparse, performative, one idea per slide
2. **Working decks** (coauthors, yourself) — can be more detailed, document reasoning, preserve uncertainty

It also recognizes that people may want different **visual styles**:

1. **Professional/Academic** — a consistent "house style" for outward-facing work
2. **Colorful/Expressive** — unique, creative designs for internal work or personal preference

You can use the same style for both, or different styles for different purposes. The philosophy (Three Laws, titles as assertions, compile discipline) applies regardless of visual style.

## First: Ask Two Questions

Before creating or significantly editing a deck, ask:

> **Question 1: Who is the audience?**
> 1. **External** — Seminar, conference, teaching, client (sparse, performative)
> 2. **Working** — You and coauthors (detailed, documentary)

> **Question 2: What's the tone?**
> 1. **Professional/Academic** — Your house style. Muted, authoritative, consistent.
> 2. **Colorful/Expressive** — Create something unique each time.

These two answers determine density and visual style.

---

## The Philosophy (Internalize This)

### The Three Laws

**Law 1: Beauty Is Function**
- Every element earns its presence
- Nothing distracts from the point
- The eye knows where to go
- The most beautiful slide may be three words on a blank background

**Law 2: Cognitive Load Is the Enemy**
- One idea per slide. ONE. This is not a guideline.
- Too many points → zero points retained
- Dense text → nothing read
- Complex charts → confusion, not insight

**Law 3: The Slide Serves the Spoken Word**
- The slide is the visual anchor, not the content itself
- If slides can be understood without speaking, you've written a document
- If you must read slides aloud, you've failed twice

### Titles Are Assertions, Not Labels

**Weak**: "Results"
**Strong**: "Treatment increased distance by 61 miles on average"

**Weak**: "Literature Review"
**Strong**: "Prior work ignores the supply-side margin"

If someone reads only slide titles in sequence, they should understand the argument.

### The MB/MC Equivalence

Optimal rhetoric equalizes marginal benefit to marginal cost across all slides:

$$\frac{MB_1}{MC_1} = \frac{MB_2}{MC_2} = \cdots = \frac{MB_n}{MC_n}$$

- **Overloaded slides** (MB/MC too low): Text running into footer, multiple competing ideas, audience gives up
- **Underloaded slides** (MB/MC too high): Wasted opportunity, attention captured but not used

Walk through the deck asking: "If I added one more element, would the benefit justify the cognitive cost?"

### Visual Grammar

- **Hierarchy**: Not all information is equal. Primary (large, prominent), Secondary (smaller), Tertiary (footer)
- **Bullets are defeat**: Find the structure hiding in your bullets—sequence, contrast, hierarchy, causal chain
- **White space**: Empty space is confidence, not waste
- **Typography**: Minimum 24pt body (18pt floor), sans-serif, never justify text
- **Charts**: One message per chart, remove chartjunk, label directly (no legends), use color to highlight

### For External Audiences

- Sparse, performative
- One idea per slide (strictly enforced)
- Titles carry the argument
- Opening grabs attention in 60 seconds
- Closing is the one memorable takeaway

### For Working Decks (Coauthors)

- Can be more detailed
- Document choices and reasoning
- Show the "why" behind decisions
- Preserve uncertainty, flag unknowns
- Enable iteration and verification
- Still follow visual hierarchy—just with more content

---

## Style Elements

Style depends on the tone answer.

---

### If Professional/Academic → User's House Style

**First, check the user's CLAUDE.md for a defined professional palette.** If they have one, use it.

If no custom palette is defined, use this default professional palette:

```latex
% Default Professional Palette
\definecolor{navy}{HTML}{1A365D}            % Primary text
\definecolor{darkgray}{HTML}{2D3748}        % Headers, emphasis
\definecolor{forest}{HTML}{276749}          % Success, positive
\definecolor{steel}{HTML}{4A5568}           % Secondary text
\definecolor{lightgray}{HTML}{718096}       % Tertiary, captions
\definecolor{offwhite}{HTML}{F7FAFC}        % Background tint
```

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{default}
\usecolortheme{default}

% Strip navigation chrome
\setbeamertemplate{navigation symbols}{}

% Professional frame styling
\setbeamercolor{frametitle}{fg=darkgray,bg=white}
\setbeamercolor{title}{fg=darkgray}
\setbeamercolor{normal text}{fg=navy}
\setbeamercolor{itemize item}{fg=steel}
\setbeamercolor{itemize subitem}{fg=lightgray}

% Clean, professional feel
\setbeamerfont{frametitle}{series=\bfseries}
```

**Professional style principles:**
- Muted, authoritative colors
- One accent color used sparingly
- Primary color for body text, darker shade for headers
- Generous white space, no clutter
- Authority through restraint

---

### If Colorful/Expressive → Create Something Unique

When the user chooses this option, **design something new each time**.

**Guidelines for unique styles:**
- Choose a cohesive palette (3-5 colors max)
- One dominant color, one accent, one neutral
- Match the mood of the content
- Be bold but maintain readability
- Every deck should feel like it was made just for this moment

**Example palettes to inspire (create new ones each time):**
- Sunset: warm coral, deep purple, cream
- Nordic: ice blue, charcoal, soft white
- Earth: terracotta, sage green, warm sand
- Midnight: deep indigo, gold accent, silver text

The point is: make something beautiful that shows care.

---

### Beamer Setup (Both Styles)
```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{default}
\usecolortheme{default}

% Strip navigation chrome
\setbeamertemplate{navigation symbols}{}
```

### TikZ Figures
- Use consistent node styles across the deck
- Rounded corners for boxes
- Clear directional arrows
- Labels positioned deliberately (not auto-placed)

### Data Visualization
- ggplot2 or TikZ with minimal chartjunk
- Direct labels (no legends requiring eye movement)
- Color highlights the key comparison
- One message per chart

---

## The Compile Loop

**ZERO TOLERANCE FOR WARNINGS.** We aim for perfection. Every compile must be completely clean — no overfull hbox (not even 0.5pt), no underfull vbox, no font warnings. "Close enough" is not acceptable.

After any edit to a .tex file:

### Step 1: Compile
```bash
cd [directory]
pdflatex -interaction=nonstopmode [file].tex
```

### Step 2: Check for Errors
Look for lines starting with `!` — these are fatal errors.

### Step 3: Check for Warnings — FIX ALL OF THEM

**Overfull hbox**: Text or figures too wide — even 0.5pt must be fixed
- Fix: Rephrase text, shorten words, add `@{}` to table columns, scale figures

**Underfull hbox**: Awkward spacing
- Fix: Rephrase or adjust paragraph breaks

**Overfull vbox**: Too much content for slide
- Fix: Split slide or reduce content, tighten `\vspace`

**Do not proceed until all warnings are resolved.**

### Step 4: Check TikZ Coordinates

TikZ positioning errors don't trigger compile warnings but produce visual errors:
- Labels at wrong positions
- Nodes overlapping
- Arrows pointing incorrectly

**Verify intentionality**: For each coordinate (x, y), ask: "Is this where I want it, or did I want (x + τ, y + ε)?" This may require calculation or careful visual inspection.

**Manually verify**: Open PDF, check each TikZ figure visually.

### Step 5: Check ggplot/Figure Labels

External figures (ggplot, matplotlib) can have label positioning problems:
- Axis labels cut off
- Legend overlapping data
- Text outside figure bounds

**These don't trigger compile errors.** Visual inspection required.

### Step 6: Recompile Until Clean

Goal: **Zero warnings, zero visual errors.** Do not consider the work complete until this is achieved.

---

## Workflow Summary

1. **Ask**: External or working audience?
2. **Ask**: Professional or colorful tone?
3. **Apply style**: User's house palette (from CLAUDE.md) OR create something unique
4. **Create/Edit**: Following the three laws
5. **Compile**: `pdflatex -interaction=nonstopmode`
6. **Fix errors**: Lines starting with `!`
7. **Fix warnings**: Overfull/underfull boxes
8. **Visual check**: TikZ coordinates, figure labels
9. **Repeat** until clean
10. **Open PDF**: `open [file].pdf`

---

## Quick Reference

| Principle | Rule |
|-----------|------|
| Ideas per slide | ONE |
| Title style | Assertion, not label |
| Minimum font | 24pt (18pt floor) |
| Bullets | Avoid—find the structure |
| White space | Confidence, not waste |
| Charts | One message, direct labels |
| Compile target | Zero warnings |

---

## Full Philosophy Reference

For the complete essay: `~/mixtapetools/presentations/rhetoric_of_decks.md`

This skill embodies that philosophy. You don't need to re-read it every time—just follow the principles above.
