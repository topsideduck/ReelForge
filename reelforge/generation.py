from g4f.client import Client


class Generator:
    def __init__(self, language: str, system_instructions: str) -> None:
        """
        Generator class that initialises a GPT-4o instance with system
        instructions to generate scripts.

        Args:
            language (str): the language of the script/video.
            system_instructions (str): the default instructions to be passed
                to the model to set its behaviour. include instructions here on
                how the script should be generated.
        """

        # TODO: customizability of model (currently only GPT-4o)
        self.language: str = language

        # Dictionary that stores the conversation between the user and model.
        # Always starts with the system instructions as the first item.
        self._conversation: list[dict[str, str]] = [
            {
                "role": "system",
                "content": system_instructions
                + """\\n
Your response must only contain the script, there must be no sign of anything else, such as your affirmation of the request.
Do not use formatting or emojis in your response.
Return your response in json format, with the fields being "title" and "script". 
The "title" field is a string, and the "script" field is a list of string, where each string is a sentence from the script.
Json doesn't allow line breaks, so replace all line breaks in the script with "\n".
             """,
            }
        ]

        self._client: Client = Client()

    # Language deletion not allowed as a language is always required.
    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        # TODO: get supported languages for each model without hard coding it.
        supported_languages: list[str] = ['Albanian', 'Amharic', 'Arabic', 'Armenian', 'Bengali', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'Estonian', 'Finnish', 'French', 'Georgian', 'German', 'Greek', 'Gujarati', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Kannada', 'Kazakh', 'Korean', 'Latvian', 'Lithuanian', 'Macedonian', 'Malay', 'Malayalam', 'Marathi', 'Mongolian', 'Norwegian', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Romanian', 'Russian', 'Serbian', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Swahili', 'Swedish', 'Tagalog', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Vietnamese']

        # Check if the language is supported.
        if language.lower().capitalize() not in supported_languages:
            raise ValueError(
                f"{language} is not supported! Supported languages: "
                f"{", ".join(supported_languages).strip(', ')}."
            )

        else:
            self._language: str = language

    # Setting conversation is not allowed as the conversation should not be
    # externally modified.
    @property
    def conversation(self) -> list[dict[str, str]]:
        return self._conversation

    @conversation.deleter
    def conversation(self) -> None:
        del self._conversation[1:]
