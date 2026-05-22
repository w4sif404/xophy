from utils.colors import CYAN, GREEN, RESET

def show_menu():
    print(CYAN + "\nSelect Recon Module:\n" + RESET)
    print(GREEN + "1️⃣  WHOIS Lookup")
    print("2️⃣  DNS Enumeration")
    print("3️⃣  Email OSINT")
    print("4️⃣  Run All")
    print("0️⃣  Exit" + RESET)

    choice = input("\nEnter choice: ")
    return choice.strip()
