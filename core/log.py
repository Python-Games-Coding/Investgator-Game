from datetime import datetime

def PrintLn(word, moudle="Core"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[" + current_time + "] " + '[' + moudle + '] ' + word)
