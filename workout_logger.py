from datetime import datetime
import os
import json

#function to log a workout that was completed
def log_workout(name, amount, type):
    #if file doesn't exist, create it
    if not os.path.exists("./workout_log.json"):
        with open("workout_log.json","w") as file:
            json.dump([], file, indent=2) #add empty array

    #get data from log
    with open("workout_log.json", "r") as file:
        data = json.load(file)
    
    #add the new workout to the log
    data.append({"exercise":name, "amount":amount, "type":type, "time":datetime.now().isoformat()})
    
    #write data back to file
    with open("workout_log.json","w") as file:
        json.dump(data, file, indent=2) #add empty array

    return True

#show last {rows} workouts user has completed, pulled from workout_log.json
def show_history(rows=10):
    #make sure log file exists
    if os.path.exists("./workout_log.json"):
        with open("workout_log.json", "r") as file:
            data = json.load(file)
        
        #data is a list of JSON objects in order from oldest to newest, get last X of list
        data_to_print = data[-rows:] #rows from the end
        maxLength = max(len(entry["exercise"]) for entry in data_to_print) if data_to_print else 0 #get the length of the longest exercise for formting

        #print here
        print("=====Recent Workouts=====")
        for row in data_to_print[::-1]:#flips list subset around so oldest gets printed first
            name = row["exercise"]
            type = row["type"]
            amount = row['amount']
            time = datetime.fromisoformat(row["time"]) #first get the timestamp which is stored in log as string
            formattedTime = time.strftime('%Y-%m-%d %H:%M') #now format it

            if type == "reps":
                print(formattedTime, f"{formattedTime} -- {name:<{maxLength}} amount: {amount:<3} reps")
            elif type == "time":
                print(formattedTime, f"{formattedTime} -- {name:<{maxLength}} amount: {amount:<3} seconds")
            else:
                print(formattedTime, f"{formattedTime} -- {name:<{maxLength}} amount: {amount:<3} units")

    #if file doesn't exist, print error message
    else:
        print("log file workout_log.json doesn't exist")
    return

def show_stats():
    #if not workout history, return
    if not os.path.exists("./workout_log.json"):
        print("No workour history detected")
        return
    #get data
    with open("workout_log.json", "r") as file:
            data = json.load(file)
    #initialize dics for counting stats
    exercise_stats ={}
    #calculate stats across exercises
    for exercise in data:
        exercise_name = exercise['exercise']
        if exercise_name in exercise_stats:
            exercise_stats[exercise_name]["set_count"] +=1
            exercise_stats[exercise_name]["total_amount"] += exercise["amount"]
            exercise_stats[exercise_name]["average_amount"] = exercise_stats[exercise_name]["total_amount"]/exercise_stats[exercise_name]["set_count"]

        else:
            exercise_stats[exercise_name] = {
                "set_count":1,
                "total_amount": exercise["amount"],
                "average_amount":exercise["amount"],
                "type": exercise["type"]
            }
    
    #print results
    maxLength = max(len(entry) for entry in exercise_stats.keys()) #get the length of the longest exercise name for formting
    print("=====Workout Stats=====")
    for exercise in exercise_stats: #NOTE, itterating over a dict like this ONLY provides the keys, not the values
        set_count = exercise_stats[exercise]["set_count"] #so here we need to explicitly pull the value
        total_amount = exercise_stats[exercise]["total_amount"]
        type = exercise_stats[exercise]["type"] if exercise_stats[exercise]["type"] == "reps" else "seconds"
        average = exercise_stats[exercise]["average_amount"]
        print(f"Exercise: {exercise:<{maxLength}} Total Sets: {set_count:<2} Total_amount: {total_amount:<6} {type:<7} Average Per Set: {average:5.2f} {type:<7}")

