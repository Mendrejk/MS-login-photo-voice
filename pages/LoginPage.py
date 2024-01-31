import os
from tkinter import ttk, messagebox
import tkinter as tk

from media import AudioCapture, VideoCapture, VoiceComparison, FaceComparison


class LoginPage:
    def __init__(self, root, show_start_page):
        self.root = root
        self.show_start_page = show_start_page
        self.audio_canvas = None
        self.video_canvas = None
        self.video_capture = None
        self.audio_capture = None
        self.username_entry = None
        self.capture_photo_button = None
        self.capture_audio_button = None
        self.login_button = None
        self.take_photo_button = None
        self.saved_photo = None

    def validate_username(self):
        username = self.username_entry.get()

        photo_file_path = f"{username}.jpg"
        audio_file_path = f"{username}.wav"

        # TODO: remove the True condition - it's just for testing
        if True or os.path.exists(photo_file_path) and os.path.exists(audio_file_path):
            self.capture_audio_button.config(state="normal")
            self.capture_photo_button.config(state="normal")
            self.login_button.config(state="normal")
        else:
            messagebox.showerror("Error", "Invalid username.")

    def capture_audio(self):
        if self.video_capture is not None:
            self.video_capture.stop()

        self.audio_capture = AudioCapture.AudioCapture(self.audio_canvas)
        self.audio_capture.capture_audio()

    def start_capturing_photo(self):
        if self.audio_capture is not None:
            self.audio_capture.stop()

        self.video_capture = VideoCapture.VideoCapture(self.video_canvas)
        self.video_capture.start_video_capture()

        self.take_photo_button.config(state="normal")

    def capture_photo(self):
        self.saved_photo = self.video_capture.take_photo()
        self.video_capture = None
        self.take_photo_button.config(state="disabled")

    def login(self):
        username = self.username_entry.get()

        photo_file_path = f"{username}.jpg"
        audio_file_path = f"{username}.wav"

        # Load the audio and photo data
        registered_audio_data = AudioCapture.load(audio_file_path)
        registered_photo_data = VideoCapture.load(photo_file_path)

        # Placeholder comparison methods
        audio_match = VoiceComparison.compare(registered_audio_data, self.audio_capture.frames)
        photo_match = FaceComparison.compare(registered_photo_data, self.saved_photo)

        if audio_match and photo_match:
            messagebox.showinfo("Success", "Login successful.")
        else:
            messagebox.showerror("Error", "Login failed.")

    def show(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack()

        username_button = ttk.Button(self.root, text="Confirm Username", command=self.validate_username)
        username_button.pack()

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

        self.take_photo_button = ttk.Button(video_frame, text="Take Photo", command=self.start_capturing_photo)
        self.take_photo_button.pack()
        self.take_photo_button.config(state="disabled")

        self.capture_audio_button = ttk.Button(self.root, text="Capture Voice", command=self.capture_audio)
        self.capture_audio_button.pack()
        self.capture_audio_button.config(state="disabled")

        self.capture_photo_button = ttk.Button(self.root, text="Capture Photo", command=self.start_capturing_photo)
        self.capture_photo_button.pack()
        self.capture_photo_button.config(state="disabled")

        back_button = ttk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack()

        self.login_button = ttk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()
        self.login_button.config(state="disabled")
