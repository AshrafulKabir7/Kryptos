"""
CSE721: Introduction to Cryptography
Classical Cryptography - Substitution Cipher
Implements: Encryption, Decryption, Frequency Analysis, Brute Force Attack
"""

import string
from collections import Counter


# Standard English letter frequencies (percentage)
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

# English letters sorted by frequency (most to least common)
ENGLISH_BY_FREQ = sorted(ENGLISH_FREQ, key=ENGLISH_FREQ.get, reverse=True)


class SubstitutionCipher:
    """Monoalphabetic Substitution Cipher with Frequency Analysis and Brute Force."""

    def __init__(self):
        self.alphabet = string.ascii_uppercase

    # ------------------------------------------------------------------ #
    #  Key helpers
    # ------------------------------------------------------------------ #
    def validate_key(self, key: str) -> bool:
        """
        Validates that key is a 26-letter permutation of A-Z.
        E.g. "QWERTYUIOPASDFGHJKLZXCVBNM"
        """
        key = key.upper()
        if len(key) != 26:
            return False
        if sorted(key) != list(self.alphabet):
            return False
        return True

    def key_to_mapping(self, key: str) -> dict:
        """Convert key string to encryption mapping dict: plaintext_letter -> cipher_letter."""
        key = key.upper()
        return {self.alphabet[i]: key[i] for i in range(26)}

    def invert_mapping(self, mapping: dict) -> dict:
        """Invert a mapping for decryption: cipher_letter -> plaintext_letter."""
        return {v: k for k, v in mapping.items()}

    def display_key_table(self, key: str):
        """Print the substitution key table."""
        key = key.upper()
        mapping = self.key_to_mapping(key)
        print("\n  Substitution Key Table:")
        print("  " + "-" * 54)
        plain  = "  Plain : " + " ".join(self.alphabet)
        cipher = "  Cipher: " + " ".join(key)
        print(plain)
        print(cipher)
        print("  " + "-" * 54)

    # ------------------------------------------------------------------ #
    #  Encryption
    # ------------------------------------------------------------------ #
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt plaintext using substitution cipher.
        Non-alphabetic characters are preserved unchanged.
        """
        if not self.validate_key(key):
            raise ValueError("Key must be a 26-letter permutation of A-Z.")

        mapping = self.key_to_mapping(key)
        ciphertext = []
        for ch in plaintext.upper():
            if ch in mapping:
                ciphertext.append(mapping[ch])
            else:
                ciphertext.append(ch)
        return "".join(ciphertext)

    # ------------------------------------------------------------------ #
    #  Decryption
    # ------------------------------------------------------------------ #
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt ciphertext using substitution cipher.
        Non-alphabetic characters are preserved unchanged.
        """
        if not self.validate_key(key):
            raise ValueError("Key must be a 26-letter permutation of A-Z.")

        mapping  = self.key_to_mapping(key)
        inv_map  = self.invert_mapping(mapping)
        plaintext = []
        for ch in ciphertext.upper():
            if ch in inv_map:
                plaintext.append(inv_map[ch])
            else:
                plaintext.append(ch)
        return "".join(plaintext)

    # ------------------------------------------------------------------ #
    #  Frequency Analysis
    # ------------------------------------------------------------------ #
    def frequency_analysis(self, text: str) -> dict:
        """
        Perform frequency analysis on text.
        Returns dict of letter -> (count, percentage).
        """
        text = text.upper()
        letters_only = [ch for ch in text if ch.isalpha()]
        total = len(letters_only)
        if total == 0:
            return {}
        counts = Counter(letters_only)
        result = {}
        for letter in self.alphabet:
            count = counts.get(letter, 0)
            pct = (count / total) * 100
            result[letter] = (count, round(pct, 2))
        return result

    def display_frequency_analysis(self, text: str, label: str = "Text"):
        """Print formatted frequency analysis table."""
        freq = self.frequency_analysis(text)
        if not freq:
            print("  No alphabetic characters found.")
            return

        print(f"\n  Frequency Analysis of {label}:")
        print("  " + "-" * 60)
        print(f"  {'Letter':<8} {'Count':<8} {'Ciphertext%':<14} {'English%':<10} {'Diff'}")
        print("  " + "-" * 60)

        # Sort by ciphertext frequency descending
        for letter in sorted(freq, key=lambda x: freq[x][1], reverse=True):
            count, pct = freq[letter]
            eng_pct = ENGLISH_FREQ.get(letter, 0.0)
            diff = round(pct - eng_pct, 2)
            bar = "█" * int(pct)
            print(f"  {letter:<8} {count:<8} {pct:<14.2f} {eng_pct:<10.2f} {diff:+.2f}  {bar}")
        print("  " + "-" * 60)

    # ------------------------------------------------------------------ #
    #  Brute Force / Frequency-Analysis Attack
    # ------------------------------------------------------------------ #
    def frequency_attack(self, ciphertext: str) -> tuple:
        """
        Attempt to crack substitution cipher using frequency analysis.
        Maps the most frequent cipher letters to the most frequent English letters.
        Returns (guessed_key_string, decrypted_text).
        """
        freq = self.frequency_analysis(ciphertext)
        # Sort cipher letters by their frequency in ciphertext (desc)
        cipher_by_freq = sorted(freq, key=lambda x: freq[x][1], reverse=True)

        # Map cipher letters to English letters by matching frequency ranks
        guessed_mapping = {}
        for i, cipher_letter in enumerate(cipher_by_freq):
            if i < len(ENGLISH_BY_FREQ):
                guessed_mapping[cipher_letter] = ENGLISH_BY_FREQ[i]

        # Build the guessed key string (positions A-Z)
        guessed_key = []
        for plain_letter in self.alphabet:
            # Find which cipher letter maps to this plain letter position
            # guessed_mapping: cipher -> plain, so we need cipher such that
            # cipher -> plain == plain_letter
            found = False
            for c_letter, p_letter in guessed_mapping.items():
                if p_letter == plain_letter:
                    guessed_key.append(c_letter)
                    found = True
                    break
            if not found:
                guessed_key.append('?')

        # Decrypt ciphertext using guessed mapping (cipher->plain)
        decrypted = []
        for ch in ciphertext.upper():
            if ch.isalpha():
                decrypted.append(guessed_mapping.get(ch, '?'))
            else:
                decrypted.append(ch)

        # The "key" in the standard sense: for each plain letter, what cipher letter?
        # We have inv_guessed_mapping: plain -> cipher
        inv_guess = {v: k for k, v in guessed_mapping.items()}
        key_str = "".join(inv_guess.get(l, '?') for l in self.alphabet)

        return key_str, "".join(decrypted)

    def brute_force_display(self, ciphertext: str):
        """
        Display the frequency-analysis based attack result.
        True brute force over 26! keys is computationally infeasible.
        We use the frequency analysis heuristic as a practical approximation.
        """
        print("\n  [!] True brute force over all 26! ≈ 4×10²⁶ keys is computationally")
        print("      infeasible. Using frequency-analysis heuristic attack instead.")
        key_guess, decrypted = self.frequency_attack(ciphertext)
        print(f"\n  Guessed Key (plain->cipher): {key_guess}")
        print(f"  Decrypted Text (guess)     : {decrypted}")
        return key_guess, decrypted


