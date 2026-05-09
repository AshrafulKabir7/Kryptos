import random


class ECPoint:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def is_infinity(self):
        return self.infinity

    def __eq__(self, other):
        if not isinstance(other, ECPoint):
            return False
        if self.infinity and other.infinity:
            return True
        if self.infinity or other.infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.infinity:
            return "O (point at infinity)"
        return f"({self.x}, {self.y})"

    def __hash__(self):
        if self.infinity:
            return hash(None)
        return hash((self.x, self.y))


class EllipticCurve:
    def __init__(self, p, a, b, G, n, name="Custom"):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n
        self.name = name
        disc = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if disc == 0:
            raise ValueError("Singular curve! Choose different a, b parameters.")

    def is_on_curve(self, P):
        if P.is_infinity():
            return True
        lhs = pow(P.y, 2, self.p)
        rhs = (pow(P.x, 3, self.p) + self.a * P.x + self.b) % self.p
        return lhs == rhs

    def mod_inv(self, k):
        if k % self.p == 0:
            raise ValueError("Modular inverse of zero.")
        return pow(k, self.p - 2, self.p)

    def point_add(self, P, Q):
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P
        if P.x == Q.x:
            if P.y != Q.y or P.y == 0:
                return ECPoint(None, None, infinity=True)
            return self.point_double(P)
        lam = (Q.y - P.y) * self.mod_inv(Q.x - P.x) % self.p
        x3 = (lam * lam - P.x - Q.x) % self.p
        y3 = (lam * (P.x - x3) - P.y) % self.p
        return ECPoint(x3, y3)

    def point_double(self, P):
        if P.is_infinity():
            return P
        if P.y == 0:
            return ECPoint(None, None, infinity=True)
        lam = (3 * P.x * P.x + self.a) * self.mod_inv(2 * P.y) % self.p
        x3 = (lam * lam - 2 * P.x) % self.p
        y3 = (lam * (P.x - x3) - P.y) % self.p
        return ECPoint(x3, y3)

    def scalar_multiply(self, k, P):
        k = k % self.n
        result = ECPoint(None, None, infinity=True)
        addend = ECPoint(P.x, P.y)
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        return result

    def list_all_multiples(self, max_points=50):
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

    def generate_key_pair(self):
        d = random.randint(1, self.n - 1)
        Q = self.scalar_multiply(d, self.G)
        return d, Q

    def ecdh_shared_key(self, private_key, other_public_key):
        return self.scalar_multiply(private_key, other_public_key)

    def display_curve_info(self):
        print(f"\n  Curve: {self.name}")
        print("  " + "-" * 55)
        print(f"  Equation : y^2 = x^3 + {self.a}x + {self.b}  (mod {self.p})")
        print(f"  Base point G = {self.G}")
        print(f"  Order n  = {self.n}")
        print("  " + "-" * 55)


def get_small_demo_curve():
    G = ECPoint(2, 7)
    return EllipticCurve(11, 1, 6, G, 13, name="Demo: y^2 = x^3 + x + 6 (mod 11)")


def get_secp256k1():
    p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    return EllipticCurve(p, 0, 7, ECPoint(Gx, Gy), n, name="secp256k1 (Bitcoin curve)")


def get_p256():
    p  = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    a  = -3 % p
    b  = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
    Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    n  = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    return EllipticCurve(p, a, b, ECPoint(Gx, Gy), n, name="NIST P-256")


