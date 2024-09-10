# OpenAI Whisper Transcription UI

This is a Speech-to-Text transcription web app, built mostly by AI, which uses OpenAI's whisper at its code.

## Running

1. Generate a virtual environment (venv) `python3 -m venv env`
1. Enter the venv `source ./env/bin/activate`
1. Install the requirements `pip install -r requirements.txt`
1. Run the flask app: `python app.py`

***N.B.** by default the app will run the whisper "medium" model, which might be either too heavy for your machine or not heavy enough. In order to specify a different model, you can use the `MODEL` environment variable.*

*For example, to run with the large model, the following run command should be used:* `MODEL='large' python app.py`
