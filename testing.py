import cv2
import numpy as np
import easyocr
import csv
import os
from datetime import datetime

# --- FORCE STABLE CONNECTION (TCP) ---
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

# --- CONFIGURATION ---
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
minArea = 1000
db_file = 'database.csv'

# GUI Constants
CAM_X, CAM_Y = 50, 150
CAM_W, CAM_H = 1200, 700
SIDEBAR_X = 1300

# --- EXIT BUTTON COORDINATES ---
EXIT_BTN_W, EXIT_BTN_H = 220, 60
EXIT_BTN_X1 = CANVAS_WIDTH - EXIT_BTN_W - 30
EXIT_BTN_Y1 = 20
EXIT_BTN_X2 = EXIT_BTN_X1 + EXIT_BTN_W
EXIT_BTN_Y2 = EXIT_BTN_Y1 + EXIT_BTN_H

def handle_clicks(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if EXIT_BTN_X1 <= x <= EXIT_BTN_X2 and EXIT_BTN_Y1 <= y <= EXIT_BTN_Y2:
            print("System Shutdown via Exit Button.")
            os._exit(0)

# --- 1. SETUP DATABASE ----
known_plates = []
def load_database():
    global known_plates
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, db_file)
    if os.path.exists(db_path):
        with open(db_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row: known_plates.append(row[0].replace(" ", "").upper())
    else:
        with open(db_path, 'w') as f: pass

load_database()

# --- 2. INITIALIZE OCR ---
reader = easyocr.Reader(['en'], gpu=False) 

# --- 3. VIDEO CAPTURE & CASCADE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(current_dir, "haarcascade_russian_plate_number.xml")
plateCascade = cv2.CascadeClassifier(xml_path)

# Using Sub-stream (102) for better stability over network
# REPLACE 'admin' and 'your_password'
camera_url = "rtsp://admin:Dreamteam2026@192.168.1.64:554/Streaming/Channels/102"

cap = cv2.VideoCapture(camera_url)

# Set a small buffer to prevent lag/decoding errors
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Global Variables
last_detected_plate = "--------"
last_status = "Scanning"
status_color = (150, 150, 150)
plate_crop = np.zeros((120, 350, 3), np.uint8)
log_entry = ["-", "-", "-"]

win_name = "ST. MATTHEW ANPR - FULLSCREEN"
cv2.namedWindow(win_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback(win_name, handle_clicks)

while True:
    success, img = cap.read()
    
    # If a frame fails, try to grab the next one instead of crashing
    if not success:
        print("Frame drop... retrying")
        continue 
    
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, 3), 40, dtype=np.uint8)

    # Header Bar
    cv2.rectangle(canvas, (0, 0), (CANVAS_WIDTH, 100), (0, 69, 255), -1)
    cv2.putText(canvas, "ST. MATTHEW ANPR SYSTEM", (600, 70), 
                cv2.FONT_HERSHEY_DUPLEX, 2.2, (255, 255, 255), 3)

    # Exit Button
    cv2.rectangle(canvas, (EXIT_BTN_X1, EXIT_BTN_Y1), (EXIT_BTN_X2, EXIT_BTN_Y2), (20, 20, 180), -1)
    cv2.rectangle(canvas, (EXIT_BTN_X1, EXIT_BTN_Y1), (EXIT_BTN_X2, EXIT_BTN_Y2), (255, 255, 255), 2)
    cv2.putText(canvas, "EXIT SYSTEM", (EXIT_BTN_X1 + 25, EXIT_BTN_Y1 + 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        if w * h > minArea:
            imgRoi = img[y:y+h, x:x+w]
            plate_crop = cv2.resize(imgRoi, (350, 120))
            
            try:
                # OCR can be slow on CPU; this is where the stream usually "piles up"
                output = reader.readtext(imgRoi)
                if output:
                    last_detected_plate = output[0][1].replace(" ", "").upper()
                    if last_detected_plate in known_plates:
                        last_status = "AUTHORIZED"
                        status_color = (0, 255, 0)
                    else:
                        last_status = "UNAUTHORIZED"
                        status_color = (0, 0, 255)
                    log_entry = [last_detected_plate, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "IN"]
            except: pass
            cv2.rectangle(img, (x, y), (x + w, y + h), status_color, 3)

    # 1. Camera Feed
    img_resized = cv2.resize(img, (CAM_W, CAM_H))
    canvas[CAM_Y : CAM_Y+CAM_H, CAM_X : CAM_X+CAM_W] = img_resized
    cv2.rectangle(canvas, (CAM_X, CAM_Y), (CAM_X + CAM_W, CAM_Y + CAM_H), (200, 200, 200), 2)
    cv2.putText(canvas, "LIVE CAMERA VIEW", (CAM_X, CAM_Y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 2. Output Panel
    cv2.putText(canvas, "DETECTION LOG", (SIDEBAR_X, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.rectangle(canvas, (SIDEBAR_X, 220), (SIDEBAR_X + 350, 340), (255, 255, 255), -1)
    canvas[220:340, SIDEBAR_X : SIDEBAR_X+350] = plate_crop 
    
    cv2.putText(canvas, "PLATE NUMBER:", (SIDEBAR_X, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
    cv2.putText(canvas, last_detected_plate, (SIDEBAR_X, 470), cv2.FONT_HERSHEY_DUPLEX, 2.5, (180, 100, 255), 3)
    cv2.putText(canvas, "STATUS:", (SIDEBAR_X, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
    cv2.putText(canvas, last_status, (SIDEBAR_X, 630), cv2.FONT_HERSHEY_DUPLEX, 2.5, status_color, 4)

    # 3. Bottom Table
    table_y = 880
    cv2.rectangle(canvas, (CAM_X, table_y), (CANVAS_WIDTH - 50, table_y + 150), (30, 30, 30), -1)
    cv2.rectangle(canvas, (CAM_X, table_y), (CANVAS_WIDTH - 50, table_y + 50), (80, 80, 80), -1)
    
    headers = ["VEHICLE NO.", "TIMESTAMP", "GATE STATUS"]
    for i, h_text in enumerate(headers):
        cv2.putText(canvas, h_text, (CAM_X + 50 + (i*600), table_y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    cv2.putText(canvas, log_entry[0], (CAM_X + 50, table_y + 110), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.putText(canvas, log_entry[1], (CAM_X + 650, table_y + 110), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.putText(canvas, log_entry[2], (CAM_X + 1250, table_y + 110), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    cv2.imshow(win_name, canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()