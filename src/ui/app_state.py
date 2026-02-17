from PyQt6.QtCore import QObject, pyqtSignal
from qcircuit.objects import GateOp
from qcircuit.backend import QiskitBackend


class AppState(QObject):
    """
    Global application state.

    Single source of truth for:
    - Circuit structure
    - Execution state
    - UI selection state
    - Quantum system outputs
    """

    # Structural changes
    circuit_changed = pyqtSignal()
    state_changed = pyqtSignal()
    system_changed = pyqtSignal()
    selection_changed = pyqtSignal()
    theme_changed = pyqtSignal(str)  # Emits theme name

    def __init__(self, num_qubits: int, num_steps: int):
        super().__init__()

        self.num_qubits = num_qubits
        self.num_steps = num_steps
        self.theme = "light"  # Default theme

        # steps[step][qubit] -> GateOp | None
        self.steps: list[list[GateOp | None]] = [
            [None for _ in range(num_qubits)]
            for _ in range(num_steps)
        ]

        self.current_step = 0

        # UI selection state
        # selected_gate may also be "C" or "A" (control markers)
        self.selected_gate: str | None = None
        self.selected_theta: float = 0.0

        # Quantum system outputs (produced elsewhere)
        self.statevector = None
        self.measurement_probs = None
        self.measurement_results = []
        self.qubit_views = None
        self.system = None
        
        # Backend for quantum simulation
        self.backend = QiskitBackend(num_qubits)
        self._initialize_system()

    def add_gate(self, step: int, gate_op: GateOp):
        if not (0 <= step < self.num_steps):
            raise IndexError("Invalid step")

        for qubit in gate_op.targets:
            if not (0 <= qubit < self.num_qubits):
                raise IndexError("Invalid qubit")

            self.steps[step][qubit] = gate_op

        self.circuit_changed.emit()

    def remove_gate(self, step: int, qubit: int):
        if not (0 <= step < self.num_steps):
            raise IndexError("Invalid step")
        if not (0 <= qubit < self.num_qubits):
            raise IndexError("Invalid qubit")

        gate = self.steps[step][qubit]
        if gate is None:
            return

        # If removing a control marker, also remove any gate that depends on it
        if gate.name in {"C", "AC"}:
            # Find and remove the gate that uses this control
            for q in range(self.num_qubits):
                if q != qubit:
                    other_gate = self.steps[step][q]
                    if other_gate:
                        if gate.name == "C" and other_gate.controls == [qubit]:
                            self.steps[step][q] = None
                        elif gate.name == "AC" and other_gate.anti_controls == [qubit]:
                            self.steps[step][q] = None
        
        # If removing a gate with control, also remove the control marker
        if gate.controls:
            for c_qubit in gate.controls:
                control_gate = self.steps[step][c_qubit]
                if control_gate and control_gate.name == "C":
                    self.steps[step][c_qubit] = None
        
        if gate.anti_controls:
            for ac_qubit in gate.anti_controls:
                control_gate = self.steps[step][ac_qubit]
                if control_gate and control_gate.name == "AC":
                    self.steps[step][ac_qubit] = None

        self.steps[step][qubit] = None
        self.circuit_changed.emit()

    def clear_circuit(self):
        self.steps = [
            [None for _ in range(self.num_qubits)]
            for _ in range(self.num_steps)
        ]
        self.current_step = 0
        self.circuit_changed.emit()
        self.state_changed.emit()

    def set_selected_gate(self, gate: str | None):
        self.selected_gate = gate
        if gate not in {"RX", "RY", "RZ"}:
            self.selected_theta = 0.0
        self.selection_changed.emit()

    def set_selected_theta(self, theta: float):
        self.selected_theta = theta
        self.selection_changed.emit()

    def set_theme(self, theme_name: str):
        """Change the application theme."""
        if theme_name in {"light", "dark"}:
            self.theme = theme_name
            self.theme_changed.emit(theme_name)

    def step(self):
        if self.current_step < self.num_steps:
            self.current_step += 1
            self.execute_circuit_to_current_step()
            self.state_changed.emit()

    def run_all(self):
        self.current_step = self.num_steps
        self.execute_circuit_to_current_step()
        self.state_changed.emit()

    def run_to(self, target_step: int):
        target_step = max(0, min(target_step, self.num_steps))
        self.current_step = target_step
        self.execute_circuit_to_current_step()
        self.state_changed.emit()

    def reset(self):
        self.current_step = 0
        self._initialize_system()
        self.state_changed.emit()

    def set_num_qubits(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.steps = [
            [None for _ in range(num_qubits)]
            for _ in range(self.num_steps)
        ]
        self.current_step = 0
        self.backend = QiskitBackend(num_qubits)
        self._initialize_system()
        self.circuit_changed.emit()
        self.state_changed.emit()

    def set_num_steps(self, num_steps: int):
        self.num_steps = num_steps
        self.steps = [
            [None for _ in range(self.num_qubits)]
            for _ in range(num_steps)
        ]
        self.current_step = 0
        self.circuit_changed.emit()
        self.state_changed.emit()

    def set_statevector(self, statevector):
        self.statevector = statevector
        self.system_changed.emit()

    def set_measurement_probs(self, probs):
        self.measurement_probs = probs
        self.system_changed.emit()

    def set_measurement_results(self, results):
        self.measurement_results = results
        self.system_changed.emit()

    def set_qubit_views(self, views):
        self.qubit_views = views
        self.system_changed.emit()
    
    def execute_circuit_to_current_step(self):
        """Execute circuit up to current_step and update quantum state"""
        try:
            if self.current_step == 0:
                # Reset to initial state
                self._initialize_system()
            else:
                result = self.backend.execute(self.steps, self.current_step)
                self.system = result['system']
                self.set_statevector(result['statevector'])
                self.set_measurement_probs(result['probabilities'])
                self.set_measurement_results(result.get('measurements', []))
        except Exception as e:
            print(f"Error executing circuit: {e}")
            self._initialize_system()
    
    def _initialize_system(self):
        """Initialize system to |0...0> state"""
        from core.system import System
        self.system = System(self.num_qubits)
        self.statevector = None
        self.measurement_probs = None
        self.measurement_results = []
        self.system_changed.emit()
