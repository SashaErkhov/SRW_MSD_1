from generator import generator, experiment
from sort import counting_sort, MSD_sort
import json

def test_generator():
  print("test of generator")
  print("mu = [0.7, 0.3]")
  mu = 0.7
  print("P = [[0.7, 0.3], [0.2, 0.8]]")
  P = [0.7, 0.2]
  print("n = 10")
  n = 10
  print("digit: 10 +- 5")
  digit = 10
  delta_of_digit = 5
  a = generator(n, digit, delta_of_digit, mu, P)
  print("a = ")
  print(*a, sep="\n")

def test_counting_sort():
  print("arr = ['101', '110', '100', '100', '011']")
  arr = ['101', '110', '100', '100', '011']
  print("left = 0, right = len(arr), digit = 0")
  left = 0
  right = len(arr)
  digit = 0
  cnt, groups = counting_sort(arr, left, right, digit)
  print("cnt = ", cnt)
  print("groups = ", groups)
  print("sorted_arr = ")
  print(*arr, sep='\n')

def test_MSD_sort():
  print("arr = ['101', '110', '100', '100', '011']")
  arr = ['101', '110', '100', '100', '011']
  cnt = MSD_sort(arr, 5)
  print("cnt =", cnt)
  print("sorted_arr =", *arr)

def exp_1():
  number = 10_000
  n = 100
  k = 1000
  delta = 500
  mu = 0.7
  P = [0.7, 0.2]
  exp = experiment(number, n, k, delta, mu, P)
  with open("exp_E_simple.txt", "w") as f:
    f.write(f'{number}\n')
    f.write(f'{n}\n')
    f.write(f'{k}\n')
    f.write(f'{delta}\n')
    f.write(f'{mu}\n')
    f.write(f'{P[0]} {P[1]}\n')
    for p in exp:
      f.write(f'{p} ')
    f.write('\n')

def exp_2():
  exp_2_json = {}

  # Фиксирую разряды и распределение
  k = 1_000_000
  delta = 1_000
  mu = 0.7
  P = [0.7, 0.2]

  exp_2_json["k"] = k
  exp_2_json["delta"] = delta
  exp_2_json["mu"] = mu
  exp_2_json["P"] = P
  exp_2_json["experiments"] = dict()

  number = 100

  for n in range(1000, 1_000_000, 1000):
    exp_2_json["experiments"]["number"] = number
    exp_2_json["experiments"]["experiments"] = experiment(
      number, n, k, delta, mu, P
      )
    print(f"{n}/1_000_000 Done")
  
  with open("exp_2.json", "w", encoding="utf-8") as f:
    json.dump(exp_2_json, f, indent = 2)


if __name__ == '__main__':
  exp_2()