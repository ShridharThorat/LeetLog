import os
import csv
import re
import datetime

# CONSTANTS
FIELDS = ['Number', 'Difficulty', 'Date', 'Name', 'Topic', 'Time', 'Note']

ROOT_PATH = ""  # The path to the root folder
DIRS = ['0_easy','1_medium','2_hard']  # The sub-directories you want to read from
CSV_NAME = "leetcode_data.csv"  # You could rename this to whatever

APPEND = False  # Modifies whether you rewrite the file, or just add the new questions to it
START = "02-02-25"  # Questions solved from the START to today will be added
DATE_FORMAT = f'%d-%m-%y'  # Keep this formatting consistent in all your files
START_DATE = datetime.datetime.strptime(START,f'%d-%m-%y')
WRITE_MODE = "a" if APPEND and os.path.exists(CSV_NAME) else "w"

LINES_TO_READ = 10  # The number of lines read from the top of every file

def extract_data_from_file(filepath, lines_to_read=LINES_TO_READ):
    """
    Extracts the problem number, name, difficulty, topics, and solution time from the top of the file.
    Expected lines in the file include:
      - "# Problem: <number>. <Name>"
      - "# <Difficulty>"
      - "# Topics: <topic1>, <topic2>, ..."
      - Later, a line like "# Total Time: <number> minutes"
    """
    data = {
        'Number': '',
        'Difficulty': '',
        'Date': '',
        'Name': '',
        'Topic': '[]',  # default to empty list
        'Time': '',
        'Note': ''
    }
    
    # 1. Read all `lines_to_read` lines and add them to a list
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for _ in range(lines_to_read):
            line = f.readline()
            if not line:
                break
            lines.append(line.strip())
    
    # --- Extract Problem Number and Name ---
    # Input "# Problem: 217. Contains Duplicate"
    # Extraction: 217, Contains Duplicate
    for i, line in enumerate(lines):
        if line.lower().find("problem") != -1:
            # Remove the prefix and try to capture a number and the rest of the line
            # This regex allows for either a dot or hyphen after the number.
            match = re.search(r"# Problem:\s*(\d+)[\.\-]?\s*(.+)", line)
            if match:
                data['Number'] = match.group(1).zfill(4)  # 1 -> 0001
                data['Name'] = match.group(2)
                lines.pop(i)
            else:
                print(f"\tError finding the Number and name in `{line}`")
            break
    
    # --- Extract Difficulty ---
    raw_diff = lines.pop(0)
    raw_diff = raw_diff.split("#")[1]
    difficulty = raw_diff.strip().lower().capitalize()
    data['Difficulty'] = difficulty

    # --- Extract Topics ---
    # Expected format: "# Topics: array, hashtable, sorting"
    for i, line in enumerate(lines):
        if line.lower().find("topics") != -1:
            topics_str = line.split(":", 1)[1].strip()
            # Create a list of topics by splitting on commas and stripping whitespace.
            topics_list = [topic.strip().capitalize() for topic in topics_str.split(",") if topic.strip()]
            # Save as a string representation of a list (as shown in your example output).
            data['Topic'] = str(topics_list)
            lines.pop(i)
            break
        
    # --- Extract Date ---
    for i, line in enumerate(lines):
        if line.lower().find("date") != -1:
            date_str = line.split(":", 1)[1].strip()
            if date_str:
                date_obj = datetime.datetime.strptime(date_str, f'%d-%m-%y')
                data['Date'] = date_obj
            else:
                data['Date'] = None
            lines.pop(i)
            break

    # --- Extract Time ---
    # Look for the line with the solution time.
    # Expected format: "# Total time: 20 minutes"
    for i, line in enumerate(lines):
        if line.lower().find("total time") != -1:
            match = re.search(
                r"# Total time:\s*"
                r"(?:(\d+)\s*(?:h|hr|hrs|hour|hours))?\s*"
                r"(?:(\d+)\s*(?:m|min|minutes))?",
                line,
                re.IGNORECASE
            )
            if match:
                hours = match.group(1)
                minutes = match.group(2)
                # Build the output string based on which groups were captured.
                if hours and minutes:
                    duration = round(int(hours) + float(minutes)/60,2)
                    data['Time'] = duration
                elif hours:
                    data['Time'] = round(int(hours),2)
                elif minutes:
                    data['Time'] = round(float(minutes)/60,2)
            lines.pop(i)
            break
    
    # --- Extract Note ---
    for i, line in enumerate(lines):
        if line.lower().find("note") != -1:
            note_str = line.split(":", 1)[1].strip()
            data['Note'] = str(note_str)
            lines.pop(i)
            break
    
    return data

def main():
    rows = []    
    existing_numbers = set()
    
    # If appending, load existing data to avoid duplicates
    if APPEND and os.path.exists(CSV_NAME):
        with open(CSV_NAME, "r", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_numbers.add(row['Number'])

    # Walk through the directory and subdirectories.
    for directory in DIRS:
        dir_path = os.path.join(ROOT_PATH, directory)
        
        # Check if the path is valid
        if not os.path.isdir(dir_path):
            print(f"\tDirectory {dir_path} does not exist. Skipping.")
            continue
        
        # If valid, read it
        all_files = os.listdir(dir_path)
        all_files.sort()
        for filename in all_files:
            if 'init' not in filename and filename.endswith(".py"):
                filepath = os.path.join(dir_path, filename)
                data = extract_data_from_file(filepath, LINES_TO_READ)
                
                if data['Number']: # Only add rows that have a valid problem number.
                    if not APPEND:
                        if data['Date']:
                            data['Date'] = data['Date'].strftime(DATE_FORMAT)
                        rows.append(data)
                    
                    # if append mode, we only include dates from start_date and beyond
                    elif data['Number'] not in existing_numbers:
                        data_date = data['Date']
                        if data_date and data_date >= START_DATE:
                            data['Date'] = data['Date'].strftime(DATE_FORMAT)
                            rows.append(data)
                        else:
                            print(f"\tSkipping {filepath} (Date before {START_DATE.strftime(DATE_FORMAT)})")
                else:
                    print(f"\tSkipping {filepath} because no problem number was found.")
                    
        

    # Write the collected data to a CSV file.
    with open(CSV_NAME, WRITE_MODE, newline='', encoding='utf-8') as csvfile:        
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
        
        if WRITE_MODE=="w":
            writer.writeheader()
            
        for row in rows:
            writer.writerow(row)

    print(f"\tData successfully {'appended to' if APPEND else 'written to'} {CSV_NAME}")

if __name__ == "__main__":
    main()
