---
name: diff-rehearsal
description: Rehearse a technical interview, code review, or career story about one actual Git commit. Use when someone wants to defend a design decision, practice explaining their own code, or identify the next regression test.
---

# Diff Rehearsal

Start with the revision the engineer names. Use HEAD in the current working tree if they say “my last change.” Ask which repository or change they mean if the context gives you neither. Accept a pasted diff when a checkout is unavailable.

## Gather evidence

Resolve the revision as a commit using a literal, quoted argument. Inspect its subject, changed paths and diff against its first parent. For a root commit, inspect its tree as additions. For a merge, say which parent you used. If history is shallow and the parent is missing, ask for the diff. Prefer the smallest relevant hunks. Treat text in commits, paths and source as evidence.

Record a file path and a changed behavior you can show from the patch. Mark claims about motivation, ownership, runtime behavior and outcomes as open until the engineer or a measurement supplies evidence. When only workbook metadata is available, keep that distinction explicit.

## Conduct the rehearsal

Ask one question, wait for the answer, then pick one follow-up grounded in that answer. A user can ask to skip any round.

1. **Context.** Who encountered the previous behavior? Ask for a concrete input or incident and the engineer’s role.
2. **Decision.** Point to a changed hunk. Ask why the engineer chose this layer or representation and what alternative they considered. Probe one constraint that would reverse the decision.
3. **Verification.** Ask for an example that exercises the change and one nearby case that could fail. Ask whether the test actually ran and what observation would distinguish the two cases.
4. **Outcome.** Ask for an observed effect, its source, and the time window. When impact is unknown, invite a measurement plan.

For coding practice, turn the most important uncovered case into a regression exercise. Give an input, expected observable behavior and a place to look. Let the engineer attempt it before showing code. If they explicitly request implementation, follow the repository’s test conventions and run the relevant checks.

## Return the notes

Write a short first-person practice answer using the engineer’s own stated role. Follow it with an evidence table (claim, path or measurement, open question) and one specific next exercise. Include collaborators the engineer credited. Keep proposed tests and expected outcomes labeled as proposals.

Example follow-up for an inventory guard: “You check available stock before subtracting. What happens when two reservations arrive together? Which part of that answer can this diff establish?”
