ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

PAD = 'X'


def keyword_to_order(keyword):
    keyword = keyword.upper()
    n = len(keyword)
    pairs = []
    for i in range(n):
        pairs.append((keyword[i], i))
    pairs_sorted = sorted(pairs)
    order = [0] * n
    for rank, (letter, original_col) in enumerate(pairs_sorted):
        order[original_col] = rank
    return order


def columnar_encrypt(text, order):
    n_cols = len(order)
    n_rows = (len(text) + n_cols - 1) // n_cols
    pad_needed = n_rows * n_cols - len(text)
    text = text.upper() + PAD * pad_needed

    grid = []
    for r in range(n_rows):
        row = list(text[r * n_cols:(r + 1) * n_cols])
        grid.append(row)

    read_order = sorted(range(n_cols), key=lambda i: order[i])

    result = []
    for col in read_order:
        for row in grid:
            result.append(row[col])
    return "".join(result)


def columnar_decrypt(text, order, original_len=None):
    n_cols = len(order)
    length = original_len or len(text)
    n_rows = (length + n_cols - 1) // n_cols
    read_order = sorted(range(n_cols), key=lambda i: order[i])

    col_data = {}
    idx = 0
    for col in read_order:
        col_data[col] = list(text[idx:idx + n_rows])
        idx += n_rows

    recovered = "".join(col_data[c][r] for r in range(n_rows) for c in range(n_cols))
    return recovered[:original_len] if original_len else recovered.rstrip(PAD)


def encrypt(plaintext, keyword1, keyword2):
    key1 = keyword_to_order(keyword1)
    key2 = keyword_to_order(keyword2)

    text = "".join(ch for ch in plaintext.upper() if ch.isalpha())
    print(f"\n  Plaintext       : {text}")

    after_first = columnar_encrypt(text, key1)
    print(f"  After round 1   : {after_first}")

    ciphertext = columnar_encrypt(after_first, key2)
    print(f"  Ciphertext      : {ciphertext}")
    return ciphertext


def decrypt(ciphertext, keyword1, keyword2, original_len=None):
    key1 = keyword_to_order(keyword1)
    key2 = keyword_to_order(keyword2)

    ciphertext = ciphertext.upper().replace(" ", "")
    after_undo2 = columnar_decrypt(ciphertext, key2, original_len=len(ciphertext))
    print(f"\n  After undoing round 2: {after_undo2}")

    plaintext = columnar_decrypt(after_undo2, key1, original_len)
    print(f"  Recovered plaintext  : {plaintext}")
    return plaintext


def frequency_analysis(text):
    letters = [ch for ch in text.upper() if ch.isalpha()]
    total = len(letters)
    if total == 0:
        return {}
    return {ch: (letters.count(ch), round(letters.count(ch) / total * 100, 2))
            for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}


def print_frequency_table(text, label="Text"):
    freq = frequency_analysis(text)
    if not freq:
        print("  No letters found.")
        return
    print(f"\n  Frequency Analysis - {label}:")
    print(f"  {'Letter':<8} {'Count':<8} {'Text %':<12} {'English %'}")
    print("  " + "-" * 50)
    for ch in sorted(freq, key=lambda x: freq[x][1], reverse=True):
        count, pct = freq[ch]
        eng = ENGLISH_FREQ.get(ch, 0.0)
        print(f"  {ch:<8} {count:<8} {pct:<12.2f} {eng:.2f}")
    print("\n  Note: Transposition ciphers keep letter frequencies unchanged.")


def run():
    print("\n" + "=" * 55)
    print("       DOUBLE TRANSPOSITION CIPHER")
    print("=" * 55)

    while True:
        print("\n  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Frequency Analysis")
        print("  0. Back")

        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            plaintext = input("  Plaintext      : ").strip()
            kw1 = input("  First keyword  : ").strip()
            kw2 = input("  Second keyword : ").strip()
            ct = encrypt(plaintext, kw1, kw2)
            print(f"\n  Final Ciphertext: {ct}")

        elif choice == "2":
            ciphertext = input("  Ciphertext     : ").strip()
            kw1 = input("  First keyword  : ").strip()
            kw2 = input("  Second keyword : ").strip()
            orig = input("  Original length (Enter to skip): ").strip()
            orig_len = int(orig) if orig.isdigit() else None
            pt = decrypt(ciphertext, kw1, kw2, orig_len)
            print(f"\n  Plaintext: {pt}")

        elif choice == "3":
            text = input("  Enter text: ").strip()
            print_frequency_table(text, label="Input")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
