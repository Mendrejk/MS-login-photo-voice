import tkinter as tk

import cv2
import threading

from PIL import Image, ImageTk


class VideoCaptureThread(threading.Thread):
    def __init__(self):
        super(VideoCaptureThread, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.running = False
        self.frame = None

    def run(self):
        self.running = True
        img_counter = 0

        while self.running:
            ret, frame = self.cam.read()
            self.frame = frame
            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                self.stop()
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
            # elif the window is closed with the X button
            elif cv2.getWindowProperty('frame', 0) == -1:
                self.stop()

    def stop(self):
        self.running = False
        self.cam.release()
        cv2.destroyAllWindows()


class VideoCapture:
    def __init__(self, canvas: tk.Canvas):
        self.video_thread = VideoCaptureThread()
        self.canvas: tk.Canvas = canvas
        self.frame = None

    def _update_canvas(self):
        frame = self.video_thread.frame
        if frame is not None:
            # Convert the image from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the image from OpenCV to PIL format
            image = Image.fromarray(frame)

            # Convert the image from PIL to PhotoImage format
            image = ImageTk.PhotoImage(image)

            # Clear the canvas and create a new image item
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=image, anchor='nw')

        if self.video_thread.running:
            self.canvas.after(1, self._update_canvas, self.canvas)  # Update the canvas every 1 ms

    def capture_photo(self):
        # Create a canvas for the video capture
        self.canvas.pack(side='left', expand=True)

        # Start the video capture thread
        self.video_thread.start()

        # Start the function to update the video canvas
        self._update_canvas()
