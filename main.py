import os
import time
from bs4 import BeautifulSoup
import re
from HelloLLM import askLLM
from filterOut import saveCompleted

#LLM Format breakdown detection and logging

def html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

def process_file(file_name, nickname):
    try:
        with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
            contents = file.read()

            # Detect if contents are HTML and convert to plain text if true
            if '<html>' in contents.lower() or bool(re.search('<.*?>', contents)):
                contents = html_to_text(contents)

            chunked_lines = []
            for line in contents.splitlines():
                for i in range(0, len(line), 1000):
                    chunked_lines.append(line[i:i+1000])
            chunked_lines = chunked_lines[:15]
            if len(contents) > 1250:
                with open('input.txt', 'w') as input_file:
                    input_file.write('\n'.join(chunked_lines[:min(len(chunked_lines), 16)]))
            else:
                with open('input.txt', 'w') as input_file:
                    input_file.write('\n'.join(chunked_lines))
        print(f"Starting: {nickname}.")
        if len(contents) >= 50:
            elapsed, chars, charsRate = askLLM(time.time(), file_name)
            saveCompleted(file_name, elapsed, chars, charsRate, nickname)
            print(f"{elapsed}\n{chars}\n{charsRate}")
        else:
            print("File too short, skipping...")
            saveCompleted(file_name, 0, 0, 0, nickname)
    except FileNotFoundError:
        print(f"Warning: {file_name} does not exist. Skipping...")

def main():
    directory_path = "/Users/matias/Library/Mobile Documents/com~apple~CloudDocs/Pitt/CMPINF1205/Project/Data/"
    completed_substrings = set()

    try:
        with open('completed.txt', 'r') as completed_file:
            for line in completed_file:
                line_stripped = line.strip()
                # Store all unique substrings of the last 20 characters from each line
                for i in range(len(line_stripped) - 20 + 1):
                    completed_substrings.add(line_stripped[i:i+20])
    except FileNotFoundError:
        print("Warning: completed.txt does not exist. Proceeding with processing all files.")

    try:
        with open('txt.txt', 'r') as sample_file:
            for line in sample_file:
                file_name = line.strip()
                to_check = file_name[-20:]
                # Check if this substring exists in the set of completed_substrings
                if any(to_check in s for s in completed_substrings):
                    print(f"Skipping already processed file: {file_name}")
                    continue  # Skip this file as it's already been processed
                time.sleep(3)
                full_path = os.path.join(directory_path, file_name)
                process_file(full_path, file_name)
                #input("Pausing for user input...")
    except FileNotFoundError:
        print("Error: File does not exist.")
        
if __name__ == "__main__":
    main()
