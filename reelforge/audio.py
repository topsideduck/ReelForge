import base64
import json

import requests


class Audio:
    def __init__(self) -> None:
        """
        Audio class that handles tts and subtitle generation.
        """
        self.tts_endpoint: str = "https://countik.com/api/text/speech"

    def tts(self, text: str) -> bytes:
        """
        Generate speech from the provided text using the countik api.

        Args:
            text (str): The text to convert to speech.

        Returns:
            bytes: The audio data in bytes, to be stored in .mp3
        """
        headers: dict[str, str] = {"Content-Type": "application/json"}

        # The default voice is the tiktok female tts voice.
        data: dict[str, str] = {"text": text, "voice": "en_us_001"}

        # Send a request to the api to generate the audio file.
        request: requests.Response = requests.post(
            url=self.tts_endpoint,
            headers=headers, json=data
        )

        # Extract the audio data from the response and return it.
        audio_bytes: bytes = base64.b64decode(
            s=json.loads(request.content.decode())["v_data"]
        )

        return audio_bytes
