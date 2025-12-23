from openai import OpenAI

client = OpenAI(
    base_url='http://127.0.0.1:8899/v1',
    api_key="dummy_key"
)
audio_file= open("./demo.wav", "rb")

transcription = client.audio.transcriptions.create(
    model="sensevoice", 
    file=audio_file
)

print(transcription.text)