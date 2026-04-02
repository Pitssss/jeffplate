import cv2
import easyocr
import csv
import os

# --- CONFIGURATION ---
frameWidth = 1000  
frameHeight = 480 
minArea = 500
db_file = 'database.csv'

# --- 1. SETUP OFFLINE DATABASE ---
known_plates = []

def load_database():
    global known_plates
    known_plates = [] # Clear list
    
    # We use absolute path for database too, just to be safe
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, db_file)

    if os.path.exists(db_path):
        with open(db_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row: 
                    known_plates.append(row[0].replace(" ", "").upper())
        print(f"Database Loaded: {known_plates}")
    else:
        print("Database file not found. Creating a new one...")
        with open(db_path, 'w') as f:
            pass 

load_database()

# --- 2. INITIALIZE OCR ---
print("Initializing OCR Engine...") 
reader = easyocr.Reader(['en'], gpu=False) 

# --- 3. VIDEO CAPTURE & XML SETUP (FIXED) ---

# Find the absolute path to the XML file
current_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(current_dir, "haarcascade_russian_plate_number.xml")

# Load the cascade using the full path
plateCascade = cv2.CascadeClassifier(xml_path)

# CHECK: Did it load correctly?
if plateCascade.empty():
    print("--------------------------------------------------")
    print("CRITICAL ERROR: The XML file was not found!")
    print(f"I tried to look here: {xml_path}")
    print("Please make sure 'haarcascade_russian_plate_number.xml' is inside that folder.")
    print("--------------------------------------------------")
    exit() # Stop program to prevent crash

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
count = 0

print("System Ready. Press 's' to save/scan.")

while True:
    success, img = cap.read()
    if not success:
        break
        
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    # Default color (Red - Unauthorized/Scanning)
    box_color = (0, 0, 255) 
    status_text = "Scanning..."

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            imgRoi = img[y:y+h, x:x+w]
            
            # --- REAL-TIME RECOGNITION BLOCK ---
            try:
                output = reader.readtext(imgRoi)
                detected_text = ""
                for result in output:
                    detected_text += result[1]
                
                clean_text = detected_text.replace(" ", "").upper()
                
                if clean_text in known_plates:
                    box_color = (0, 255, 0) # Green
                    status_text = f"AUTHORIZED: {clean_text}"
                else:
                    box_color = (0, 0, 255) # Red
                    status_text = f"UNAUTHORIZED: {clean_text}"
                    
            except Exception as e:
                print("OCR Error:", e)

            cv2.rectangle(img, (x, y), (x + w, y + h), box_color, 2)
            cv2.putText(img, status_text, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, box_color, 2)
            cv2.imshow("Number Plate", imgRoi)

    cv2.imshow("Result", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and 'imgRoi' in locals():
        # Ensure IMAGES folder exists
        images_dir = os.path.join(current_dir, "IMAGES")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
            
        cv2.imwrite(os.path.join(images_dir, f"{str(count)}.jpg"), imgRoi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (15, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1
        
    elif key == ord('q'):
        break