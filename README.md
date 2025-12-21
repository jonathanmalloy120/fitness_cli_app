# Exercise Generator
## A tool for generating and tracking exercises in your workout

This is a basic program designed to recommend exercises for your workout. It comes with a suite of recommended starter exercises, as well as the ability to add your own exercises. It also has basic logging capabilities ad the ability to look back at the exercises you did in an individual workout session, or over all time.

**-----Installation and setup-----**

To install you will need python installed. 

1. Clone the entire repo to a directory and CD into the directory

2. By default, the program will create all files it needs to operate in the root directory as well as a very small exercise set (only pushups and planks). Exercises are stored in exercises.json. 

If desired delete that file (if exists) and rename

    `exercises.example.json -->exercises.json`

To access a larger set of pre-created exercises

**-----Use-----**

There are 4 commands that this program supports:

1.
    `python exercise.py add_exercise`
    This allows you to add excercises to the list of available choices. This will prompt the user to create an exercise by entering 5 inputs:

    1. Name of exercise

    2. "reps" (if the exercise is base on number of repetitions eg a push up) or "time" (if the exercise should be held for a period of time eg a plank)

    3. Base Amount -- The amount or reps/time a user would like for the EASIEST possible set of this exercise. Excerises can be made more difficult by providing a scaling factor

    4. scaling factor -- 
        FOR REPS EXERCISES this should be a float (generally between 0.3 and 0.5, higher values means reps will be added more quickly at higher fitness levels). 
        FOR TIME EXERCISES this should be an int representing the number of additional seconds to add to the exercise per fitness level

    5. A description of the exercise

2.
    `python exercise.py generate`

    This is the main function of the program, and will start a workout session and generate exercises 1 at a time for the user to perform. Each time the program will ask the user if they completed the exercise (y/n) and would they like to generate another (y/n). Once a user declines to enter another exercise, the program will automatically end the workout session

    Optionally, the user may enter a fitness score, for example for a fitness score of 3 use:

    `python exercise.py generate --fitness_score 3`

    higher numbers result in more difficult exercises for the workout session. Note that exercises tend to increase in difficulty quickly

3.
    `python exercise.py stats`

    This will display stats about your workout. By default it will show the most recent completed session, however you can optionally add a session id as follows:

    `python exercise.py stats --sessionID ABC123`

    To show stats on a specicic session. Currently session ids are only stored in session_log.json

4.
    `python exercise.py all_stats`

    This will show you aggregated stats across all workouts ever completed

**-----Example Use-----**

```python
Fitness_app % python exercise.py generate --fitness_score 2
Exercise #1
Do ~15~ Squats
Did you comeplete the exercise?(y/n) y
logging exercise
would you like another exercise? (y/n) y
generating another... 
Exercise #2
Do ~14~ Calf Raises
Did you comeplete the exercise?(y/n) y
logging exercise
would you like another exercise? (y/n) y
generating another... 
Exercise #3
Do ~8~ Arnold Press
Did you comeplete the exercise?(y/n) y
logging exercise
would you like another exercise? (y/n) y
generating another... 

```