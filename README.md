# Character Chat ✨

A kids' chatbot web app where children can have conversations with their favorite cartoon, video game, and movie characters — powered by the Claude API.

Built as a static GitHub Pages site. No server, no accounts, no data stored anywhere except the user's own device.

## Features

- Chat with characters from SpongeBob, Bluey, Mario, Sonic, Frozen, Toy Story, and more
- AI-generated follow-up suggestions after each reply so kids always know what to say next
- Safe, age-appropriate responses (tuned for ages 6–9)
- Works on mobile and desktop
- API key stored locally in `localStorage` — never leaves the device except to call Anthropic directly

## Setup

1. Get an Anthropic API key at [console.anthropic.com](https://console.anthropic.com)
2. Open the app and paste your key in the one-time setup screen
3. Pick a character and start chatting

## Running locally

Any static file server works:

```bash
npx serve .
```

Then open `http://localhost:3000`.

## Project structure

```
index.html          # Landing page with app cards
kids-chatbot.html   # Character chat app
```

## Tech

- Vanilla HTML/CSS/JS — no build step, no dependencies
- [Claude API](https://docs.anthropic.com) (`claude-sonnet-4-6`) for character responses and suggestion generation
- Hosted on GitHub Pages
