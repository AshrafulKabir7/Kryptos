ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

PAD = 'X'


def parse_number_key(key_str):
    result = []
    parts = key_str.split(',')
    for part in parts:
        clean_part = part.strip()
        number = int(clean_part)
        result.append(number)
    return result


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
    
    text_list = []
    for ch in plaintext.upper():
        if ch.isalpha():
            text_list.append(ch)
    text = "".join(text_list)
    
    print(f"\n  Plaintext       : {text}")

    remainder = len(text) % block_size
    if remainder != 0:
        pad_needed = block_size - remainder
        for _ in range(pad_needed):
            text += PAD

    ciphertext = ""
    original_grids = []
    permuted_grids = []

    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        
        # Build original matrix explicitly
        orig_grid = []
        for r in range(n_rows):
            row_data = []
            for c in range(n_cols):
                index = r * n_cols + c
                row_data.append(block[index])
            orig_grid.append(row_data)
        
        # Build permuted matrix explicitly
        perm_grid = []
        for new_r in range(n_rows):
            orig_r = row_perm[new_r] - 1
            new_row = []
            for new_c in range(n_cols):
                orig_c = col_perm[new_c] - 1
                char = orig_grid[orig_r][orig_c]
                new_row.append(char)
            perm_grid.append(new_row)
            
        original_grids.append(orig_grid)
        permuted_grids.append(perm_grid)
        
        # Read out the permuted matrix to build ciphertext
        for r in range(n_rows):
            for c in range(n_cols):
                ciphertext += perm_grid[r][c]
            
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
    
    plaintext = ""
    original_grids = [] 
    permuted_grids = [] 

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        
        # Build permuted matrix (this is what we received)
        perm_grid = []
        for r in range(n_rows):
            row_data = []
            for c in range(n_cols):
                index = r * n_cols + c
                row_data.append(block[index])
            perm_grid.append(row_data)
            
        # Reconstruct original matrix
        orig_grid = []
        for r in range(n_rows):
            empty_row = []
            for c in range(n_cols):
                empty_row.append("")
            orig_grid.append(empty_row)
            
        # Fill the original matrix
        for new_r in range(n_rows):
            orig_r = row_perm[new_r] - 1
            for new_c in range(n_cols):
                orig_c = col_perm[new_c] - 1
                char = perm_grid[new_r][new_c]
                orig_grid[orig_r][orig_c] = char
                
        original_grids.append(perm_grid)
        permuted_grids.append(orig_grid)
        
        # Read out the reconstructed matrix
        for r in range(n_rows):
            for c in range(n_cols):
                plaintext += orig_grid[r][c]
            
    if original_len is not None:
        final_plaintext = plaintext[:original_len]
    else:
        final_plaintext = plaintext.rstrip(PAD)
    
    return {
        "result": final_plaintext,
        "original_grids": original_grids,
        "permuted_grids": permuted_grids,
        "dimensions": {"rows": n_rows, "cols": n_cols}
    }


def frequency_analysis(text):
    letters = []
    for ch in text.upper():
        if ch.isalpha():
            letters.append(ch)
    
    total = len(letters)
    if total == 0:
        return {}
    
    result = {}
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
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
            if orig.isdigit():
                orig_len = int(orig)
            else:
                orig_len = None
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
