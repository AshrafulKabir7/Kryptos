import random
import time


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def miller_rabin(n, k=20):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1
        if miller_rabin(n):
            return n


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist.")
    return x % phi


def string_to_int(msg):
    return int.from_bytes(msg.encode("utf-8"), "big")


def int_to_string(n):
    byte_len = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_len, "big").decode("utf-8", errors="replace")


def trial_division_factor(n, limit=100_000):
    if n % 2 == 0:
        return 2, n // 2
    i = 3
    while i * i <= n and i <= limit:
        if n % i == 0:
            return i, n // i
        i += 2
    return None, None


def pollards_rho(n, max_iter=200_000):
    if n % 2 == 0:
        return 2
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    itr = 0
    while d == 1 and itr < max_iter:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
        itr += 1
    if d != n:
        return d
    return n


def factorization_attack(n, bit_len):
    print(f"\n  [Factorization Attack on {bit_len}-bit modulus]")
    print(f"  n = {n}\n")
    start = time.time()

    p, q = trial_division_factor(n)
    if p and q:
        elapsed = time.time() - start
        print(f"  Method: Trial Division")
        print(f"  p = {p}")
        print(f"  q = {q}")
        print(f"  Time: {elapsed:.4f} s")
        print(f"  p x q == n? {p * q == n}")
        return p, q

    print("  Trying Pollard's Rho algorithm...")
    for attempt in range(20):
        factor = pollards_rho(n)
        if 1 < factor < n:
            p = factor
            q = n // factor
            if p * q == n and miller_rabin(p) and miller_rabin(q):
                elapsed = time.time() - start
                print(f"  Method: Pollard's Rho (attempt {attempt + 1})")
                print(f"  p = {p}")
                print(f"  q = {q}")
                print(f"  Time: {elapsed:.4f} s")
                print(f"  p x q == n? {p * q == n}")
                return p, q

    elapsed = time.time() - start
    print(f"  Factorization FAILED after {elapsed:.2f} s.")
    return None, None


n = None
e = None
d = None
p = None
q = None
bit_size = None


def generate_keys(bits=1024):
    global n, e, d, p, q, bit_size
    bit_size = bits
    half = bits // 2

    print(f"\n  Generating {bits}-bit RSA key pair...")

    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi_n) != 1:
        e = 3
        while gcd(e, phi_n) != 1:
            e += 2

    d = mod_inverse(e, phi_n)
    print("  Key generation complete.")


def display_keys():
    if n is None:
        print("  No keys generated yet.")
        return
    print(f"\n  RSA Key Details ({bit_size}-bit):")
    print("  " + "-" * 60)
    print(f"  p           : {p}")
    print(f"  q           : {q}")
    print(f"  n = p x q   : {n}")
    print(f"  phi(n)      : {(p - 1) * (q - 1)}")
    print(f"  e (public)  : {e}")
    print(f"  d (private) : {d}")
    print("  " + "-" * 60)


def encrypt(message):
    if n is None or e is None:
        raise ValueError("Generate keys first.")
    m = string_to_int(message)
    if m >= n:
        raise ValueError("Message too long for this key size.")
    return pow(m, e, n)


def decrypt(ciphertext):
    if n is None or d is None:
        raise ValueError("Generate keys first.")
    m = pow(ciphertext, d, n)
    return int_to_string(m)


def run():
    print("\n" + "=" * 55)
    print("       RSA PUBLIC-KEY CRYPTOSYSTEM")
    print("=" * 55)

    while True:
        print("\n  1. Generate Keys")
        print("  2. Encrypt a message")
        print("  3. Decrypt a message")
        print("  4. Show key details")
        print("  5. Factorization attack (demo)")
        print("  0. Back")

        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            size_str = input("  Key size in bits [default 1024]: ").strip()
            bits = int(size_str) if size_str.isdigit() else 1024
            generate_keys(bits)
            print(f"  e : {e}")
            print(f"  n : {str(n)[:60]}...")
            print(f"  d : {str(d)[:60]}...")

        elif choice == "2":
            if n is None:
                print("  Generate keys first (option 1).")
                continue
            msg = input("  Plaintext message: ").strip()
            try:
                ct = encrypt(msg)
                print(f"  Plaintext  : {msg}")
                print(f"  Ciphertext : {ct}")
                print(f"  Ciphertext : {hex(ct)}")
            except ValueError as ex:
                print(f"  Error: {ex}")

        elif choice == "3":
            if n is None:
                print("  Generate keys first (option 1).")
                continue
            ct_str = input("  Ciphertext (integer): ").strip()
            try:
                ct = int(ct_str)
                pt = decrypt(ct)
                print(f"  Plaintext : {pt}")
            except Exception as ex:
                print(f"  Error: {ex}")

        elif choice == "4":
            display_keys()

        elif choice == "5":
            if n is None:
                print("  Generate keys first (option 1).")
                continue
            print(f"  Current key size: {bit_size} bits")
            confirm = input("  Attempt factorization? (y/n): ").strip().lower()
            if confirm == "y":
                factorization_attack(n, bit_size)

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
