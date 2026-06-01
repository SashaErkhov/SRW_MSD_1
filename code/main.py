from generator import generator, experiment
from sort import counting_sort, MSD_sort
from scipy import stats
import json
from specific import H, sigma_square
from math import log, sqrt, log2, floor
import matplotlib.pyplot as plt
import resource
import numpy as np

def update_exp_E():
  with open('experiments/exp_E.json', 'r') as f:
    exp_E = json.load(f)
  P = exp_E["P"]
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

    alpha = 0.05
    df = old_data["number"] - 1
    t_crit = stats.t.ppf(1 - alpha / 2, df) # Двусторонний
    standard_error = sqrt(s_sq) / old_data["number"] ** 0.5
    CI = [overline_x - t_crit * standard_error, overline_x + t_crit * standard_error]
    new_data["alpha"] = alpha
    new_data["t_crit"] = t_crit
    new_data["standard_error"] = standard_error
    new_data["CI"] = CI

    H_val = H(P)
    n = old_data["n"]
    main_part_E = (n * log(n)) / H_val
    new_data["H"] = H_val
    new_data["main_part_E"] = main_part_E

    exp_E["experiments"][i] = new_data
  with open('exp_E_update.json', 'w', encoding="utf-8") as f:
    json.dump(exp_E, f, indent = 2)

def drow_exp_E_update():
  with open('experiments/exp_E_update.json', 'r') as f:
    exp_E = json.load(f)
  x = [i["n"] for i in exp_E["experiments"]]
  y = [i["overline_X"] for i in exp_E["experiments"]]
  y_min = [i["CI"][0] for i in exp_E["experiments"]]
  y_max = [i["CI"][1] for i in exp_E["experiments"]]

  lower_error = [val - min_val for val, min_val in zip(y, y_min)]
  upper_error = [max_val - val for val, max_val in zip(y, y_max)]
  asymmetric_error = [lower_error, upper_error]

  plt.figure()
  plt.errorbar(x, y, yerr=asymmetric_error, fmt='o', color='royalblue', 
             ecolor='lightcoral', elinewidth=3, capsize=5, label=r'$\overline{X}$ в дов интервале')

  y = [i["main_part_E"] for i in exp_E["experiments"]]
  plt.plot(x, y, color='darkorange', marker='o', linestyle='-', linewidth=2, markersize=8, label='Главная компонента Е')
  
  plt.title('Доверительные интервалы')
  plt.xlabel('n')
  plt.ylabel('Трудоемкость')
  plt.grid(True, linestyle='--', alpha=0.6)
  plt.legend()
  #plt.xscale('log')  # Растянет сжатые точки по горизонтали
  #plt.yscale('log')  # Растянет их по вертикали, чтобы они не лежали на нулевой отметке

  plt.grid(True, which="both", linestyle='--', alpha=0.5)
  plt.show()

def exp_1():
  mu = 0.7
  P = [0.7, 0.2]
  exp_1 = {
    "mu": mu,
    "P": P,
    "experiments": []
  }

  number = 60

  n = 4096 * 2 * 10
  while True:
    print(f'{n} - start')
    k = n * 2
    delta = k // 2
    experiments = [None] * number
    for i in range(number):
      arr = generator_numpy(n, k, delta, mu, P)
      print(f"{n} - {i} - generate")
      experiments[i] = MSD_sort(arr, n)
      print(f"{n} - {i} - sort")
    data = {
      "number": number,
      "n": n,
      "k": k,
      "delta": delta,
      "experiments": experiments
    }
    print(f'{n} - Done')
    exp_1["experiments"].append(data)
    with open("exp_1_1.json", "w", encoding="utf-8") as f: 
      json.dump(exp_1, f, indent = 2)
    print(f'{n} - Send')
    n *= 2

