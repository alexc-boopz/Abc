# Kenji Shorts kit

Locked-in code and style for the Kenji anime YouTube Shorts series.

- `make.py`: Kenji character, palette, fonts, caption and badge styles, and the scene renderer (1080x1920, 30 fps). Set `OUT` to your scenes folder.
- `scenes.py`: Episode 1 (Part 1, day trading), the template for every new episode (`from make import *`).
- `audio.py`: generated music and sound effects. Edit `starts`, `END` and the hit times for each episode.
- `episodes.md`: log of every episode posted, so each new one continues the story.

Rules: 30 to 40 seconds, 8 or 9 scenes, a big hook in scene 1, a fail, a twist, and an end card teasing the next part. Every episode has a new premise. Always include "not financial advice."
