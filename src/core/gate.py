import numpy as np
from core.operator import Operator
from core.system import System

class Gate(Operator):
    def __init__ (self, op: np.ndarray, name: str):
        super().__init__(op, name)
        self._check_unitary()
        self._check_shape()

    def __generate_gate (self, n: int, target: int = None) -> np.ndarray:
        """
        Generate a gate for n qubits.
        """
        gate = np.eye(1)
        for i in range(n):
            if i == target:
                gate = np.kron(gate, self.op)
            else:
                gate = np.kron(gate, np.eye(2))
        return gate

        
    def _apply(self, s: System, target: int = None) -> None:
        """
        Apply the operator to the system.

        If the gate is a single-target gate, use 'target'.
        If the gate is a multi-target gate, use 'targets'.
        """
        
        s = s @ self.__generate_gate(s.num_qubits, target=target)

class RotationGate(Gate):
    def __init__ (self, axis: str, theta: float):
        if axis == "X":
            op = np.array([
                [np.cos(theta/2), -1j * np.sin(theta/2)],
                [-1j * np.sin(theta/2), np.cos(theta/2)]
            ])
            name = f"R_X({theta})"
        elif axis == "Y":
            op = np.array([
                [np.cos(theta/2), -np.sin(theta/2)],
                [np.sin(theta/2), np.cos(theta/2)]
            ])
            name = f"R_Y({theta})"
        elif axis == "Z":
            op = np.array([
                [np.exp(-1j * theta / 2), 0],
                [0, np.exp(1j * theta / 2)]
            ])
            name = f"R_Z({theta})"
        else:
            raise ValueError(f"Invalid rotation axis: {axis}")

        super().__init__(op, name)

class ControlledGate(Operator):
    def __init__(
        self,
        base_gate: Gate,
        controls: dict[int, int],  # index -> 0 or 1
        targets: list[int]
    ):
        self.base_gate = base_gate
        self.controls = controls
        self.targets = targets

    # I dont understand a fuck lol
    
    def __generate_gate(
        n: int,
        U: np.ndarray,
        controls: dict[int, int],  # qubit_index -> 0 or 1
        targets: list[int]
    ) -> np.ndarray:

        dim = 2**n
        result = np.zeros((dim, dim), dtype=complex)

        # Iterate computational basis
        for i in range(dim):
            bits = [(i >> (n - 1 - k)) & 1 for k in range(n)]

            # Check control condition
            enabled = all(bits[q] == val for q, val in controls.items())

            if not enabled:
                result[i, i] = 1
                continue

            # Extract target subspace index
            tgt_bits = [bits[q] for q in targets]
            tgt_index = sum(b << (len(targets)-1-j) for j, b in enumerate(tgt_bits))

            for j in range(2**len(targets)):
                new_bits = bits.copy()
                for k, q in enumerate(targets):
                    new_bits[q] = (j >> (len(targets)-1-k)) & 1

                new_index = sum(b << (n - 1 - k) for k, b in enumerate(new_bits))
                result[new_index, i] += U[j, tgt_index]

        return result
    
    def _apply(self, s: System) -> None:
        s = s @ self.__generate_gate(
            n = int(np.log2(len(s))),
            U = self.base_gate.op,
            controls = self.controls,
            targets = self.targets
        )

