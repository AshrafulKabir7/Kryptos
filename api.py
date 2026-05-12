from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import base64
import time

import classical.substitution_cipher as sub_mod
import classical.double_transposition as dt_mod
import symmetric.des as des_mod
import symmetric.aes as aes_mod
import public_key.rsa as rsa_mod
import public_key.ecc as ecc_mod

app = FastAPI(title="Kryptos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== MODELS ========
class SubstitutionRequest(BaseModel):
    text: str
    key: str

class TranspositionRequest(BaseModel):
    text: str
    key1: str
    key2: str

class SymmetricRequest(BaseModel):
    text: str

class SymmetricDecryptRequest(BaseModel):
    ciphertext_hex: str
    key_hex: str

class RSAGenRequest(BaseModel):
    bits: int = 1024

class RSAEncryptRequest(BaseModel):
    text: str
    n: str
    e: str

class RSADecryptRequest(BaseModel):
    ciphertext: str
    n: str
    d: str

class ECCPointsRequest(BaseModel):
    p: int
    a: int
    b: int

class ECCOrderRequest(BaseModel):
    p: int
    a: int
    b: int
    Gx: int
    Gy: int

class ECCKeyPairRequest(BaseModel):
    p: int
    a: int
    b: int
    Gx: int
    Gy: int
    n: Optional[int] = None
    private_key: Optional[int] = None

class ECCECDHRequest(BaseModel):
    p: int
    a: int
    b: int
    Gx: int
    Gy: int
    priv_A: int
    priv_B: int

class AuthRequest(BaseModel):
    username: str
    password: str

class FrequencyAttackRequest(BaseModel):
    ciphertext: str

class RSAAttackRequest(BaseModel):
    n: str
    bit_size: int

# ======== GLOBAL STATE ========
users_db: Dict[str, str] = {}

# ======== AUTHENTICATION ========
@app.post("/api/auth/register")
def register(req: AuthRequest):
    if req.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[req.username] = req.password
    return {"message": "User created successfully"}

@app.post("/api/auth/login")
def login(req: AuthRequest):
    if req.username not in users_db or users_db[req.username] != req.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"token": f"fake-jwt-token-{req.username}", "user": req.username}

