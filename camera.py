import cv2
import os
import time

if not os.path.exists('images'):
    os.makedirs('images')

cap = cv2.VideoCapture(0)
countdown_time = 5

start_time = time.time()
while True:
    ret, frame = cap.read()


    
    if not ret:
        print("Failed to grab frame")
        break



    elapsed_time = time.time() - start_time
    remaining_time = int(countdown_time - elapsed_time)

    if remaining_time >= 0:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(remaining_time), (50, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        img_name = f"images/captured_image_{int(time.time())}.png"
        cv2.imwrite(img_name, frame)
        print(f"Image saved to {img_name}")
        break

    cv2.imshow('Countdown Live Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
