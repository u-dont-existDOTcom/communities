# Universal Project Bootstrap

Before substantive work, read `u-dont-existDOTcom/universal-dev-architecture/LESSON-INDEX.md` and the task-relevant current universal patterns. Current owner instructions and verified project state override universal guidance.

Treat chat context as temporary working memory and keep durable project state in Git.

For long-running or multi-session work, maintain one concise project-local current-state checkpoint such as `CURRENT-STATE.md` or `state/CURRENT-STATE.md`. Record the goal, active decisions and constraints, completed work, current step, remaining work, blockers, relevant evidence/artifacts/branches/commits, and next safe action.

Update the checkpoint at meaningful durable boundaries. After interruption, a new thread, context compaction, or model switch, inspect actual repository state and recent relevant commits/artifacts, reconcile the checkpoint, identify what survived, and resume from the latest verified durable boundary without repeating completed work.

For substantive work, follow the current universal lesson-closeout pattern and promote genuinely transferable lessons to the universal repository with provenance and limits.
