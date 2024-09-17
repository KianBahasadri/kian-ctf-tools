from math import lcm, gcd
def print_attack_list():
  print("""-----------------------------------------------------------------
attack1(A, B, p, g, _range):
        Performs an attack on DH when p is a composite number
        A (int) g**a mod p
        B (int) g**b mod p
        p (int) supposed to be prime
        g (int) generator
        _range (int, optional): The number of iterations for the attack. Default is False (will prompt for input).
          Returns:
              g**(ab) mod p
factor_attack(n):
        n: integer to factor
        Returns: list of factors
        Attempts to factor the given integer n
        Uses factordb and then attempts to manually factor
        Warning: kind of shit
factorDB(n):
        requests the factorization from http://factordb.com/api
        checks if its valid and returns it if it is

-----------------------------------------------------------------""")

def attack1(A, B, p, g, _range):
  # Step 1: Break p into its factors
  print("finding factors of p")
  factors = factor_attack(p):

  # Step 2: Solve the Discrete Logarithm Problem for each factor
  # i.e. g**<nth x> = A mod <nth f>
  def find_exponents(g, y, factors):
    exponents = []
    for f in factors:
      for i in range(f):
        if pow(g, i, f) == y:
          exponents.append(i)
        break
      else:
        print("WARNING: AN EXPONENT WAS NOT FOUND FOR A FACTOR, SOMETHING HAS GONE WRONG")
        print(f"exponents: {exponents}, factors: {factors}, y: {y}")
    return exponents



  import multiprocessing

  for i in range(_range):
    x = M + (i * n)
    number = nth_int_root(x, e)
    dec = int.to_bytes(number, (number.bit_length() + 7) // 8)
    if plaintext in dec:
      print(i, '--', int.to_bytes(number, (number.bit_length() + 7) // 8))
    elif i % 1000 == 0:
      print(i)
      #print(dec[:32])

def attack2(n):
  db = factorDB(n)
  if db:
    print(db)
    return db
  else:
    if n > 10**20:
      print("WARNING: if n is made up of large primes this is gonna take a long time")
      print("Reccomend to use https://gitlab.inria.fr/cado-nfs instead")
    print("Factor DB failed factorization, continuing manually")
    from sympy import factorint
    print(factorint(n))

def factorDB(n):
  import json
  import requests
  response = requests.get(f"http://factordb.com/api?query={n}")
  datadict = json.loads(response.content)
  if datadict['status'] in ('C', 'U', 'C*', 'U*'):
    return None
  else:
    return datadict['factors']


#-----------------------------------------------------------------
print_attack_list()
