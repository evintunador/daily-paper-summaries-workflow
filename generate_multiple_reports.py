import openai
from time import time, sleep
from halo import Halo
import textwrap
import yaml
import os
import PyPDF2
from config import prompts, cleanup


###     file operations

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def save_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def cleanup_file(filepath):
    clean_content = ''
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            # Remove lines starting with specific string
            if line.startswith("Q: "):
                continue
            
            # Remove specific string instances
            modified_line = line.replace("A: ", '')

            clean_content += modified_line #outfile.write(modified_line)

    with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(clean_content)




###     API functions

def chatbot(conversation, model="gpt-3.5-turbo-16k", temperature=0):
    max_retry = 3
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature)
            text = response['choices'][0]['message']['content']

            spinner.stop()
            
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = conversation.pop(0)
                print('\n\nDEBUG: Trimming oldest message')
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
    print('\n\nCHATBOT:\n%s' % formatted_text)




if __name__ == '__main__':
    # instantiate chatbot, variables
    openai.api_key = open_file('key_openai.txt').strip()

    # Get list of all PDF files in the input folder
    pdf_files = [f for f in os.listdir('pdfs-to-summarize/') if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        # Check if the report already exists in the output folder
        filename = 'txt-summaries/' + pdf_file.replace('.pdf', '.txt')
        if os.path.exists(filename):
            continue

        # Open the PDF file
        try:
            with open('pdfs-to-summarize/' + pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                paper = ''
                for page_num in list(range(0,len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    paper += page.extract_text()
        except PyPDF2.errors.PdfReadError:
            print(f"Error reading file: {pdf_file}")
            continue


        if len(paper) > 22000:
            paper = paper[0:22000]
        ALL_MESSAGES = [{'role':'system', 'content': paper}]
        report = ''
        for p in prompts:
            ALL_MESSAGES.append({'role':'user', 'content': p})
            response, tokens = chatbot(ALL_MESSAGES)
            chat_print(response)
            ALL_MESSAGES.append({'role':'assistant', 'content': response})
            report += '\n\nQ: %s\nA: %s' % (p, response)

        # Save the report in the output folder with the same name as the PDF file but with .txt extension
        save_file(filename, report.strip())

        # clean it up to make it less obvious that a chatbot was writing this
        if cleanup == True:
            cleanup_file(filename)