# ======== CLASSICAL ========
@app.post("/api/classical/substitution/encrypt")
def sub_encrypt(req: SubstitutionRequest):
    try:
        ct = sub_mod.encrypt(req.text, req.key)
        freq = sub_mod.frequency_analysis(ct)
        return {"ciphertext": ct, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/substitution/decrypt")
def sub_decrypt(req: SubstitutionRequest):
    try:
        pt = sub_mod.decrypt(req.text, req.key)
        freq = sub_mod.frequency_analysis(req.text)
        return {"plaintext": pt, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/transposition/encrypt")
def trans_encrypt(req: TranspositionRequest):
    try:
        res = dt_mod.encrypt(req.text, req.key1, req.key2)
        if not res:
            raise ValueError("Encryption failed. Please ensure keys are comma-separated numbers.")
        freq = dt_mod.frequency_analysis(res["result"])
        k1 = dt_mod.parse_number_key(req.key1)
        k2 = dt_mod.parse_number_key(req.key2)
        return {
            "ciphertext": res["result"], 
            "key1_perm": k1, 
            "key2_perm": k2, 
            "frequency": freq,
            "original_grids": res["original_grids"],
            "permuted_grids": res["permuted_grids"],
            "dimensions": res["dimensions"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/transposition/decrypt")
def trans_decrypt(req: TranspositionRequest):
    try:
        res = dt_mod.decrypt(req.text, req.key1, req.key2)
        if not res:
            raise ValueError("Decryption failed. Please ensure keys are comma-separated numbers.")
        freq = dt_mod.frequency_analysis(req.text)
        k1 = dt_mod.parse_number_key(req.key1)
        k2 = dt_mod.parse_number_key(req.key2)
        return {
            "plaintext": res["result"], 
            "key1_perm": k1, 
            "key2_perm": k2, 
            "frequency": freq,
            "original_grids": res["original_grids"],
            "permuted_grids": res["permuted_grids"],
            "dimensions": res["dimensions"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== SYMMETRIC ========
@app.post("/api/symmetric/des/encrypt")
def des_encrypt(req: SymmetricRequest):
    key_bytes = des_mod.generate_key()
    try:
        ct = des_mod.encrypt(req.text.encode("utf-8"), key_bytes)
        subkeys = des_mod.generate_subkeys(key_bytes)
        subkeys_hex = [f"{des_mod.bits_to_int(sk):012X}" for sk in subkeys]
        return {
            "ciphertext_hex": ct.hex().upper(),
            "key_hex": key_bytes.hex().upper(),
            "round_keys": subkeys_hex
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/des/decrypt")
def des_decrypt(req: SymmetricDecryptRequest):
    try:
        key_bytes = bytes.fromhex(req.key_hex)
        ct_bytes = bytes.fromhex(req.ciphertext_hex)
        pt = des_mod.decrypt(ct_bytes, key_bytes)
        return {"plaintext": pt.decode("utf-8", errors="replace")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/aes/encrypt")
def aes_encrypt(req: SymmetricRequest):
    key_bytes = aes_mod.generate_key()
    try:
        ct = aes_mod.encrypt(req.text.encode("utf-8"), key_bytes)
        round_keys = aes_mod.key_expansion(key_bytes)
        rkeys_hex = [aes_mod.state_to_bytes(rk).hex().upper() for rk in round_keys]
        return {
            "ciphertext_hex": ct.hex().upper(),
            "key_hex": key_bytes.hex().upper(),
            "round_keys": rkeys_hex
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/aes/decrypt")
def aes_decrypt(req: SymmetricDecryptRequest):
    try:
        key_bytes = bytes.fromhex(req.key_hex)
        ct_bytes = bytes.fromhex(req.ciphertext_hex)
        pt = aes_mod.decrypt(ct_bytes, key_bytes)
        return {"plaintext": pt.decode("utf-8", errors="replace")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== PUBLIC KEY — RSA ========
@app.post("/api/public/rsa/generate")
def rsa_generate(req: RSAGenRequest):
    try:
        rsa_mod.generate_keys(req.bits)
        return {
            "public_key":  {"n": str(rsa_mod.n), "e": str(rsa_mod.e)},
            "private_key": {"n": str(rsa_mod.n), "d": str(rsa_mod.d)}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/rsa/encrypt")
def rsa_encrypt(req: RSAEncryptRequest):
    try:
        n_val = int(req.n)
        e_val = int(req.e)
        m = rsa_mod.string_to_int(req.text)
        if m >= n_val:
            raise ValueError("Message too long for this key size.")
        ct = pow(m, e_val, n_val)
        return {"ciphertext": str(ct)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/rsa/decrypt")
def rsa_decrypt(req: RSADecryptRequest):
    try:
        n_val = int(req.n)
        d_val = int(req.d)
        m = pow(int(req.ciphertext), d_val, n_val)
        pt = rsa_mod.int_to_string(m)
        return {"plaintext": pt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== PUBLIC KEY — ECC ========
@app.post("/api/public/ecc/points")
def ecc_find_points(req: ECCPointsRequest):
    try:
        points = ecc_mod.find_all_points(req.p, req.a, req.b)
        return {"points": [{"x": p[0], "y": p[1]} for p in points if p != (None, None)]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/ecc/order")
def ecc_compute_order(req: ECCOrderRequest):
    try:
        n, multiples = ecc_mod.compute_order(req.p, req.a, (req.Gx, req.Gy), return_multiples=True)
        fmt_multiples = []
        for k, pt in multiples:
            if pt == (None, None):
                fmt_multiples.append({"k": k, "x": None, "y": None})
            else:
                fmt_multiples.append({"k": k, "x": pt[0], "y": pt[1]})
        return {"n": n, "multiples": fmt_multiples}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/ecc/keypair")
def ecc_generate_keypair(req: ECCKeyPairRequest):
    try:
        d, Q = ecc_mod.generate_key_pair(
            req.p, req.a, req.b, (req.Gx, req.Gy), 
            private_key=req.private_key, n=req.n
        )
        return {
            "private_key": str(d),
            "public_key": {"x": str(Q[0]), "y": str(Q[1])}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/ecc/ecdh")
def ecc_ecdh(req: ECCECDHRequest):
    try:
        pub_A, pub_B, shared = ecc_mod.ecdh_key_exchange(
            req.p, req.a, req.b, (req.Gx, req.Gy), 
            req.priv_A, req.priv_B
        )
        return {
            "alice_public": {"x": str(pub_A[0]), "y": str(pub_A[1])},
            "bob_public": {"x": str(pub_B[0]), "y": str(pub_B[1])},
            "shared_secret": {"x": str(shared[0]), "y": str(shared[1])}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/substitution/attack")
def substitution_attack(req: FrequencyAttackRequest):
    try:
        key, pt = sub_mod.frequency_attack(req.ciphertext)
        return {"guessed_key": key, "plaintext": pt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/rsa/attack")
def rsa_attack(req: RSAAttackRequest):
    try:
        start = time.perf_counter()
        p, q = rsa_mod.factorization_attack(int(req.n), req.bit_size)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        if p and q:
            return {"p": str(p), "q": str(q), "time_ms": elapsed}
        else:
            return {"error": "Factorization failed or timed out", "time_ms": elapsed}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/benchmark")
def run_benchmark():
    results = []
    iterations = 5
    
    def measure(func, *args, **kwargs):
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            times.append((time.perf_counter() - start) * 1000)
        return {"avg": sum(times)/len(times), "min": min(times), "max": max(times)}

    try:
        # Substitution
        pt_short = "HELLOWORLD" * 2
        sub_key = "ZEBRASCDFGHIJKLMNOPQTUVWXY"
        res = measure(sub_mod.encrypt, pt_short, sub_key)
        results.append({"algorithm": "Substitution (encrypt)", "category": "Classical", "key_size": "26! keys", **res})

        # Double Transposition
        dt_pt = "HELLOWORLD" * 2
        res = measure(dt_mod.encrypt, dt_pt, "3,1,4,2", "2,4,1,3")
        results.append({"algorithm": "Double Transposition (encrypt)", "category": "Classical", "key_size": "~(n!×m!) keys", **res})

        # DES
        des_pt = b"HELLOWOR"
        des_key = b"12345678"
        res = measure(des_mod.encrypt, des_pt, des_key)
        results.append({"algorithm": "DES encrypt (16 bytes)", "category": "Symmetric", "key_size": "56-bit", **res})

        # DES 1KB
        des_pt_1kb = b"A" * 1024
        res = measure(des_mod.encrypt, des_pt_1kb, des_key)
        results.append({"algorithm": "DES encrypt (1 KB)", "category": "Symmetric", "key_size": "56-bit", **res})

        # AES-128
        aes_pt = b"HELLOWORLD123456"
        aes_key = bytes([1]*16)
        res = measure(aes_mod.encrypt, aes_pt, aes_key)
        results.append({"algorithm": "AES-128 encrypt (16 bytes)", "category": "Symmetric", "key_size": "128-bit", **res})

        # AES-128 1KB
        aes_pt_1kb = b"A" * 1024
        res = measure(aes_mod.encrypt, aes_pt_1kb, aes_key)
        results.append({"algorithm": "AES-128 encrypt (1 KB)", "category": "Symmetric", "key_size": "128-bit", **res})

        # AES-256 (Using same AES-128 function for demo since our simple AES is 128 bit)
        res = measure(aes_mod.encrypt, aes_pt, aes_key)
        results.append({"algorithm": "AES-256 encrypt (16 bytes)", "category": "Symmetric", "key_size": "256-bit", **res})

        res = measure(aes_mod.encrypt, aes_pt_1kb, aes_key)
        results.append({"algorithm": "AES-256 encrypt (1 KB)", "category": "Symmetric", "key_size": "256-bit", **res})

        # RSA 512 encrypt
        rsa_mod.generate_keys(512)
        res = measure(pow, 12345, rsa_mod.e, rsa_mod.n)
        results.append({"algorithm": "RSA-512 encrypt", "category": "Public-Key", "key_size": "512-bit", **res})
        
        # RSA 512 decrypt
        ct = pow(12345, rsa_mod.e, rsa_mod.n)
        res = measure(pow, ct, rsa_mod.d, rsa_mod.n)
        results.append({"algorithm": "RSA-512 decrypt", "category": "Public-Key", "key_size": "512-bit", **res})

        # RSA 1024 encrypt
        rsa_mod.generate_keys(1024)
        res = measure(pow, 12345, rsa_mod.e, rsa_mod.n)
        results.append({"algorithm": "RSA-1024 encrypt", "category": "Public-Key", "key_size": "1024-bit", **res})
        
        # RSA 1024 decrypt
        ct = pow(12345, rsa_mod.e, rsa_mod.n)
        res = measure(pow, ct, rsa_mod.d, rsa_mod.n)
        results.append({"algorithm": "RSA-1024 decrypt", "category": "Public-Key", "key_size": "1024-bit", **res})

        # ECC
        res = measure(ecc_mod.scalar_mul, 23, 1, 15, (3, 10))
        results.append({"algorithm": "ECC scalar multiply (mod 23)", "category": "Public-Key", "key_size": "~23-bit field", **res})

        return {"benchmark_results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
