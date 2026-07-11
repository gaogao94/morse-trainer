# Morse Trainer

A responsive, interactive Morse code learning tool that runs entirely in the browser. No server, no dependencies — just open `index.html` and start practicing.


## Features

- **Binary tree visualization** — see every Morse character as a node in the dit/dah decision tree. Click any node to hear its code.
- **Key & spacebar input** — hold the key button or spacebar to send Morse code. Release timing decides dit vs dah.
- **Real-time decoding** — your input appears instantly as letters, with visual feedback on the tree.
- **Study mode** — explore freely. Click nodes to listen, send characters to see them decoded.
- **Test mode** — the app prompts a random character; you send its Morse code. Track correct/error rate.
- **Adjustable speed** — slider + numeric input, defaults to 10 WPM. Affects dit/dah timing and decode timeouts.
- **Proportional scaling** — the entire UI scales up on tall windows and keeps natural size on short ones.
- **Punctuation & prosigns** — `. , ? / = AR HH` supported as both input and reference.
- **Depth labels** — layer numbers on the left show how many symbols deep each character sits in the tree.
- **Dark theme** — designed for focused, low-eye-strain practice sessions.

## How to Use

### Open the app

```
open index.html
```

or drag it into any modern browser.

### Sending Morse code

- **Press and hold** the on-screen key button or your **spacebar**.
- **Short press** (< 240ms at 10 WPM) = dit (·)
- **Long press** (≥ 240ms) = dah (−)
- Release to register the symbol. After a brief pause, the character is committed.

### Word spacing

Pause between characters to have a space inserted automatically. The word timeout is generous (12 unit times) — you have over a second at 10 WPM to start the next character.

### Special codes

| Code | Action |
|------|--------|
| `......` (6+ dots) | Backspace — delete the last character |
| `.-.-.` | End of message (AR) |

### Modes

- **学习** (Study) — explore the tree, click to hear, send freely.
- **测试** (Test) — answer character prompts. Score tracked at the bottom.

### Filters

- **全部** (All) — show letters and numbers in the tree.
- **字母** (Letters) — A–Z only.
- **数字** (Numbers) — 0–9 only.

### Speed adjustment

Default is **10 WPM**. Use the slider or type a number directly (1–60). Timing values update below:

| Parameter | Formula | 10 WPM | 20 WPM |
|-----------|---------|--------|--------|
| Unit (dit length) | 1200 / wpm | 120ms | 60ms |
| Dit/Dah threshold | 2 units | 240ms | 120ms |
| Character timeout | 3 units | 360ms | 180ms |
| Word timeout | 12 units | 1440ms | 720ms |

## Files

```
morse-trainer/
├── index.html      # The entire application (HTML + CSS + JS)
├── README.md       # This file
└── .gitignore
```

## License

MIT
