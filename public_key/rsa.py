"""
CSE721: Introduction to Cryptography
Public-Key Cryptography - RSA
Implements: Key Generation, Encryption, Decryption, Factorization Attack
No external crypto libraries used. Big-integer arithmetic via Python's built-in int.
"""

import os
import math
import random
import time


# ============================================================
#  Number Theory Utilities
# ============================================================

def miller_rabin(n: int, k: int = 20) -> bool:
    """
    Miller-Rabin probabilistic primality test.
    Returns True if n is probably prime, False if composite.
    k = number of rounds (higher k = lower false-positive rate).
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
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


def generate_prime(bits: int) -> int:
    """Generate a random probable prime of the given bit length."""
    while True:
        n = random.getrandbits(bits)
        # Set MSB and LSB to ensure correct bit length and odd number
        n |= (1 << (bits - 1)) | 1
        if miller_rabin(n):
            return n


def extended_gcd(a: int, b: int) -> tuple:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def mod_inverse(e: int, phi: int) -> int:
    """Compute modular inverse of e mod phi using extended GCD."""
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist (gcd != 1).")
    return x % phi


# ============================================================
#  Factorization Attacks
# ============================================================

def trial_division_factor(n: int, limit: int = 10_000_000) -> tuple:
    """
    Trial division: finds small prime factors up to `limit`.
    Feasible for small RSA keys (up to ~256-bit demos).
    Returns (p, q) if factored, else (None, None).
    """
    if n % 2 == 0:
        return 2, n // 2
    i = 3
    while i * i <= n and i <= limit:
        if n % i == 0:
            return i, n // i
        i += 2
    return None, None


def pollards_rho(n: int, max_iter: int = 100_000) -> int:
    """
    Pollard's Rho algorithm for integer factorization.
    Returns a non-trivial factor of n, or n itself if failed.
    """
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
        d = math.gcd(abs(x - y), n)
        itr += 1
    if d != n:
        return d
    return n   # Failed


def factorization_attack(n: int, bit_len: int) -> tuple:
    """
    Attempt to factor RSA modulus n.
    Uses Pollard's rho (practical up to ~256-bit keys in reasonable time).
    Returns (p, q) or (None, None) if failed/timeout.
    """
    print(f"\n  [Factorization Attack on {bit_len}-bit modulus]")
    print(f"  n = {n}")
    print()

    start = time.time()

    # Try trial division for tiny factors
    p, q = trial_division_factor(n, limit=100_000)
    if p and q:
        elapsed = time.time() - start
        print(f"  Method: Trial Division")
        print(f"  p = {p}")
        print(f"  q = {q}")
        print(f"  Time: {elapsed:.4f} s")
        print(f"  Verification: p × q == n? {p * q == n}")
        return p, q

    # Try Pollard's rho
    print("  Trying Pollard's Rho algorithm...")
    for attempt in range(20):
        factor = pollards_rho(n, max_iter=200_000)
        if 1 < factor < n:
            p = factor
            q = n // factor
            if p * q == n and miller_rabin(p) and miller_rabin(q):
                elapsed = time.time() - start
                print(f"  Method: Pollard's Rho (attempt {attempt+1})")
                print(f"  p = {p}")
                print(f"  q = {q}")
                print(f"  Time: {elapsed:.4f} s")
                print(f"  Verification: p × q == n? {p * q == n}")
                return p, q

    elapsed = time.time() - start
    print(f"  Factorization FAILED after {elapsed:.2f} s.")
    print(f"  Note: Practical attacks on 512+ bit RSA moduli require")
    print(f"        specialized algorithms (GNFS) and significant compute.")
    return None, None


# ============================================================
#  Message Encoding / Decoding
# ============================================================

def string_to_int(msg: str) -> int:
    """Encode a string as a big integer (UTF-8 bytes)."""
    return int.from_bytes(msg.encode("utf-8"), "big")

def int_to_string(n: int) -> str:
    """Decode a big integer back to a UTF-8 string."""
    byte_len = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_len, "big").decode("utf-8", errors="replace")


# ============================================================
#  RSA Class
# ============================================================

class RSA:
    """
    Textbook RSA implementation.
    Warning: Textbook RSA is NOT semantically secure — use only for educational purposes.
    """

    def __init__(self):
        self.n   = None
        self.e   = None
        self.d   = None
        self.p   = None
        self.q   = None
        self.bit_size = None

    # ------------------------------------------------------------------ #
    #  Key generation
    # ------------------------------------------------------------------ #
    def generate_keys(self, bits: int = 1024):
        """
        Generate RSA key pair of the given modulus bit size.
        Supported: 512, 1024 (or any valid size).
        """
        self.bit_size = bits
        half = bits // 2

        print(f"\n  Generating {bits}-bit RSA key pair...")
        print("  (Generating two distinct primes p and q...)")

        # Generate two distinct primes of half the key size
        self.p = generate_prime(half)
        self.q = generate_prime(half)
        while self.q == self.p:
            self.q = generate_prime(half)

        self.n = self.p * self.q
        phi_n  = (self.p - 1) * (self.q - 1)

        # Choose e: commonly 65537
        self.e = 65537
        if math.gcd(self.e, phi_n) != 1:
            # Fallback: find a valid e
            self.e = 3
            while math.gcd(self.e, phi_n) != 1:
                self.e += 2

        # Compute d = e^-1 mod phi(n)
        self.d = mod_inverse(self.e, phi_n)

        print(f"\n  ✓ Key generation complete.")
        return self.get_public_key(), self.get_private_key()

    def get_public_key(self) -> dict:
        return {"n": self.n, "e": self.e, "bits": self.bit_size}

    def get_private_key(self) -> dict:
        return {"n": self.n, "d": self.d, "p": self.p, "q": self.q}

    def display_keys(self):
        """Print public and private key details."""
        if self.n is None:
            print("  No keys generated yet.")
            return
        print(f"\n  RSA Key Details ({self.bit_size}-bit):")
        print("  " + "-" * 70)
        print(f"  p (first prime)   : {self.p}")
        print(f"  q (second prime)  : {self.q}")
        print(f"  n = p×q (modulus) : {self.n}")
        print(f"  φ(n) = (p-1)(q-1) : {(self.p-1)*(self.q-1)}")
        print(f"  e (public exponent): {self.e}")
        print(f"  d (private exponent): {self.d}")
        print("  " + "-" * 70)
        print(f"  Public  Key: (e={self.e}, n=<{self.bit_size}-bit number>)")
        print(f"  Private Key: (d=<{self.bit_size}-bit number>, n=<{self.bit_size}-bit number>)")

    # ------------------------------------------------------------------ #
    #  Encryption / Decryption
    # ------------------------------------------------------------------ #
    def encrypt(self, message: str, n: int = None, e: int = None) -> int:
        """
        Encrypt message string using RSA public key (e, n).
        Returns ciphertext as integer.
        """
        n = n or self.n
        e = e or self.e
        if n is None or e is None:
            raise ValueError("Public key (n, e) not set. Generate keys first.")

        m = string_to_int(message)
        if m >= n:
            raise ValueError("Message too long for this key size.")
        c = pow(m, e, n)
        return c

    def decrypt(self, ciphertext: int, n: int = None, d: int = None) -> str:
        """
        Decrypt ciphertext integer using RSA private key (d, n).
        Returns original message string.
        """
        n = n or self.n
        d = d or self.d
        if n is None or d is None:
            raise ValueError("Private key (n, d) not set. Generate keys first.")

        m = pow(ciphertext, d, n)
        return int_to_string(m)

    # ------------------------------------------------------------------ #
    #  Factorization attack demo
    # ------------------------------------------------------------------ #
    def run_factorization_attack(self):
        """
        Demonstrate factorization attack on the current RSA modulus.
        Practical only for small key sizes (≤ 256 bits in reasonable time).
        """
        if self.n is None:
            print("  No keys generated. Run key generation first.")
            return
        factorization_attack(self.n, self.bit_size)


# ============================================================
#  Interactive CLI
# ============================================================

def run():
    rsa = RSA()
    print("\n" + "=" * 60)
    print("       RSA PUBLIC-KEY CRYPTOSYSTEM")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("  1. Generate Keys")
        print("  2. Encrypt a message")
        print("  3. Decrypt a message")
        print("  4. Show key details")
        print("  5. Factorization attack (demo)")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            print("  Key sizes: 512 / 1024 / custom")
            size_str = input("  Enter key size in bits [default 1024]: ").strip()
            bits = int(size_str) if size_str.isdigit() else 1024
            pub, priv = rsa.generate_keys(bits)
            print(f"\n  Public Key  (e): {pub['e']}")
            print(f"  Public Key  (n): {str(pub['n'])[:60]}...")
            print(f"  Private Key (d): {str(priv['d'])[:60]}...")

        elif choice == "2":
            if rsa.n is None:
                print("  Please generate keys first (option 1).")
                continue
            msg = input("  Enter plaintext message: ").strip()
            try:
                ct = rsa.encrypt(msg)
                print(f"\n  Plaintext   : {msg}")
                print(f"  Ciphertext  : {ct}")
                print(f"  Ciphertext  : {hex(ct)}")
            except ValueError as ex:
                print(f"  Error: {ex}")

        elif choice == "3":
            if rsa.n is None:
                print("  Please generate keys first (option 1).")
                continue
            ct_str = input("  Enter ciphertext (integer): ").strip()
            try:
                ct = int(ct_str)
                pt = rsa.decrypt(ct)
                print(f"\n  Ciphertext : {ct}")
                print(f"  Plaintext  : {pt}")
            except Exception as ex:
                print(f"  Error: {ex}")

        elif choice == "4":
            rsa.display_keys()

        elif choice == "5":
            if rsa.n is None:
                print("  Please generate keys first (option 1).")
                continue
            print("\n  Note: For demonstration, use a small key (e.g. 64 or 128 bits).")
            print(f"  Current key size: {rsa.bit_size} bits")
            confirm = input("  Attempt factorization? (y/n): ").strip().lower()
            if confirm == "y":
                rsa.run_factorization_attack()

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
