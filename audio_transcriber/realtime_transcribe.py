import asyncio
import pyaudio
import websockets
import json

# Your Deepgram API key
DEEPGRAM_API_KEY = ''

# Deepgram WebSocket URL
DEEPGRAM_URL = 'wss://api.deepgram.com/v1/listen'

# Audio stream configuration
CHUNK = 1024           # Number of audio frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1           # Mono audio
RATE = 16000           # Sampling rate (Deepgram prefers 16kHz)

# Path to the text file where transcriptions will be written
OUTPUT_FILE = "transcriptions.txt"

# Function to write transcription to the file
def write_transcription_to_file(transcription):
    with open(OUTPUT_FILE, 'a') as f:
        f.write(transcription + "\n")

# Function to stream audio to Deepgram and handle transcriptions
async def stream_audio_to_deepgram():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Open a WebSocket connection to Deepgram
    async with websockets.connect(
        DEEPGRAM_URL,
        extra_headers={'Authorization': f"Token {DEEPGRAM_API_KEY}"}
    ) as websocket:
        print("Listening to real-time audio. Press Ctrl+C to stop.")

        try:
            while True:
                # Read audio chunk and send it to Deepgram
                data = stream.read(CHUNK, exception_on_overflow=False)
                await websocket.send(data)

                # Receive the transcription result
                response = await websocket.recv()

                # Parse the response and extract the transcribed text
                result = json.loads(response)
                if 'channel' in result and 'alternatives' in result['channel']:
                    transcript = result['channel']['alternatives'][0].get('transcript', '').strip()

                    # If there is a transcription, write it to the file
                    if transcript:
                        print(f"Transcription: {transcript}")
                        write_transcription_to_file(transcript)

        except KeyboardInterrupt:
            print("Stopped streaming.")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

if __name__ == '__main__':
    asyncio.run(stream_audio_to_deepgram())
