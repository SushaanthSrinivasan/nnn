import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

def record_audio(output_dir="./recordings", filename="recording.mp3", duration=10, samplerate=48000):
    """
    Record audio and save as an MP3 file.
    
    Parameters:
        output_dir (str): Directory to save the recording.
        filename (str): Name of the output MP3 file.
        duration (int): Duration of the recording in seconds.
        samplerate (int): Sample rate for recording.
    """
    try:
        # Set the device to sof-hda-dsp (index 4)
        sd.default.device = 4
        print(f"Using device: {sd.query_devices(sd.default.device)}")

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filepath = os.path.join(output_dir, filename)
        print(f"Recording for {duration} seconds with sample rate {samplerate} Hz...")

        # Record audio
        audio_data = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=2,  # Use 2 channels for stereo
            dtype="int16"
        )
        sd.wait()  # Wait until the recording is finished
        print("Recording complete. Saving to temporary WAV file...")

        # Save as a temporary WAV file
        wav_filename = os.path.join(output_dir, "temp.wav")
        write(wav_filename, samplerate, audio_data)

        # Convert WAV to MP3
        print("Converting WAV to MP3...")
        audio = AudioSegment.from_wav(wav_filename)
        audio.export(f'/app/{filepath}', format="mp3")
        os.remove(wav_filename)  # Clean up the temporary file

        print(f"Saved recording as {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    record_audio(duration=10)
