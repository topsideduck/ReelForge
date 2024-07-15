import base64
import json
import os
import uuid

from datetime import timedelta

import requests
import srt_equalizer

from moviepy.editor import AudioFileClip


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
            url=self.tts_endpoint, headers=headers, json=data
        )

        # Extract the audio data from the response and return it.
        audio_bytes: bytes = base64.b64decode(
            s=json.loads(request.content.decode())["v_data"]
        )

        return audio_bytes

    @staticmethod
    def _convert_to_srt_time_format(total_seconds: int) -> str:
        """
        Helper function to convert total seconds to the
        SRT time format: HH:MM:SS,mmm
        """
        if total_seconds == 0:
            return "0:00:00,0"

        return (
            str(object=timedelta(seconds=total_seconds)).rstrip("0").replace(".", ",")
        )

    def generate_subtitles(
        self, sentences: list[str], audio_clips: list[AudioFileClip]
    ) -> str:

        start_time = 0
        subtitles: list[str] = []

        for i, (sentence, audio_clip) in enumerate(
            iterable=zip(sentences, audio_clips), start=1
        ):
            duration: int = audio_clip.duration
            end_time: int = start_time + duration

            # Format: subtitle index, start time --> end time, sentence
            subtitle_entry: str = (
                f"{i}\n{self._convert_to_srt_time_format(start_time)} --> "
                f"{self._convert_to_srt_time_format(end_time)}\n{sentence}\n"
            )

            subtitles.append(subtitle_entry)

            # Update start time for the next subtitle.
            start_time += duration

        subtitles: str = "\n".join(subtitles)

        # Write a temporary subtitles file and equalize it.
        subtitles_path: str = f"{uuid.uuid4()}.srt"

        with open(file=subtitles_path, mode="w") as file:
            file.write(subtitles)

        srt_equalizer.equalize_srt_file(
            srt_path=subtitles_path, output_srt_path=subtitles_path, target_chars=10
        )

        # Read the equalized subtitles file and return its contents, while deleting the file.
        equalized_subtitles: str = open(file=subtitles_path, mode="r").read()
        os.remove(path=subtitles_path)

        return equalized_subtitles
