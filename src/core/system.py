import numpy as np

class System:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.state = np.zeros((2**num_qubits, 1), dtype=complex)
        self.state[0][0] = 1.0  # Initialize to |0...0> state

    def __call__(self, *args, **kwds):
        return self.state
    
    def __eq__(self, value):
        return np.array_equal(self.state, value)
    
    def __str__(self):
        return str(self.state)
    
    def __repr__(self):
        return f"System(num_qubits={self.num_qubits}, state={self.state})"
    
    def __len__(self):
        return len(self.state)
    
    def __matmul__(self, other: np.ndarray) -> 'System':
        new_state = np.dot(other, self.state)
        new_system = System(self.num_qubits)
        new_system.state = new_state
        return new_system
    
    def __rmatmul__(self, other: np.ndarray) -> 'System':
        new_state = np.dot(other, self.state)
        new_system = System(self.num_qubits)
        new_system.state = new_state
        return new_system
    
    

    
