ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

PAD = 'X'


def parse_number_key(key_str):
    """
    Parses a comma-separated string of 1-based indices into a list of integers.
    Example: '3, 5, 1, 4, 2' -> [3, 5, 1, 4, 2]
    """
    return [int(x.strip()) for x in key_str.split(',')]


def encrypt(plaintext, row_key_str, col_key_str):
    try:
        row_perm = parse_number_key(row_key_str)
        col_perm = parse_number_key(col_key_str)
    except ValueError:
        print("  Error: Keys must be comma-separated numbers.")
        return None

    n_rows = len(row_perm)
    n_cols = len(col_perm)
    block_size = n_rows * n_cols
    
    text = "".join(ch for ch in plaintext.upper() if ch.isalpha())
    print(f"\n  Plaintext       : {text}")

    pad_needed = (block_size - (len(text) % block_size)) % block_size
    text += PAD * pad_needed

    flat_perm = [(row_perm[r]-1) * n_cols + (col_perm[c]-1) 
                 for r in range(n_rows) for c in range(n_cols)]

    ciphertext = ""
    original_grids = []
    permuted_grids = []

    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        new_block = "".join(block[idx] for idx in flat_perm)
        ciphertext += new_block
        
        original_grids.append([list(block[r * n_cols : (r + 1) * n_cols]) for r in range(n_rows)])
        permuted_grids.append([list(new_block[r * n_cols : (r + 1) * n_cols]) for r in range(n_rows)])
            
    return {
        "result": ciphertext,
        "original_grids": original_grids,
        "permuted_grids": permuted_grids,
        "dimensions": {"rows": n_rows, "cols": n_cols}
    }


def decrypt(ciphertext, row_key_str, col_key_str, original_len=None):
    try:
        row_perm = parse_number_key(row_key_str)
        col_perm = parse_number_key(col_key_str)
    except ValueError:
        print("  Error: Keys must be comma-separated numbers.")
        return None

    n_rows = len(row_perm)
    n_cols = len(col_perm)
    block_size = n_rows * n_cols
    
    ciphertext = ciphertext.upper().replace(" ", "")
    if len(ciphertext) % block_size != 0:
        print(f"  Error: Ciphertext length must be a multiple of the block size ({block_size}).")
        return None
    
    flat_perm = [(row_perm[r]-1) * n_cols + (col_perm[c]-1) 
                 for r in range(n_rows) for c in range(n_cols)]

    plaintext = ""
    original_grids = [] 
    permuted_grids = [] 

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        orig_block = [""] * block_size
        for new_idx, orig_idx in enumerate(flat_perm):
            orig_block[orig_idx] = block[new_idx]
        recovered_str = "".join(orig_block)
        plaintext += recovered_str
        
        original_grids.append([list(block[r * n_cols : (r + 1) * n_cols]) for r in range(n_rows)])
        permuted_grids.append([list(recovered_str[r * n_cols : (r + 1) * n_cols]) for r in range(n_rows)])
            
    final_plaintext = plaintext[:original_len] if original_len else plaintext.rstrip(PAD)
    
    return {
        "result": final_plaintext,
        "original_grids": original_grids,
        "permuted_grids": permuted_grids,
        "dimensions": {"rows": n_rows, "cols": n_cols}
    }


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
    print("       DOUBLE TRANSPOSITION CIPHER (MATRIX)")
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
            plaintext = input("  Plaintext                         : ").strip()
            kw1 = input("  Row permutation (e.g., 3,5,1,4,2) : ").strip()
            kw2 = input("  Column permutation (e.g., 1,3,2)  : ").strip()
            res = encrypt(plaintext, kw1, kw2)
            if res:
                print(f"\n  Final Ciphertext: {res['result']}")

        elif choice == "2":
            ciphertext = input("  Ciphertext                        : ").strip()
            kw1 = input("  Row permutation (e.g., 3,5,1,4,2) : ").strip()
            kw2 = input("  Column permutation (e.g., 1,3,2)  : ").strip()
            orig = input("  Original length (Enter to skip)   : ").strip()
            orig_len = int(orig) if orig.isdigit() else None
            res = decrypt(ciphertext, kw1, kw2, orig_len)
            if res:
                print(f"\n  Plaintext: {res['result']}")

        elif choice == "3":
            text = input("  Enter text: ").strip()
            print_frequency_table(text, label="Input")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
