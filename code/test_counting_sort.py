import pytest
from hypothesis import given, strategies as st
from sort import counting_sort 


# --- Тесты для обычных базовых сценариев ---

@pytest.mark.parametrize("arr, target_digit, expected_arr", [
    # Тест 1: Простая сортировка по первому символу (индекс 0)
    (["10", "01", "00", "11"], 0, ["01", "00", "10", "11"]),
    
    # Тест 2: Сортировка по второму символу (индекс 1)
    (["10", "01", "00", "11"], 1, ["10", "00", "01", "11"]),
    
    # Тест 3: Строки разной длины (короткие должны уйти в начало, в group[0])
    (["1", "01", "", "0"], 0, ["", "01", "0", "1"]),
])
def test_counting_sort_basic(arr, target_digit, expected_arr):
    """Проверка корректности перестановки элементов во всем массиве."""
    arr_copy = arr.copy()
    left = 0
    right = len(arr_copy)
    
    counting_sort(arr_copy, left, right, target_digit)
    assert arr_copy == expected_arr


# --- Тесты для подмассивов (left и right) ---

def test_counting_sort_subarrays():
    """Проверяем, что функция сортирует только внутри [left, right) и не трогает остальное."""
    arr = ["11", "10", "01", "00", "11"]
    # Сортируем только элементы с индекса 1 по 3 включительно: ["10", "01", "00"] по индексу 1
    # Ожидаем, что они превратятся в ["10", "00", "01"]
    left, right = 1, 4
    target_digit = 1
    
    counting_sort(arr, left, right, target_digit)
    assert arr == ["11", "10", "00", "01", "11"]


# --- Тесты для возвращаемых групп (границы бакетов) ---

def test_counting_sort_groups_boundaries():
    """Проверяем, что возвращаемые группы точно соответствуют границам бакетов."""
    # Разряд 0:
    # "" -> длина 0 (категория 0)
    # "01", "0" -> начинаются с '0' (категория 1)
    # "10", "1" -> начинаются с '1' (категория 2)
    arr = ["10", "01", "", "1", "0"]
    left, right = 0, len(arr)
    
    _, groups = counting_sort(arr, left, right, target_digit=0)
    
    # Ожидаемый порядок после сортировки: ["", "01", "0", "10", "1"]
    # Категория 0: индекс 0 (длина 1) -> [0, 1)
    # Категория 1: индексы 1, 2 (длина 2) -> [1, 3)
    # Категория 2: индексы 3, 4 (длина 2) -> [3, 5)
    assert groups == [(0, 1), (1, 3), (3, 5)]
    
    # Проверяем, что элементы внутри групп действительно соответствуют своим критериям
    g0_start, g0_end = groups[0]
    g1_start, g1_end = groups[1]
    g2_start, g2_end = groups[2]
    
    assert all(len(s) <= 0 for s in arr[g0_start:g0_end])
    assert all(len(s) > 0 and s[0] == '0' for s in arr[g1_start:g1_end])
    assert all(len(s) > 0 and s[0] == '1' for s in arr[g2_start:g2_end])


# --- Краевые случаи (Edge Cases) ---

def test_counting_sort_empty_and_single():
    """Проверка работы с пустым массивом или массивом из 1 элемента."""
    # Пустой подмассив
    arr1 = []
    res, groups = counting_sort(arr1, 0, 0, 0)
    assert arr1 == []
    assert res == 0
    assert groups == [(0, 0), (0, 0), (0, 0)]

    # Один элемент
    arr2 = ["1"]
    res, groups = counting_sort(arr2, 0, 1, 0)
    assert arr2 == ["1"]
    assert groups == [(0, 0), (0, 0), (0, 1)]


# --- Property-based тесты (Случайные данные любой сложности) ---

@given(
    # Генерируем список строк, состоящих только из '0' и '1', длиной от 0 до 10 символов
    arr=st.lists(st.text(alphabet="01", max_size=10), min_size=0, max_size=50),
    target_digit=st.integers(min_value=0, max_value=10)
)
def test_counting_sort_property_stable(arr, target_digit):
    """Автоматический тест на случайных массивах для проверки стабильности и корректности."""
    left = 0
    right = len(arr)
    
    # Делаем копию для работы нашей функции
    arr_to_sort = arr.copy()
    
    # Вызываем тестируемую функцию
    res, groups = counting_sort(arr_to_sort, left, right, target_digit)
    
    # Проверяем базовое свойство: общее количество элементов не изменилось
    assert len(arr_to_sort) == len(arr)
    
    # Проверяем корректность разделения на группы (бакеты)
    g0 = arr_to_sort[groups[0][0] : groups[0][1]]
    g1 = arr_to_sort[groups[1][0] : groups[1][1]]
    g2 = arr_to_sort[groups[2][0] : groups[2][1]]
    
    # 1. Все элементы в g0 должны быть короче target_digit
    assert all(target_digit >= len(s) for s in g0)
    
    # 2. Все элементы в g1 должны иметь '0' на позиции target_digit
    assert all(target_digit < len(s) and s[target_digit] == '0' for s in g1)
    
    # 3. Все элементы в g2 должны иметь '1' на позиции target_digit
    assert all(target_digit < len(s) and s[target_digit] == '1' for s in g2)
    
    # 4. Проверка стабильности (Stability). 
    # Элементы внутри одной группы должны сохранить свой относительный изначальный порядок.
    def get_relative_order(sub_group, original_list):
        # Находим индексы элементов sub_group в исходном массиве
        indices = []
        start_search = 0
        for item in sub_group:
            idx = original_list.index(item, start_search)
            indices.append(idx)
            # Сдвигаем указатель, так как элементы могут дублироваться
            start_search = idx + 1 
        return indices

    for group in [g0, g1, g2]:
        indices = get_relative_order(group, arr)
        # Индексы должны строго возрастать, если сортировка стабильна
        assert indices == sorted(indices)