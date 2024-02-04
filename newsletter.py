import os
from datetime import datetime
from config import newsletter_prompt

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

######## INITIAL AGGREGATION OF SUMMARIES
indiv_summaries = 'txt-summaries'
concat_summaries = f'concat_summaries.txt'

#directory = os.path.dirname(concat_summaries)
#if not os.path.exists(directory):
#    os.makedirs(directory)

# Open the output file
with open(concat_summaries, 'w') as outfile:
    
    # Loop over the files in the folder
    for filename in os.listdir(indiv_summaries):
        
        # Check if the file is a text file
        if filename.endswith('.txt'):
            # Write the filename to the output file
            outfile.write(f'### {filename[:-4].title()}\n')

            # Open the input file
            with open(os.path.join(indiv_summaries, filename), 'r') as infile:
                # Write the contents of the input file to the output file
                outfile.write(f"{infile.read()}\n\n\n")



######## GPT WRITING THE NEWSLETTER INTRO

from openai import OpenAI
from time import time, sleep
from halo import Halo
import textwrap

###     file operations
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

###     API functions
def chatbot(conversation, model="gpt-3.5-turbo-16k", temperature=0):
    max_retry = 3
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = client.chat.completions.create(model=model, messages=conversation, temperature=temperature)
            text = response.choices[0].message.content

            spinner.stop()
            
            return text#, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = conversation.pop(0)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)

def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nCHATBOT:\n\n%s' % formatted_text)


SECRET_KEY = open_file('key_openai.txt').strip()
client = OpenAI(api_key=SECRET_KEY)

paper = open_file(f'concat_summaries.txt').strip()
if len(paper) > 80000:
    paper = paper[0:80000]

ALL_MESSAGES = [{'role':'system', 'content': paper}]
report = ''
p = newsletter_prompt

ALL_MESSAGES.append({'role':'user', 'content': p})
response = chatbot(ALL_MESSAGES)#, tokens
chat_print(response)
ALL_MESSAGES.append({'role':'assistant', 'content': response})


######### BRING IT ALL TOGETHER
body = f'concat_summaries.txt'

with open(body, 'r') as src_file:
    body_txt = src_file.read()

file_path = f'newsletter.txt'

# Write the message
with open(file_path, 'w') as outfile:
    outfile.write(f'This article was written by gpt-3.5-turbo-16k on {today}. \nWARNING: CITATIONS MAY BE INCORRECT \n\n')
    outfile.write(f'{response}\n\n')
    outfile.write(f'To watch the accompanying video with commentery on all the articles, click below. \n\n\n')
    outfile.write(f'{body_txt}')
    outfile.write(f'\n\nPlease consider checking out my youtube channel where I provide thoughts and commentary on new AI publications.\nhttps://youtube.com/@Tunadorable\nhttps://youtube.com/playlist?list=PLPefVKO3tDxP7iFzaSOkOZnXQ4Bkhi9YB&si=ndXJfDFfMkE_b8w7')
    outfile.write(f'\n\nThank you to Dave Shapiro who wrote the first version of the script I use to get these summaries using OpenAI\'s API and a codebot script that I have also found useful in this project.')
    outfile.write(f'\nhttps://www.youtube.com/@DavidShapiroAutomator \nhttps://github.com/daveshap/Quickly_Extract_Science_Papers \nhttps://github.com/daveshap/Coding_ChatBot_Assistant')
    outfile.write(f'\n\nHere is the most up-to-date version of the script workflow I currently use:\nhttps://github.com/evintunador/daily-paper-summaries-workflow')



