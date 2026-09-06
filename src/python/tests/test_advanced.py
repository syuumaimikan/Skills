import unittest
import math
import cmath
from src.python.ml_primitives.attention import ScaledDotProductAttention
from src.python.algorithms.fast_fourier_transform import fft, ifft


class TestAdvancedModules(unittest.TestCase):
    def test_attention_mechanism(self):
        # 3 tokens, embedding dimension 4
        q = [[1.0, 0.0, 1.0, 0.0], [0.0, 2.0, 0.0, 1.0], [1.0, 1.0, 0.0, 0.0]]
        k = [[1.0, 0.0, 1.0, 0.0], [0.0, 2.0, 0.0, 1.0], [1.0, 1.0, 0.0, 0.0]]
        v = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]

        out, weights = ScaledDotProductAttention.forward(q, k, v)
        self.assertEqual(len(out), 3)
        self.assertEqual(len(out[0]), 2)
        # Weights should sum to 1 per row
        for row in weights:
            self.assertAlmostEqual(sum(row), 1.0, places=5)

    def test_fft_and_ifft(self):
        signal = [1.0 + 0j, 1.0 + 0j, 1.0 + 0j, 1.0 + 0j, 0.0 + 0j, 0.0 + 0j, 0.0 + 0j, 0.0 + 0j]
        transformed = fft(signal)
        self.assertEqual(len(transformed), 8)

        recovered = ifft(transformed)
        for original, rec in zip(signal, recovered):
            self.assertAlmostEqual(original.real, rec.real, places=5)
            self.assertAlmostEqual(original.imag, rec.imag, places=5)


if __name__ == "__main__":
    unittest.main()
