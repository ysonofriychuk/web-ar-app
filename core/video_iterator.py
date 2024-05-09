import datetime
import cv2
import threading
import time


class VideoIterator:
    def __init__(self, path="videos/default.mp4"):
        self.__vf = cv2.VideoCapture(path)
        self.__cur_frame = None
        self.__lock = threading.Lock()

        # Получаем FPS и вычисляем интервал обновления кадра
        fps = self.__vf.get(cv2.CAP_PROP_FPS) if self.__vf.get(cv2.CAP_PROP_FPS) > 0 else 60
        self.__frame_interval = 1.0 / fps

        # Запускаем поток для обновления кадра
        self.__running = True
        self.__thread = threading.Thread(target=self.__update_frame)
        self.__thread.start()

    def __del__(self):
        self.__running = False
        self.__thread.join()
        self.__vf.release()

    def __update_frame(self):
        while self.__running:
            with self.__lock:
                grabbed, frame = self.__vf.read()
                if not grabbed:
                    # Если достигнут конец файла, начинаем сначала
                    self.__vf.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    grabbed, frame = self.__vf.read()
                    if not grabbed:
                        continue
                self.__cur_frame = frame
            time.sleep(self.__frame_interval)

    def source(self):
        with self.__lock:
            return self.__cur_frame
