"""
Cooley-Tukey Radix-2 Fast Fourier Transform (FFT) and Inverse FFT (IFFT)
Time Complexity: O(N log N)
"""

import cmath
import math
from typing import List


def fft(x: List[complex]) -> List[complex]:
    """
    Computes 1D Fast Fourier Transform using Cooley-Tukey decimation-in-time.
    Input length must be a power of 2.
    """
    n = len(x)
    if n <= 1:
        return x

    if (n & (n - 1)) != 0:
        # Pad to next power of 2
        next_power = 1 << (n - 1).bit_length()
        x = x + [0j] * (next_power - n)
        n = next_power

    even = fft(x[0::2])
    odd = fft(x[1::2])

    factor = [cmath.exp(-2j * math.pi * k / n) for k in range(n // 2)]
    
    first_half = [even[k] + factor[k] * odd[k] for k in range(n // 2)]
    second_half = [even[k] - factor[k] * odd[k] for k in range(n // 2)]
    
    return first_half + second_half


def ifft(x: List[complex]) -> List[complex]:
    """
    Computes Inverse Fast Fourier Transform.
    """
    n = len(x)
    # Conjugate input
    x_conj = [complex(c.real, -c.imag) for c in x]
    # Forward FFT
    transformed = fft(x_conj)
    # Conjugate and scale
    return [complex(c.real / n, -c.imag / n) for c in transformed]
