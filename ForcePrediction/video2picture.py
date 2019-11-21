import cv2
import os


def video2picture(video, dir, name, ext='jpg'):
    cap = cv2.VideoCapture(video)
    os.makedirs(dir, exist_ok=True)
    path = os.path.join(dir, name)
    n_picture = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0
    while True:
        ret, picture = cap.read()
        if ret:
            picture = cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)  # grayscale
            cv2.imwrite('{}_{}.{}'.format(
                path, str(n).zfill(n_picture), ext), picture)
            n += 1
        else:
            return


video2picture('20191101/2019110110302.wmv', 'dataset_2', 'gray')
print('Finish')
