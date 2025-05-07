import os
import binascii
import mimetypes
from mutagen.mp3 import MP3
from PyPDF2 import PdfReader
from PIL import Image

def analyze_file(filepath):
    result = {}

    # File metadata
    result['Filename'] = os.path.basename(filepath)
    result['File Size (bytes)'] = os.path.getsize(filepath)
    
    # Hex signature (first 20 bytes)
    with open(filepath, 'rb') as file:
        header = file.read(20)
        result['Hex Header'] = binascii.hexlify(header).decode()

    # File type from mimetypes
    mime_type, _ = mimetypes.guess_type(filepath)
    result['MIME Type'] = mime_type or 'Unknown'

    extension = os.path.splitext(filepath)[1].lower()

    # Additional info based on file type
    try:
        if extension in ['.mp4', '.mov', '.avi']:
            import cv2
            video = cv2.VideoCapture(filepath)
            frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video.get(cv2.CAP_PROP_FPS)
            duration = frames / fps if fps else 0
            result['Video Duration (s)'] = round(duration, 2)
            video.release()

        elif extension == '.mp3':
            audio = MP3(filepath)
            result['Audio Duration (s)'] = round(audio.info.length, 2)

        elif extension == '.pdf':
            reader = PdfReader(filepath)
            result['PDF Page Count'] = len(reader.pages)

        elif extension in ['.png', '.gif']:
            with Image.open(filepath) as img:
                result['Image Format'] = img.format
                result['Image Size'] = f"{img.width}x{img.height}"
    except Exception as e:
        result['Error'] = f"Analysis failed: {str(e)}"

    return result
