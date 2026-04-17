"""
CSE721: Introduction to Cryptography
Symmetric-Key Cryptography - Data Encryption Standard (DES)
Implements: Encryption, Decryption, Key Schedule (all 16 round keys)
Fully from scratch — no external crypto libraries.
"""

import os
import struct


# ============================================================
#  DES LOOKUP TABLES (standard FIPS 46-3)
# ============================================================

# Initial Permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7,
]

# Final Permutation (IP^-1)
FP = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
]

# Expansion E (32-bit -> 48-bit)
E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1,
]

# P permutation (32-bit)
P = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25,
]

# Permuted Choice 1 (PC1) — 64-bit key -> 56-bit
PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4,
]

# Permuted Choice 2 (PC2) — 56-bit -> 48-bit subkey
PC2 = [
    14, 17, 11, 24,  1,  5,  3, 28,
    15,  6, 21, 10, 23, 19, 12,  4,
    26,  8, 16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32,
]

# Left-shift schedule for key schedule
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-Boxes (S1..S8), each 4 rows × 16 cols
SBOXES = [
    # S1
    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
    ],
    # S2
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
    ],
    # S3
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],
    ],
    # S4
    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
    ],
    # S5
    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
    ],
    # S6
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
    ],
    # S7
    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
    ],
    # S8
    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
    ],
]


# ============================================================
#  Bit-manipulation helpers
# ============================================================

def bytes_to_bits(data: bytes) -> list:
    """Convert bytes to list of bits (MSB first)."""
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits: list) -> bytes:
    """Convert list of bits (MSB first) back to bytes."""
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        out.append(byte)
    return bytes(out)

def permute(bits: list, table: list) -> list:
    """Apply a permutation table (1-indexed) to a bit list."""
    return [bits[t - 1] for t in table]

def xor_bits(a: list, b: list) -> list:
    """XOR two equal-length bit lists."""
    return [x ^ y for x, y in zip(a, b)]

def left_rotate(bits: list, n: int) -> list:
    """Left-rotate a bit list by n positions."""
    return bits[n:] + bits[:n]

def bits_to_int(bits: list) -> int:
    val = 0
    for b in bits:
        val = (val << 1) | b
    return val

def int_to_bits(val: int, length: int) -> list:
    bits = []
    for i in range(length - 1, -1, -1):
        bits.append((val >> i) & 1)
    return bits


# ============================================================
#  DES Core
# ============================================================

