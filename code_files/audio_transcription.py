import librosa
import noisereduce as nr
from scipy.signal import butter, lfilter
import soundfile as sf
from pydub import AudioSegment
import os

import whisper


def convert_to_wav(input_audio_path):

    file_extension = os.path.splitext(input_audio_path)[1].lower()

    if file_extension == ".wav":
        return input_audio_path

    print("Converting audio to .wav format...")
    audio = AudioSegment.from_file(input_audio_path)
    wav_output_path = os.path.join(
        "output_files/audio_outputs/converted_audios",
        os.path.basename(input_audio_path).replace(file_extension, ".wav"),
    )
    wav_output_path = os.path.normpath(wav_output_path)
    audio.export(wav_output_path, format="wav")
    print(f"Conversion complete: {wav_output_path}")
    return wav_output_path


def preprocess_audio(wav_audio_path, output_audio_path, target_sample_rate=16000):

    print("Loading audio...")
    audio, sr = librosa.load(wav_audio_path, sr=target_sample_rate)

    print("Trimming silence...")
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=20)

    print("Normalizing audio...")
    audio_normalized = librosa.util.normalize(audio_trimmed)

    print("Reducing background noise...")
    audio_denoised = nr.reduce_noise(y=audio_normalized, sr=sr, prop_decrease=0.8)

    print("Applying bandpass filter...")
    audio_filtered = bandpass_filter(audio_denoised, lowcut=300, highcut=3400, fs=sr)

    print("Saving processed audio...")
    sf.write(output_audio_path, audio_filtered, sr)

    print("Audio preprocessing complete.")
    return output_audio_path


def bandpass_filter(audio, lowcut, highcut, fs, order=5):

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    filtered_audio = lfilter(b, a, audio)
    return filtered_audio


print("converting audio to text")

import time
from openai import OpenAI


def split_audio(wav_audio_path, chunk_length_ms=5 * 60 * 1000):
    audio = AudioSegment.from_wav(wav_audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunk_path = (
            f"{os.path.splitext(wav_audio_path)[0]}_chunk_{i//chunk_length_ms}.wav"
        )
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def audio_to_text_with_openai(input_audio_path):
    wav_audio_path = convert_to_wav(input_audio_path)
    print(f"input audio for transcription: {wav_audio_path}")
    audio_file_name = os.path.basename(wav_audio_path)
    processed_audio_path = os.path.join(
        "output_files/audio_outputs/processed_audios", audio_file_name
    )

    print(f"Processed audio: {processed_audio_path}")
    audio_path = preprocess_audio(
        wav_audio_path, processed_audio_path, target_sample_rate=16000
    )
    print(f"Audio passed to whisper model: {processed_audio_path}")
    # ---------------------chunking the audio ---------------------------------------
    audio_length = AudioSegment.from_file(audio_path).duration_seconds
    print(f"Audio length: {audio_length} seconds")
    chunked_audio_paths = []
    if audio_length > 300:
        print("Audio too long, splitting into chunks...")
        chunked_audio_paths = split_audio(audio_path)
    else:
        chunked_audio_paths = [audio_path]

    client = OpenAI(api_key="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")
    full_transcription = ""

    start_time = time.time()
    for chunk_path in chunked_audio_paths:

        print(f"Transcribing chunk: {chunk_path}")

        with open(chunk_path, "rb") as audio_file:
            transcription = client.audio.translations.create(
                model="whisper-1", file=audio_file
            )
        full_transcription += transcription.text + "\n"
    end_time = time.time()
    transcription_time = end_time - start_time

    print(f"Time taken for transcription: {transcription_time:.2f} seconds")
    print("Transcription complete.")
    return full_transcription


# # model = whisper.load_model("large")
# start_time = time.time()
# # transcription_result = model.transcribe(audio_path)
# with open(audio_path, "rb") as audio_file:
#     transcription = client.audio.translations.create(
#         model="whisper-1", file=audio_file
#     )

# # Calculate the time taken
# end_time = time.time()
# transcription_time = end_time - start_time

# # Print the time taken for transcription
# print(f"Time taken for transcription: {transcription_time:.2f} seconds")

# # Get the transcription text
# output_text = transcription.text
# # output_text = transcription_result["text"]
