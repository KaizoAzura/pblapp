from flask import Flask, render_template, request, redirect, url_for, session
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ini_kunci_rahasia_123'

FOLDER_HASIL = 'static/hasil'
app.config['UPLOAD_FOLDER'] = FOLDER_HASIL

# Pastikan folder hasil ada
if not os.path.exists(FOLDER_HASIL):
    os.makedirs(FOLDER_HASIL)

@app.route('/')
def index():
    hasil_gambar = session.pop('hasil_gambar', None)
    nama_file_asli = session.pop('nama_file_asli', None)
    nama_file_grayscale = session.pop('nama_file_grayscale', None)
    return render_template(
        'index.html',
        hasil_gambar=hasil_gambar,
        nama_file_asli=nama_file_asli,
        nama_file_grayscale=nama_file_grayscale
    )

@app.route('/result')
def result():
    semua_file = os.listdir(FOLDER_HASIL)
    hasil_gambar = [f for f in semua_file if f.startswith('hasil_')]
    return render_template('result.html', hasil_gambar=hasil_gambar)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['gambar']
    if file:
        filename = secure_filename(file.filename)

        # Simpan gambar asli
        path_asli = os.path.join(FOLDER_HASIL, filename)
        file.save(path_asli)

        # Baca dan konversi ke grayscale
        img = cv2.imread(path_asli)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nama_gray = f"gray_{filename}"
        path_gray = os.path.join(FOLDER_HASIL, nama_gray)
        cv2.imwrite(path_gray, gray)

        # Deteksi tepi
        blur = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blur, 100, 200)
        nama_hasil = f"hasil_{filename}"
        path_hasil = os.path.join(FOLDER_HASIL, nama_hasil)
        cv2.imwrite(path_hasil, edges)

        # Simpan ke session
        session['nama_file_asli'] = filename
        session['nama_file_grayscale'] = nama_gray
        session['hasil_gambar'] = nama_hasil

        return redirect(url_for('index'))

    return 'No file uploaded', 400

if __name__ == '__main__':
    app.run(debug=True)