# ------------------------------------------------------------------ #
#  Interactive CLI
# ------------------------------------------------------------------ #
def run():
    sc = SubstitutionCipher()
    print("\n" + "=" * 60)
    print("       SUBSTITUTION CIPHER")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Frequency Analysis")
        print("  4. Brute Force / Frequency Attack")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            plaintext = input("  Enter plaintext: ").strip()
            print("  Enter 26-letter key (e.g. QWERTYUIOPASDFGHJKLZXCVBNM):")
            key = input("  Key: ").strip()
            try:
                sc.display_key_table(key)
                ct = sc.encrypt(plaintext, key)
                print(f"\n  Plaintext : {plaintext.upper()}")
                print(f"  Ciphertext: {ct}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "2":
            ciphertext = input("  Enter ciphertext: ").strip()
            print("  Enter 26-letter key used for encryption:")
            key = input("  Key: ").strip()
            try:
                sc.display_key_table(key)
                pt = sc.decrypt(ciphertext, key)
                print(f"\n  Ciphertext: {ciphertext.upper()}")
                print(f"  Plaintext : {pt}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            text = input("  Enter text to analyze: ").strip()
            sc.display_frequency_analysis(text, label="Input Text")

        elif choice == "4":
            ciphertext = input("  Enter ciphertext to attack: ").strip()
            sc.display_frequency_analysis(ciphertext, label="Ciphertext")
            sc.brute_force_display(ciphertext)

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
