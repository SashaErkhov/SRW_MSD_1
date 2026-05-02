import random
from sort import MSD_sort

def generator(
    n: int,
    k: int,
    delta: int,
    mu: float,
    P: list[float],
):
  array = []
  for _ in range(n):
    if random.random() < mu:
      word = '0'
    else:
      word = '1'
    real_num_k = k + random.randint(-delta, delta)
    for __ in range(real_num_k - 1):
      if word[-1] == '0':
        if random.random() < P[0]:
          word = word + '0'
        else:
          word = word + '1'
      else:
        if random.random() < P[1]:
          word = word + '0'
        else:
          word = word + '1'
    array.append(word)
  return array

def experiment(
    number: int,
    n: int,
    k: int,
    delta: int,
    mu: int,
    P: list[float]
) -> list[int]:
  res = [None] * number
  for i in range(number):
    res[i] = MSD_sort(generator(n, k, delta, mu, P),n)
  return res
