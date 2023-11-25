from flask import Flask, render_template, request
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os

app = Flask(__name__)

def load_image(image_path):
    return cv2.imread(image_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imageauthenticity')
def image_authenticity():
    return render_template('imageauthenticity.html')

@app.route('/similarity')
def similarity():
    return render_template('similarity.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    technique = "copy-paste"
    file1 = request.files['image1']
    file2 = request.files['image2']

    if file1 and file2:
        # Define the paths to save the uploaded images
        original_image_path = 'static/original.png'
        suspicious_image_path = 'static/suspicious.png'

        # Save the uploaded images
        file1.save(original_image_path)
        file2.save(suspicious_image_path)

        # Load and process the images
        original = load_image(original_image_path)
        suspicious = load_image(suspicious_image_path)

        threshold = 0.8
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        suspicious_gray = cv2.cvtColor(suspicious, cv2.COLOR_BGR2GRAY)
        similarity_score = ssim(original_gray, suspicious_gray)

        if similarity_score < threshold:
            if technique == "copy-paste":
                print("Copy-paste forgery detected.")
            else:
                print("Forgery detected, but the technique is unknown.")
            similarity_score_percent = int(similarity_score * 100)
            return render_template('result.html', similarity_score=similarity_score_percent, original_image=original_image_path, suspicious_image=suspicious_image_path)
        else:
            return "Image not suspicious enough."
    else:
        return "NO IMAGES FOUND"

@app.route('/upload1', methods=['POST'])
def upload_file1():
    file1 = request.files['image1']
    file2 = request.files['image2']

    if file1 and file2:
        # Define the paths to save the uploaded images
        original_image_path = 'static/image.png'
        suspicious_image_path = 'static/image1.png'

        # Save the uploaded images
        file1.save(original_image_path)
        file2.save(suspicious_image_path)

        # Check image similarity
        result = check_similarity(original_image_path, suspicious_image_path)
        if result:
            print("The images are similar.")
            return "The images are similar."
        else:
            print("The images are different.")
            return "The images are different."
    else:
        return "Image not found."


def check_similarity(img1_path, img2_path):
    tolerance = 2

    if not (os.path.exists(img1_path) and os.path.exists(img2_path)):
        raise ValueError("One or both image files do not exist.")

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1.shape == img2.shape:
        diff = cv2.absdiff(img1, img2)
        b, g, r = cv2.split(diff)

        if (np.all(b <= tolerance) and np.all(g <= tolerance) and np.all(r <= tolerance)):
            return True

    return False

if __name__ == '__main__':
    app.run()
