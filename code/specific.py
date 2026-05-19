from math import log

def _normalyze_P(P: list[float]) -> list[list[float]]:
  return [[P[0], 1-P[0]], [P[1], 1-P[1]]]

def pi(P: list[float]) -> tuple[float]:
  new_P = _normalyze_P(P)
  return (new_P[1][0]/(new_P[1][0] + new_P[0][1]), 
          new_P[0][1]/(new_P[1][0] + new_P[0][1]))

def H_i(P: list[float]) -> tuple[float]:
  new_P = _normalyze_P(P)
  H_0 = - new_P[0][0]*log(new_P[0][0]) - new_P[0][1]*log(new_P[0][1])
  H_1 = - new_P[1][0]*log(new_P[1][0]) - new_P[1][1]*log(new_P[1][1])
  return H_0, H_1

def H(P: list[float]) -> float:
  pi_0, pi_1 = pi(P)
  H_0, H_1 = H_i(P)
  return pi_0*H_0 + pi_1*H_1

def sigma_square(P: list[float]) -> float:
  pi_0, pi_1 = pi(P)
  H_0, H_1 = H_i(P)
  H_val = H(P)
  new_P = _normalyze_P(P)
  return pi_0*new_P[0][0]*new_P[0][1]/H_val**3 * \
    (log(new_P[0][0]/new_P[0][1]) + (H_1 - H_0)/(new_P[0][1]+new_P[1][0]))**2 + \
    pi_1*new_P[1][0]*new_P[1][1]/H_val**3 * \
    (log(new_P[1][0]/new_P[1][1]) + (H_1 - H_0)/(new_P[0][1]+new_P[1][0]))**2