def find_C():
  from scipy.optimize import linprog
  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)

  # Ax <= b
  A = []
  b = []

  for p in exp_E_update["experiments"]:
    n = p["n"]
    H_val = p["H"]
    ci_low, ci_high = p["CI"]
    const_term = (2.0 / H_val) * n * log(n)

    # C * n <= ci_high - const_term
    A.append([n])
    b.append(ci_high - const_term)

    # B * n >= ci_low - A * (n*log(n)) =>   - B * n <= -ci_low + A * (n*log(n))
    A.append([-n])
    b.append(const_term - ci_low)

  res = linprog(c=[0], A_ub=A, b_ub=b, bounds=[(None, None)])

  if res.success:
    C_found = res.x[0]
    print(f"C = {C_found}")
    return C_found
  else:
    return None

def check_K():
  n = 1_000
  mu = 0.7
  P = [0.7, 0.2]
  number = 60

  data = {
    "n": n,
    "mu": mu,
    "P": P,
    "number": number,
    "experiments": []
  }
  k = int(log(n))
  print(f"k = {k}")

  def send():
    delta = lambda k: k // 2
    exp = experiment(number, n, k, delta(k), mu, P)
    overline_X = sum(exp) / number

    data["experiments"].append(dict())
    data["experiments"][-1]["k"] = k
    data["experiments"][-1]["delta"] = delta(k)
    data["experiments"][-1]["overline_X"] = overline_X

  send()
  k = n
  print(f"k = {k}")
  send()
  k = 2 * n
  print(f"k = {k}")
  send()
  k = 4 * n
  print(f"k = {k}")
  send()
  k = 8 * n
  print(f"k = {k}")
  send()
  with open("check_K.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent = 2)

def draw_Delta():
  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)
  exp = exp_E_update["experiments"]
  n = [p["n"] for p in exp]
  Delta = [(p["overline_X"] - p["main_part_E"])/p["n"] for p in exp]
  for i in range(1, len(n)):
    print(exp[i]["overline_X"] / exp[i-1]["overline_X"])
  plt.plot(n, Delta, marker='o')
  plt.xlabel('n')
  plt.ylabel(r'$\dfrac{\Delta}{n}$')
  plt.grid(True)
  plt.show()

def check_C(B):
  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)
  for p in exp_E_update["experiments"]:
    ci_low, ci_high = p["CI"]
    x = (2.0 / p["H"]) * p["n"] * log(p["n"]) + B * p["n"]
    if not (ci_low <=  x and x <= ci_high):
      print(ci_low, x, ci_high)
      return False
  return True

def find_C_Var():
  global_low = float("-inf")
  global_high = float("inf")
  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)
  P = exp_E_update["P"]
  for p in exp_E_update["experiments"]:
    ci_low, ci_high = p["CI_chi_2"]
    n = p["n"]
    local_low = (ci_low - sigma_square(P)*n*log(n)) / (n * sqrt(log(n)))
    local_high = (ci_high - sigma_square(P)*n*log(n)) / (n * sqrt(log(n)))
    global_low = max(global_low, local_low)
    global_high = min(global_high, local_high)
  print(f'C = [{global_low}, {global_high}]')

def update_exp_E_2():

  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)
  for p in exp_E_update["experiments"]:
    alpha = p["alpha"]
    df = p["number"] - 1
    s_sq = p["S^2"]
    chi_2_low = stats.chi2.ppf(alpha/2, df)
    chi_2_high = stats.chi2.ppf(1 - alpha/2, df)
    CI_low = (df * s_sq) / chi_2_high
    CI_high = (df * s_sq) / chi_2_low
    p["CI_chi_2"] = [CI_low, CI_high]
  with open("experiments/exp_E_update.json", "w") as f:
    json.dump(exp_E_update, f, indent = 2)

def check_C_in_CI():
  C = 34.124080237097495
  with open("experiments/exp_E_update.json", "r") as f:
    exp_E_update = json.load(f)
  P = exp_E_update["P"]
  def Var(n):
    return sigma_square(P)*n*log(n) + C * n * sqrt(log(n))
  for p in exp_E_update["experiments"]:
    x = Var(p["n"])
    ci_l, ci_h = p["CI_chi_2"]
    if not (ci_l <= x and x <= ci_h):
      print(f'n = {p["n"]}')
      print(f'ci = {ci_l}, {ci_h}')
      print(f'Var = {x}')
      print(f'S^2 = {p["S^2"]}')
      return False
  return True

