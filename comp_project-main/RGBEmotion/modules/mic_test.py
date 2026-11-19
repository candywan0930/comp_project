import pyaudio
import numpy as np
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording...")
try:
    while True:
        data = stream.read(CHUNK)
        # 轉成數組
        audio_np = np.frombuffer(data, dtype=np.int16)
        # RMS 音量
        rms = np.sqrt(np.mean(np.square(audio_np.astype(np.float32))))
        print(f"Volume: {rms:.1f}")
        time.sleep(0.3)
except KeyboardInterrupt:
    print("stop recording...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
