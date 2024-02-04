import os

def make_folder_if_none(path):  
    if not os.path.exists(path):
        os.makedirs(path)

make_folder_if_none("pdfs-to-summarize")
make_folder_if_none("txt-summaries")
make_folder_if_none("txt-summaries/to-be-concatenated")
make_folder_if_none("txt-summaries/send-to-Obsidian")
make_folder_if_none("concatenated-summaries")


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Couldn't delete {filename} file from {folder_path} folder bc Error occurred: \n{e}")

delete_all_files_in_folder("pdfs-to-summarize")
delete_all_files_in_folder("txt-summaries")
delete_all_files_in_folder("txt-summaries/to-be-concatenated")
delete_all_files_in_folder("txt-summaries/send-to-Obsidian")
delete_all_files_in_folder("concatenated-summaries")

try:
    if os.path.isfile('timestamps.txt'):
        os.remove('timestamps.txt')
except Exception as e:
    print(f"Couldn't delete timestamps.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('newsletter.txt'):
        os.remove('newsletter.txt')
except Exception as e:
    print(f"Couldn't delete newsletter.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('concat_summaries.txt'):
        os.remove('concat_summaries.txt')
except Exception as e:
    print(f"Couldn't delete concat_summaries.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('newsletter_podcast.mp3'):
        os.remove('newsletter_podcast.mp3')
except Exception as e:
    print(f"Couldn't delete newsletter_podcast.mp3 bc Error occurred: \n{e}")