def exp_for_frequency():
  n = 10_000

  k = n * 2
  delta = k // 2
  mu = 0.7
  P = [0.7, 0.2]

  C = 34.124080237097495
  Var = sigma_square(P) * n * log(n) + C * n * sqrt(log(n))
  sigma = sqrt(Var)
  alpha = 0.05
  z_crit = stats.norm.ppf(1 - alpha/2)

  Delta = sigma * 0.05

  number = int(((z_crit * sigma) / Delta) ** 2)
  experiments = experiment(number, n, k, delta, mu, P)
  data = {
    "n": n, 
    "k": k, 
    "delta": delta, 
    "mu": mu, 
    "P": P, 
    "number": number, 
    "experiments": experiments
  }
  with open('exp_for_frequency.json', 'w') as f:
    json.dump(data, f, indent = 2)

def freq_analyze():
  with open("experiments/exp_for_frequency.json", "r") as f:
    exp = json.load(f)
  number = exp["number"]
  experiments = exp["experiments"]
  overlune_X = sum(experiments) / number
  s_sq = (sum([(p - overlune_X)**2 for p in experiments])) / (number - 1)

  cnt, bins, ignored = plt.hist(experiments, bins = 'auto',
                                density = True, alpha = 0.6,
                                color='skyblue', edgecolor='gray', 
                                label='Экспериментальные данные')
  
  x = np.linspace(bins.min(), bins.max(), 100)
  pdf = stats.norm.pdf(x, loc = overlune_X, scale = sqrt(s_sq))
  plt.plot(x, pdf, color = 'crimson',lw = 2.5, label = 'Теоретическая плотность')

  plt.xlabel('Трудоёмкость')
  plt.ylabel('Плотность вероятности')
  plt.grid(True, linestyle='--', alpha=0.5)
  plt.legend(fontsize = 8)

  #plt.savefig("freq.png", dpi = 300, bbox_inches="tight")
  plt.show()

def pirson():
  with open("experiments/exp_for_frequency.json", "r") as f:
    exp = json.load(f)
  number = exp["number"]
  experiments = exp["experiments"]
  overline_X = sum(experiments) / number
  s_sq = (sum([(p - overline_X)**2 for p in experiments])) / (number - 1)
  alpha = 0.05

  bins = 1 + floor(log2(number))
  print(f'Было {bins} бакетов')
  counts, bin_edges = np.histogram(experiments, bins = bins)
  expected_edges = bin_edges.copy()
  expected_edges[0] = -np.inf
  expected_edges[-1] = np.inf

  theory = np.diff(stats.norm.cdf(expected_edges, loc = overline_X, scale = sqrt(s_sq)))
  expected_cnt = theory * number
  
  obs = list(counts)
  exp = list(expected_cnt)
  i = 0
  while i < len(exp):
    if exp[i] < 5 and len(exp) > 1:
      if i < len(exp) - 1:
        exp[i+1] += exp[i]
        obs[i+1] += obs[i]
        exp.pop(i)
        obs.pop(i)
      else:
        exp[i-1] += exp[i]
        obs[i-1] += obs[i]
        exp.pop(i)
        obs.pop(i)
        i -= 1
    else:
      i += 1

  counts_merged = np.array(obs)
  expected_cnt_merged = np.array(exp)
  print(f'Осталось {len(expected_cnt_merged)} бакетов')

  assert len(expected_cnt_merged) > 3
  assert np.all(expected_cnt_merged >= 5)

  chi2_stat, p_value = stats.chisquare(f_obs=counts_merged, f_exp=expected_cnt_merged, ddof=2)

  print(f"Статистика Хи-квадрат: {chi2_stat}")
  print(f"p-value: {p_value:}")

  if p_value > alpha:
      print(f"p-value > {alpha}. Нулевая гипотеза НЕ отклоняется.")
      print("Экспериментальные данные согласуются с теоретическим нормальным распределением.")
  else:
      print(f"p-value <= {alpha}. Нулевая гипотеза отклоняется.")
      print("Экспериментальные данные статистически значимо отличаются от теории.")

if __name__ == '__main__':
  limit = 8 * 1024 * 1024 * 1024
  resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
  pirson()