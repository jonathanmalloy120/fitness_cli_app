import math
import os
import json
import random
import string
from session_management import add_exercise_to_session
from workout_logger import log_workout


#get the exercises that exist from exerises.json (or create it if it doesn't exist)
def load_exercises():
    if os.path.exists("./exercises.json"):
        with open("exercises.json", "r") as file:
            data = json.load(file)
        return data
    else:
        starter_exercises = {
            "push_ups": {
            "name": "Push-Ups",
            "type": "reps",
            "base_amount": 6,
            "scaling_factor": 0.3,
            "description": "Standard push-ups"
        },
        "plank": {
            "name": "Plank",
            "type": "time",
            "base_amount": 30,
            "scaling_factor": 10.0,
            "description": "Hold plank position"
        }
        }
        with open("exercises.json", 'w') as file:
            json.dump(starter_exercises, file, indent=2)
        return starter_exercises

#pick an exercise that was retrieved from our file. Fitness score default is 1 from bash parser so won't be null
def choose_exercise(fitness_score):
    data = load_exercises()
    last_exercise = None
    #check for previous exercise
    if os.path.exists("last_exercise.txt"):
        with open("last_exercise.txt","r") as file:
            last_exercise = file.read().strip()
    #select all possible choices
    choices = list(data.keys())
    #remove previous exercise from list of choices
    if last_exercise and last_exercise in choices:
        choices.remove(last_exercise)
    #choose new exercise
    chosen_exercise_name = random.choice(choices)
    chosen_exercise = data[chosen_exercise_name].copy()

    with open("last_exercise.txt","w") as file:
        file.write(chosen_exercise_name)

    return modify_exercise(chosen_exercise,fitness_score)

#add "amount" to our exercise based on the "base_amount" and fitness score
def modify_exercise(exercise, fitness_score):
    if exercise["type"] == "reps":
        #if reps, scale by the scaling factor per fitness score
        exercise["amount"] = math.floor(exercise["base_amount"] * (1 + (fitness_score - 1) * exercise["scaling_factor"]))
    elif exercise["type"] == "time":
        #if a time exercise, add a scalling factor # of seconds per fitness score
        exercise["amount"] = exercise["base_amount"] + (fitness_score * exercise["scaling_factor"])
    else:
        #if other kind, don't modify (shouldn't happen )
        exercise["amount"] = exercise["base_amount"]

    return exercise

#add a new exercise to the list
def add_exercise():
#gather user input
    #name
    name = input("enter name of new exercise:").strip()

    #type
    type = input("enter exercise type (reps/time):").strip().lower()
    #confirm type is reps or time
    while type not in ["reps","time"]:
        type = input("invalid type, please enter 'reps' or 'time: ").strip().lower()
    
    #base_amount
    while True:
        try:
            base_amount = int(input("enter the base amount of the new exercise: "))
            break #leaves loop entirely if no errors
        except ValueError:
            print("base amount must be an int, please try again: ")
    
    #scaling_factor
    while True:
        try:
            scaling_factor = float(input("enter the scaling factor of the new exercise:"))
            break #leaves loop entirely if no errors
        except ValueError:
            print("scaling factor must be a float, please try again: ")

    #description
    description = input("enter the description of the new exercise:").strip().lower()

    #add exercise
    confirm = input(f"confirm adding {name}, {type}, {base_amount}, {scaling_factor}, {description}? y/n: ")
    if confirm == "y" or confirm =="":
        current_exercises = load_exercises()
        #add new exercise to file
        current_exercises[name.lower().replace(" ","_").replace("-","_")] = {
        "name":name, 
        "type":type, 
        "base_amount":base_amount, 
        "scaling_factor":scaling_factor, 
        "description":description
        }

        with open("exercises.json", 'w') as file:
            json.dump(current_exercises, file, indent=2)
    else:
        print("exercise not added")

    return

def generate_exercise(fitness_score):
    exercise_count = 1
    continue_workout = True
    while continue_workout:
        print(f"Exercise #{exercise_count}")
        exercise =  choose_exercise(fitness_score)
        if exercise["type"] == "reps":
            print(f"Do ~{exercise['amount']}~ {exercise['name']}")
        elif exercise["type"] == "time":
            print(f"Do a {exercise['name']} for ~{exercise['amount']}~ seconds")
        #in case of a different type
        else:
            print(f"Do ~{exercise['amount']}~ {exercise['name']}")
        
        #add logic to see if the user finished the exercise
        completed = input("Did you comeplete the exercise?(y/n) ").strip().lower()
        if completed == "y":
            print("logging exercise")
            #add to larger log
            log_workout(exercise["name"], exercise["amount"], exercise["type"])
            #add to session
            add_exercise_to_session(exercise)
        else:
            print("nothing logged")

        #Check to see if user wants to continue
        continue_response = input("would you like another exercise? (y/n) ").strip().lower()
        if continue_response == "y":
            exercise_count +=1
            print("generating another... ")
        elif continue_response == "n":
            print("ending workouts")
            continue_workout = False
        else:
            print("incorrect input. Ending workouts")
            continue_workout = False