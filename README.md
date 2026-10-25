# DNA Visualization (catalog #459)

Al Sweigart — *The Big Book of Small Python Projects*, Project #21.

| Artifact | Path |
|----------|------|
| Book step order | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Reference Python (terminal script) | [`reference/dna.py`](./reference/dna.py) |
| Shared animation logic | [`dna_core.py`](./dna_core.py) |
| Runnable web app (FastAPI) | [`web/`](./web/) — port **3005** |
| Upstream | [dna.py on GitHub](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/dna.py) |

Web stack is **Python (FastAPI + uvicorn)**, not a TypeScript port.

Code walkthrough for contributors: [`web/ARCHITECTURE.md`](./web/ARCHITECTURE.md). Inline comments in `dna_core.py`, `web/main.py`, and `web/static/app.js`.
