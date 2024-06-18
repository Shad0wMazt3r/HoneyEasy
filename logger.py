def log(log_data, log_file):
    with open(log_file, "a") as log:
        log.write(log_data)