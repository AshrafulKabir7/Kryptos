import sys
import os
import traceback

from classical.substitution_cipher import SubstitutionCipher
from classical.double_transposition import DoubleTransposition
from symmetric.des import DES
from symmetric.aes import AES
from public_key.rsa import RSA
from public_key.ecc import get_p256, get_small_demo_curve

def test_substitution():
    print("Testing Substitution Cipher...")
    sc = SubstitutionCipher()
    plaintext = "HELLOWORLD"
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    
    try:
        ct = sc.encrypt(plaintext, key)
        pt = sc.decrypt(ct, key)
        assert pt == plaintext, f"Expected {plaintext}, got {pt}"
        print("  [SUCCESS] Substitution Cipher works")
        return True
    except Exception as e:
        print(f"  [FAILED] Substitution Cipher: {e}")
        traceback.print_exc()
        return False

def test_double_transposition():
    print("Testing Double Transposition Cipher...")
    dt = DoubleTransposition()
    plaintext = "HELLOWORLD"
    kw1 = "KEYONE"
    kw2 = "KEYTWO"
    
    try:
        ct, k1, k2 = dt.encrypt(plaintext, None, None, keyword1=kw1, keyword2=kw2)
        pt = dt.decrypt(ct, k1, k2, original_len=len(plaintext))
        assert pt == plaintext, f"Expected {plaintext}, got {pt}"
        print("  [SUCCESS] Double Transposition works")
        return True
    except Exception as e:
        print(f"  [FAILED] Double Transposition: {e}")
        traceback.print_exc()
        return False

def test_des():
    print("Testing DES...")
    des = DES()
    plaintext = b"HelloWorld123!"
    key = des.generate_key()
    
    try:
        ct = des.encrypt(plaintext, key)
        pt = des.decrypt(ct, key)
        assert pt == plaintext, f"Expected {plaintext}, got {pt}"
        print("  [SUCCESS] DES works")
        return True
    except Exception as e:
        print(f"  [FAILED] DES: {e}")
        traceback.print_exc()
        return False

def test_aes():
    print("Testing AES...")
    aes = AES()
    plaintext = b"HelloWorld123!"
    key = aes.generate_key()
    
    try:
        ct = aes.encrypt(plaintext, key)
        pt = aes.decrypt(ct, key)
        assert pt == plaintext, f"Expected {plaintext}, got {pt}"
        print("  [SUCCESS] AES works")
        return True
    except Exception as e:
        print(f"  [FAILED] AES: {e}")
        traceback.print_exc()
        return False

def test_rsa():
    print("Testing RSA...")
    rsa = RSA()
    plaintext = "HelloWorld123!"
    
    try:
        pub, priv = rsa.generate_keys(512)
        ct = rsa.encrypt(plaintext)
        pt = rsa.decrypt(ct)
        assert pt == plaintext, f"Expected {plaintext}, got {pt}"
        print("  [SUCCESS] RSA works")
        return True
    except Exception as e:
        print(f"  [FAILED] RSA: {e}")
        traceback.print_exc()
        return False

def test_ecc():
    print("Testing ECC...")
    
    try:
        curve = get_p256()
        da, Qa = curve.generate_key_pair()
        db, Qb = curve.generate_key_pair()
        shared_a = curve.ecdh_shared_key(da, Qb)
        shared_b = curve.ecdh_shared_key(db, Qa)
        assert shared_a == shared_b, "Shared keys do not match!"
        print("  [SUCCESS] ECC works")
        return True
    except Exception as e:
        print(f"  [FAILED] ECC: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    results = {
        "Substitution": test_substitution(),
        "Double Transposition": test_double_transposition(),
        "DES": test_des(),
        "AES": test_aes(),
        "RSA": test_rsa(),
        "ECC": test_ecc(),
    }
    
    print("\n--- Summary ---")
    for k, v in results.items():
        print(f"{k}: {'Pass' if v else 'Fail'}")
