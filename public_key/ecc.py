"""
CSE721: Introduction to Cryptography
Public-Key Cryptography - Elliptic Curve Cryptography (ECC)
Implements:
  - ECC over prime field Fp: y² ≡ x³ + ax + b (mod p)
  - All multiples of base point (list of all nP)
  - Key generation (private/public key)
  - Elliptic Curve Diffie-Hellman (ECDH) key exchange
No external crypto libraries used.
"""

import os
import random


# ============================================================
#  Elliptic Curve Point
# ============================================================

class ECPoint:
    """
    Represents a point (x, y) on an elliptic curve,
    or the point at infinity (identity element).
    """
    def __init__(self, x, y, infinity: bool = False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def is_infinity(self) -> bool:
        return self.infinity

    def __eq__(self, other) -> bool:
        if not isinstance(other, ECPoint):
            return False
        if self.infinity and other.infinity:
            return True
        if self.infinity or other.infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        if self.infinity:
            return "O (point at infinity)"
        return f"({self.x}, {self.y})"

    def __hash__(self):
        if self.infinity:
            return hash(None)
        return hash((self.x, self.y))


# ============================================================
#  Elliptic Curve Arithmetic over Fp
# ============================================================

class EllipticCurve:
    """
    Elliptic curve: y² ≡ x³ + ax + b (mod p)
    Domain parameters: p (prime), a, b, G (base point), n (order of G)
    """

    def __init__(self, p: int, a: int, b: int, G: ECPoint, n: int, name: str = "Custom"):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n
        self.name = name
        self._validate()

    def _validate(self):
        """Check non-singular condition: 4a³ + 27b² ≠ 0 mod p."""
        disc = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if disc == 0:
            raise ValueError("Singular curve! Choose different a, b parameters.")

    def is_on_curve(self, P: ECPoint) -> bool:
        """Check if point P lies on the curve."""
        if P.is_infinity():
            return True
        lhs = pow(P.y, 2, self.p)
        rhs = (pow(P.x, 3, self.p) + self.a * P.x + self.b) % self.p
        return lhs == rhs

    def mod_inv(self, k: int) -> int:
        """Modular inverse using Fermat's little theorem (p is prime)."""
        if k % self.p == 0:
            raise ValueError("Modular inverse of zero.")
        return pow(k, self.p - 2, self.p)

    # ------------------------------------------------------------------ #
    #  Point addition and doubling
    # ------------------------------------------------------------------ #
    def point_add(self, P: ECPoint, Q: ECPoint) -> ECPoint:
        """Add two points on the elliptic curve."""
        # Identity cases
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P
        # Point negation P + (-P) = O
        if P.x == Q.x:
            if P.y != Q.y or P.y == 0:
                return ECPoint(None, None, infinity=True)
            # P == Q: point doubling
            return self.point_double(P)

        # General case: P ≠ Q
        lam = (Q.y - P.y) * self.mod_inv(Q.x - P.x) % self.p
        x3 = (lam * lam - P.x - Q.x) % self.p
        y3 = (lam * (P.x - x3) - P.y) % self.p
        return ECPoint(x3, y3)

    def point_double(self, P: ECPoint) -> ECPoint:
        """Double a point on the elliptic curve: 2P."""
        if P.is_infinity():
            return P
        if P.y == 0:
            return ECPoint(None, None, infinity=True)

        lam = (3 * P.x * P.x + self.a) * self.mod_inv(2 * P.y) % self.p
        x3  = (lam * lam - 2 * P.x) % self.p
        y3  = (lam * (P.x - x3) - P.y) % self.p
        return ECPoint(x3, y3)

    def scalar_multiply(self, k: int, P: ECPoint) -> ECPoint:
        """
        Scalar multiplication: compute k*P using double-and-add.
        Efficient O(log k) method.
        """
        k = k % self.n
        result = ECPoint(None, None, infinity=True)  # Start with identity
        addend = ECPoint(P.x, P.y)                   # Copy of P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        return result

    # ------------------------------------------------------------------ #
    #  List all multiples of G
    # ------------------------------------------------------------------ #
    def list_all_multiples(self, max_points: int = 50) -> list:
        """
        Compute all multiples nG for n = 1, 2, ..., min(order, max_points).
        Returns list of (n, ECPoint).
        """
        multiples = []
        current = ECPoint(self.G.x, self.G.y)
        for k in range(1, min(self.n + 1, max_points + 1)):
            multiples.append((k, current))
            if current.is_infinity():
                break
            if k < self.n:
                current = self.point_add(current, self.G)
            else:
                current = ECPoint(None, None, infinity=True)
        return multiples

    # ------------------------------------------------------------------ #
    #  Key generation
    # ------------------------------------------------------------------ #
    def generate_key_pair(self) -> tuple:
        """
        Generate ECC key pair.
        Private key: random integer d in [1, n-1]
        Public key:  Q = d * G
        Returns (d, Q).
        """
        d = random.randint(1, self.n - 1)
        Q = self.scalar_multiply(d, self.G)
        return d, Q

    # ------------------------------------------------------------------ #
    #  ECDH Key Exchange
    # ------------------------------------------------------------------ #
    def ecdh_shared_key(self, private_key: int, other_public_key: ECPoint) -> ECPoint:
        """
        Compute ECDH shared secret: shared = private_key * other_public_key.
        Both parties compute the same shared point.
        """
        return self.scalar_multiply(private_key, other_public_key)

    def display_curve_info(self):
        """Print curve domain parameters."""
        print(f"\n  Elliptic Curve: {self.name}")
        print("  " + "-" * 55)
        print(f"  Equation  : y² ≡ x³ + {self.a}x + {self.b}  (mod {self.p})")
        print(f"  Field     : GF({self.p})")
        print(f"  a         : {self.a}")
        print(f"  b         : {self.b}")
        print(f"  Base point: G = {self.G}")
        print(f"  Order n   : {self.n}  (#{self.n} points on curve)")
        print("  " + "-" * 55)


# ============================================================
#  Predefined Curves
# ============================================================

def get_small_demo_curve() -> EllipticCurve:
    """
    Classic textbook demo curve: y² ≡ x³ + x + 6 (mod 11)
    Base point G = (2, 7), group order n = 13.
    Shows all 13 distinct multiples — perfect for classroom demos.
    """
    p = 11
    a = 1
    b = 6
    G = ECPoint(2, 7)
    n = 13
    return EllipticCurve(p, a, b, G, n, name="Demo Curve: y²=x³+x+6 (mod 11)")


def _compute_point_order(curve: EllipticCurve, G: ECPoint) -> int:
    """Compute order of point G by repeated addition."""
    P = ECPoint(G.x, G.y)
    for k in range(1, 1000):
        P = curve.point_add(P, G)
        if P.is_infinity():
            return k + 1
    return 1000


def get_secp256k1() -> EllipticCurve:
    """
    secp256k1 — the Bitcoin elliptic curve.
    y² = x³ + 7 (mod p)
    """
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    G  = ECPoint(Gx, Gy)
    return EllipticCurve(p, a, b, G, n, name="secp256k1 (Bitcoin curve)")


def get_p256() -> EllipticCurve:
    """
    NIST P-256 (prime256v1) curve.
    """
    p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    a = -3 % p
    b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
    Gx= 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    Gy= 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    G = ECPoint(Gx, Gy)
    return EllipticCurve(p, a, b, G, n, name="NIST P-256")


# ============================================================
#  Interactive CLI
# ============================================================

def run():
    print("\n" + "=" * 60)
    print("       ELLIPTIC CURVE CRYPTOGRAPHY (ECC)")
    print("=" * 60)

    # Curve selection
    print("\n  Select curve:")
    print("  1. Demo Curve over F_97 (small, good for listing all points)")
    print("  2. secp256k1 (Bitcoin curve, 256-bit)")
    print("  3. NIST P-256 (256-bit)")
    print("  4. Custom curve (manual input)")
    curve_choice = input("\n  Select curve [1/2/3/4]: ").strip()

    if curve_choice == "1":
        curve = get_small_demo_curve()
    elif curve_choice == "2":
        curve = get_secp256k1()
    elif curve_choice == "3":
        curve = get_p256()
    elif curve_choice == "4":
        try:
            print("\n  Enter curve domain parameters:")
            p  = int(input("  p (prime field modulus): ").strip())
            a  = int(input("  a: ").strip())
            b  = int(input("  b: ").strip())
            Gx = int(input("  G.x (base point x): ").strip())
            Gy = int(input("  G.y (base point y): ").strip())
            n  = int(input("  n (order of G): ").strip())
            G  = ECPoint(Gx, Gy)
            curve = EllipticCurve(p, a, b, G, n, name="Custom Curve")
        except ValueError as e:
            print(f"  Error: {e}")
            return
    else:
        print("  Invalid choice, defaulting to Demo Curve.")
        curve = get_small_demo_curve()

    curve.display_curve_info()

    # Verify base point is on curve
    if not curve.is_on_curve(curve.G):
        print("  WARNING: Base point G is NOT on the curve!")
    else:
        print(f"\n  ✓ Base point G is on the curve.")

    while True:
        print("\nOptions:")
        print("  1. List all multiples of G (nG for n = 1, 2, ...)")
        print("  2. Generate key pair")
        print("  3. ECDH Key Exchange (two-party demo)")
        print("  4. Scalar multiplication (custom k*G)")
        print("  5. Show curve info")
        print("  0. Back to Main Menu")
        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            max_pts = input("  Max multiples to show [default 30, full order for small curves]: ").strip()
            max_pts = int(max_pts) if max_pts.isdigit() else 30
            multiples = curve.list_all_multiples(max_pts)
            print(f"\n  Multiples of G (Base Point P = G = {curve.G}):")
            print("  " + "-" * 55)
            for k, pt in multiples:
                print(f"  {k}P = {pt}")
            print("  " + "-" * 55)
            print(f"  Total multiples shown: {len(multiples)}")
            last_k, last_pt = multiples[-1]
            if last_pt.is_infinity():
                print(f"  ✓ Order of G confirmed: {last_k}")

        elif choice == "2":
            d, Q = curve.generate_key_pair()
            print(f"\n  Private Key d : {d}")
            print(f"  Public Key  Q : {Q}")
            print(f"  Q = d × G = {d} × {curve.G}")
            if not curve.is_on_curve(Q):
                print("  WARNING: Public key Q is NOT on the curve!")
            else:
                print("  ✓ Public key Q is on the curve.")

        elif choice == "3":
            print("\n  === ECDH Key Exchange Simulation ===")
            print("  Generating key pairs for Alice and Bob...")
            da, Qa = curve.generate_key_pair()
            db, Qb = curve.generate_key_pair()

            print(f"\n  Alice:")
            print(f"    Private key (da) : {da}")
            print(f"    Public key  (Qa) : {Qa}")

            print(f"\n  Bob:")
            print(f"    Private key (db) : {db}")
            print(f"    Public key  (Qb) : {Qb}")

            # Both compute shared key
            shared_alice = curve.ecdh_shared_key(da, Qb)   # Alice: da * Qb
            shared_bob   = curve.ecdh_shared_key(db, Qa)   # Bob:   db * Qa

            print(f"\n  Alice computes: da × Qb = {shared_alice}")
            print(f"  Bob   computes: db × Qa = {shared_bob}")

            if shared_alice == shared_bob:
                print(f"\n  ✓ Shared key matches! ECDH successful.")
                print(f"  Shared Key: {shared_alice}")
                print(f"  Shared Key x-coordinate: {shared_alice.x}")
            else:
                print("  ✗ ERROR: Shared keys do not match!")

            print("\n  Custom a/b input:")
            use_custom = input("  Enter custom private keys? (y/n): ").strip().lower()
            if use_custom == "y":
                try:
                    a_in = int(input(f"  Alice's private key (1 to {curve.n-1}): ").strip())
                    b_in = int(input(f"  Bob's private key   (1 to {curve.n-1}): ").strip())
                    Qa_c = curve.scalar_multiply(a_in, curve.G)
                    Qb_c = curve.scalar_multiply(b_in, curve.G)
                    sk_a = curve.ecdh_shared_key(a_in, Qb_c)
                    sk_b = curve.ecdh_shared_key(b_in, Qa_c)
                    print(f"\n  Alice's public key: {Qa_c}")
                    print(f"  Bob's   public key: {Qb_c}")
                    print(f"  Shared key (Alice): {sk_a}")
                    print(f"  Shared key (Bob)  : {sk_b}")
                    print(f"  Match: {sk_a == sk_b}")
                except ValueError:
                    print("  Invalid input.")

        elif choice == "4":
            k_str = input(f"  Enter scalar k (1 to {curve.n-1}): ").strip()
            try:
                k = int(k_str)
                result = curve.scalar_multiply(k, curve.G)
                print(f"\n  {k} × G = {result}")
                if not result.is_infinity():
                    print(f"  On curve: {curve.is_on_curve(result)}")
            except ValueError:
                print("  Invalid scalar.")

        elif choice == "5":
            curve.display_curve_info()

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
