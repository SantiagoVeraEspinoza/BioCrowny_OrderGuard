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
    return render_template('packagescan.html') #ActCantidad index packagescan

@app.route('/packagescan') # Roger - Renderizar HTML de scaneo de orden
def home2():
    return render_template('packagescan.html')

@app.route('/orderdetails/<string:order_id>') # Roger - Crear la pagina de detalles con base a la ID de la orden
def order_details(order_id):
    return render_template('order-details.html', order_id=order_id)

@app.route('/ActCantidad/<int:order_id>/<int:cantidad_Total>/<int:cantidad_Escaneada>') #Endpoint para ir a la página de actualizar cantidad 
def act_cantidad(order_id, cantidad_Total, cantidad_Escaneada): 
    return render_template('ActCantidad.html', order_id=order_id, cantidad_Total=cantidad_Total, cantidad_Escaneada=cantidad_Escaneada)  

@app.route('/scan', methods=['POST']) #Endpoint para escanear el QR y obtener la información
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
        
        type = data.split()[0] #Que tipo de qr es ?
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
        
       # type = orden #Que tipo de qr es ?
        CantidadEscaneada = 5
        id = 1
        
        api_url = f"http://localhost:3000/{id}/{CantidadEscaneada}"  # Cambia esto por tu URL
        
        # Hacer la solicitud PUT
        response = requests.put(api_url)

        if response.status_code == 200:
            return {
                "Exito"
            }
        else:
            return {
                "Sin exito"
            }

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500


@app.route('/updateOrden/<int:can_Esc>/<int:id_Orden>', methods=['PUT']) #Endpoint para actualizar la cantidad escaneada
def updateOrden(can_Esc, id_Orden): 
    try:
        file = request.files.get('qr_code')
        if not file:
            return {"error": "No file uploaded"}, 400

        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return {"error": "Invalid file type. Please upload a PNG or JPG image."}, 400

        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            return {"error": "Failed to read image. Ensure the file is a valid image."}, 400

        # Convert to grayscale for better QR detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)

        # Detect QR Code
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(filtered)

        if bbox is None or not data:
            return {"error": "No QR code detected. Ensure proper lighting, clear image, and avoid reflections."}, 400

        if not re.search(r'((producto)|(orden)|(paquete))\s\d+', data):
            return {"error": "Invalid QR code, please provide a valid BioCrowny Code."}, 400

        tipo_qr = "orden"
        cantidadEscaneada = can_Esc #Cantidad escaneada de la orden
        id = id_Orden #Id de la orden

        # API endpoint correcto
        api_url = f"http://localhost:3000/orden/{id}/{cantidadEscaneada}"  
        # URL QUE DA {"error":"Error al actualizar: 404 Client Error: Not Found for url: http://localhost:3000/orden/2/5"}

        payload = {"id": id, "CantidadEscaneada": cantidadEscaneada}

        # Hacer la solicitud PUT
        response = requests.put(api_url, json=payload)
        response.raise_for_status()  # Si hay error, lanza una excepción
        cantNueva = str(cantidadEscaneada + 1)

        return {"mensaje": "Cantidad escaneada actualizada correctamente a "+cantNueva}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error al actualizar: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}, 500


@app.route('/scanpackage', methods=['POST']) # Llamada de API por Roger para escanear paquete y conseguir sus ordenes
def scanpackage_qr(): 
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
        
        if not re.search(r'^paquete\s\d+$', data):
            return "Invalid QR code, please provide a valid package QR code. ", 400

        type = data.split()[0]
        id = data.split()[1]
        
        api_url = f"http://localhost:3000/orden/{id}"  # Cambia esto por tu URL
        
        # Hacer la solicitud GET
        response = requests.get(api_url)
        data = json.loads(response.text)

        print(data)

        print(response.text)

        return_data = "Data not available..."

        if type == 'paquete': 
            return_data = data #['OrderID']
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return f"{return_data}"
        else:
            return f"QR Code Data: {data}\nFailed to send request: {response.status_code}"
    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
