import re
import math
import getpass


def assess(password):
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_num   = bool(re.search(r'[0-9]', password))
    has_sym   = bool(re.search(r'[^A-Za-z0-9]', password))
    no_repeat = not bool(re.search(r'(.)\1\1', password))
    long_enough = length >= 12

    pool = 0
    if has_upper: pool += 26
    if has_lower: pool += 26
    if has_num:   pool += 10
    if has_sym:   pool += 32

    entropy = round(length * math.log2(pool)) if pool > 0 and length > 0 else 0

    criteria = {
        "At least 12 characters": long_enough,
        "Uppercase letter (A-Z)": has_upper,
        "Lowercase letter (a-z)": has_lower,
        "Number (0-9)":           has_num,
        "Special character":      has_sym,
        "No triple-repeats":      no_repeat,
    }

    passed = sum(criteria.values())

    if entropy == 0:        tier, label = 0, "Very weak"
    elif entropy < 28:      tier, label = 1, "Very weak"
    elif entropy < 36:      tier, label = 2, "Weak"
    elif entropy < 50:      tier, label = 3, "Fair"
    elif entropy < 60:      tier, label = 4, "Good"
    elif entropy < 80:      tier, label = 5, "Strong"
    else:                   tier, label = 6, "Very strong"

    tips = []
    if not long_enough: tips.append("Make it at least 12 characters — length matters most.")
    if not has_upper:   tips.append("Add an uppercase letter (A–Z).")
    if not has_lower:   tips.append("Add a lowercase letter (a–z).")
    if not has_num:     tips.append("Include at least one number (0–9).")
    if not has_sym:     tips.append("Use a special character like !, @, #, $, or %.")
    if not no_repeat:   tips.append("Avoid repeating the same character 3+ times in a row.")
    if tier <= 2:       tips.append("Try a passphrase: four random words are memorable and strong.")

    return {
        "length": length,
        "pool": pool,
        "entropy": entropy,
        "tier": tier,
        "label": label,
        "criteria": criteria,
        "passed": passed,
        "crack_time": crack_time(entropy),
        "tips": tips,
    }


def crack_time(entropy):
    if entropy == 0:
        return "instant"
    guesses_per_sec = 1e10
    secs = (2 ** entropy) / guesses_per_sec
    if secs < 1:        return "< 1 second"
    if secs < 60:       return f"{int(secs)} seconds"
    if secs < 3600:     return f"{int(secs/60)} minutes"
    if secs < 86400:    return f"{int(secs/3600)} hours"
    if secs < 31536000: return f"{int(secs/86400)} days"
    if secs < 3.15e9:   return f"{int(secs/31536000)} years"
    return "centuries"


def bar(tier, width=30):
    filled = int((tier / 6) * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def color(text, tier):
    codes = {1: "\033[91m", 2: "\033[93m", 3: "\033[33m",
             4: "\033[32m", 5: "\033[36m", 6: "\033[92m"}
    reset = "\033[0m"
    return f"{codes.get(tier, '')}{text}{reset}"


def print_report(r):
    print()
    print("=" * 44)
    print("         Password Strength Report")
    print("=" * 44)

    label_colored = color(r["label"], r["tier"])
    print(f"\n  Strength : {label_colored}")
    print(f"  {bar(r['tier'])}")

    print(f"\n  Length      : {r['length']} characters")
    print(f"  Char pool   : {r['pool']} possible characters")
    print(f"  Entropy     : {r['entropy']} bits")
    print(f"  Crack time  : {r['crack_time']}  (at 10B guesses/sec)")

    print(f"\n  Criteria ({r['passed']}/6 passed):")
    for name, passed in r["criteria"].items():
        mark = color("✔", 5) if passed else color("✘", 1)
        print(f"    {mark}  {name}")

    if r["tips"]:
        print("\n  Suggestions:")
        for tip in r["tips"]:
            print(f"    •  {tip}")

    print()


def main():
    print("=" * 44)
    print("      Password Strength Checker")
    print("=" * 44)

    while True:
        print("\nOptions:")
        print("  1. Check a password (hidden input)")
        print("  2. Check a password (visible input)")
        print("  3. Exit")

        choice = input("\nChoose (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break
        elif choice == "1":
            password = getpass.getpass("  Enter password: ")
        elif choice == "2":
            password = input("  Enter password: ")
        else:
            print("  Invalid choice.")
            continue

        if not password:
            print("  No password entered.")
            continue

        result = assess(password)
        print_report(result)


if __name__ == "__main__":
    main()
