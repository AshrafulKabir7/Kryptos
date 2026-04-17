#!/usr/bin/env python3
"""
CSE721: Introduction to Cryptography
Project: Implementation and Security Analysis of Classical and Modern Cryptographic Algorithms

Main entry point — interactive CLI menu.

Author: CSE721 Student
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classical.substitution_cipher import run as run_substitution
from classical.double_transposition import run as run_double_transposition
from symmetric.des import run as run_des
from symmetric.aes import run as run_aes
from public_key.rsa import run as run_rsa
from public_key.ecc import run as run_ecc


BANNER = r"""
╔══════════════════════════════════════════════════════════════════════╗
║         CSE721: Introduction to Cryptography                        ║
║  Implementation and Security Analysis of Cryptographic Algorithms   ║
╚══════════════════════════════════════════════════════════════════════╝
"""

ALGORITHMS = {
    "1": {
        "label": "Classical Cryptography",
        "sub": {
            "1": ("Substitution Cipher  (Encrypt / Decrypt / Frequency Analysis / Brute Force)", run_substitution),
            "2": ("Double Transposition (Encrypt / Decrypt / Frequency Analysis)",               run_double_transposition),
        },
    },
    "2": {
        "label": "Symmetric-Key Cryptography",
        "sub": {
            "1": ("DES – Data Encryption Standard       (Encrypt / Decrypt / Round Keys)", run_des),
            "2": ("AES – Advanced Encryption Standard   (Encrypt / Decrypt / Round Keys)", run_aes),
        },
    },
    "3": {
        "label": "Public-Key Cryptography",
        "sub": {
            "1": ("RSA  (Key Gen / Encrypt / Decrypt / Factorization Attack)", run_rsa),
            "2": ("ECC  (Key Gen / ECDH / All Multiples of G)",                run_ecc),
        },
    },
}


def print_banner():
    print(BANNER)


def main_menu():
    while True:
        print_banner()
        print("  MAIN MENU")
        print("  " + "─" * 55)
        for key, cat in ALGORITHMS.items():
            print(f"  {key}. {cat['label']}")
        print("  0. Exit")
        print("  " + "─" * 55)
        choice = input("\n  Select category: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        elif choice in ALGORITHMS:
            cat = ALGORITHMS[choice]
            print(f"\n  {cat['label']}")
            print("  " + "─" * 55)
            for k, (desc, _) in cat["sub"].items():
                print(f"  {k}. {desc}")
            print("  0. Back")
            sub = input("\n  Select algorithm: ").strip()

            if sub == "0":
                continue
            elif sub in cat["sub"]:
                _, runner = cat["sub"][sub]
                try:
                    runner()
                except KeyboardInterrupt:
                    print("\n\n  [Interrupted — returning to main menu]")
                except Exception as exc:
                    print(f"\n  [Unexpected error: {exc}]")
                    import traceback
                    traceback.print_exc()
            else:
                print("  Invalid option.")
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main_menu()
