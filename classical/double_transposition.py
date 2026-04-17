"""
CSE721: Introduction to Cryptography
Classical Cryptography - Double Transposition Cipher
Implements: Encryption, Decryption, Frequency Analysis
"""

import math
from collections import Counter


ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

PAD_CHAR = 'X'


class DoubleTransposition:
    """
    Double Columnar Transposition Cipher.

    Each key is a list of column indices (0-based permutation).
    Example key for 4 columns: [1, 3, 0, 2]
    Alternatively, pass a keyword string and it will be converted.
    """

    # ------------------------------------------------------------------ #
    #  Key helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def keyword_to_permutation(keyword: str) -> list:
        """
        Convert a keyword to a column permutation order.
        E.g., "KEY" -> sorted order: E(0), K(1), Y(2) => positions [1,0,2]
        Returns 0-based list of column read-order.
        """
        keyword = keyword.upper()
        indexed = sorted(range(len(keyword)), key=lambda i: (keyword[i], i))
        # 'indexed' gives: for sorted position j, the original column is indexed[j]
        # We need: for each original column i, what is its read order?
        order = [0] * len(keyword)
        for rank, col in enumerate(indexed):
            order[col] = rank
        return order

    @staticmethod
    def validate_permutation(perm: list) -> bool:
        n = len(perm)
        return sorted(perm) == list(range(n))

    @staticmethod
    def display_grid(text: str, num_cols: int, title: str = "Grid"):
        """Display text arranged in a grid."""
        num_rows = math.ceil(len(text) / num_cols)
        padded = text + PAD_CHAR * (num_rows * num_cols - len(text))
        print(f"\n  {title} ({num_rows} rows × {num_cols} cols):")
        print("  Col: " + " ".join(f"{i:^3}" for i in range(num_cols)))
        print("  " + "-" * (num_cols * 4 + 5))
        for r in range(num_rows):
            row_chars = padded[r * num_cols: (r + 1) * num_cols]
            print(f"  R{r:<2}: " + " ".join(f" {c} " for c in row_chars))

    # ------------------------------------------------------------------ #
    #  Single transposition
    # ------------------------------------------------------------------ #
    def _single_encrypt(self, text: str, key: list) -> str:
        """
        Apply one columnar transposition.
        key: permutation of column indices.
        """
        n_cols = len(key)
        n_rows = math.ceil(len(text) / n_cols)
        # Pad with PAD_CHAR
        padded = text.upper() + PAD_CHAR * (n_rows * n_cols - len(text))

        # Build grid: row-major
        grid = []
        for r in range(n_rows):
            grid.append(list(padded[r * n_cols: (r + 1) * n_cols]))

        # Read columns in sorted order of key
        # key[i] = rank of column i, so we read columns in order of increasing rank
        col_order = sorted(range(n_cols), key=lambda i: key[i])

        result = []
        for col in col_order:
            for row in grid:
                result.append(row[col])
        return "".join(result)

    def _single_decrypt(self, text: str, key: list, original_len: int = None) -> str:
        """
        Reverse one columnar transposition.
        """
        n_cols = len(key)
        n_rows = math.ceil(len(text) / n_cols) if not original_len else math.ceil(original_len / n_cols)
        total = n_rows * n_cols

        # Number of cells in each column
        # All columns have n_rows cells (with possible padding)
        col_order = sorted(range(n_cols), key=lambda i: key[i])

        # Distribute ciphertext back into columns
        col_data = {}
        idx = 0
        for col in col_order:
            col_data[col] = list(text[idx: idx + n_rows])
            idx += n_rows

        # Read row-major to recover padded plaintext
        result = []
        for r in range(n_rows):
            for c in range(n_cols):
                result.append(col_data[c][r])

        recovered = "".join(result)
        # Strip padding
        if original_len is not None:
            recovered = recovered[:original_len]
        else:
            recovered = recovered.rstrip(PAD_CHAR)
        return recovered

    # ------------------------------------------------------------------ #
    #  Double transposition
    # ------------------------------------------------------------------ #
    def encrypt(self, plaintext: str, key1, key2,
                keyword1: str = None, keyword2: str = None) -> tuple:
        """
        Double transposition encryption.
        Pass either (key1, key2) as integer permutation lists OR
        (keyword1, keyword2) as strings.
        Returns (ciphertext, key1_perm, key2_perm).
        """
        if keyword1:
            key1 = self.keyword_to_permutation(keyword1)
        if keyword2:
            key2 = self.keyword_to_permutation(keyword2)

        if not self.validate_permutation(key1):
            raise ValueError(f"Key1 is not a valid permutation: {key1}")
        if not self.validate_permutation(key2):
            raise ValueError(f"Key2 is not a valid permutation: {key2}")

        text = "".join(ch for ch in plaintext.upper() if ch.isalpha())
        print(f"\n  Plaintext (alpha only): {text}")
        self.display_grid(text, len(key1), "Step 1 – Before First Transposition")

        after_first = self._single_encrypt(text, key1)
        print(f"\n  After 1st Transposition: {after_first}")
        self.display_grid(after_first, len(key2), "Step 2 – Before Second Transposition")

        ciphertext = self._single_encrypt(after_first, key2)
        print(f"\n  After 2nd Transposition (Ciphertext): {ciphertext}")
        return ciphertext, key1, key2

    def decrypt(self, ciphertext: str, key1: list, key2: list,
                original_len: int = None) -> str:
        """
        Double transposition decryption.
        Reverses key2 first, then key1.
        """
        ciphertext = ciphertext.upper().replace(" ", "")
        # Pass exact intermediate length to avoid stripping padding X prematurely
        intermediate_len = len(ciphertext)
        after_first_inv = self._single_decrypt(ciphertext, key2, original_len=intermediate_len)
        print(f"\n  After reversing 2nd Transposition: {after_first_inv}")
        plaintext = self._single_decrypt(after_first_inv, key1, original_len)
        print(f"  Recovered Plaintext: {plaintext}")
        return plaintext

    # ------------------------------------------------------------------ #
    #  Frequency analysis (note: transposition preserves letter frequencies)
    # ------------------------------------------------------------------ #
    def frequency_analysis(self, text: str) -> dict:
        """Compute letter frequency statistics."""
        text = text.upper()
        letters = [ch for ch in text if ch.isalpha()]
        total = len(letters)
        if total == 0:
            return {}
        counts = Counter(letters)
        result = {}
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            count = counts.get(letter, 0)
            pct = (count / total) * 100
            result[letter] = (count, round(pct, 2))
        return result

    def display_frequency_analysis(self, text: str, label: str = "Text"):
        """Print formatted frequency analysis. Note: transposition ciphers preserve letter freq."""
        freq = self.frequency_analysis(text)
        if not freq:
            print("  No alphabetic characters found.")
            return

        print(f"\n  Frequency Analysis of {label}:")
        print("  Note: Transposition preserves letter frequencies (same as plaintext).")
        print("  " + "-" * 58)
        print(f"  {'Letter':<8} {'Count':<8} {'Text %':<12} {'English %':<12}")
        print("  " + "-" * 58)
        for letter in sorted(freq, key=lambda x: freq[x][1], reverse=True):
            count, pct = freq[letter]
            eng = ENGLISH_FREQ.get(letter, 0.0)
            bar = "█" * int(pct)
            print(f"  {letter:<8} {count:<8} {pct:<12.2f} {eng:<12.2f} {bar}")
        print("  " + "-" * 58)
        print("  Security Note: Because letter frequencies are preserved, transposition")
        print("  ciphers are vulnerable to frequency analysis — unlike substitution ciphers.")