class DES:
    """
    Full DES (Data Encryption Standard) implementation from scratch.
    Operates on 8-byte (64-bit) blocks with a 56-bit effective key (64-bit with parity).
    """

    def __init__(self):
        self._subkeys = []          # List of 16 × 48-bit round keys
        self._key_hex = ""

    # ------------------------------------------------------------------ #
    #  Key schedule
    # ------------------------------------------------------------------ #
    def generate_subkeys(self, key_bytes: bytes) -> list:
        """
        Generate 16 subkeys from the 64-bit DES key.
        Returns list of 16 sublists, each 48 bits.
        """
        assert len(key_bytes) == 8, "DES key must be exactly 8 bytes (64 bits)."
        key_bits = bytes_to_bits(key_bytes)
        # PC1: 64 -> 56 bits
        key56 = permute(key_bits, PC1)
        C, D = key56[:28], key56[28:]

        subkeys = []
        for i in range(16):
            C = left_rotate(C, SHIFT_SCHEDULE[i])
            D = left_rotate(D, SHIFT_SCHEDULE[i])
            CD = C + D
            subkey = permute(CD, PC2)   # 56 -> 48 bits
            subkeys.append(subkey)

        self._subkeys = subkeys
        return subkeys

    # ------------------------------------------------------------------ #
    #  Feistel F-function
    # ------------------------------------------------------------------ #
    def _f_function(self, R: list, subkey: list) -> list:
        """
        DES Feistel F-function:
        E(R) XOR K -> 8 S-boxes -> P permutation
        """
        # Expansion: 32 -> 48 bits
        R_expanded = permute(R, E)
        # XOR with subkey
        xored = xor_bits(R_expanded, subkey)
        # S-box substitution: 48 -> 32 bits
        sbox_out = []
        for i in range(8):
            block6 = xored[i * 6: (i + 1) * 6]
            row = (block6[0] << 1) | block6[5]        # bits 1 and 6
            col = bits_to_int(block6[1:5])             # bits 2-5
            val = SBOXES[i][row][col]
            sbox_out.extend(int_to_bits(val, 4))
        # P permutation: 32 -> 32 bits
        return permute(sbox_out, P)

    # ------------------------------------------------------------------ #
    #  Block cipher (one 8-byte block)
    # ------------------------------------------------------------------ #
    def _process_block(self, block: bytes, encrypt: bool) -> bytes:
        """Encrypt or decrypt a single 8-byte block."""
        bits = bytes_to_bits(block)
        # Initial permutation
        bits = permute(bits, IP)
        L, R = bits[:32], bits[32:]

        keys = self._subkeys if encrypt else list(reversed(self._subkeys))

        for i in range(16):
            f_out = self._f_function(R, keys[i])
            new_R = xor_bits(L, f_out)
            L = R
            R = new_R

        # Final permutation (FP = IP^-1), note the swap: R then L
        pre_fp = R + L
        result_bits = permute(pre_fp, FP)
        return bits_to_bytes(result_bits)

    # ------------------------------------------------------------------ #
    #  Padding (PKCS#5 / PKCS#7)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _pad(data: bytes) -> bytes:
        pad_len = 8 - (len(data) % 8)
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 8:
            raise ValueError("Invalid padding.")
        return data[:-pad_len]

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #
    def generate_key(self) -> bytes:
        """Generate a random 64-bit DES key."""
        return os.urandom(8)

    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt plaintext bytes using DES-ECB with PKCS#5 padding."""
        self.generate_subkeys(key)
        padded = self._pad(plaintext)
        ciphertext = b""
        for i in range(0, len(padded), 8):
            ciphertext += self._process_block(padded[i:i+8], encrypt=True)
        return ciphertext

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt ciphertext bytes using DES-ECB."""
        self.generate_subkeys(key)
        plaintext = b""
        for i in range(0, len(ciphertext), 8):
            plaintext += self._process_block(ciphertext[i:i+8], encrypt=False)
        return self._unpad(plaintext)

    # ------------------------------------------------------------------ #
    #  Display helpers
    # ------------------------------------------------------------------ #
    def display_subkeys(self, key: bytes):
        """Print all 16 round subkeys."""
        subkeys = self.generate_subkeys(key)
        print("\n  DES Round Subkeys (K1 – K16):")
        print("  " + "-" * 58)
        print(f"  {'Round':<8} {'Subkey (48-bit hex)':<20} {'Binary (48 bits)'}")
        print("  " + "-" * 58)
        for i, sk in enumerate(subkeys, 1):
            # Convert 48 bits to 6 bytes (padded to 8 hex chars)
            sk_int = bits_to_int(sk)
            sk_hex = f"{sk_int:012X}"
            sk_bin = "".join(str(b) for b in sk[:24]) + " " + "".join(str(b) for b in sk[24:])
            print(f"  K{i:<7} {sk_hex:<20} {sk_bin}")
        print("  " + "-" * 58)


# ============================================================
#  Interactive CLI
# ============================================================

def run():
    des = DES()
    print("\n" + "=" * 60)
    print("       DATA ENCRYPTION STANDARD (DES)")
    print("=" * 60)

    # Auto-generate key
    key = des.generate_key()
    print(f"\n  [Auto-generated Key]: {key.hex().upper()}")

    while True:
        print("\nOptions:")
        print("  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Show all 16 round subkeys")
        print("  4. Generate new key")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            pt_str = input("  Enter plaintext: ").strip()
            pt_bytes = pt_str.encode("utf-8")
            ct = des.encrypt(pt_bytes, key)
            print(f"\n  Plaintext  (hex): {pt_bytes.hex().upper()}")
            print(f"  Ciphertext (hex): {ct.hex().upper()}")
            print(f"  Ciphertext (b64): {__import__('base64').b64encode(ct).decode()}")

        elif choice == "2":
            ct_hex = input("  Enter ciphertext (hex): ").strip().replace(" ", "")
            try:
                ct = bytes.fromhex(ct_hex)
                pt = des.decrypt(ct, key)
                print(f"\n  Ciphertext (hex): {ct.hex().upper()}")
                print(f"  Plaintext       : {pt.decode('utf-8', errors='replace')}")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            des.display_subkeys(key)

        elif choice == "4":
            key = des.generate_key()
            print(f"\n  [New Key Generated]: {key.hex().upper()}")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
