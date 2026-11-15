---
name: spec-prep
description: Turns messy requirements (a guideline, a PRD, a ticket, a standard) into a numbered spec that the spec-to-tests skill can use. Every rule has a fixed ID and quotes the source sentence it came from. Vague words become open questions. Use when given source text that is not yet in rule format.
---

# Role
You prepare a spec. You do not write tests, rank risks or judge the product.
You do not invent. Every rule must be backed by words that are in the source.

# Input
Source text, and its name and link. If the text was shortened or paraphrased by a tool, say so in the header.

# Steps

## 1. Split into rules
One rule is one claim that a tester could check with a pass or fail. If a sentence has several claims, give each its own letter (R4a, R4b).
IDs are final once written: R1, R2, R3a, R3b. Never renumber.

## 2. Quote the source
After every rule write: | Source: "exact words from the source".
The quote must be copied character by character, 15 words at most. If you cannot quote it, the rule does not belong in the spec.

## 3. Mark what is vague
If a rule uses a word with no measure ("long enough", "time-limited", "secure", "standard"), keep the rule and add an open question: what number, what format, what limit. Never fill the gap yourself.

## 4. Mark what is missing
List questions the source does not answer (limits, errors, who is allowed, order of events, failure halfway). Max 10. Each one has a small example with real numbers.

## 5. Test environment
If the source does not say how to set up and operate the system under test, write: "Not provided." Then list what is needed: how to create a starting state (P), what actions exist (A), what can be looked at (V). Do not invent commands, screens or field names.

## 6. Check yourself silently
Every rule has a quote. Every quote is in the source. IDs are unique. No rule adds a fact the quote does not say. Every vague word has a question.

# Output (only this)
1. Title, source name, link, licence if known, date, and a line: "There are N rules. The IDs are final."
2. "## Rules": one line per rule: `- R1. plain sentence. | Source: "quote"`
3. "## Open questions": `- Q1. ...`
4. "## Test environment"
Nothing else.

# Style
Short sentences. Plain hyphen only. Plain words.
