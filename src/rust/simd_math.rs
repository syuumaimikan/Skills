//! High-Throughput SIMD-friendly Math Operations

/// Computes dot product of two f32 slices using chunked loop unrolling
pub fn dot_product(a: &[f32], b: &[f32]) -> f32 {
    assert_eq!(a.len(), b.len(), "Vectors must have equal length");

    let chunks_a = a.chunks_exact(8);
    let chunks_b = b.chunks_exact(8);
    let remainder_a = chunks_a.remainder();
    let remainder_b = chunks_b.remainder();

    let mut sum0 = 0.0f32;
    let mut sum1 = 0.0f32;
    let mut sum2 = 0.0f32;
    let mut sum3 = 0.0f32;
    let mut sum4 = 0.0f32;
    let mut sum5 = 0.0f32;
    let mut sum6 = 0.0f32;
    let mut sum7 = 0.0f32;

    for (ca, cb) in chunks_a.zip(chunks_b) {
        sum0 += ca[0] * cb[0];
        sum1 += ca[1] * cb[1];
        sum2 += ca[2] * cb[2];
        sum3 += ca[3] * cb[3];
        sum4 += ca[4] * cb[4];
        sum5 += ca[5] * cb[5];
        sum6 += ca[6] * cb[6];
        sum7 += ca[7] * cb[7];
    }

    let mut total = sum0 + sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7;
    for (&x, &y) in remainder_a.iter().zip(remainder_b.iter()) {
        total += x * y;
    }

    total
}

/// Cache-oblivious Matrix Multiplication C = A * B
pub fn matrix_multiply_2d(n: usize, a: &[f32], b: &[f32], c: &mut [f32]) {
    assert_eq!(a.len(), n * n);
    assert_eq!(b.len(), n * n);
    assert_eq!(c.len(), n * n);

    c.fill(0.0);

    // Cache-friendly IkJ loop ordering
    for i in 0..n {
        for k in 0..n {
            let r = a[i * n + k];
            for j in 0..n {
                c[i * n + j] += r * b[k * n + j];
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dot_product() {
        let v1 = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0];
        let v2 = vec![2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
        // 2 + 6 + 12 + 20 + 30 + 42 + 56 + 72 + 90 = 330
        let result = dot_product(&v1, &v2);
        assert!((result - 330.0).abs() < 1e-5);
    }

    #[test]
    fn test_matrix_multiply() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let b = vec![2.0, 0.0, 1.0, 2.0];
        let mut c = vec![0.0; 4];
        matrix_multiply_2d(2, &a, &b, &mut c);
        // [1*2 + 2*1, 1*0 + 2*2] = [4, 4]
        // [3*2 + 4*1, 3*0 + 4*2] = [10, 8]
        assert_eq!(c, vec![4.0, 4.0, 10.0, 8.0]);
    }
}
