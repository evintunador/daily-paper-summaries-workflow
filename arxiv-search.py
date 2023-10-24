import arxiv
import time
import textwrap
import tkinter as tk
from tkinter import ttk
import requests
from threading import Thread
from config import restrict_to_most_recent, max_results
import os


if not os.path.exists("pdfs-to-summarize"):
    os.makedirs("pdfs-to-summarize")

# Python function to read words from a text file and store each line as a string in a list.
def read_lines_from_file(filename):
    """
    Read lines from a text file and store them as strings in a list.
    
    Parameters:
    - filename (str): The name of the text file to read from.
    
    Returns:
    - List[str]: A list containing each line from the text file as a string.
    """
    lines = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line.strip())  # Remove leading/trailing whitespace
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return lines



# search terms
include_terms = read_lines_from_file("search_terms_include.txt")
exclude_terms = read_lines_from_file("search_terms_exclude.txt")

include, exclude = 'all:"', 'all:"'
for term in include_terms: 
    include += term + '" OR all:"'
for term in exclude_terms: 
    exclude += term + '" OR all:"'
include = include[:-9]
exclude = exclude[:-9]
print("\nIncluded Terms:\n", include)
print("\nExcluded Terms:\n", exclude)

if len(include_terms) > 0 & len(exclude_terms) > 0:
    query = f'(cat:cs.AI OR cat:cs.ML OR cat:stat.ML) AND ({include}) ANDNOT ({exclude})'
elif len(include_terms) > 0:
    query = f'(cat:cs.AI OR cat:cs.ML OR cat:stat.ML) AND ({include})'
elif len(exclude_terms) > 0:
    query = f'(cat:cs.AI OR cat:cs.ML OR cat:stat.ML) ANDNOT ({exclude})'
else:
    query = f'cat:cs.AI OR cat:cs.ML OR cat:stat.ML'
print("\nQuery:\n", query)



# Define the search parameters
search = arxiv.Search(
    query = query,
    max_results=max_results,  
    sort_by=arxiv.SortCriterion.SubmittedDate,  # Sort by submission date
    sort_order=arxiv.SortOrder.Descending  # In descending order, so the most recent articles come first
)

results = search.results()
papers = []

i = 0
for result in results:
    if (i == 0) & restrict_to_most_recent:
        today = result.published.date()
    elif restrict_to_most_recent & (today != result.published.date()):
        break
        
    papers.append({"title": result.title, "url": result.pdf_url})
    print('Title: ', result.title)
    print('Abstract: ', textwrap.fill(result.summary, width=220))
    if not restrict_to_most_recent:
        print('Publishing date ', result.published)
    print('PDF URL: ', result.pdf_url)
    #print(result.categories)
    #print('DOI ', result.doi)
    print('\n')

    # Sleep for 5 seconds to avoid overloading the server
    time.sleep(5)
    i += 1

print(f"Total papers: {i}")



# Function to download PDF from arXiv
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

# Function to handle button click and initiate download in a new thread
def on_button_click(url, filename):
    thread = Thread(target=download_pdf, args=(url, filename))
    thread.start()







# Create the main window
root = tk.Tk()
root.title("arXiv Paper Downloader")

# Create a canvas and a vertical scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = ttk.Frame(canvas)

# Configure canvas and add the frame to it
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

for i, paper in enumerate(papers):
    #label = ttk.Label(frame, text=paper["title"])
    #label.grid(row=i, column=0, sticky=tk.W)
    
    button = ttk.Button(frame, text=paper['title'], command=lambda url=paper['url'], fn=f"pdfs-to-summarize/{paper['title']}.pdf".replace(":", " -"): on_button_click(url, fn))
    button.grid(row=i, column=1)

# Update frame size and set canvas scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Place canvas and scrollbar in the GUI
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Enable resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()