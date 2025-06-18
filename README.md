# summarize-youtube

Summarize YouTube videos using LLMs and timestamps from the command line.

## Installation (Development)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
summarize-youtube "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

You can specify a different OpenAI model with `--model` if desired.

## Global Installation

See the RECIPE.md for a script to install globally and add to your PATH.

## Requirements
- Python 3.8+
- OpenAI API key (set as environment variable `OPENAI_API_KEY`) 