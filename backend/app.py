from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from moviepy import VideoFileClip
from datetime import datetime
import os
import time
import shutil

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

def compress_image(filepath: str, output_path: str, quality: int = 60):
    with Image.open(filepath) as img:
        img.save(output_path, optimize=True, quality=quality)

def compress_pdf(input_path: str, output_path: str):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, 'wb') as f:
        writer.write(f)

def compress_video(input_path: str, output_path: str):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, bitrate='500k', codec='libx264')

def gerar_timestamp():
    agora = datetime.now()
    return agora.strftime('%Y%m%d%H%M%S%f')[:-3]  # Retira os 3 últimos dígitos dos microssegundos para dar milissegundos

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')

    if len(files) == 1:
        file = files[0]

        timestamp = gerar_timestamp()
        original_filename = file.filename
        original_extension = os.path.splitext(original_filename)[1]

        public_download_name = f"[COMPRESSED]+{original_filename}"

        original_saved_name = f"{timestamp}[ORIGINAL]{original_extension}"
        original_path = os.path.join(UPLOAD_FOLDER, original_saved_name)
        file.save(original_path)

        compressed_saved_name = f"{timestamp}[COMPRESSED]{original_extension}"
        compressed_path = os.path.join(UPLOAD_FOLDER, compressed_saved_name)

        if original_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            compress_image(original_path, compressed_path)

        elif original_filename.lower().endswith('.pdf'):
            compress_pdf(original_path, compressed_path)

        elif original_filename.lower().endswith(('.mp4', '.mov', '.avi')):
            compress_video(original_path, compressed_path)

        else:
            shutil.copy(original_path, compressed_path)
        public_download_name = f"[COMPRESSED]+{original_filename}"

        return send_file(
            compressed_path,
            as_attachment=True,
            download_name=public_download_name
        )

    else:
        return jsonify({'erro': 'Ainda não suportamos múltiplos ficheiros para download automático'})

if __name__ == '__main__':
    app.run(debug=True)