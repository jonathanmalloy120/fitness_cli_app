import argparse
from exercise_manager import  add_exercise, generate_exercise
from workout_logger import show_history, show_stats
from session_management import start_session, end_session
from session_stats import calculate_stats

def main():
    #main parser for our commands
    parser = argparse.ArgumentParser(description="This is an exercise generator")

    #add subparsers for different comands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    #generate command for making an exercise
    generate_parser = subparsers.add_parser("generate", help="create an exercise")
    #add an arguement to the "generate" command (the fitness score)
    generate_parser.add_argument("--fitness_score", type=int, default=1, help="a difficulty multiplier for the exercise (default 1)")

    #command for adding an exercise to the list
    add_exercise_parser = subparsers.add_parser("add_exercise", help="add this exercise to the list")

    #command for listing all available exercises
    list_exercise_parser = subparsers.add_parser("all_stats", help="see all excerice stats")

    #command for getting stats on a specific session
    session_stat_parser = subparsers.add_parser("stats", help="see stats on a specific session")
    session_stat_parser.add_argument("--sessionID", type=str, default="default", help="the id of ther session you want stats about")
    
    args = parser.parse_args()
    #**************************************
    #generate command for creating an exercise for the user to do
    # python exercise.py generate
    # --fitness_score <int>
    #**************************************
    if args.command == "generate":
        start_session()
        generate_exercise(args.fitness_score)
        end_session()

    #**************************************
    #add exercise command for adding a new exercise to the list of available option
    #python exercise.py add_exercise
    #**************************************
    elif args.command == "add_exercise":
        print("add exercise command detected")
        #all logic moved into function
        add_exercise()
        
    #**************************************
    #list exercise command for printing our workout history
    #python exercise.py all_stats
    #**************************************
    elif args.command == "all_stats":
        print("list exercise command detected")
        show_history()
        show_stats()

    #**************************************
    #list exercise command for printing our workout history
    #python exercise.py stats
    # --sessionID <string>
    #**************************************    
    elif args.command == "stats":
        print("stats command detected")
        calculate_stats(args.sessionID)

if __name__ == "__main__":
    main()