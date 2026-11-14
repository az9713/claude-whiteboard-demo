# Claude Whiteboard Demo: From Video to Visual Explainer

**Live page: https://az9713.github.io/claude-whiteboard-demo/**

This repo is a demo of a workflow, not a summary of a video. It shows how a Claude whiteboard can be used to **visualize, organize and query** the content of a long talk, and then **present** the result as a polished scrolling web page.

The source material happens to be Ben Davis's video ["Software is solved"](https://www.youtube.com/watch?v=qfZhblrmSxM). The subject matter is incidental; the method works for any talk, paper or transcript.

![The whiteboard used to build the page](board.svg)

## The workflow

| Stage | What happened on the whiteboard |
|---|---|
| **1. Visualize** | Claude read the transcript and laid out the argument as six sections: claim, shift, limits, a five-step method loop (drawn as an actual loop), proof, and predictions. |
| **2. Query** | Questions were asked against the board itself. *"What is a fake API?"* grew a new explainer next to the step it clarified. *"The #1 skill is too cryptic"* turned a one-line quote into a three-move pattern with examples. |
| **3. Distill** | *"Distill the behavior changes"* compressed the whole talk into a stop → start table. *"Still too cryptic, make it actionable"* added a third column, "Try this," with something concrete for every row. |
| **4. Organize** | *"Clean up the whiteboard"* moved each explainer under the step it explains and renumbered everything into one top-to-bottom read. |
| **5. Present** | The board became a single scrolling HTML page with the same order and content, built for reading rather than panning around a canvas. |

## Why a whiteboard first

- **Shape before words.** Laying ideas out spatially exposes the structure of an argument (a loop, a sequence, a comparison) before any prose is written.
- **Questions become edits.** Every point of confusion is answered *on the board*, where it belongs, so the material improves where it was unclear.
- **A canvas to think, a page to publish.** A whiteboard is the right tool for exploring and reorganizing; a linear page is the right tool for readers. This repo shows the handoff from one to the other.

## What's in the repo

- `index.html`: the final page. A single self-contained file with no dependencies, which follows the reader's light or dark mode.
- `board.svg`: a map of the final whiteboard, redrawn from its layout data.
- `tools/board_svg.py`: the script that draws `board.svg`.

## Notes

The content is an unofficial summary written from the video's auto-generated transcript, so some product and model names may be mistranscribed. The "Try this" examples in the table are the summarizer's, built from the workflow Ben describes. Not affiliated with Ben Davis or any company mentioned.
