from datetime import datetime

def PrintLn(ward):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[" + current_time + "] " + ward)
