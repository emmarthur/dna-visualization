/**
 * Browser-side controller for the DNA animation page.
 *
 * We do not compute helix rows here — the Python server runs dna_core.next_row()
 * and pushes each line over Server-Sent Events (SSE). This file only:
 *   - opens/closes EventSource("/stream")
 *   - appends lines to the <pre id="output">
 *   - trims old lines so the DOM stays lightweight
 */

const output = document.getElementById("output");
const runBtn = document.getElementById("run-btn");
const pauseBtn = document.getElementById("pause-btn");
const clearBtn = document.getElementById("clear-btn");
const statusEl = document.getElementById("status");

// Keep roughly this many lines visible; older lines drop off the top.
const MAX_LINES = 120;

/** Active EventSource while animation is running; null when paused. */
let source = null;

/**
 * Append one ASCII row and scroll the panel down.
 * Using textContent (not innerHTML) because lines are plain text from the server.
 */
function appendLine(line) {
  output.textContent += line + "\n";
  const lines = output.textContent.split("\n");
  if (lines.length > MAX_LINES) {
    output.textContent = lines.slice(-MAX_LINES).join("\n");
  }
  output.scrollTop = output.scrollHeight;
}

/** Close SSE and reset button state (same idea as Ctrl-C in the terminal script). */
function stopStream() {
  if (source) {
    source.close();
    source = null;
  }
  runBtn.disabled = false;
  pauseBtn.disabled = true;
  statusEl.textContent = "Paused";
  statusEl.classList.remove("running");
}

runBtn.addEventListener("click", () => {
  if (source) return;

  runBtn.disabled = true;
  pauseBtn.disabled = false;
  statusEl.textContent = "Running";
  statusEl.classList.add("running");

  // EventSource automatically reconnects on some errors; we close on error below.
  source = new EventSource("/stream");

  source.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (typeof data.line === "string") {
        appendLine(data.line);
      }
    } catch {
      // Skip bad payloads rather than breaking the whole UI.
    }
  };

  source.onerror = () => {
    stopStream();
    statusEl.textContent =
      "Stream unavailable — start the demo server on port 3005, then press Run";
  };
});

pauseBtn.addEventListener("click", () => {
  stopStream();
});

clearBtn.addEventListener("click", () => {
  output.textContent = "";
});

document.querySelectorAll("[data-help-jump]").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.getElementById("help-heading")?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
});
