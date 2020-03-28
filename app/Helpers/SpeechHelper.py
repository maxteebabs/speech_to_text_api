from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
class SpeechHelper:
    def convertToText(self, storage_uri, language_code='en-us'):
        # storage_uri URI  gs://cloud-samples-data/speech/brooklyn_bridge.mp3
        client = speech_v1p1beta1.SpeechClient()
        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = 44100
        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.MP3
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }

        audio = {"uri": storage_uri}

        convertedTxt = ""
        try:
            response = client.recognize(config, audio)
            for result in response.results:
                # First alternative is the most probable result
                alternative = result.alternatives[0]
                convertedTxt = alternative.transcript
                break
        except Exception as err:
            raise(err)
        return convertedTxt
