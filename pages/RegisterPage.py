from tkinter import ttk
import tkinter as tk

from media import AudioCapture, VideoCapture


class RegisterPage:
    def __init__(self, root, show_start_page):
        self.root = root
        self.show_start_page = show_start_page
        self.voice_canvas = None
        self.video_canvas = None
        self.video_capture = None
        self.audio_capture = None

    def register(self):
        pass
    #     username = self.entry_username.get()
    #     c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, voice_sample_path, photo_sample_path))
    #     conn.commit()

    def capture_photo(self):
        self.video_capture = VideoCapture.VideoCapture(self.video_canvas)
        self.video_capture.capture_photo()

    def capture_audio(self):
        self.audio_capture = AudioCapture.AudioCapture(self.voice_canvas)
        self.audio_capture.capture_audio()

    def show(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        username_entry = ttk.Entry(self.root)
        username_entry.pack()

        ttk.Button(self.root, text="Capture Voice", command=self.capture_audio)

        ttk.Button(self.root, text="Capture Photo", command=self.capture_photo)

        ttk.Button(self.root, text="Register", command=self.register)

        back_button = ttk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack()

        media_frame = ttk.Frame(self.root)
        media_frame.grid(row=2, column=1)

        self.voice_canvas = tk.Canvas(media_frame, width=800, height=800, highlightthickness=2, highlightbackground="red")
        self.video_canvas = tk.Canvas(media_frame, width=800, height=800, highlightthickness=2, highlightbackground="blue")