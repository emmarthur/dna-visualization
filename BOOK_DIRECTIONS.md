# Book directions — DNA Visualization

**Catalog #459** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #21**

- Online chapter: [inventwithpython.com/bigbookpython/project21.html](https://inventwithpython.com/bigbookpython/project21.html)
- Upstream code: [dna.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/dna.py)
- Local reference copy: [`reference/dna.py`](./reference/dna.py)
- Shared logic (web + tests): [`dna_core.py`](./dna_core.py)

## What the book asks you to build

A **scrolling ASCII animation** of a DNA double helix. Each frame prints one row from the `ROWS` list. Most rows use `{}` placeholders for a random base pair (A–T, T–A, C–G, or G–C). Rows at index **0** and **9** are fixed rungs (`##` only). The loop runs forever until Ctrl-C.

## Constants

| Name | Value |
|------|-------|
| `PAUSE` | `0.15` seconds between rows |
| `ROWS` | 18 string templates (see source) |

## Step order (follow the book's source)

1. Print title and *Press Ctrl-C to quit...*; **`time.sleep(2)`**.
2. Set **`rowIndex = 0`**.
3. **`while True`:**
   - **`rowIndex = rowIndex + 1`**; wrap to `0` at `len(ROWS)`.
   - If **`rowIndex == 0` or `rowIndex == 9`**: print `ROWS[rowIndex]` and **`continue`** (no sleep on these in the book loop for spacer rows—only the formatted rows sleep).
   - Else: **`random.randint(1, 4)`** → pick left/right nucleotides (A/T or C/G pairs).
   - **`print(ROWS[rowIndex].format(left, right))`**
   - **`time.sleep(PAUSE)`**
4. On **`KeyboardInterrupt`**, exit.

## Web version (`web/` — FastAPI)

| Book step | Web equivalent |
|-----------|----------------|
| `print` each row | **Run** opens **SSE** `/stream`; browser appends lines to `<pre>` |
| `time.sleep(PAUSE)` | Same delay in the stream generator |
| Ctrl-C | **Pause** closes the EventSource |
| Main loop body | [`dna_core.next_row()`](./dna_core.py) (same index and random pair rules) |

Run: [`web/README.md`](./web/README.md) — **port 3005**.
