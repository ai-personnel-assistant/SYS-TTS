from flask import Flask, request, jsonify, send_file
import subprocess
import json
import os

app = Flask(__name__)


@app.route('/speak', methods=['POST'])
def speak_audio():
    if 'text' not in request.json or "id" not in request.json:
        return jsonify({ "status": 400, 'error': 'No data'}), 400
    
    audio_id = request.json['id']
    text = request.json['text']
    filepath = f"audio/output/{audio_id}.wav"
    model = "fr_FR_upmc/fr_FR-upmc-medium.onnx"

    if not os.path.exists("audio/output"):
        os.mkdir("audio/output")

    # Appel de la commande piper pour générer le fichier audio
    subprocess.run(f'echo "{text}" | piper --model models/{model} --speaker 1 --output_file {filepath}', shell=True)
    print(f"Audio file generated: {filepath}")
    return jsonify({'id': audio_id}), 200

@app.route('/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    filepath = f"audio/output/{audio_id}.wav"
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3800)
