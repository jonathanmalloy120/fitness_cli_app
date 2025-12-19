from datetime import datetime
import json
import os

def start_session():
    #create a new session
    session_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    session = {
        "session_id":session_id,
        "start_time":datetime.now().isoformat(),
        "end_time": None,
        "exercises":[]
    }

    #add session to temp active session file
    with open("active_session.json","w") as file:
        json.dump(session,file, indent=2)
    
    return session

#get the current active session (look for active session in active_session.json)
def get_current_session():
    if os.path.exists("active_session.json"):
        with open("active_session.json", "r") as file:
            return json.load(file)
    else:
        return None

#Add end time to session
def end_session():
    session = get_current_session()
    if session:
        session["end_time"] = datetime.now().isoformat()
        #now write the session to the session log
        #if session log doesn't exist, create it as empty array
        if not os.path.exists("session_log.json"):
            with open("session_log.json","w") as file:
                json.dump([],file)
        #now load session log
        with open("session_log.json","r") as file:
            sessions = json.load(file)
        #add current session to log
        sessions.append(session)
        #write log back
        with open("session_log.json","w") as file:
            json.dump(sessions, file, indent=2)
        #post final message to user
        print(f"Session ended -- You completed {len(session['exercises'])} exercises this session")
        return True
    else:
        print("no active session exists")
        return False

#add an exercise to a session
def add_exercise_to_session(exercise):
    session = get_current_session()
    #if session exists, add exercise to it
    if session:
        session["exercises"].append(exercise)
        #write session back
        with open("active_session.json", "w") as file:
            json.dump(session,file,indent=2)
    else:
        print("Exercise not added, no active session exists")
        return False
    #write session back as active session