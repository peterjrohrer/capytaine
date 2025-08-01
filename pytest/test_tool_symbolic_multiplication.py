import pytest
import numpy as np
from capytaine.tools.symbolic_multiplication import SymbolicMultiplication, supporting_symbolic_multiplication

def test_definition():
    zero = SymbolicMultiplication("0")
    assert zero.symbol == "0"
    assert isinstance(zero, SymbolicMultiplication)

def test_multiplication():
    zero = SymbolicMultiplication("0")
    b = 2 * zero
    assert b.value == 2 * zero.value

def test_division():
    zero = SymbolicMultiplication("0")
    b = 2 * zero
    assert b / zero == 2

def test_double_division():
    zero = SymbolicMultiplication("0")
    b = 7 * zero * zero
    assert b / (zero * zero) == 7

def test_invert_division():
    zero = SymbolicMultiplication("0")
    b = 9 * zero
    assert zero / b == pytest.approx(1/9)

def test_float():
    zero = SymbolicMultiplication("0")
    b = 4.5 * zero
    assert float(b) == pytest.approx(0.0)

def test_numpy_array():
    zero = SymbolicMultiplication("0")
    b = np.random.rand(10) * zero
    assert (b / zero).shape == (10,)

def test_numpy_array_sum():
    zero = SymbolicMultiplication("0")
    b = np.ones(10) * zero
    assert (np.sum(b) / zero) == 10

def test_numpy_matmul():
    zero = SymbolicMultiplication("0")
    b = np.random.rand(10) * zero
    A = np.random.rand(10, 10)
    c = A @ b
    assert (c/zero).shape == (10,)

def test_undefined_case():
    assert np.isnan(float(SymbolicMultiplication("0", np.inf)))
    assert np.isnan(float(SymbolicMultiplication("∞", 0.0)))

def test_supporting_symbolic_multiplication():
    zero = SymbolicMultiplication("0")

    @supporting_symbolic_multiplication
    def my_linear_operator(A, x):
        return np.linalg.solve(A, x)

    b = np.random.rand(10) * zero
    A = np.random.rand(10, 10)
    c = my_linear_operator(A, b)
    assert (c/zero).shape == (10,)

