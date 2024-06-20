import os

def log(log_data, log_file):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_file = "logs/"+log_file
    with open(log_file, "a") as log:
        log.write(log_data)