import cv2
import numpy as np
from paddleocr import PaddleOCR
from datetime import datetime

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def process_video(video_path): 1usage
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = ocr.ocr(rgb_frame, cls=True)

        detected_texts = ""

        if results:
            for line in results:
                if line:
                    for word_info in line:
                        if word_info and len(word_info) >= 2:
                            text = word_info[1][0]
                            detected_texts += text + " "

                            cv2.polylines(frame, pts=[np.int32(box)], isClosed=True, color=(0, 255, 0), thickness=2)

                            cv2.putText(frame, text, org=(int(box[0][0]), int(box[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color=(0, 0, 255), thickness=2)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.putText(frame, text= "Licensed Plates:", org=(10, 80), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
        cv2.putText(frame, text= detected_text.strip(), org=(10, 150), cv2.FONT_HERSHEY_SIMPLEX, fontScale=2.5, color=(0, 255, 0), thickness=8)

        cv2.imshow(winname= 'License Plate Recognition', cv2.resize(frame, dsize= (640, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_file_path = "path_to_your_video.mp4"
    process_video(video_file_path)