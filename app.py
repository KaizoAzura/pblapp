from flask import Flask, render_template, request, redirect, url_for, session
import cv2
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
app.secret_key = 'ini_kunci_rahasia_123'  # <<-- DI SINI

UPLOAD_FOLDER = 'static/hasil'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    hasil_gambar = session.pop('hasil_gambar', None)
    return render_template('index.html', hasil_gambar=hasil_gambar)

# result image route
@app.route('/result')
def result():
    hasil_folder = app.config['UPLOAD_FOLDER']
    semua_file = os.listdir(hasil_folder)
    
    hasil_gambar = [f for f in semua_file if f.startswith('hasil_')]
    
    return render_template('result.html', hasil_gambar=hasil_gambar)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['gambar']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(img, (5, 5), 1.4)
        edges = cv2.Canny(blur, 100, 200)

        hasil_filename = f"hasil_{filename}"
        hasil_path = os.path.join(app.config['UPLOAD_FOLDER'], hasil_filename)
        cv2.imwrite(hasil_path, edges)

        session['hasil_gambar'] = hasil_filename
        return redirect(url_for('index'))

    return 'No file uploaded', 400

if __name__ == '__main__':
    app.run(debug=True)
