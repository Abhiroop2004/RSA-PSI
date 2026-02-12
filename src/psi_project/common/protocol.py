import secrets, math
from . import algebra
import hashlib


def random_e(phi: int, bits: int = 32) -> int:
    """
    Pick random e such that gcd(e, phi) = 1.
    bits controls size of e (default: 32-bit).
    """
    assert bits >= 16

    while True:
        e = secrets.randbits(bits) | 1  # make it odd
        if 1 < e < phi and math.gcd(e, phi) == 1:
            return e
        
def GENRSA(bits: int = 1024):
    """
    Generates RSA params (N, e, d)
    bits: number of bits for the modulus N
    """
    half = bits // 2
    p = algebra.generate_large_prime(half)
    q = algebra.generate_large_prime(half)
    N = p * q
    phi = (p - 1) * (q - 1)
    e = random_e(phi)
    d = algebra.modinv(e, phi)
    return N, e, d

def H(x):
    """Generate a hash of x using SHA-256 and return the digest.
    """
    digest = hashlib.sha256(x).digest()
    return int.from_bytes(digest, byteorder='big')

def H1(x: str, n: int) -> int:
    """
    Full Domain Hash into Z_n^* (RSA group)
    """
    target_length = (n.bit_length() + 7) // 8
    counter = 0

    while True:
        shake = hashlib.shake_256()
        shake.update(x.encode())
        shake.update(counter.to_bytes(4, 'big'))

        candidate = int.from_bytes(shake.digest(target_length),byteorder='big') % n

        if 1 < candidate < n and math.gcd(candidate, n) == 1:   return candidate
        
        counter += 1