import cv2 as cv

source = "rtsp://210.99.70.120:1935/live/cctv004.stream"
# source = 0  # 웹캠 테스트용

cap = cv.VideoCapture(source)

if not cap.isOpened():
    print("Video source cannot open")
    exit()

ret, frame = cap.read()
if not ret:
    print("Cannot read first frame")
    cap.release()
    exit()

height, width = frame.shape[:2]
fps = 20

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('record.avi', fourcc, fps, (width, height))

recording = False
flip_mode = False

while True:
    if flip_mode:
        show_frame = cv.flip(frame, 1)
    else:
        show_frame = frame.copy()

    if recording:
        cv.circle(show_frame, (30, 30), 10, (0, 0, 255), -1)
        out.write(show_frame)

    cv.imshow("Video Recorder", show_frame)

    key = cv.waitKey(1)

    if key == 27:
        break
    elif key == 32:
        recording = not recording
    elif key == ord('f'):
        flip_mode = not flip_mode

    ret, frame = cap.read()
    if not ret:
        print("Video stream ended or disconnected")
        break

cap.release()
out.release()
cv.destroyAllWindows()