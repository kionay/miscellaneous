import random
import os

# Increase these two global variables to increase the difficulty.
approved_inputs = [1,2,3,4,5,6]
code_length = 4

rules = """
The object of the game: guess the secret {0}-digit number.
The {0}-digit number only contains these inputs: {1}

After each guess you are given feedback in the form of
    (*) Asterisks and
    (-) Dashes.

Each set of feedback will be up to {0} combinations of asterisks and dashes.

An asterisk is placed for each number that is correct in both color and position.
A dash indicates the existence of a correct number, but in the wrong position.

If there are duplicate numbers in the guess they cannot all be awarded a symbol unless they correspond to the same amount of duplicate numbers in the hidden answer.

For example, if the code is 4 digits long, the hidden number is 5577, and you guess 5557 then the feedback provided will be two asterisks for the two correct 5's, nothing for the third 5 as there is not a third 5 in the answer, and another asterisk for the 7.
No indication is given of the fact that the answer also includes a second 7.
""".format(code_length,approved_inputs)

def clear_screen(): # handles windows and linux
    clear_screen_map = {"nt":"cls", # windows
                        "posix":"clear"} # linux
    os.system(clear_screen_map[os.name])

def get_feedback(code,guess):
    feedback_reply = ""
    for index,item in enumerate(guess):
        if item == code[index]: # correct number, correct position
            feedback_reply += "*"
        elif item in code: # correct number, wrong position
            feedback_reply += "-"
        else:
            # I'm using a zero character to pad the feedback, it ends up being removed.
            feedback_reply += "0"
    index_replace_list = []
    # This next for loop is key. We need to remove dashes if that number has already been hinted with an asterisk
    # For example, if the code is 5577 and they guess 5557 we're giving them three asterisks. Two for the first two 5s and one for the last seven.
    # Doing 'char in code' for dashes will yield a feedback of "**-*", but according to the original game since we already provided asterisks for the number 5 then it does not also get a dash.
    for index,item in enumerate(feedback_reply):
        if item == "-": # only do this to dashes
            for idx in range(0,code_length):
                # If this guessed item == the -'ed guess item (but skips the dashed position)
                if guess[idx] == guess[index] and idx != index and feedback_reply[idx] == "*":
                    # If we have already given that number an asterisk in the feedback somewhere else
                    # Add it to the list we will use to remove characters.
                    index_replace_list.append(index)       
    for item in index_replace_list:
        feedback_reply = feedback_reply[:item] + "0" + feedback_reply[item+1:] # replace the found 'invalid' dashes with zeros
    # We return having replaced the zeroes with nothing, and then sorting the feedback.
    # The sorting is so that the position of asterisks and dashes doesn't clue you in to the answer.
    # Asterisks are always first, dashes are always second.
    return "".join(sorted(feedback_reply.replace("0","")))

def after_game():
    replay = yes_no("Would you like to play again? (Y/n)")
    if replay:
        return True
    else:
        clear_screen()
        menu = yes_no("Would you like to return to the main menu? (Y/n)")
        if menu:
            # A keen eye will note that handle_menu is actually recursion here.
            # Some recursion seems more elegent to me than trying to logically decurse.
            # Similarly I have a feeling that memories issues aren't going to arise from such a simple program.
            handle_menu()
        else:
            input("Press any key to exit.")
            exit()

def yes_no(question,loop=True):
    affirm_list = ["Y","YES","YE","SI","OUI","YA","YAH","YEAH","YUS","SURE"] # I like to be verbose.
    negate_list = ["N","NO","NIET","NEIN","JO","NE"]
    first = True
    while first or loop:
        first = False
        reply = input(question).upper() # always do .upper() to make the answer case-insensitive
        if reply == "" or reply in affirm_list:
            return True
        elif reply in negate_list:
            return False
        else:
            print("Unknown Response.")
        
    
def play_game():
    clear_screen()
    replay_flag = True
    while replay_flag: # replay loop
        code = "".join([str(random.choice(approved_inputs)) for x in range(0,code_length)])
        try_count = 0
        print("The code has been set.")
        guess_flag = True
        while guess_flag:
            this_guess = input("Tries remining: {0:02d}. Your guess: ".format(10-try_count)) # always let them know how many tries are left
            # Limit guessing to being only numbers, being only 4 characters long, and being within a list of approved numbers (6 to make it easier.)
            if this_guess.isdigit() and len(this_guess) == code_length and any(str(num) in this_guess for num in approved_inputs):
                #valid formatted guess
                if this_guess == code: # correct answer
                    clear_screen()
                    print("{} is correct!".format(code))
                    if after_game():
                        clear_screen()
                        break
                if try_count >= 9: # wrong answer + game over
                    clear_screen()
                    print("The code was {}".format(code))
                    print("You used all of your guesses. Game Over.")
                    if after_game():
                        clear_screen()
                        break
                try_count += 1 # wrong answer
                feedback = get_feedback(code,this_guess) # get feedback and print it
                print("Feedback: {}".format(feedback))
            else:
                print("Guess is in an invalid format. Must be {} inputs from this list: {}".format(code_length,approved_inputs))
                continue

# display_menu is only called by hadle_menu.
# I separated it out into a small function to make changing the 'UI' easier.
def display_menu(error=""): 
    print("\t--Mastermind--")
    print(error)
    print("1. Play\n"
          "2. Rules\n"
          "3. Exit\n")
    return input("choice: ")

# Simple menu logic.
def handle_menu():
    menu_error = ""
    while True:
        clear_screen()
        menu_choice = display_menu(menu_error)
        menu_error = ""
        if menu_choice not in ["1","2","3"]:
            os.system("cls")
            menu_error = "Unknown menu choice, please try again."
            continue
        elif menu_choice == "1":
            play_game()
        elif menu_choice == "2":
            clear_screen()
            print(rules)
            input("Press any key to return to the menu.")
            continue
        else:
            input("Press any key to exit.")
            exit()

handle_menu()
