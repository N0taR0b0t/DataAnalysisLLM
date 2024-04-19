from langchain_community.llms import Ollama
from GPT import gpt_interact
import sys
import re
import time

ollama = Ollama(base_url='http://localhost:11434', model="Llama2-13B")

def read_categories():
    try:
        with open('categories.txt', 'r') as file:
            # Normalize and validate categories when reading
            categories = [line.strip() for line in file.readlines() if line.strip() and all(c.isalpha() or c.isspace() for c in line)]
        return categories
    except FileNotFoundError:
        return ["Engagement", "Ads and Products", "Internal References"]

def update_categories(new_categories):
    existing_categories = set(read_categories())
    updated_categories = existing_categories.union(set(new_categories))
    with open('categories.txt', 'w') as file:
        for category in sorted(updated_categories):
            file.write(f"{category}\n")

def askLLM(start_time, filename):
    categories = read_categories()
    try:
        # Read the contents of Instructions.txt
        with open("Instructions.txt", "r") as instructions_file:
            instructions_content = instructions_file.read()
        categories_text = "Category List: " + ", ".join(sorted(set(categories)))  # Remove duplicates and sort

        with open("input.txt", "r") as input_file:
            input_content = input_file.read()

        trimmed_filename = filename[-65:] if len(filename) > 65 else filename
        filename_text = "Filename: " + trimmed_filename + "\n"
        combined_query = f"{instructions_content}\n{filename_text}\n{categories_text}\n{input_content}"

        with open("prompt.txt", "w") as prompt_file:
            prompt_file.write(combined_query)

        response = gpt_interact(combined_query)
        
        with open("output.txt", "w") as output_file:
            output_file.write(response)

        new_extracted_categories = set()
        matches = re.findall(r"'(.*?)'", response)
        for match in [m.strip() for m in matches]:  # Strip spaces from extracted categories
            normalized_match = match.lower()  # Normalize to lower case for consistent comparison
            if normalized_match not in [c.lower() for c in categories]:  # Comparison against lower-cased list
                new_extracted_categories.add(match)

        # Update categories if new ones were added
        if new_extracted_categories:
            update_categories(new_extracted_categories)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure input.txt exists.")
        sys.exit()
    except Exception as e:
        print(f"Unexpected error: {e}.")
        sys.exit()

    end_time = time.time()
    execution_time = end_time - start_time
    char_count = len(combined_query)
    chars_per_second = char_count / execution_time if execution_time > 0 else 0

    return f"Execution Time: {execution_time:.2f} seconds", f"Character Count: {char_count}", f"Characters per Second: {chars_per_second:.2f}"
