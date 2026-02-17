from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
from qcircuit.interpreter import CircuitInterpreter
from core.system import System

class QiskitBackend:
    """
    Temporary Qiskit backend for circuit execution
    """
    def __init__(self, num_qubits: int, rng: np.random.Generator | None = None):
        self.num_qubits = num_qubits
        self.interpreter = CircuitInterpreter(num_qubits)
        self.rng = rng or np.random.default_rng()

    def execute(self, steps: list[list], up_to_step: int = None) -> dict:
        """
        Execute circuit and return quantum state information
        Returns:
            {
                'statevector': Statevector object,
                'probabilities': dict {basis_state: probability},
                'system': System object (for compatibility),
                'measurements': list of measurement events
            }
        """
        steps_to_run = steps if up_to_step is None else steps[:up_to_step]

        statevector = Statevector.from_int(0, 2**self.num_qubits)
        measurements: list[dict[str, object]] = []

        for step_index, step in enumerate(steps_to_run):
            qc = self.interpreter.build_step_circuit(step)
            if qc.data:
                statevector = statevector.evolve(qc)

            meas_qubits = self._extract_measurement_qubits(step)
            if meas_qubits:
                outcome, statevector = self._measure_statevector(statevector, meas_qubits)
                measurements.append({
                    "step": step_index,
                    "qubits": meas_qubits,
                    "outcome": outcome
                })

        probs = self.get_measurement_probabilities(statevector)
        system = self.convert_to_system(statevector)
        return {
            'statevector': statevector,
            'probabilities': probs,
            'system': system,
            'measurements': measurements
        }

    def get_statevector(self, qc: QuantumCircuit) -> Statevector:
        return Statevector.from_instruction(qc)

    def get_measurement_probabilities(self, statevector: Statevector) -> dict:
        probs = statevector.probabilities_dict()
        return probs

    def convert_to_system(self, statevector: Statevector) -> System:
        # Convert Qiskit Statevector to System object
        arr = statevector.data.reshape((-1, 1))
        system = System(self.num_qubits)
        system.state = arr
        return system

    def _extract_measurement_qubits(self, step: list) -> list[int]:
        qubits = []
        for op in step:
            if op is None:
                continue
            if op.name == "M":
                qubits.extend(op.targets)
        return sorted(set(qubits))

    def _measure_statevector(
        self,
        statevector: Statevector,
        qubits: list[int]
    ) -> tuple[str, Statevector]:
        num_qubits = self.num_qubits
        state = statevector.data.copy()

        outcome_count = 2**len(qubits)
        probs = np.zeros(outcome_count)

        for basis_index, amp in enumerate(state):
            p = abs(amp) ** 2
            if p == 0:
                continue
            outcome = 0
            for i, q in enumerate(qubits):
                bit = (basis_index >> q) & 1
                outcome |= bit << i
            probs[outcome] += p

        sample = self.rng.random()
        cumulative = 0.0
        chosen = outcome_count - 1
        for outcome, p in enumerate(probs):
            cumulative += p
            if sample <= cumulative + 1e-12:
                chosen = outcome
                break

        for basis_index in range(len(state)):
            if not self._matches_outcome(basis_index, qubits, chosen):
                state[basis_index] = 0

        norm = np.linalg.norm(state)
        if norm > 0:
            state /= norm

        outcome_bits = "".join(
            "1" if (chosen >> i) & 1 else "0" for i in range(len(qubits))
        )
        return outcome_bits, Statevector(state)

    @staticmethod
    def _matches_outcome(basis_index: int, qubits: list[int], outcome: int) -> bool:
        for i, q in enumerate(qubits):
            if ((basis_index >> q) & 1) != ((outcome >> i) & 1):
                return False
        return True
