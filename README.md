# LeetLog
Gives a quick way to log data about the question's you have solved into a csv.
If imported to Google Sheets, you can use it efficiently to revise notes and understand how long different question take.

## Instructions
1. Make sure you have defined the constants in the `file_reader.py`.
2. Run `file_reader.py` to make your new csv file, or simply add the new questions.
3. Copy the google sheet template [here](https://docs.google.com/spreadsheets/d/1P_z4wKKSM7Mgpcb_e7fETVz0-PCaAMmJQHyXrfVQ0Zg/edit?gid=18351213#gid=18351213) to your own google account.
4. Follow the instructions for importing
5. Click *Extensions* in the menu bar and select *App Scripts*.
6. This will open a new `Untitled Project` App Script. Copy the code in `dropper.gs` into the `Code.gs` file.
7. Write click the `Generate Dropdown` image and click the 3 dots in the top-right corner to *Assign a Script*.
8. Type the name of the function: `dropdownGenerator` and press Ok.
9. Click the button to test it out. It should create dropdown tags in the Topics column automatically.

## Current File Structure
Each folder has a `__init__.py` to initialise them as modules. It's convenient when you want to debug problems like linked lists which don't actually give you the `Node` classes in leetcode. 

To prevent the module not found error, add the root directory to the python path in the `.env` file. For convenience, make sure it's the absolute path. Check if the formatting is correct as well, it is currently formatted for MacOS.

```
\0_easy
    __init__.py
    XXXX.py
\1_medium
\2_hard
.env
file_reader.py
template.py
```

The `template.py` file can be copied for every new question you do. Other than having some key information about each question, it lets you time your solutions as well.

Files for questions should be named XXXX.py (e.g 0001.py or 1234.py) for your convenience. It doesn't really matter though since the problem number comes from the data in the file.

## Python Header for each file
1. Problem number: The number on leetcode
2. Problem Description
3. Topics: A list of topics from leetcode
4. Date solved (keep the format consistent across all files)
5. Time Taken
    * E.g "1 hr 2min, 1 hour and 2 minutes, 1hr2min, 1h2m"
6. Efficiency (*Not added to the csv*)
7. Notes (This needs to be in one line. You can modify `file_reader.py` if you want to change it.)

```py
# Problem: X - DESCRIPTION
# DIFFICULTY
# Topics:

"""
# Date : 07-02-25
# Total time:  minutes
#  ms, beats %
# NOTE:
```

For example:
```py
# Problem: 1. Two Sum
# Easy
# Topics: Array, Hashtable

"""
# Date: 19-01-25
# Total time: 20 min
# 1313 ms, beats 43.96%
# NOTE: Iterate through the array and for each number, add `value, index` pair-since we don't care about which `4` we look at in [1,2,4,4,4]. Also check if the complement exists already, and if so, return the current index and the complement's index. Otherwise return [0,0].
```
