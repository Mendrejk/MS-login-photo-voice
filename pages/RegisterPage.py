import os
from tkinter import ttk, messagebox
import tkinter as tk

from media import AudioCapture, VideoCapture


class RegisterPage:
    def __init__(self, root, show_start_page):
        self.root = root
        self.show_start_page = show_start_page
        self.audio_canvas = None
        self.video_canvas = None
        self.video_capture = None
        self.audio_capture = None
        self.saved_photo = None
        self.save_photo_button = None
        self.username_entry = None

    def register(self):
        username = self.username_entry.get()

        # Check if the username is not empty
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        photo_file_path = f"{username}.jpg"
        audio_file_path = f"{username}.wav"

        # Check if the files do not exist
        if os.path.exists(photo_file_path) or os.path.exists(audio_file_path):
            messagebox.showerror("Error", "Files with the inputted username and .jpg or .wav extensions currently exist.")
            return

        self.video_capture.save(photo_file_path)
        self.audio_capture.save(audio_file_path)

        self.show_start_page()

    def start_capturing_photo(self):
        if self.audio_capture is not None:
            self.audio_capture.stop()

        self.video_capture = VideoCapture.VideoCapture(self.video_canvas)
        self.video_capture.start_video_capture()

        self.save_photo_button.config(state="normal")

    def capture_photo(self):
        self.saved_photo = self.video_capture.take_photo()
        self.video_capture = None
        self.save_photo_button.config(state="disabled")

    def capture_audio(self):
        if self.video_capture is not None:
            self.video_capture.stop()

        self.audio_capture = AudioCapture.AudioCapture(self.audio_canvas)
        self.audio_capture.capture_audio()

    def show(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack()

        ttk.Button(self.root, text="Capture Voice", command=self.capture_audio).pack()

        ttk.Button(self.root, text="Capture Photo", command=self.start_capturing_photo).pack()

        ttk.Button(self.root, text="Register", command=self.register).pack()

        back_button = ttk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack()

        media_frame = ttk.Frame(self.root)
        media_frame.pack()

        self.audio_canvas = tk.Canvas(media_frame, width=800, height=800, highlightthickness=2,
                                      highlightbackground="red")
        self.audio_canvas.pack(side='left')

        video_frame = ttk.Frame(media_frame)
        video_frame.pack(side='left')

        self.video_canvas = tk.Canvas(video_frame, width=800, height=800, highlightthickness=2,
                                      highlightbackground="blue")
        self.video_canvas.pack()

        self.save_photo_button = ttk.Button(video_frame, text="Save Photo", command=self.capture_photo)
        self.save_photo_button.pack()
        self.save_photo_button.config(state="disabled")
