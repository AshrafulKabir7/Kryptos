ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

ENGLISH_BY_FREQ = sorted(ENGLISH_FREQ, key=ENGLISH_FREQ.get, reverse=True)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def validate_key(key):
    key = key.upper()
    if len(key) != 26:
        return False
    if sorted(key) != list(ALPHABET):
        return False
    return True

def make_enc_map(key):
    key = key.upper()
    mapping = {}
    for i in range(26):
        mapping[ALPHABET[i]] = key[i]
    return mapping


def encrypt(plaintext, key):
    if not validate_key(key):
        raise ValueError("Key must be a 26-letter permutation of A-Z.")
    enc_map = make_enc_map(key)
    result = []
    for ch in plaintext.upper():
        if ch in enc_map:
            result.append(enc_map[ch])
        else:
            result.append(ch)
    return "".join(result)


def decrypt(ciphertext, key):
    if not validate_key(key):
        raise ValueError("Key must be a 26-letter permutation of A-Z.")
    enc_map = make_enc_map(key)
    dec_map = {}
    for plain, cipher in enc_map.items():
        dec_map[cipher] = plain
    result = []
    for ch in ciphertext.upper():
        if ch in dec_map:
            result.append(dec_map[ch])
        else:
            result.append(ch)
    return "".join(result)


def frequency_analysis(text):
    letters = []
    for ch in text.upper():
        if ch.isalpha():
            letters.append(ch)
    total = len(letters)
    if total == 0:
        return {}
    result = {}
    for ch in ALPHABET:
        count = letters.count(ch)
        percentage = round(count / total * 100, 2)
        result[ch] = (count, percentage)
    return result


def print_frequency_table(text, label="Text"):
    freq = frequency_analysis(text)
    if not freq:
        print("  No letters found.")
        return
    print(f"\n  Frequency Analysis - {label}:")
    print(f"  {'Letter':<8} {'Count':<8} {'Text %':<12} {'English %':<12} Diff")
    print("  " + "-" * 58)
    for ch in sorted(freq, key=lambda x: freq[x][1], reverse=True):
        count, pct = freq[ch]
        eng = ENGLISH_FREQ.get(ch, 0.0)
        print(f"  {ch:<8} {count:<8} {pct:<12.2f} {eng:<12.2f} {pct - eng:+.2f}")


def frequency_attack(ciphertext):
    freq = frequency_analysis(ciphertext)

    cipher_ranked = sorted(freq, key=lambda x: freq[x][1], reverse=True)

    guess = {}
    for i in range(26):
        cipher_letter = cipher_ranked[i]
        english_letter = ENGLISH_BY_FREQ[i]
        guess[cipher_letter] = english_letter

    decrypted = []
    for ch in ciphertext.upper():
        if ch.isalpha():
            decrypted.append(guess.get(ch, ch))
        else:
            decrypted.append(ch)

    inv = {}
    for cipher_letter, plain_letter in guess.items():
        inv[plain_letter] = cipher_letter

    key_str = ""
    for ch in ALPHABET:
        key_str += inv.get(ch, '?')

    return key_str, "".join(decrypted)


def run():
    print("\n" + "=" * 55)
    print("         SUBSTITUTION CIPHER")
    print("=" * 55)

    while True:
        print("\n  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Frequency Analysis")
        print("  4. Frequency Attack")
        print("  0. Back")

        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            plaintext = input("  Plaintext : ").strip()
            key = input("  Key (26 letters): ").strip()
            try:
                ct = encrypt(plaintext, key)
                print(f"  Ciphertext: {ct}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "2":
            ciphertext = input("  Ciphertext: ").strip()
            key = input("  Key (26 letters): ").strip()
            try:
                pt = decrypt(ciphertext, key)
                print(f"  Plaintext : {pt}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            text = input("  Enter text: ").strip()
            print_frequency_table(text, label="Input")

        elif choice == "4":
            ciphertext = input("  Ciphertext to attack: ").strip()
            print("  (Using frequency analysis — true brute force over 26! keys is infeasible)")
            key_guess, result = frequency_attack(ciphertext)
            print(f"  Guessed Key: {key_guess}")
            print(f"  Decrypted  : {result}")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
