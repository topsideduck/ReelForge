class Generator:
    def __init__(self, language: str, system_instructions: str) -> None:
        self.language: str = language

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
