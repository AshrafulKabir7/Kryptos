import fastapi
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import base64

# Import algorithms
from classical.substitution_cipher import SubstitutionCipher
from classical.double_transposition import DoubleTransposition
from symmetric.des import DES, bits_to_int
from symmetric.aes import AES, state_to_bytes
from public_key.rsa import RSA
from public_key.ecc import get_small_demo_curve, get_secp256k1, get_p256, EllipticCurve

app = FastAPI(title="CSE721 Crypto API")

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

# ======== GLOBAL STATE (for convenience) ========
rsa_instance = RSA()

# Simple in-memory user database
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
    sc = SubstitutionCipher()
    try:
        ct = sc.encrypt(req.text, req.key)
        freq = sc.frequency_analysis(ct)
        return {"ciphertext": ct, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/substitution/decrypt")
def sub_decrypt(req: SubstitutionRequest):
    sc = SubstitutionCipher()
    try:
        pt = sc.decrypt(req.text, req.key)
        freq = sc.frequency_analysis(req.text)
        return {"plaintext": pt, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/transposition/encrypt")
def trans_encrypt(req: TranspositionRequest):
    dt = DoubleTransposition()
    try:
        # Use string keywords
        ct, k1, k2 = dt.encrypt(req.text, None, None, keyword1=req.key1, keyword2=req.key2)
        freq = dt.frequency_analysis(ct)
        return {"ciphertext": ct, "key1_perm": k1, "key2_perm": k2, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/classical/transposition/decrypt")
def trans_decrypt(req: TranspositionRequest):
    dt = DoubleTransposition()
    try:
        k1 = dt.keyword_to_permutation(req.key1)
        k2 = dt.keyword_to_permutation(req.key2)
        # Without exact length, it strips trailing Xs
        pt = dt.decrypt(req.text, k1, k2)
        freq = dt.frequency_analysis(req.text)
        return {"plaintext": pt, "frequency": freq}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== SYMMETRIC ========
@app.post("/api/symmetric/des/encrypt")
def des_encrypt(req: SymmetricRequest):
    des = DES()
    key_bytes = des.generate_key()
    try:
        ct = des.encrypt(req.text.encode('utf-8'), key_bytes)
        
        # gather subkeys
        subkeys = des._subkeys
        subkeys_hex = []
        for sk in subkeys:
            subkeys_hex.append(f"{bits_to_int(sk):012X}")
            
        return {
            "ciphertext_hex": ct.hex().upper(),
            "key_hex": key_bytes.hex().upper(),
            "round_keys": subkeys_hex
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/des/decrypt")
def des_decrypt(req: SymmetricDecryptRequest):
    des = DES()
    try:
        key_bytes = bytes.fromhex(req.key_hex)
        ct_bytes = bytes.fromhex(req.ciphertext_hex)
        pt = des.decrypt(ct_bytes, key_bytes)
        return {"plaintext": pt.decode('utf-8', errors='replace')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/aes/encrypt")
def aes_encrypt(req: SymmetricRequest):
    aes = AES()
    key_bytes = aes.generate_key()
    try:
        ct = aes.encrypt(req.text.encode('utf-8'), key_bytes)
        # gather round keys
        round_keys = aes._round_keys
        rkeys_hex = []
        for rk in round_keys:
            rk_bytes = state_to_bytes(rk)
            rkeys_hex.append(rk_bytes.hex().upper())
            
        return {
            "ciphertext_hex": ct.hex().upper(),
            "key_hex": key_bytes.hex().upper(),
            "round_keys": rkeys_hex
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/symmetric/aes/decrypt")
def aes_decrypt(req: SymmetricDecryptRequest):
    aes = AES()
    try:
        key_bytes = bytes.fromhex(req.key_hex)
        ct_bytes = bytes.fromhex(req.ciphertext_hex)
        pt = aes.decrypt(ct_bytes, key_bytes)
        return {"plaintext": pt.decode('utf-8', errors='replace')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== PUBLIC KEY ========
@app.post("/api/public/rsa/generate")
def rsa_generate(req: RSAGenRequest):
    try:
        pub, priv = rsa_instance.generate_keys(req.bits)
        # Return as strings to avoid JS Number precision loss
        return {
            "public_key": {"n": str(pub["n"]), "e": str(pub["e"])},
            "private_key": {"n": str(priv["n"]), "d": str(priv["d"])}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/rsa/encrypt")
def rsa_encrypt(req: RSAEncryptRequest):
    try:
        ct = rsa_instance.encrypt(req.text, int(req.n), int(req.e))
        return {"ciphertext": str(ct)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/public/rsa/decrypt")
def rsa_decrypt(req: RSADecryptRequest):
    try:
        pt = rsa_instance.decrypt(int(req.ciphertext), int(req.n), int(req.d))
        return {"plaintext": pt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======== ECC ========
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
        from public_key.ecc import ECPoint
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
    uvicorn.run("api:app", host="12 multi", port=8000, reload=True)