# ------------------------------------------------------------------ #
#  Interactive CLI
# ------------------------------------------------------------------ #
def run():
    dt = DoubleTransposition()
    print("\n" + "=" * 60)
    print("       DOUBLE TRANSPOSITION CIPHER")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Frequency Analysis")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            plaintext = input("  Enter plaintext: ").strip()
            print("  Key type — enter (1) keyword strings or (2) integer permutations:")
            ktype = input("  Choice [1/2]: ").strip()
            try:
                if ktype == "1":
                    kw1 = input("  First keyword : ").strip()
                    kw2 = input("  Second keyword: ").strip()
                    ct, k1, k2 = dt.encrypt(plaintext, None, None,
                                            keyword1=kw1, keyword2=kw2)
                    print(f"\n  Key 1 permutation: {k1}")
                    print(f"  Key 2 permutation: {k2}")
                else:
                    raw1 = input("  First permutation (space-separated, e.g. 1 3 0 2): ")
                    raw2 = input("  Second permutation: ")
                    k1 = [int(x) for x in raw1.split()]
                    k2 = [int(x) for x in raw2.split()]
                    ct, k1, k2 = dt.encrypt(plaintext, k1, k2)
                print(f"\n  Final Ciphertext: {ct}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "2":
            ciphertext = input("  Enter ciphertext: ").strip()
            print("  Key type — enter (1) keyword strings or (2) integer permutations:")
            ktype = input("  Choice [1/2]: ").strip()
            orig_len = input("  Original plaintext length (optional, press Enter to skip): ").strip()
            orig_len = int(orig_len) if orig_len.isdigit() else None
            try:
                if ktype == "1":
                    kw1 = input("  First keyword : ").strip()
                    kw2 = input("  Second keyword: ").strip()
                    k1 = dt.keyword_to_permutation(kw1)
                    k2 = dt.keyword_to_permutation(kw2)
                else:
                    raw1 = input("  First permutation (space-separated): ")
                    raw2 = input("  Second permutation: ")
                    k1 = [int(x) for x in raw1.split()]
                    k2 = [int(x) for x in raw2.split()]
                pt = dt.decrypt(ciphertext, k1, k2, orig_len)
                print(f"\n  Plaintext: {pt}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            text = input("  Enter text to analyze: ").strip()
            dt.display_frequency_analysis(text, "Input Text")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
