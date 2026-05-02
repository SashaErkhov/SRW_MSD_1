

def counting_sort(
    arr: list[str],
    left: int,
    right: int,
    target_digit: int
) -> tuple[int, list[tuple[int, int]]]:
  n = right - left
  R = 3 # None 0 1
  C = [0] * (R + 1)
  res = 0 # count of operations

  for i in range(left, right):
    if target_digit >= len(arr[i]):
      ch = 0
    elif arr[i][target_digit] == '0':
      res += 1
      ch = 1
    else:
      res += 1
      ch = 2
    C[ch+1] += 1
  
  for i in range(R):
    C[i+1] += C[i]

  new_arr = [None] * n
  for i in range(left, right):
    if target_digit >= len(arr[i]):
      ch = 0
    elif arr[i][target_digit] == '0':
      res += 1
      ch = 1
    else:
      res += 1
      ch = 2
    new_arr[C[ch]] = arr[i]
    C[ch] += 1

  for i in range(n):
    arr[i + left] = new_arr[i]
  
  groups = []
  start = left
  for i in range(R):
    end = C[i] + left
    groups.append((start, end))
    start = end

  return res, groups

def MSD_sort(
    arr: list[str],
    n: int
) -> int:
  stack = [(0, 0, n)] # digit, left, right
  total_count = 0

  while stack:
    digit, left, right = stack.pop()
    if right-left <= 1 or digit >= max(len(arr[i]) for i in range(left, right)):
      continue
    count, groups = counting_sort(arr, left, right, digit)
    total_count += count
    for i in range(1, len(groups)):
      new_left, new_right = groups[i]
      if new_right - new_left > 1:
        stack.append((digit+1, new_left, new_right))
  
  return total_count
