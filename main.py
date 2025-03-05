from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
import requests
import re
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_qr():
    try:
        file = request.files.get('qr_code')
        if not file:
            return "No file uploaded", 400
        
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return "Invalid file type. Please upload a PNG or JPG image.", 400
        
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return "Failed to read image. Ensure the file is a valid image.", 400

        # Convert to grayscale for better QR detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filtering to preserve edges while reducing noise
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)

        # Detect QR Code
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(filtered)

        # Debug: Save processed image for manual inspection
        cv2.imwrite("debug_qr.png", filtered)
        
        # Debugging step: Check if OpenCV detects a QR code at all
        if bbox is not None:
            for point in bbox:
                cv2.circle(img, tuple(map(int, point[0])), 5, (0, 255, 0), -1)
            cv2.imwrite("debug_bbox.png", img)  # Save image with detected QR
        
        if bbox is None or not data:
            return "No QR code detected. Ensure proper lighting, clear image, and avoid reflections.", 400
        
        if not re.search(r'((producto)|(orden)|(paquete))\s\d+', data):
            return "Invalid QR code, please provide a valid BioCrowny Code.", 400
        
        type = data.split()[0]
        id = data.split()[1]
        
        api_url = f"http://localhost:3000/{type}/{id}"  # Cambia esto por tu URL
        
        # Hacer la solicitud GET
        response = requests.get(api_url)
        data = json.loads(response.text)

        return_data = "Data not available..."
        if type == 'producto':
            return_data = data['Nombre']
        if type == 'paquete':
            return_data = data
        if type == 'orden':
            return_data = data
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return f"{return_data}"
        else:
            return f"QR Code Data: {data}\nFailed to send request: {response.status_code}"
    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
