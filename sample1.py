import cv2
import numpy as np
from paddleocr import PaddleOCR
from datetime import datetime

ocr = PaddleOCR(use_textline_orientation=True, lang='en')

def process_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = ocr.predict(rgb_frame)

        detected_texts = ""

        if results:
            for res in results:
                boxes = res['dt_polys']
                texts = res['rec_texts']

                for box, text in zip(boxes, texts):

                    detected_texts += text + " "

                    cv2.polylines(frame, [np.int32(box)], True, (0,255,0), 2)

                    cv2.putText(frame, text,
                                (int(box[0][0]), int(box[0][1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0,0,255), 2)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cv2.putText(frame, current_time, (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.putText(frame, "Licensed Plates:", (10,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, detected_texts.strip(), (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,255,0), 8)

        cv2.imshow("License Plate Recognition", cv2.resize(frame,(640,480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()
