def load(env_var):
    with open(".config_honeyeasy", "r") as f:
        for line in f:
            if line.startswith(env_var):
                return line.split("=")[1].strip()
    return None
def save(env_var, val):
    with open(".config_honeyeasy", "a") as f:
        f.write(f"{env_var}={val}\n")

def banner_load(env_var):
    env_banner = env_var + "_BANNER"
    banner = ""
    with open(".config_honeyeasy", "r") as f:
        for line in f:
            if line.startswith(env_banner):
                banner = line.split("=")[1].strip().replace("\\n", "\n").replace('"', "")
                return banner
                
