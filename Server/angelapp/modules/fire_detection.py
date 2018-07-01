import cv2
import numpy as np
import os

print(os.getcwd())

def detect(): 
    
    video_file = os.path.join(os.getcwd(), 'angelapp/modules/classification/Data/video.mp4')

    video = cv2.VideoCapture(video_file)

    count = 0
    num_frames = 0
    (grabbed, frame) = video.read()
    print(frame.shape)
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(os.path.join(os.getcwd(), 'angelapp/media/output.avi'), -1, 20.0, (frame.shape[1], frame.shape[0]))

    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
            break

        num_frames += 1

        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
        lower = [18, 50, 50]
        upper = [35, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(frame, hsv, mask=mask)
        out.write(output)
        no_red = cv2.countNonZero(mask)
        # cv2.imshow("output", output)
        #print("output:", frame)
        # print('asdasdasada')
        if int(no_red) > 20000:
            count += 1
            # print ('Fire detected')
        #print(int(no_red))
    #print("output:".format(mask))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    percent_fire = (count / num_frames) * 100
    if (percent_fire >= 10):
        print("Fire Detected")

    cv2.destroyAllWindows()
    # video.release()
    out.release()

    print('yooo', out)
    return (out, percent_fire >= 10)
