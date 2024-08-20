# In the problems.txt file, randomly chooses the next unfinished problem out of the selected categories
import io, fileinput
from termcolor import colored
import random


FILE_PATH = "C:\\Users\\HP\\Downloads\\problems.txt"


def markSolved(problemSet, problemName, message):
    global unsolvedProblems

    try:
        with fileinput.input(FILE_PATH, encoding="utf-8", inplace=True) as file:
            for line in file:
                newLine = line.replace(problemName, problemName + " ★ " + message)
                print(newLine, end='') # redirected into the file since inplace is true
    except:
        print(colored("Could not open file (not found or in use). Exiting...", "red"))
        exit(1)
    
    # Now that we're sure the file replacement worked, also delete from the dict
    unsolvedProblems[problemSet].remove(problemName)
# --- end of markSolved function

def colourProblemName(problemName, includeSuffix=True) -> str:
    '''
    Changes the colour of problemName and also finds a suffixed difficulty 
    in parentheses (easy), (medium), (hard) to colour appropriately as well. 
    Optionally set includeSuffix to remove the difficulty text. \n
    If no difficulty is listed, simply monocolour the entire string.
    '''

    # Suffixes to find and colourize
    easy = colored("(easy)", "green")
    medium = colored("(medium)", "yellow")
    hard = colored("(hard)", "red")
    colourDifficulties = [easy, medium, hard]

    suffix = -1
    slice = len(problemName)
    
    # Search for each suffix
    difficulties = ["(easy)", "(medium)", "(hard)"]
    for i, difficulty in enumerate(difficulties):
        ret = problemName.find(difficulty)
        if ret != -1:
            slice = ret
            suffix = i
            break
    

    # Colour the title light blue and get the appropriate suffix if found
    if includeSuffix:
        problemTitle = colored(problemName[:slice], "light_blue")
    else: # strip off the excess whitespace if there is no suffix included
        problemTitle = colored(problemName[:slice].strip(), "light_blue")

    problemDiff = ''
    if suffix != -1 and includeSuffix:
        problemDiff = colourDifficulties[suffix]

    return problemTitle + problemDiff
# --- end of colourProblemName

def handleAfterSolving(problemSet):
    '''
    Intended to be called directly after solving a problem (after markSolved). 
    Prompts user to solve another problem or to exit program. \n
    This function will terminate the program if asked to, so assume finding 
    another problem if anything returns from this function.
    '''

    global unsolvedProblems
    print("New problem or exit?")
    print("\tNew problem - 1")
    print("\tExit - 2")
    while True:
        response = input(colored("Choice: ", "yellow"))

        try:
            response = int(response)
        except:
            print(colored("Not a number, try again", "red"))
            continue

        match response:
            case 1:
                print("Okay, finding another problem")
                return
            case 2: # Quit
                print("Exiting...")
                exit(0)
            case _:
                print(colored("Invalid number, try again", "red"))

try:
    file = io.open(FILE_PATH, mode="r", encoding="utf-8")
except:
    print(colored("Could not open file (not found or in use). Exiting...", "red"))
    exit(1)

unsolvedProblems = {}
headerNames = []

needHeader = True
curHeader = ''
for line in file:
    # Skip empty lines and signal that header will be coming next
    if line == '\n':
        needHeader = True
        continue

    line = line.strip()
    # If we need a header, make it a key in the dict
    if needHeader == True:
        unsolvedProblems[line] = []
        headerNames.append(line)
        curHeader = line
        needHeader = False
        continue

    # Otherwise this line is the name of a problem
    # Skip if it's already solved
    if '★' in line:
        continue
    else:
        unsolvedProblems[curHeader].append(line)

file.close()

# ---------------- Interactive terminal interface -------------------
for i, name in enumerate(headerNames):
    if len(unsolvedProblems[name]) == 0:
        print(name + " - FULLY SOLVED")
    else:
        print(name + " - " + str(i + 1))

print(colored("\nAdd problem sets by entering the number corresponding to the category you want", "yellow"))
problemSets = []
while True:
    print("\tSelected problem sets:")
    if len(problemSets) == 0:
        print("\tNone")
    else:
        for set in problemSets:
            print("\t" + set)

    response = input(colored("Select category (or 0 to finish): ", "yellow"))
    try:
        response = int(response)
        # If valid (1-based) index and there are unsolved problems, add it to the set (if not included yet)
        if (response > 0 and response < len(headerNames) and 
                len(unsolvedProblems[headerNames[response - 1]]) != 0 and
                headerNames[response - 1] not in problemSets):
            problemSets.append(headerNames[response - 1])
            print(colored(headerNames[response - 1] + " was added!", "green"))
        elif response == 0:
            break
        else:
            print(colored("Invalid number, try again", "red"))
    except:
        print(colored("Not a number, try again", "red"))

if len(problemSets) == 0:
    print("No problem sets chosen, exiting...")
    exit(0)

# --------------------- Solving problems section code ------------------
numRerolls = 0
chooseNewProblem = True
while len(problemSets) > 0:
    if chooseNewProblem:
        randNum = random.randint(0, len(problemSets) - numRerolls - 1) # Exclude the last indices when rerolling
        problemSet = problemSets[randNum]
        problemName = unsolvedProblems[problemSet][0] # Take first problem from that set
        print("Your random problem selected is:", colourProblemName(problemName))
    chooseNewProblem = True

    print("\tOptions:")
    print("\tMark as solved - 1")
    print("\tHINT: Reveal problem category - 2")
    print("\tSkip (pick a different set's problem) - 3")
    print("\tQuit program (don't mark as solved) - 4")

    response = input(colored("Choice: ", "yellow"))
    try:
        response = int(response)
    except:
        print(colored("Not a number, try again", "red"))
    
    match response:
        case 1: # mark solved
            response = input(colored("Good job!", "green") + " Select a message to save next to the problem (leave blank for default 'solved'): ")
            response = response if response != '' else 'solved'
            markSolved(problemSet, problemName, response)
            if len(unsolvedProblems[problemSet]) == 0: # Remove set as a selectable option if finished
                print(colored("Congrats", "green"), "on", colored("completing", "light_magenta"), f"{problemSet}!")
                problemSets.remove(problemSet)
            numRerolls = 0
            handleAfterSolving(problemSet) # As long as this function didn't kill program, keep going
        case 2: # reveal category
            print("The category for", colourProblemName(problemName, False), "is:", colored(problemSet, "light_blue"))
            chooseNewProblem = False
        case 3: # skip and reroll
            if numRerolls >= len(problemSets) - 1:
                print(colored("No more problem sets.", "red"), "Rerolling from every selected set again...")
                numRerolls = 0
            else:
                # Move the chosen problem to the far right of the list and reroll
                lastValidIndex = len(problemSets) - numRerolls - 1
                problemSets[randNum], problemSets[lastValidIndex] = problemSets[lastValidIndex], problemSets[randNum] # swap
                numRerolls += 1
                print("Okay, skipping...")
        case 4: # exit program
            print("Exiting...")
            exit(0)
        case _: # Default case
            print(colored("Invalid number, try again", "red"))

# If we escape the loop, we've run out of problems
print(colored("\nYou've solved every problem in all of your selected categories!", "light_magenta"))
print(colored("Well done, see you next time!", "light_magenta"))
