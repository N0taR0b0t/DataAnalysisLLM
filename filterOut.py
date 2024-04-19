import re

categories = []

def update_categories(new_categories):
    global categories
    updated_categories = set(categories).union(set(new_categories))
    categories = sorted(list(updated_categories))

def saveCompleted(Dir, elapsed, chars, charsRate, nickname):
    detected = []
    extracted_categories = []
    
    if (str(chars) != "0"):
        with open("output.txt", "r") as input_file:
            input_content = input_file.read()

        choice_match = re.search(r"choice: ([^\n]*)", input_content, re.IGNORECASE)
        if choice_match:
            extracted_categories = re.findall(r"'(.*?)'", choice_match.group(1))
            
            if not extracted_categories:
                extracted_categories = [cat.strip() for cat in choice_match.group(1).split(',') if cat.strip()]

            for category in extracted_categories:
                normalized_category = category.strip().capitalize()
                if normalized_category in categories and normalized_category not in detected:
                    detected.append(normalized_category)

        if not detected:
            detected.extend([cat.strip().capitalize() for cat in extracted_categories][:6])

    combined_save = "; ".join([str(detected), str(elapsed), str(chars), str(charsRate), str(nickname)]) + "\n"

    with open("completed.txt", "a") as prompt_file:
        prompt_file.write(combined_save)
