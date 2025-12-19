import json
import os

#get a session from the log
def get_session(sessionID):
    #if sessionID is "default", just get the most recent session from the log
    if os.path.exists("session_log.json"):
        with open("session_log.json", "r") as file:
            data = json.load(file)
    else:
        print("No session log exists")
        return
    #now, check for the sessionId or if "default"
    if sessionID == "default":
        return data[-1] #return most recent 
    else:
        for session in data:
            if session["session_id"] == sessionID:
                return session #loop through and return matching session
    #if no matching session found, return none
    return None

#calculate and display stats from a given session
def calculate_stats(sessionID):
    session = get_session(sessionID)
    if not session:
        print(f"No session found with id {sessionID}")
    
    print("The session is:", session)