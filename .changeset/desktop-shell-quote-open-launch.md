---
'@e2b/desktop': patch
'@e2b/desktop-python': patch
---

Shell-quote arguments to `open`/`launch`/`getWindowTitle` (JS) and `open`/`launch`/`get_window_title` (Python) so URLs with `&`, paths with spaces, and other shell metacharacters are passed intact. `launch(app)` with no URI no longer appends an empty argument.
