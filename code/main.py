from generator import generator

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

if __name__ == '__main__':
  test_generator()