def run():
    print("\n" + "=" * 55)
    print("       ELLIPTIC CURVE CRYPTOGRAPHY (ECC)")
    print("=" * 55)

    print("\n  Select curve:")
    print("  1. Demo Curve (small, good for listing all points)")
    print("  2. secp256k1 (Bitcoin curve, 256-bit)")
    print("  3. NIST P-256 (256-bit)")
    print("  4. Custom curve")
    curve_choice = input("\n  Select [1/2/3/4]: ").strip()

    if curve_choice == "1":
        curve = get_small_demo_curve()
    elif curve_choice == "2":
        curve = get_secp256k1()
    elif curve_choice == "3":
        curve = get_p256()
    elif curve_choice == "4":
        try:
            print("\n  Enter curve parameters:")
            p  = int(input("  p (prime): ").strip())
            a  = int(input("  a: ").strip())
            b  = int(input("  b: ").strip())
            Gx = int(input("  G.x: ").strip())
            Gy = int(input("  G.y: ").strip())
            n  = int(input("  n (order): ").strip())
            curve = EllipticCurve(p, a, b, ECPoint(Gx, Gy), n, name="Custom Curve")
        except ValueError as ex:
            print(f"  Error: {ex}")
            return
    else:
        print("  Defaulting to Demo Curve.")
        curve = get_small_demo_curve()

    curve.display_curve_info()

    if not curve.is_on_curve(curve.G):
        print("  WARNING: Base point G is NOT on the curve!")
    else:
        print("  Base point G is on the curve.")

    while True:
        print("\n  1. List all multiples of G")
        print("  2. Generate key pair")
        print("  3. ECDH Key Exchange")
        print("  4. Scalar multiplication (k * G)")
        print("  5. Show curve info")
        print("  0. Back")

        choice = input("\nSelect: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            max_pts = input("  Max multiples to show [default 30]: ").strip()
            max_pts = int(max_pts) if max_pts.isdigit() else 30
            multiples = curve.list_all_multiples(max_pts)
            print(f"\n  Multiples of G:")
            print("  " + "-" * 40)
            for k, pt in multiples:
                print(f"  {k}G = {pt}")
            print("  " + "-" * 40)
            print(f"  Total shown: {len(multiples)}")

        elif choice == "2":
            d, Q = curve.generate_key_pair()
            print(f"\n  Private Key d : {d}")
            print(f"  Public Key  Q : {Q}")
            if not curve.is_on_curve(Q):
                print("  WARNING: Public key Q is NOT on the curve!")

        elif choice == "3":
            print("\n  ECDH Key Exchange — Alice and Bob")
            da, Qa = curve.generate_key_pair()
            db, Qb = curve.generate_key_pair()

            print(f"\n  Alice: da = {da},  Qa = {Qa}")
            print(f"  Bob  : db = {db},  Qb = {Qb}")

            shared_alice = curve.ecdh_shared_key(da, Qb)
            shared_bob   = curve.ecdh_shared_key(db, Qa)

            print(f"\n  Alice computes da * Qb = {shared_alice}")
            print(f"  Bob   computes db * Qa = {shared_bob}")

            if shared_alice == shared_bob:
                print("  Shared keys match! ECDH successful.")
                print(f"  Shared Key x: {shared_alice.x}")
            else:
                print("  ERROR: Shared keys do not match!")

            use_custom = input("\n  Enter custom private keys? (y/n): ").strip().lower()
            if use_custom == "y":
                try:
                    a_in = int(input(f"  Alice's private key (1 to {curve.n - 1}): ").strip())
                    b_in = int(input(f"  Bob's private key   (1 to {curve.n - 1}): ").strip())
                    Qa_c = curve.scalar_multiply(a_in, curve.G)
                    Qb_c = curve.scalar_multiply(b_in, curve.G)
                    sk_a = curve.ecdh_shared_key(a_in, Qb_c)
                    sk_b = curve.ecdh_shared_key(b_in, Qa_c)
                    print(f"  Alice public key: {Qa_c}")
                    print(f"  Bob   public key: {Qb_c}")
                    print(f"  Shared key match: {sk_a == sk_b}")
                except ValueError:
                    print("  Invalid input.")

        elif choice == "4":
            k_str = input(f"  Enter k (1 to {curve.n - 1}): ").strip()
            try:
                k = int(k_str)
                result = curve.scalar_multiply(k, curve.G)
                print(f"  {k} * G = {result}")
            except ValueError:
                print("  Invalid scalar.")

        elif choice == "5":
            curve.display_curve_info()

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    run()
