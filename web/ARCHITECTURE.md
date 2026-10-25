# How this web app works (reader’s guide)

```
Browser (index.html + app.js)
    │  Run → new EventSource("/stream")
    ▼
FastAPI main.py  stream_animation()
    │  loop: next_row(state) from dna_core.py
    │  yield SSE  data: {"line": "..."}
    ▼
dna_core.py
    │  ROWS templates + random A/T, C/G pairs
    ▼
(Same rules as reference/dna.py terminal loop)
```

| File | Role |
|------|------|
| `../dna_core.py` | Single source of truth for one animation step |
| `../reference/dna.py` | Original print/sleep script for terminal use |
| `main.py` | HTTP routes: page + SSE stream |
| `templates/index.html` | Shell UI + Help |
| `static/app.js` | SSE client, append lines to `<pre>` |
| `static/style.css` | Layout and colors only |

**Pause behavior:** Rows at index 0 and 9 in `ROWS` are spacer rungs; the book skips `sleep` after them. `next_row()` returns `should_pause=False` for those; the SSE loop only `asyncio.sleep(PAUSE)` when `should_pause` is true.
