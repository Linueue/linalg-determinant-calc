import numpy as np
import argparse

# Give gooning shits

# Calculates the determinant
# Requires the mat to be a square matrix
def determinant(mat: np.array) -> float:
    shape = mat.shape
    if shape[0] != shape[1]:
        raise RuntimeError(f"Array has shape {shape}, but determinant only supports square matrices, however, you can multiply the matrix to its transpose to get its determinant.")

    EPSILON = 1e-12
    newmat = mat.copy().astype(np.float64)
    p = 1

    column_view = newmat.T

    # reduce to REF
    for i in range(shape[0]):
        column = column_view[i]
        row = newmat[i]

        # E1
        # We do np.abs so, we may be able to pick negatives
        swap_idx = np.argmax(np.abs(column[i:])) + i

        if i != swap_idx:
            newmat[[swap_idx, i]] = newmat[[i, swap_idx]]
            p *= -1

        # E2
        # We are eliminating E2 as we don't need a row to be normalized,
        # that is, we don't need it our pivot to be 1
        value = row[i]

        # We check if the current pivot is near 0
        # If it is, that means it's linearly dependent
        if np.abs(value) <= EPSILON:
            return 0.0

        # This is the E2
        # newmat[i] /= value
        # p *= value

        # E3
        for j in range(i + 1, shape[0]):
            scalar = -newmat[j][i] / value
            newmat[j] += row * scalar

    return p * np.diag(newmat).prod()

def determinant_cofactor(mat: np.array) -> float:
    def get_submat(_mat: np.array, row: int, col: int) -> np.array:
        n, _ = _mat.shape
        rows = np.arange(n) != row
        cols = np.arange(n) != col
        submat = _mat[rows][:, cols]
        return submat

    EPSILON = 1e-12

    def _det(_mat: np.array) -> float:
        n, _ = _mat.shape

        if n == 2:
            a, b = _mat[0]
            c, d = _mat[1]
            return a * d - b * c

        d = 0

        for i in range(n):
            submat = get_submat(_mat, 0, i)
            # -1^(i + j)
            p = 1 if i % 2 == 0 else -1
            c = _mat[0][i]

            if c <= EPSILON:
                continue

            d += p * c * _det(submat)

        return d

    return _det(mat)

def test_random(iters: int = 150):
    print(" -- Random -- ")
    for i in range(iters):
        mat = np.random.randint(0, 10, size=(5, 5))
        det_A = determinant_cofactor(mat)
        det_B = np.linalg.det(mat)
        issame = np.isclose(det_A, det_B, rtol=1e-8, atol=1e-10)
        print(f"{det_A:10.2f} == {det_A:10.2f} | {issame}")

def test_pivot(iters: int = 150):
    print(" -- Pivot -- ")
    for i in range(iters):
        mat = np.eye(5, 5) * np.random.randint(1, 10)
        det_A = determinant_cofactor(mat)
        det_B = np.linalg.det(mat)
        issame = np.isclose(det_A, det_B, rtol=1e-8, atol=1e-10)
        print(f"{det_A:10.2f} == {det_A:10.2f} | {issame}")

def test_linearly_independent():
    print(" -- Linear Independence -- ")
    mat = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [0, 0, 0],
    ])
    print(mat)
    det_A = determinant_cofactor(mat)
    det_B = np.linalg.det(mat)
    issame = np.isclose(det_A, det_B, rtol=1e-8, atol=1e-10)
    print(f"{det_A:10.2f} == {det_A:10.2f} | {issame}")

def main():
    parser = argparse.ArgumentParser(description="Determinant calculator.")
    parser.add_argument("--test", action="store_true", help="Runs a test suite.")
    args = parser.parse_args()

    if args.test:
        test_random()
        test_pivot()
        test_linearly_independent()
        return

    test = np.random.randint(low=0, high=10, size=(5, 5))

    a = determinant(test)
    b = np.linalg.det(test)
    print(f" -- A --\n{a}\n -- B --\n{b}")

if __name__ == "__main__":
    main()
