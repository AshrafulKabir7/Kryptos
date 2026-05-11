import random

# A point at infinity will be represented as (None, None)

def is_on_curve(p, a, b, point):
    if point == (None, None):
        return True
    x, y = point
    lhs = (y * y) % p
    rhs = (x * x * x + a * x + b) % p
    return lhs == rhs

def point_add(p, a, P1, P2):
    if P1 == (None, None): return P2
    if P2 == (None, None): return P1
    
    x1, y1 = P1
    x2, y2 = P2
    
    if x1 == x2 and y1 != y2:
        return (None, None)
        
    if P1 == P2:
        if y1 == 0:
            return (None, None)
        # Point doubling
        lam_num = (3 * x1 * x1 + a) % p
        lam_den = pow(2 * y1, p - 2, p)
    else:
        # Point addition
        lam_num = (y2 - y1) % p
        lam_den = pow((x2 - x1) % p, p - 2, p)
        
    lam = (lam_num * lam_den) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    
    return (x3, y3)

def scalar_mul(p, a, k, P):
    result = (None, None)
    addend = P
    
    while k > 0:
        if k % 2 == 1:
            result = point_add(p, a, result, addend)
        addend = point_add(p, a, addend, addend)
        k = k // 2
        
    return result

def find_all_points(p, a, b):
    # Only allow for small primes to prevent server lockup
    if p > 10000:
        raise ValueError("Prime p is too large to find all points. Please use p < 10000.")
        
    points = [(None, None)] # Always includes infinity
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        # Find square roots of rhs mod p (brute force for small p is fine)
        for y in range(p):
            if (y * y) % p == rhs:
                points.append((x, y))
    return points

def compute_order(p, a, P):
    if P == (None, None):
        return 1
        
    current = P
    n = 1
    while current != (None, None):
        current = point_add(p, a, current, P)
        n += 1
        # Failsafe
        if n > 10000:
            raise ValueError("Order is too large to compute by brute force, or point is not a generator.")
    return n

def generate_key_pair(p, a, b, G, private_key=None, n=None):
    if not is_on_curve(p, a, b, G):
        raise ValueError("Generator point G is not on the curve.")
        
    if private_key is None:
        if n is None:
            n = compute_order(p, a, G)
        private_key = random.randint(2, n - 1)
        
    public_key = scalar_mul(p, a, private_key, G)
    return private_key, public_key

def ecdh_key_exchange(p, a, b, G, priv_A, priv_B):
    # Alice computes her public key
    pub_A = scalar_mul(p, a, priv_A, G)
    # Bob computes his public key
    pub_B = scalar_mul(p, a, priv_B, G)
    
    # Alice receives pub_B and computes shared secret
    shared_A = scalar_mul(p, a, priv_A, pub_B)
    
    # Bob receives pub_A and computes shared secret
    shared_B = scalar_mul(p, a, priv_B, pub_A)
    
    if shared_A != shared_B:
        raise ValueError("Shared secrets do not match!")
        
    return pub_A, pub_B, shared_A

def run():
    print("\n  ECC CLI - Refactored into simple procedural functions.")
    print("  Refer to the Web UI for the fully interactive version.")

if __name__ == "__main__":
    run()
