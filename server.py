#!/usr/bin/env python3


from flask import Flask, request, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 1.5 * 1024 * 1024 * 1024  # Max size 1.5GB

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload new File</h1>
    <form method="POST" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/connect', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return f'File successfully uploaded and saved at {file_path}'
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle server-side errors

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!", 200

if __name__ == '__main__':
    # Run the server on IP 10.10.1.40 and port 443 (with HTTPS, ensure SSL certs are in place)
    app.run(debug=True, host='10.10.1.40', port=5000)
