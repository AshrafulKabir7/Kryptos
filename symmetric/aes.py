"""
CSE721: Introduction to Cryptography
Symmetric-Key Cryptography - Advanced Encryption Standard (AES-128)
Implements: Encryption, Decryption, Key Expansion (all 11 round keys)
Fully from scratch — no external crypto libraries.
"""

import os


# ============================================================
#  AES LOOKUP TABLES
# ============================================================

# AES S-box (SubBytes forward)
SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]

# AES Inverse S-box (SubBytes inverse)
INV_SBOX = [
    0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
    0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
    0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
    0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
    0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
    0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
    0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
    0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
    0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
    0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
    0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
    0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
    0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
    0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
    0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
    0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d,
]

# Round constants for key expansion
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]


# ============================================================
#  GF(2^8) arithmetic (for MixColumns)
# ============================================================

def xtime(a: int) -> int:
    """Multiply by 2 in GF(2^8) with irreducible polynomial 0x1b."""
    if a & 0x80:
        return ((a << 1) ^ 0x1b) & 0xFF
    return (a << 1) & 0xFF

def gmul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8)."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result


# ============================================================
#  AES state helpers (4×4 byte matrix, column-major)
# ============================================================

def bytes_to_state(data: bytes) -> list:
    """Convert 16 bytes to 4×4 state matrix (column-major)."""
    state = [[0] * 4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            state[r][c] = data[r + 4 * c]
    return state

def state_to_bytes(state: list) -> bytes:
    """Convert 4×4 state matrix back to 16 bytes (column-major)."""
    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[r + 4 * c] = state[r][c]
    return bytes(out)


# ============================================================
#  AES Operations
# ============================================================

def sub_bytes(state: list) -> list:
    """SubBytes: apply S-box to every byte."""
    return [[SBOX[state[r][c]] for c in range(4)] for r in range(4)]

def inv_sub_bytes(state: list) -> list:
    """Inverse SubBytes: apply inverse S-box."""
    return [[INV_SBOX[state[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(state: list) -> list:
    """ShiftRows: cyclically shift row r left by r positions."""
    new_state = [row[:] for row in state]
    for r in range(1, 4):
        new_state[r] = state[r][r:] + state[r][:r]
    return new_state

def inv_shift_rows(state: list) -> list:
    """Inverse ShiftRows: cyclically shift row r right by r positions."""
    new_state = [row[:] for row in state]
    for r in range(1, 4):
        new_state[r] = state[r][4-r:] + state[r][:4-r]
    return new_state

def mix_columns(state: list) -> list:
    """MixColumns: multiply each column by fixed matrix in GF(2^8)."""
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        new_state[0][c] = gmul(col[0],2) ^ gmul(col[1],3) ^ col[2]          ^ col[3]
        new_state[1][c] = col[0]          ^ gmul(col[1],2) ^ gmul(col[2],3) ^ col[3]
        new_state[2][c] = col[0]          ^ col[1]          ^ gmul(col[2],2) ^ gmul(col[3],3)
        new_state[3][c] = gmul(col[0],3) ^ col[1]          ^ col[2]          ^ gmul(col[3],2)
    return new_state

def inv_mix_columns(state: list) -> list:
    """Inverse MixColumns."""
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        new_state[0][c] = gmul(col[0],0x0e)^gmul(col[1],0x0b)^gmul(col[2],0x0d)^gmul(col[3],0x09)
        new_state[1][c] = gmul(col[0],0x09)^gmul(col[1],0x0e)^gmul(col[2],0x0b)^gmul(col[3],0x0d)
        new_state[2][c] = gmul(col[0],0x0d)^gmul(col[1],0x09)^gmul(col[2],0x0e)^gmul(col[3],0x0b)
        new_state[3][c] = gmul(col[0],0x0b)^gmul(col[1],0x0d)^gmul(col[2],0x09)^gmul(col[3],0x0e)
    return new_state

def add_round_key(state: list, round_key: list) -> list:
    """AddRoundKey: XOR state with round key (both 4×4)."""
    return [[state[r][c] ^ round_key[r][c] for c in range(4)] for r in range(4)]


# ============================================================
#  AES Key Expansion
# ============================================================

def key_expansion(key: bytes) -> list:
    """
    Expand 16-byte AES-128 key into 11 round keys (44 words of 4 bytes each).
    Returns list of 11 round keys, each a 4×4 byte matrix.
    """
    assert len(key) == 16, "AES-128 requires a 16-byte key."
    # Work in terms of 4-byte words
    W = []
    for i in range(4):
        W.append(list(key[4*i:4*i+4]))

    for i in range(4, 44):
        temp = W[i-1][:]
        if i % 4 == 0:
            # RotWord: left rotate 1 byte
            temp = temp[1:] + temp[:1]
            # SubWord: apply S-box
            temp = [SBOX[b] for b in temp]
            # XOR with Rcon
            temp[0] ^= RCON[i // 4 - 1]
        W.append([W[i-4][j] ^ temp[j] for j in range(4)])

    # Convert words to 4×4 state matrices (one per round: 11 total)
    round_keys = []
    for rk in range(11):
        rk_bytes = []
        for w in range(4):
            rk_bytes.extend(W[rk * 4 + w])
        round_keys.append(bytes_to_state(bytes(rk_bytes)))
    return round_keys


# ============================================================
#  AES Main Class
# ============================================================

class AES:
    """
    AES-128 implementation from scratch.
    Block size: 128 bits (16 bytes).
    Key size:   128 bits (16 bytes).
    Rounds:     10
    """

    def __init__(self):
        self._round_keys = []

    def generate_key(self) -> bytes:
        """Generate a random 128-bit AES key."""
        return os.urandom(16)

    # ------------------------------------------------------------------ #
    #  Block-level encrypt / decrypt
    # ------------------------------------------------------------------ #
    def _encrypt_block(self, block: bytes, round_keys: list) -> bytes:
        """Encrypt one 16-byte block."""
        state = bytes_to_state(block)
        # Initial round key addition
        state = add_round_key(state, round_keys[0])

        for rnd in range(1, 10):
            state = sub_bytes(state)
            state = shift_rows(state)
            state = mix_columns(state)
            state = add_round_key(state, round_keys[rnd])

        # Final round (no MixColumns)
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, round_keys[10])

        return state_to_bytes(state)

    def _decrypt_block(self, block: bytes, round_keys: list) -> bytes:
        """Decrypt one 16-byte block."""
        state = bytes_to_state(block)
        state = add_round_key(state, round_keys[10])

        for rnd in range(9, 0, -1):
            state = inv_shift_rows(state)
            state = inv_sub_bytes(state)
            state = add_round_key(state, round_keys[rnd])
            state = inv_mix_columns(state)

        # Final round
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[0])

        return state_to_bytes(state)

    # ------------------------------------------------------------------ #
    #  Padding (PKCS#7)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _pad(data: bytes) -> bytes:
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16:
            raise ValueError("Invalid AES padding.")
        return data[:-pad_len]

    # ------------------------------------------------------------------ #
    #  Public API (ECB mode for simplicity)
    # ------------------------------------------------------------------ #
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt plaintext bytes using AES-128-ECB with PKCS#7 padding."""
        round_keys = key_expansion(key)
        self._round_keys = round_keys
        padded = self._pad(plaintext)
        ct = b""
        for i in range(0, len(padded), 16):
            ct += self._encrypt_block(padded[i:i+16], round_keys)
        return ct

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt ciphertext bytes using AES-128-ECB."""
        round_keys = key_expansion(key)
        self._round_keys = round_keys
        pt = b""
        for i in range(0, len(ciphertext), 16):
            pt += self._decrypt_block(ciphertext[i:i+16], round_keys)
        return self._unpad(pt)

    # ------------------------------------------------------------------ #
    #  Display helpers
    # ------------------------------------------------------------------ #
    def display_round_keys(self, key: bytes):
        """Print all 11 round keys (round 0 = initial, rounds 1-10 = Feistel rounds)."""
        round_keys = key_expansion(key)
        self._round_keys = round_keys
        print("\n  AES-128 Round Keys (K0 – K10):")
        print("  " + "-" * 62)
        print(f"  {'Round':<8} {'Round Key (hex, 128 bits)'}")
        print("  " + "-" * 62)
        for i, rk in enumerate(round_keys):
            rk_bytes = state_to_bytes(rk)
            rk_hex = rk_bytes.hex().upper()
            # Format as 4 groups of 4 bytes
            fmt = " ".join(rk_hex[j:j+8] for j in range(0, 32, 8))
            label = "K0 (initial)" if i == 0 else f"K{i}"
            print(f"  {label:<12} {fmt}")
        print("  " + "-" * 62)


# ============================================================
#  Interactive CLI
# ============================================================

def run():
    aes = AES()
    print("\n" + "=" * 60)
    print("       ADVANCED ENCRYPTION STANDARD (AES-128)")
    print("=" * 60)

    # Auto-generate key
    key = aes.generate_key()
    print(f"\n  [Auto-generated Key]: {key.hex().upper()}")

    while True:
        print("\nOptions:")
        print("  1. Encrypt")
        print("  2. Decrypt")
        print("  3. Show all 11 round keys")
        print("  4. Generate new key")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            pt_str = input("  Enter plaintext: ").strip()
            pt_bytes = pt_str.encode("utf-8")
            ct = aes.encrypt(pt_bytes, key)
            print(f"\n  Plaintext  (hex): {pt_bytes.hex().upper()}")
            print(f"  Ciphertext (hex): {ct.hex().upper()}")
            print(f"  Ciphertext (b64): {__import__('base64').b64encode(ct).decode()}")

        elif choice == "2":
            ct_hex = input("  Enter ciphertext (hex): ").strip().replace(" ", "")
            try:
                ct = bytes.fromhex(ct_hex)
                pt = aes.decrypt(ct, key)
                print(f"\n  Ciphertext (hex): {ct.hex().upper()}")
                print(f"  Plaintext       : {pt.decode('utf-8', errors='replace')}")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            aes.display_round_keys(key)

        elif choice == "4":
            key = aes.generate_key()
            print(f"\n  [New Key Generated]: {key.hex().upper()}")

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
