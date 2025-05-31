
import cv2
import easyocr
import base64
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)
reader = easyocr.Reader(['en', 'ur'])
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def image_to_base64(image, ext=".jpg"):
    _, buffer = cv2.imencode(ext, image)
    return base64.b64encode(buffer).decode("utf-8")

@app.route("/", methods=["POST"])
def extract_cnic_from_base64():
    data = request.get_json()

    if "image_base64" not in data:
        return jsonify({"error": "Missing 'image_base64' in request"}), 400

    try:
       
        img_data = base64.b64decode(data["image_base64"])
        image_np = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

     
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_base64 = "No face detected"

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face = image_np[y:y+h, x:x+w]
            face_base64 = image_to_base64(face)

       
        results = reader.readtext(image_np)
        extracted_text = "\n".join([res[1] for res in results]) if results else "No text detected"

        return jsonify({
            "Extracted_Text": extracted_text,
            "Face_Image_Base64": face_base64
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
