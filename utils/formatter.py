from utils.colors import GREEN, CYAN, RESET

def section(title):
    print(CYAN + "\n" + "="*40)
    print(f"[ {title} ]")
    print("="*40 + RESET)

def item(key, value):
    print(GREEN + f"{key}: " + RESET + str(value))
