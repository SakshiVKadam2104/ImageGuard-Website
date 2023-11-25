import cv2
from skimage.metrics import structural_similarity as ssim

def load_image(image_path):
    return cv2.imread(image_path)

def detect_image_forgery(original_image, suspicious_image, threshold=0.9, technique="copy-paste"):
    original = load_image(original_image)
    suspicious = load_image(suspicious_image)

    if original is None or suspicious is None:
        print("Error: Unable to load one or both of the images.")
        return

    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    suspicious_gray = cv2.cvtColor(suspicious, cv2.COLOR_BGR2GRAY)

    similarity_score = ssim(original_gray, suspicious_gray)

    if similarity_score < threshold:
        # Detect the proper technique
        if technique == "copy-paste":
            # Add your copy-paste detection algorithm here
            print("Copy-paste forgery detected.")
        elif technique == "splicing":
            # Add your splicing detection algorithm here
            print("Splicing forgery detected.")
        else:
            # Use a general forgery detection algorithm
            print("Forgery detected, but the technique is unknown.")
    else:
        print("No forgery detected.")
    print(f"Similarity Score: {similarity_score}")

if __name__ == "__main__":
    original_image_path = input("Enter the path to the original image: ")
    suspicious_image_path = input("Enter the path to the suspicious image: ")
    similarity_threshold = float(input("Enter the similarity threshold (e.g., 0.9): "))
    technique = input("Enter the forgery technique (e.g., copy-paste, splicing): ")

    detect_image_forgery(original_image_path, suspicious_image_path, similarity_threshold, technique)
