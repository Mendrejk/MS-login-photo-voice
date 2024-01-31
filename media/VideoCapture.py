import tkinter as tk

import cv2
import threading

from PIL import Image, ImageTk


def load(file_path):
    photo_data = cv2.imread(file_path)
    return photo_data


class VideoCaptureThread(threading.Thread):
    def __init__(self):
        super(VideoCaptureThread, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.running = False
        self.frame = None

    def run(self):
        self.running = True
        while self.running:
            # Capture frame-by-frame
            ret, frame = self.cam.read()

            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream
            ret, jpeg = cv2.imencode('.jpg', frame)
            # frame = jpeg.tobytes()
            self.frame = frame

            # Display the resulting frame
            # cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

    def stop(self):
        self.running = False
        self.cam.release()
        cv2.destroyAllWindows()


class VideoCapture:
    def __init__(self, canvas: tk.Canvas):
        self.video_thread = VideoCaptureThread()
        self.canvas: tk.Canvas = canvas

    def _update_canvas(self):
        frame = self.video_thread.frame
        if frame is not None:
            # Convert the image from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

            # Add a PhotoImage to the Canvas
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            # Save a reference to the PhotoImage, otherwise it's garbage collected
            self.canvas.photo = photo

        # Call the _update_canvas method again after 1 ms if the video thread is still running
        if self.video_thread.running:
            self.canvas.after(1, self._update_canvas)

    def start_video_capture(self):
        # Create a canvas for the video capture
        self.canvas.pack(side='left', expand=True)

        # Start the video capture thread
        self.video_thread.start()

        # Start the function to update the video canvas
        self._update_canvas()

    def take_photo(self):
        # stop capturing video
        self.stop()

        if self.video_thread.frame is None:
            return None

        return self.video_thread.frame

    def stop(self):
        self.video_thread.stop()

    def save(self, file_path):
        if self.video_thread.frame is not None:
            cv2.imwrite(file_path, self.video_thread.frame)
