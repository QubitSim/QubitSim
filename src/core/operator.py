import numpy as np
from core.system import System

class Operator:
    def __init__ (self, op: np.ndarray, name: str):
        self.op = op
        self.name = name

    def __call__(self, *args, **kwds):
        return self.op
    
    def __eq__(self, value):
        return np.array_equal(self.op, value)
    
    def __str__(self):
        return str(self.op)

    def _check_unitary(self) -> None:
        """
        Check if the operator is unitary.

        An operator U is unitary if U * U† = I, where U† is the conjugate transpose of U
        and I is the identity matrix.
        """
        identity = np.eye(self.op.shape[0])
        product = np.dot(self.op, self.op.conj().T)

        if not np.allclose(product, identity):
            raise ValueError(f"Operator {self.name} is not unitary.")

    def _check_shape(self) -> None:
        """
        A gate must always be:
        - Unitary
        - Square
        - 2^n x 2^n for some positive integer n
        """
        if self.op.shape[0] != self.op.shape[1]:
            raise ValueError(f"Operator {self.name} is not square.")

        if self.op.shape[0] % 2 != 0 and self.op.shape[1] % 2 != 0: 
            raise ValueError(f"Operator {self.name} dimensions are not powers of 2.")
        
