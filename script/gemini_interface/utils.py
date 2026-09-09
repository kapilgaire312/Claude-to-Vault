import re


def remove_json_markdown(text)-> str:
    # This pattern finds ```json or ``` at the start and ``` at the end
    pattern = r"^```(?:json)?\s*\n?(.*?)\s*\n?```$"
    match = re.search(pattern, text.strip(), re.DOTALL)

    if match:
        return match.group(1)
    raise Exception("Invalid response from gemini.")
