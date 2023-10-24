import os
import shutil
import glob

from config import obsidian_vault_location, obsidian_vault_attachments_location, frontmatter_lines

if not os.path.exists('txt-summaries/send-to-Obsidian'):
    os.makedirs('txt-summaries/send-to-Obsidian')

def process_files(text_folder, pdf_folder, md_final_folder, pdf_final_folder):
    # Get all text files in the specified folder
    text_files = glob.glob(os.path.join(text_folder, '*.txt'))

    for text_file in text_files:
        # Get the base filename without the extension
        base_filename = os.path.basename(text_file).rsplit('.', 1)[0]

        # Find the corresponding PDF file
        pdf_file = os.path.join(pdf_folder, base_filename + '.pdf')
        if not os.path.exists(pdf_file):
            print(f"No PDF file found for {text_file}")
            continue

        # Convert the text file to a .md file
        md_file = os.path.join(text_folder, base_filename.title() + ' (pdf).md')
        with open(text_file, 'r') as f_in, open(md_file, 'w') as f_out:
            # Initiate the file w/ tags and the PDF link
            for line in frontmatter_lines:
                f_out.write(f"{line}\n")

            # Copy the contents of the text file to the .md file
            shutil.copyfileobj(f_in, f_out)

            # visible link to pdf in bottom of note
            f_out.write(f"\n\n![[{base_filename}.pdf]]")
            
        # Move the .md file to the final folder. Usually this error comes up because you tried to run the scrip twice
        try:
            shutil.move(md_file, md_final_folder)
        except shutil.Error as e:
            print(f"Error: {e}. Skipping file {md_file} because it already exists in the Obsidian Vault. Usually this error will come up because you erroneously attempted to run the script twice, although it is also possible that there is an entirely unrelated file with the same name already in the vault.")

        # Move the .pdf files to the final folder. the exception exists cuz sometimes i get antsy and add the pdf too soon
        try:
            shutil.copy(pdf_file, pdf_final_folder)
        except shutil.Error as e:
            print(f"Error: {e}. Skipping file {pdf_file} because it already exists in the Obsidian Vault.")

# Call the function with your specified folders
process_files('txt-summaries/send-to-Obsidian', 
              'pdfs-to-summarize', 
              obsidian_vault_location,
              obsidian_vault_attachments_location)
