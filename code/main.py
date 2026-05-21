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

def update_exp_E():
  with open('experiments/exp_E.json', 'r') as f:
    exp_E = json.load(f)
  for i in range(len(exp_E["experiments"])):
    old_data = exp_E["experiments"][i]
    new_data = {
      "number": old_data["number"],
      "n": old_data["n"],
      "k": old_data["k"],
      "delta": old_data["delta"]
    }
    overline_x = 0
    for j in range(old_data["number"]):
      overline_x += old_data["experiments"][j]
    overline_x /= old_data["number"]
    s_sq = 0
    for j in range(old_data["number"]):
      s_sq += (old_data["experiments"][j] - overline_x) ** 2
    s_sq /= old_data["number"] - 1
    new_data["overline_X"] = overline_x
    new_data["S^2"] = s_sq
    exp_E["experiments"][i] = new_data
  with open('exp_E_update.json', 'w', encoding="utf-8") as f:
    json.dump(exp_E, f, indent = 2)

def exp_1():
  mu = 0.7
  P = [0.7, 0.2]
  exp_1 = {
    "mu": mu,
    "P": P,
    "experiments": []
  }

  number = 20

  n = 4096 * 2 * 10
  while True:
    k = n * 2
    delta = k // 2
    data = {
      "number": number,
      "n": n,
      "k": k,
      "delta": delta,
      "experiments": experiment(number, n, k, delta, mu, P)
    }
    print(f'{n} - Done')
    exp_1["experiments"].append(data)
    with open("exp_1.json", "w", encoding="utf-8") as f: 
      json.dump(exp_1, f, indent = 2)
    print(f'{n} - Send')
    n *= 2

if __name__ == '__main__':
  exp_1()