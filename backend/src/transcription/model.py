import io
from google.oauth2 import service_account
from google.cloud import speech

clientFile = "cdef-project-86e12bdc0457.json"
credentials = service_account.Credentials.from_service_account_file(clientFile)
client = speech.SpeechClient(credentials=credentials)

# Loading audio file

with io.open("", "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code="en-US",
)
        
response = client.recognize(config=config, audio=audio)
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))