import math, secrets

def random_bit(bits : int = 16) -> int:
    """
    Returns a random number generator instance.
    bits: number of bits for the random number generator
    """
    return secrets.randbits(bits)

def random_int(n: int) -> int:
    """
    Generates a random integer in the range [0, n).
    n: upper bound (exclusive)
    """
    rng = random_bit(16)
    return rng.randint(0, n - 1)

def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using trial division.
    n: integer to check for primality
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    """
    Computes the greatest common divisor of a and b using the Euclidean algorithm.
    a, b: integers
    """
    while b:
        a, b = b, a % b
    return a

def modinv(a: int, m: int) -> int:
    """
    Computes the modular inverse of a modulo m using
    the Extended Euclidean Algorithm.
    Raises ValueError if inverse does not exist.
    """
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = egcd(a, m)

    if gcd != 1:
        raise ValueError("Modular inverse does not exist")

    return x % m

def pow(a: int, b: int, m: int) -> int:
    """
    Computes (a^b) mod m using modular exponentiation.
    a: base
    b: exponent
    m: modulus
    """
    result = 1
    a = a % m
    while b > 0:
        if (b % 2) == 1:
            result = (result * a) % m
        b = b >> 1
        a = (a * a) % m
    return result

def moddiv(a: int, b: int, m: int) -> int:
    """
    Computes (a / b) mod m using the modular inverse.
    a: numerator
    b: denominator
    m: modulus
    """
    return (a * modinv(b, m)) % m

def random_group_element(n: int) -> int:
    """
    Directly picks a random element in Z_n* without generating entire group.
    n: modulus
    """
    while True:
        r = secrets.randbelow(n - 1) + 1
        if math.gcd(r, n) == 1:
            return r

def group_mul(a: int, b: int, n: int) -> int:
    """
    Multiplies two group elements a and b modulo n.
    a, b: group elements
    n: modulus
    """
    return (a * b) % n
        
def generate_large_prime(bits: int) -> int:
    """
    Generates a large prime number with the specified number of bits.
    bits: number of bits for the prime number
    """
    while True:
        # FIX: Force the MSB to 1 to ensure the number is actually 'bits' long
        # and Force the LSB to 1 to ensure it is odd
        num = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(num):
            return num
        
def generate_large_prime(bits: int) -> int:
    while True:
        # Ensure the number has the correct bit length and is odd
        num = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(num):
            return num
        
def get_zn_star_elements(n):
    """ 
    Returns all a in [1, n-1] where gcd(a, n) == 1
    """
    return [a for a in range(1, n) if gcd(a, n) == 1]