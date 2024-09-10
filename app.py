import os
from datetime import datetime
import tempfile
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import whisper
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from pydub.utils import make_chunks

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSCRIPTION_FOLDER'] = 'transcriptions'
app.config['STATIC_FOLDER'] = 'static'
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

m = os.environ.get('MODEL', 'medium')

# Load Whisper model
model = whisper.load_model(m)

print(f'using whisper-{m}')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template('transcribe.html', filename=filename)
    return render_template('upload.html')

@socketio.on('start_transcription')
def handle_transcription(data):
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    current_date = datetime.now().strftime("%Y%m%d_%H:%M:%S")
    transcription_file = current_date + '_' + data['filename'].replace(' ', '_') + '_Transcription.txt:'

    transcription_filepath = os.path.join(app.config['TRANSCRIPTION_FOLDER'], transcription_file)

    audio = AudioSegment.from_file(filepath)
    chunk_length_ms = 30000  # 30 seconds
    chunks = make_chunks(audio, chunk_length_ms)
    total_duration = len(audio)
    transcribed_duration = 0

    emit('total_duration', {'total': total_duration})
    
    f = open(transcription_filepath, 'a')
    for _i, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            chunk.export(temp_audio.name, format="wav")
            result = model.transcribe(temp_audio.name)
            text = result["text"].strip()
            transcribed_duration += len(chunk)
            f.write(text)
            emit('transcription_update', {
                'text': text,
                'progress': (transcribed_duration / total_duration) * 100
            })
        os.unlink(temp_audio.name)
    
    f.close()
    emit('transcription_complete')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TRANSCRIPTION_FOLDER'], exist_ok=True)
    socketio.run(app, debug=True)
