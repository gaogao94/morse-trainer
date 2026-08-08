# Morse Trainer

A responsive, interactive Morse code learning tool that runs entirely in the browser. No server, no dependencies — just open `index.html` and start practicing.


## Features

- **Binary tree visualization** — see every Morse character as a node in the dit/dah decision tree. Click any node to hear its code. The tree always scales to fit its panel — no scrollbars on any screen size.
- **Key & spacebar input** — hold the key button or spacebar to send Morse code. Release timing decides dit vs dah.
- **Real-time decoding** — your input appears instantly as letters, with visual feedback on the tree.
- **Teach mode** — guided curriculum: single characters first (each with a "why this code" + mnemonic explanation), then common words (SOS, CQ, DE, 73, …). You key each character yourself on the key — correct keying auto-advances.
- **Study mode** — explore freely. Click nodes to listen, send characters to see them decoded.
- **Test mode (TX/RX)** — 发测试: the app prompts a character, you key it. 收测试: the app plays a character, you pick it from four options. Track correct/error rate.
- **Feedback** — a feedback tab POSTs to `serve.py`, which logs the message and forwards it to WeChat via the hermes agent channel.
- **Adjustable speed** — slider + numeric input, defaults to 10 WPM. Affects dit/dah timing and decode timeouts.
- **Mobile-friendly audio** — the AudioContext is pre-warmed on first touch and tones are scheduled on the audio clock, so short presses always sound.
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

- **教学** (Teach) — 单字 then 单词. Each character comes with a static explanation (why it has this code + how to memorize it).
- **学习** (Study) — explore the tree, click to hear, send freely.
- **测试** (Test) — 发测试 (you key the prompted character) or 收测试 (listen and pick from four options). Score tracked at the bottom.
- **反馈** (Feedback) — send feedback to the site owner's WeChat (requires `serve.py`, see below).

## Optional: feedback server

The app itself is static, but the feedback tab needs a tiny backend:

```
python3 serve.py 8080
```

This serves the static files AND handles `POST /api/feedback`: every message is appended to `feedback.log` and forwarded to WeChat via `hermes send --to weixin` (requires a configured [hermes](https://github.com/) agent on the host).

Environment variables:

| Var | Default | Purpose |
|-----|---------|---------|
| `FEEDBACK_DRY_RUN=1` | off | Only write `feedback.log`, don't send to WeChat (for testing) |
| `HERMES_TARGET` | `weixin` | `hermes send` target |
| `HERMES_BIN` | `hermes` | Path to the hermes binary |
| `BIND_HOST` | `127.0.0.1` | Bind address. Localhost-only is safe behind a tunnel/reverse proxy (cloudflared, nginx); set `0.0.0.0` for direct LAN/public access |

`feedback.log` contains visitor IPs and contact info, so it is created with mode `600` (owner read/write only).

Quick test:

```
FEEDBACK_DRY_RUN=1 python3 serve.py 8080 &
curl -X POST localhost:8080/api/feedback -H 'Content-Type: application/json' -d '{"msg":"test"}'
tail -1 feedback.log
hermes send --to weixin "通道测试"   # verify the real WeChat path
```

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
├── serve.py        # Optional: static server + /api/feedback -> WeChat via hermes
├── README.md       # This file
└── .gitignore
```

## License

MIT
