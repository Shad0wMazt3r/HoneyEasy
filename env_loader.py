def load(env_var):
    with open(".config") as f:
        for line in f:
            if line.startswith(env_var):
                return line.split("=")[1].strip()
    return None