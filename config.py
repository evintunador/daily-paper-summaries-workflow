### generate_multiple_reports.py 
# Mess around with these prompts to tease out specific information you're looking for
prompts = [ # don't forget commas if you add more prompts to the list
"You are an expert scientific researcher. Please provide clear, concise descriptions and explanations of the core assertions, mechanics, results, potential critiques, and implications elucidated in this paper. Specificity is preferred over broad or vague statements.",
"You are an expert scientific researcher with a wide range of cross-disciplinary background knowledge. List all of the prerequisite knowledge required in order to understand the concepts laid out in this paper. Please answer extremely concisely in a simple bulleted format. Entries should include both individual concepts as well as the names of disciplines and sub-disciplines. Also, please provide a complete citation for this paper to the best of your ability given the information provided. Only include a url if it is listed in the content of the paper." 
]
# Change this to False if you want the questions to be left in the text summary document. I prefer the cleaner look personally
cleanup = True

### send-to-obsidian.py # Irrelevant if you never run send-to-obsidian.py
# vault_location is wherever you want the .md summaries to go, and attachments_location is wherever you want the pdf files to go
# For people who use obsidian 'correctly' this might be the exact same folder
obsidian_vault_location = ''
obsidian_vault_attachments_location = ''
# lines to add to the beginning of each summary.md file in obsidian. I've left mine in as examples
frontmatter_lines = ['#pdf', '#needsToBeTagged', '#needsAddedToResearchList', '#task read & annotate this full paper'] 

### timestamps.py
# True or False
# Defaults to True because when I bulk open files in safari it displays them in reverse-chronological order
display_reverse_alphabetical = True
# The hotkey used to start the next yt chapter
hotkey = '`'
# sorry i'm not changing the end process hotkey from esc to anything else. feel free to push an update if that's a feature you want

### newsletter.py
newsletter_prompt = "The above context is a series of questions and answers where I had another AI language model summarize a variety of scientific papers for me. These papers were mostly/likely all published today, although some may have been published in the past week or two. I would like you to write me a clear, extremely concise, and informative newsletter where you run through the most interesting highlights. Your target audience is AI/ML researchers and people interested in consciousness that watch my youtube channel. Sign the newsletter as 'Tunadorable.' Feel free to ignore some articles if you feel they are not of interest to your target audience. Always ignore papers relating to natural disasters. Prioritize papers written by notable researchers and research groups. In your answer, there is no need to acknowledge the fact that you are a langauge model writing a newsletter, just get right to it so that I can easily copy & paste. Generally the string ' - ' should be replaced with ': ' since this is an error resulting from my filesystem. Do not use any markdown formatting in your response; the simplest possible plain text is preferred. Emojis are encouraged."
## honestly I should've made more config options here rather than leaving all of my own links & whatnot as default but i'm tired and this is taking too long
