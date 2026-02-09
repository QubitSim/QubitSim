from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qcircuit.interpreter import CircuitInterpreter
from core.system import System

class QiskitBackend:
    """
    Temporary Qiskit backend for circuit execution
    """
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.interpreter = CircuitInterpreter(num_qubits)

    def execute(self, steps: list[list], up_to_step: int = None) -> dict:
        """
        Execute circuit and return quantum state information
        Returns:
            {
                'statevector': Statevector object,
                'probabilities': dict {basis_state: probability},
                'system': System object (for compatibility)
            }
        """
        if up_to_step is None:
            qc = self.interpreter.build_circuit(steps)
        else:
            qc = self.interpreter.build_partial_circuit(steps, up_to_step)
        sv = self.get_statevector(qc)
        probs = self.get_measurement_probabilities(sv)
        system = self.convert_to_system(sv)
        return {
            'statevector': sv,
            'probabilities': probs,
            'system': system
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
