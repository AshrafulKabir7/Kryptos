from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import base64

import classical.substitution_cipher as sub_mod
import classical.double_transposition as dt_mod
import symmetric.des as des_mod
import symmetric.aes as aes_mod
import public_key.rsa as rsa_mod
from public_key.ecc import get_small_demo_curve, get_secp256k1, get_p256, ECPoint

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

class ECCGenRequest(BaseModel):
    curve_name: str = "P-256"

class ECCECDHRequest(BaseModel):
    curve_name: str
    private_key: int
    other_public_x: int
    other_public_y: int

class AuthRequest(BaseModel):
    username: str
    password: str

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
        ct = dt_mod.encrypt(req.text, req.key1, req.key2)
        freq = dt_mod.frequency_analysis(ct)
        k1 = dt_mod.keyword_to_order(req.key1)
        k2 = dt_mod.keyword_to_order(req.key2)
        return {"ciphertext": ct, "key1_perm": k1, "key2_perm": k2, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/transposition/decrypt")
def trans_decrypt(req: TranspositionRequest):
    try:
        pt = dt_mod.decrypt(req.text, req.key1, req.key2)
        freq = dt_mod.frequency_analysis(req.text)
        return {"plaintext": pt, "frequency": freq}
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
def get_curve(name: str):
    if name == "Demo":
        return get_small_demo_curve()
    elif name == "secp256k1":
        return get_secp256k1()
    else:
        return get_p256()

@app.post("/api/public/ecc/generate")
def ecc_generate(req: ECCGenRequest):
    try:
        curve = get_curve(req.curve_name)
        d, Q = curve.generate_key_pair()
        return {
            "domain": {"p": str(curve.p), "a": str(curve.a), "b": str(curve.b), "G": str(curve.G), "n": str(curve.n)},
            "private_key": str(d),
            "public_key": {"x": str(Q.x), "y": str(Q.y)}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/ecc/ecdh")
def ecc_ecdh(req: ECCECDHRequest):
    try:
        curve = get_curve(req.curve_name)
        other_Q = ECPoint(req.other_public_x, req.other_public_y)
        shared = curve.ecdh_shared_key(req.private_key, other_Q)
        return {
            "shared_key_x": str(shared.x),
            "shared_key_y": str(shared.y)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
