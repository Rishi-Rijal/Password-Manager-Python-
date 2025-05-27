import re
import string
import random
import secrets

def get_password_strength(password: str) -> str:
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"\W", password):
        score += 1

    if score <= 1:
        return "Weak"
    elif score in [2, 3]:
        return "Moderate"
    else:
        return "Strong"
    


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    while(True):
        password = ''.join(random.choice(chars) for _ in range(length))
        if (get_password_strength(password) == "Strong"):
            break

    return password

def random_syllable():
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    return secrets.choice(consonants) + secrets.choice(vowels)

def generate_passphrase(num_words=4, separator='-', include_number=True):
    words = [random_syllable() for _ in range(num_words)]

    if include_number:
        insert_index = secrets.randbelow(len(words) + 1)
        words.insert(insert_index, str(secrets.randbelow(90) + 10))

    return separator.join(words)



