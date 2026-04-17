# 🛡️ Kryptos
**An Interactive, High-Fidelity Educational Cryptography Dashboard**

![Kryptos Banner](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge) ![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge) ![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB?style=for-the-badge) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)

Kryptos is a comprehensive, modern web application designed for interactive learning and visualization of cryptographic algorithms. Built with a sleek, cyber-green "Web3" aesthetic, it allows users to experience the mathematics and architecture of historical ciphers, symmetric key block ciphers, and modern asymmetric key cryptography.

Created for **CSE721**.

---

## ✨ Features

### 🏛️ Classical Cryptography
*   **Substitution Cipher:** Interactive frequency analysis and key mappings.
*   **Double Transposition:** Matrix-based permutation visualization.

### 🔐 Symmetric Cryptography
*   **DES (Data Encryption Standard):** Sub-key generation tracking and bitwise operations.
*   **AES (Advanced Encryption Standard):** State transformations and round-key scheduling visualization.

### 🔑 Public Key Cryptography
*   **RSA:** Key pair generation (p, q, n, e, d), encryption, and decryption flow.
*   **Elliptic Curve Cryptography (ECC):** 
    *   Supports `demo` curves, `secp256k1` (Bitcoin curve), and `P-256`.
    *   Demonstrates Elliptic Curve Diffie-Hellman (ECDH) shared secret generation.

---

## 🛠️ Technology Stack

**Frontend:**
*   React 19 + TypeScript
*   Vite for ultra-fast bundling
*   Tailwind CSS + Framer Motion (for fluid micro-animations)
*   Shadcn UI & Radix Primitives for accessible components

**Backend:**
*   Python 3.10+
*   FastAPI (Asynchronous, highly performant API)
*   Uvicorn (ASGI web server)

---

## 🚀 Quick Start / Local Development

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)

### 1. Backend Setup
Navigate to the root directory and install Python dependencies:
```bash
pip install -r requirements_web.txt
```

Start the FastAPI server:
```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```
*The API documentation will be available at `http://127.0.0.1:8000/docs`.*

### 2. Frontend Setup
Open a new terminal window, navigate to the frontend folder:
```bash
cd frontend
npm install
```

Start the Vite development server:
```bash
npm run dev
```

---

## 🌩️ Deployment Details

Kryptos is configured with a decoupled deployment pipeline:
1.  **Frontend:** Deployable on Vercel or Netlify via the `frontend/` directory.
2.  **Backend:** Pre-configured `render.yaml` provided for easy deployment on Render as a Python Web Service. Set the frontend environment variable `VITE_API_URL` to point to the deployed backend URL.

---
*Created with focus on visual excellence and educational clarity.*
