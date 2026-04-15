# OpenAI Whisper Transcription UI

This is a Speech-to-Text transcription web app, built mostly by AI, which uses OpenAI's whisper at its core.

## Running

1. Use Python 3.10+ (3.12 recommended). On Mac, install **ffmpeg** for pydub: `brew install ffmpeg`.
1. Generate a virtual environment, e.g. `uv venv` or `python3 -m venv .venv`
1. Activate: `source .venv/bin/activate` (adjust path if needed)
1. Install: `uv pip install -r requirements.txt` or `pip install -r requirements.txt` (PyTorch uses **Metal (MPS)** on Apple Silicon.)
1. Run the flask app: `python app.py`

If transcription fails on MPS, force CPU: `WHISPER_DEVICE=cpu python app.py`.

***N.B.** by default the app will run the whisper "medium" model, which might be either too heavy for your machine or not heavy enough. In order to specify a different model, you can use the `MODEL` environment variable.*

*For example, to run with the large model, the following run command should be used:* `MODEL='large' python app.py`
