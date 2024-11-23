import os
from datetime import datetime
import httpx
from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions, FileSource
import supabase
from supabase import create_client, Client
import os
from datetime import datetime
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
from time import sleep
import uuid

# Set your Supabase credentials (replace with your actual credentials)
SUPABASE_URL = 'https://.supabase.co'  # Replace with your Supabase URL
SUPABASE_KEY = ''
# Create a Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
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
# Function to insert transcription into the database
def insert_transcription(text: str):
    try:
        # Insert data into 'transcriptions' table
        data = {
            'id': str(uuid.uuid4()),
            'Transcript': text,
            'created_at': datetime.now().isoformat()  # Using UTC for the timestamp
        }

        # Check the response status

    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        print(f"Inserting data: {data}")
        response = supabase.table("transcripts").insert(data).execute()
        print(response)  # Check the response object

    except Exception as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response}")





API_KEY = ''


def DeepgramAdapter(AUDIO_FILE):
    try:
        # STEP 1 Create a Deepgram client using the API key
        config: DeepgramClientOptions = DeepgramClientOptions()
        deepgram: DeepgramClient = DeepgramClient(API_KEY, config)

        # STEP 2 Read the audio file into memory
        current_path = os.getcwd()
        print(current_path)

        with open(f"{current_path}/{AUDIO_FILE}", "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )

        # STEP 3 Transcribe the file (synchronously)
        before = datetime.now()
        response = deepgram.listen.rest.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        after = datetime.now()

        # STEP 4 Extract and print the transcript
        if hasattr(response, "to_dict"):
            response_dict = response.to_dict()

            # Navigate to the transcript (modify key path if needed)
            if "results" in response_dict and "channels" in response_dict["results"]:
                channel_data = response_dict["results"]["channels"]
                for channel in channel_data:
                    if "alternatives" in channel:
                        for alt in channel["alternatives"]:
                            if "transcript" in alt:
                                print(f"Transcript: {alt['transcript']}")

        difference = after - before
        print(f"Time elapsed: {difference.seconds} seconds")
        return alt['transcript']

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    record_audio(duration=10)
    sleep(3)
    transcribed_text = str(DeepgramAdapter("./recordings/recording.mp3"))

    # Define the file name
    file_name = "transcription.txt"

    # Write or append to the file
    if os.path.exists(file_name):
        with open(f'/app/output/{file_name}', "a") as file:  # Append mode
            file.write(transcribed_text)
            print(f"Appended to {file_name}")
    else:
        with open(f'/app/output/{file_name}', "w") as file:  # Write mode
            file.write(transcribed_text)
            print(f"Created and wrote to {file_name}")
        data = {
            "Transcript": f'{transcribed_text}'
        }

    insert_transcription(transcribed_text)
