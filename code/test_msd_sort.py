from sort import MSD_sort
import pytest

# Тесты для MSD_sort с использованием реального counting_sort
@pytest.mark.parametrize(
    "input_arr, expected_arr",
    [
        # Пустой массив
        ([], []),
        # Массив из одного элемента
        (["0"], ["0"]),
        # Уже отсортированный массив одинаковой длины
        (["00", "01", "10", "11"], ["00", "01", "10", "11"]),
        # Массив в обратном порядке одинаковой длины
        (["11", "10", "01", "00"], ["00", "01", "10", "11"]),
        # Строки разной длины (короткие должны быть раньше длинных при одинаковом префиксе)
        (["101", "1", "0", "10", "00"], ["0", "00", "1", "10", "101"]),
        # Массив с дубликатами
        (["10", "01", "10", "00", "01"], ["00", "01", "01", "10", "10"]),
        # Все элементы одинаковые
        (["110", "110", "110"], ["110", "110", "110"]),
    ],
)
def test_msd_sort_correctness(input_arr, expected_arr):
    arr_to_sort = input_arr.copy()
    MSD_sort(arr_to_sort, len(arr_to_sort))
    assert arr_to_sort == expected_arr


def test_msd_sort_returns_int_count():
    arr = ["11", "00", "10", "01"]
    total_count = MSD_sort(arr, len(arr))
    assert isinstance(total_count, int)
    assert total_count > 0