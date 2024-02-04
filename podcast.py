from pathlib import Path
from openai import OpenAI

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()
    
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def cut_off_string(input_string, cutoff_string):
    # Find the position of the cutoff string
    cutoff_index = input_string.find(cutoff_string)
    
    # If the cutoff string is found, slice the input string up to that point
    if cutoff_index != -1:
        return input_string[:cutoff_index]
    else:
        # If the cutoff string is not found, return the original string
        # You can also choose to handle this case differently
        return input_string

SECRET_KEY = open_file('key_openai.txt').strip()
client = OpenAI(api_key=SECRET_KEY)

newsletter = open_file('newsletter.txt').strip()

# Example usage
input_str = "Here is an example string, and here is the cutoff."
cutoff_str = ", and here"

result = cut_off_string(newsletter, "Tunadorable")

speech_file_path = Path(__file__).parent / "newsletter_podcast.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=result
)

response.stream_to_file(speech_file_path)
