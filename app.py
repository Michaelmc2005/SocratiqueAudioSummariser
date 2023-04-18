from flask import Flask, request, jsonify
import summarize  # Replace this with the name of your Python module containing the updated code
from flask_cors import CORS, cross_origin
app = Flask(__name__)

def cors_allow_all(f):
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    return wrapper

@app.route('/summarize', methods=['POST'])
@cross_origin()
def summarize_audio():
    try:
        audio_file = request.files['audio']
        summary = summarize.process_audio(audio_file)  # Replace this with the function that processes the audio and returns the summary
        return jsonify(summary=summary)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
