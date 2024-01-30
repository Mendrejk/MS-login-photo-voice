import threading
import time

import tkinter as tk

import numpy as np
import pyaudio
import wave


class AudioCaptureThread(threading.Thread):
    def __init__(self):
        super(AudioCaptureThread, self).__init__()
        self.p = pyaudio.PyAudio()
        self.running = False
        self.audio_data = None

    def run(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "../voice_sample.wav"

        frames = []

        self.running = True

        def callback(in_data, frame_count, time_info, status):
            self.audio_data = np.frombuffer(in_data, dtype=np.int16)
            frames.append(in_data)
            return in_data, pyaudio.paContinue

        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback=callback)

        stream.start_stream()

        start_time = time.time()
        while time.time() - start_time < RECORD_SECONDS:
            time.sleep(0.1)

        print("finished recording")
        stream.stop_stream()
        stream.close()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.running = False
        self.stop()

    def stop(self):
        self.running = False
        self.p.terminate()


class AudioCapture:
    def __init__(self, cavas: tk.Canvas):
        self.audio_thread = AudioCaptureThread()
        self.canvas = cavas

    def _update_canvas(self):
        audio_data = self.audio_thread.audio_data

        if audio_data is not None:
            max_val = np.max(audio_data)
            scaling_factor = 1 if max_val == 0 else max_val
            audio_data = (audio_data / scaling_factor) * (self.canvas.winfo_height() / 2)
            audio_data -= np.mean(audio_data)
            audio_data += self.canvas.winfo_height() / 2
            self.canvas.delete("all")
            for i in range(len(audio_data) - 1):
                self.canvas.create_line(i, audio_data[i], i + 1, audio_data[i + 1], fill="black")
        if self.audio_thread.running:
            self.canvas.after(1, self._update_canvas)

    def capture_audio(self):
        self.canvas.pack(side='left', expand=True)
        self.audio_thread.start()
        self._update_canvas()
