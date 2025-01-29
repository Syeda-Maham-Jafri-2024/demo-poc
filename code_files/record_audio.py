import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading

# Global variables to manage recording
recording = False
audio_data = []
sample_rate = 44100  # Default sample rate (44.1 kHz)


def record_audio():
    """
    Function to start recording audio.
    """
    global recording, audio_data
    recording = True
    audio_data = []  # Reset audio data

    def callback(indata, frames, time, status):
        """
        Callback function to capture audio data.
        """
        if recording:
            audio_data.append(indata.copy())

    # Start recording using a Stream
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
        print("Recording started... Press Ctrl+C to stop.")
        while recording:
            sd.sleep(100)  # Keeps the stream running while recording


def stop_and_save(filepath="output.wav"):
    """
    Function to stop the recording and save the audio to a file at the specified path.
    """
    global recording, audio_data
    recording = False  # Stop the recording

    # Combine all recorded audio chunks into one array
    audio_data_combined = np.concatenate(audio_data, axis=0)

    # Save as a WAV file
    write(filepath, sample_rate, (audio_data_combined * 32767).astype(np.int16))
    print(f"Recording stopped and saved to {filepath}.")


# Test the recording functionality
def test_audio_recording():
    # Start recording in a thread
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()

    # The recording will keep running until you decide to stop it manually
    input("Press Enter to stop recording...")
    stop_and_save("audio_files/test_output.wav")  # Change path as needed


if __name__ == "__main__":
    test_audio_recording()
