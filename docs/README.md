# QubitSim Developer Documentation

> **QubitSim**: An educational quantum circuit simulator with explicit, step-by-step quantum state evolution visualization.

**Last Updated**: February 11, 2026  
**Project Status**: Active Development  
**Primary Maintainer**: Developer Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Module Documentation](#module-documentation)
4. [Implementation Status](#implementation-status)
5. [Development Roadmap](#development-roadmap)
6. [Setup and Development](#setup-and-development)
7. [Testing](#testing)
8. [Design Decisions](#design-decisions)

---

## Project Overview

### Purpose

QubitSim is an **educational tool** designed to make quantum circuit execution transparent and observable. Unlike production quantum computing frameworks (Qiskit, Cirq), QubitSim prioritizes pedagogical clarity over performance.

**Key differentiator**: Students can observe *how* a quantum circuit transforms quantum state, not just the final output.

### Target Audience

- Undergraduate Computer Science students
- Undergraduate Physics students (non-majors)
- Assumes familiarity with:
  - Linear algebra (vectors, matrices, tensor products)
  - Basic quantum mechanics (superposition, entanglement, Dirac notation, measurement postulate)
  - No prior experience with quantum SDKs required

### Project Goals

1. **Transparency**: Explicit visualization of quantum state at each circuit step
2. **Correctness**: Faithful implementation of quantum mechanics mathematics
3. **Usability**: Intuitive drag-and-drop interface for circuit construction
4. **Educational Focus**: 4-16 qubit limit (enough to demonstrate entanglement, manageable for visualization)

### What QubitSim is NOT

- ❌ Not a production quantum compiler
- ❌ Not optimized for performance or scalability
- ❌ Not a replacement for Qiskit/Cirq/etc.
- ❌ No noise modeling, decoherence, or hardware effects
- ❌ No quantum error correction
- ❌ Not a scientific research tool

**Focus**: Mathematical quantum computing model → quantum circuit translation for learning.

---

## Architecture

QubitSim follows a layered architecture separating concerns:

```
┌─────────────────────────────────────────────────────┐
│                   UI Layer (PyQt6)                  │
│  MainWindow, CircuitCanvas, GatePalette, Controls   │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                   AppState (State)                  │
│     Centralized application state management        │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│           Circuit Execution Layer (qcircuit/)       │
│   CircuitInterpreter, Backend, GateOp dispatch      │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│        Quantum Simulation Backend (temporary)       │
│         Currently: Qiskit (qcircuit/backend.py)     │
│         Future: Custom (core/)                      │
└─────────────────────────────────────────────────────┘
```

### Directory Structure

```
QubitSim/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/                   # Custom quantum backend (IN PROGRESS)
│   │   ├── system.py           # Quantum state representation
│   │   ├── operator.py         # Linear operators (base class)
│   │   ├── gate.py             # Gate definitions and controlled gates
│   │   └── gates.py            # Pauli, Hadamard, rotation gates
│   ├── qcircuit/               # Circuit execution layer
│   │   ├── backend.py          # Qiskit backend (temporary)
│   │   ├── interpreter.py      # Converts circuit grid → Qiskit circuit
│   │   └── objects.py          # GateOp dataclass, gate dispatch
│   └── ui/                     # User interface (PyQt6)
│       ├── main_window.py      # Main application window
│       ├── app_state.py        # Global state management
│       ├── circuit_canvas.py   # Interactive circuit builder
│       ├── gate_palette.py     # Draggable gate buttons
│       ├── control_panel.py    # Execution controls
│       └── state_display.py    # Quantum state visualization
├── docs/
│   ├── README.md               # This file (developer docs)
│   ├── DOCS.md                 # Project definition and scope
│   └── PAPER.md                # Academic paper structure (DO NOT MODIFY)
├── examples/
│   └── example_circuit.py      # Programmatic circuit example
├── tests/
│   ├── test_backend.py         # Backend unit tests
│   ├── test_integration.py     # Integration tests
│   ├── test_ui_smoke.py        # UI smoke tests
│   └── test_ui_updates.py      # UI update tests
├── requirements.txt            # Python dependencies
└── IMPLEMENTATION.md           # Implementation notes (Qiskit integration)
```

---

## Module Documentation

### `core/` - Custom Quantum Backend (Planned)

**Status**: Partial implementation, not yet integrated.

The `core/` module will be QubitSim's native quantum simulation backend, emphasizing **correctness and mathematical transparency** over optimization.

#### `core/system.py`
```python
class System:
    """Represents a quantum system state vector."""
```

- Stores quantum state as a column vector: `state: np.ndarray` (shape: `(2^n, 1)`)
- Initialized to `|0...0⟩` state
- Supports matrix multiplication via `__matmul__` for gate application

#### `core/operator.py`
```python
class Operator:
    """Base class for linear operators."""
```

- Validates unitarity: `U @ U† = I`
- Validates shape: Must be square and `2^n × 2^n`

#### `core/gate.py`
```python
class Gate(Operator):
    """Single-qubit and multi-qubit gates."""
    
class RotationGate(Gate):
    """Parametric rotation gates (RX, RY, RZ)."""
    
class ControlledGate(Operator):
    """Controlled-U gates with multiple controls."""
```

- `Gate.__generate_gate()`: Builds full `2^n × 2^n` gate via tensor products
- `ControlledGate.__generate_gate()`: Constructs controlled operations from computational basis

#### `core/gates.py`

Defines standard gate instances:
- Pauli: `X`, `Y`, `Z`
- Hadamard: `H`
- Phase: `S`, `T`
- Rotations: `Rx(θ)`, `Ry(θ)`, `Rz(θ)`

**Roadmap**:
1. Complete `core/` implementation (correctness first)
2. Validate against Qiskit results
3. Replace `qcircuit/backend.py` with native backend
4. Optimize with C++ backend (future)

---

### `qcircuit/` - Circuit Execution Layer

#### `qcircuit/objects.py`

**`GateOp` dataclass**: Unified representation of gate operations.

```python
@dataclass
class GateOp:
    name: str                      # "H", "X", "RX", "CNOT", "SWAP"
    targets: list[int]             # Target qubit indices
    controls: list[int] = None     # Control qubit indices
    anti_controls: list[int] = None
    params: dict[str, float] = None  # e.g., {"theta": 1.5708}
```

**`GATE_DISPATCH`**: Maps gate names to Qiskit application functions.

Supported gates:
- Single-qubit: `H`, `X`, `Y`, `Z`
- Rotation: `RX`, `RY`, `RZ` (with `theta` parameter)
- Controlled: `C` (control), `AC` (anti-control)
- SWAP: `SWAP` (two-target)

#### `qcircuit/interpreter.py`

**`CircuitInterpreter`**: Converts UI circuit grid → Qiskit `QuantumCircuit`.

- `build_circuit(steps)`: Builds complete circuit
- `build_partial_circuit(steps, up_to_step)`: Builds circuit up to specific step (for stepping)
- `_apply_step(step)`: Applies all gates in a single time step

**Circuit representation**: 
```python
steps[time_step][qubit] -> GateOp | None
```

#### `qcircuit/backend.py`

**`QiskitBackend`**: Temporary backend using Qiskit for quantum simulation.

```python
class QiskitBackend:
    def execute(steps, up_to_step) -> dict:
        """
        Returns:
            {
                'statevector': Qiskit Statevector object,
                'probabilities': dict {basis_state: probability},
                'system': core.System object (for compatibility)
            }
        """
```

- Uses `Statevector.from_instruction()` for state evolution
- Converts Qiskit results → `core.System` format for UI compatibility

**Note**: This is a temporary implementation. Will be replaced by `core/` backend.

---

### `ui/` - User Interface Layer

Built with **PyQt6**. All UI components are reactive to `AppState` signals.

#### `ui/app_state.py`

**Central state management** following signal/slot pattern.

```python
class AppState(QObject):
    # Signals
    circuit_changed = pyqtSignal()   # Circuit structure modified
    state_changed = pyqtSignal()     # Execution state changed
    system_changed = pyqtSignal()    # Quantum state updated
    selection_changed = pyqtSignal() # UI selection changed
    
    # State
    steps: list[list[GateOp | None]]  # Circuit grid
    current_step: int                  # Execution position
    system: System                     # Quantum state
    backend: QiskitBackend             # Simulation backend
```

**Key methods**:
- `add_gate(step, gate_op)`: Add gate to circuit
- `remove_gate(step, qubit)`: Remove gate
- `step()`: Execute one time step
- `run_all()`: Execute entire circuit
- `run_to(target_step)`: Execute to specific step
- `reset()`: Reset to initial state
- `execute_circuit_to_current_step()`: Backend execution + state update

#### `ui/main_window.py`

Main application window. Composes all UI components:
- Left: `GatePalette` (draggable gates)
- Center: `CircuitCanvas` (circuit builder)
- Right: `StateDisplay` (state visualization)
- Bottom: `ControlPanel` (execution controls)

#### `ui/circuit_canvas.py`

Interactive canvas for circuit construction.

- Grid-based layout: rows = qubits, columns = time steps
- Drag-and-drop from palette
- Right-click to delete gates
- Visual indicators for current execution step

**Drawing pipeline**:
1. Grid lines (dashed)
2. Qubit wires (horizontal lines)
3. Qubit labels (`q0`, `q1`, ...)
4. Time step labels
5. Gates (boxes with labels)
6. Current step indicator (vertical line)

#### `ui/gate_palette.py`

Displays available quantum gates organized in tabs:
- **Single-Qubit**: H, X, Y, Z, S, T
- **Rotations**: RX, RY, RZ (with angle slider)
- **Multi-Qubit**: Control, Anti-Control, SWAP

`GateButton`: Draggable QPushButton with custom MIME data.

#### `ui/control_panel.py`

Execution control interface:
- Qubit count spinner (1-16)
- Target step selector
- **Step**: Execute next step
- **Run To**: Execute to target step
- **Run All**: Execute entire circuit
- **Reset**: Reset to `|0...0⟩`

#### `ui/state_display.py`

Displays quantum state in three tabs:

1. **Amplitudes**: Complex amplitudes for each basis state
   ```
   |000⟩: 0.7071 + 0.0000i
   |111⟩: 0.7071 + 0.0000i
   ```

2. **Probabilities**: Measurement probabilities
   ```
   |000⟩: 50.00%
   |111⟩: 50.00%
   ```

3. **Details**: System metadata (num_qubits, shape, norm)

**Note**: Density matrix view is **planned** but not yet implemented.

---

## Implementation Status

### ✅ Completed

- [x] PyQt6 UI framework
- [x] Circuit canvas with drag-and-drop
- [x] Gate palette (single, rotation, multi-qubit)
- [x] Qiskit backend integration
- [x] Circuit interpreter (grid → Qiskit)
- [x] Step-by-step execution
- [x] State visualization (state vector, probabilities)
- [x] AppState signal/slot architecture
- [x] Control panel (step, run, reset)
- [x] Backend unit tests (5/5 passing)
- [x] Integration tests (3/3 passing)
- [x] UI smoke tests

### 🚧 In Progress

- [ ] Custom `core/` backend (partial implementation)
- [ ] Controlled gate visualization improvements
- [ ] SWAP gate rendering

### 📋 Planned Features

#### Short-term
- [ ] Density matrix view in state display
- [ ] Complete `core/` backend implementation
- [ ] Validation: `core/` vs Qiskit results
- [ ] Replace Qiskit backend with `core/`
- [ ] Export/import circuit JSON
- [ ] Circuit examples library

#### Medium-term
- [ ] Circuit simulation history (timeline slider)
- [ ] Measurement operation support
- [ ] Custom gate definitions
- [ ] Multi-qubit gate visualization (CNOT lines)
- [ ] Bloch sphere per-qubit view (optional)
- [ ] Circuit optimization suggestions

#### Long-term
- [ ] C++ backend for performance
- [ ] Performance benchmarks vs Qiskit
- [ ] Quantum algorithm examples (Deutsch, Grover, etc.)
- [ ] Interactive tutorials
- [ ] State vector vs density matrix comparison view
- [ ] Circuit transpilation demonstration

---

## Development Roadmap

### Phase 1: Core Backend (Current)
**Goal**: Replace Qiskit with native implementation.

1. Complete `core/gate.py` controlled gate implementation
2. Add comprehensive unit tests for `core/`
3. Validate against known quantum states (Bell, GHZ, W)
4. Integrate with `qcircuit/interpreter.py`
5. Remove Qiskit dependency

### Phase 2: Feature Completion
**Goal**: Essential educational features.

1. Density matrix representation
2. Measurement operations
3. Circuit save/load
4. Example circuits library
5. Improved multi-qubit gate visualization

### Phase 3: Performance & Optimization
**Goal**: Scale to 16 qubits smoothly.

1. Profile Python backend performance
2. Implement C++ backend with Python bindings
3. Benchmark: Python vs C++ vs Qiskit
4. Optimize UI rendering for large circuits

### Phase 4: Educational Content
**Goal**: Make self-learnable.

1. Interactive tutorials
2. Quantum algorithm examples
3. Documentation for end-users
4. Video demonstrations
5. Public release preparation

---

## Setup and Development

### Prerequisites

- Python 3.10+
- pip or conda

### Installation

```bash
# Clone repository
cd /home/andresgomez31/git/QubitSim

# Install dependencies
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

```bash
cd src
python main.py
```

Or from workspace root:
```bash
python /home/andresgomez31/git/QubitSim/src/main.py
```

### Development Workflow

1. **Make changes** in appropriate module (`core/`, `qcircuit/`, `ui/`)
2. **Run tests** to validate
3. **Test UI manually** for visual changes
4. **Update documentation** if architecture changes

**Best Practice**: Keep Qiskit backend functional while developing `core/` for comparison.

---

## Testing

### Backend Tests

Tests Qiskit integration and quantum mechanics correctness.

```bash
PYTHONPATH=src python test_backend.py
```

**Tests**:
- `test_hadamard()`: H gate → `|+⟩` state
- `test_pauli_x()`: X gate → `|1⟩` state  
- `test_rotation()`: RX(π/2)
- `test_two_qubit()`: Two-qubit circuits
- `test_partial_execution()`: Step-by-step execution

**Status**: 5/5 passing ✅

### Integration Tests

Tests AppState ↔ Backend integration.

```bash
PYTHONPATH=src python test_integration.py
```

**Tests**:
- `test_appstate_integration()`: Circuit execution through AppState
- `test_qubit_count_change()`: Backend reinitialization
- `test_measurement_probabilities()`: Probability calculation

**Status**: 3/3 passing ✅

### UI Tests

Smoke tests for UI components.

```bash
python test_ui_smoke.py
python test_ui_updates.py
```

**Tests**: Widget creation, signal emission, rendering.

**Status**: All passing ✅

### Adding New Tests

When adding features:
1. Add unit tests in `test_backend.py` for quantum mechanics
2. Add integration tests in `test_integration.py` for state management
3. Add UI tests if new widgets introduced

**Test naming convention**: `test_<feature_name>()`

---

## Design Decisions

### Why Temporary Qiskit Backend?

**Rationale**: 
- Qiskit is battle-tested and correct
- Allows UI development to proceed while `core/` is built
- Provides validation reference for custom backend
- Easy to swap out via `qcircuit/backend.py` interface

**Tradeoffs**:
- Extra dependency
- Black-box simulation (defeats transparency goal)
- Will be removed in Phase 1

### Why Grid-Based Circuit Representation?

**Rationale**:
- Intuitive: matches standard quantum circuit diagrams
- Simple indexing: `steps[time][qubit]`
- Easy to visualize execution position
- Natural for drag-and-drop UI

**Tradeoffs**:
- Sparse for large circuits (many `None` cells)
- Fixed grid size (must preallocate steps)

**Future**: Consider linked list or sparse matrix representation.

### Why State Vector Over Density Matrix?

**Rationale**:
- Simpler for pure states (most educational examples)
- Less memory: `O(2^n)` vs `O(2^2n)`
- Easier to explain to students
- Density matrix can be derived: `ρ = |ψ⟩⟨ψ|`

**Tradeoffs**:
- Cannot represent mixed states (not needed for this scope)
- Measurement must be handled separately

**Future**: Add density matrix view as derived representation.

### Why PyQt6 Over Tkinter/Web?

**Rationale**:
- Professional appearance
- Rich widget library
- Good performance for interactive graphics
- Signal/slot architecture fits reactive patterns
- Cross-platform

**Tradeoffs**:
- Larger dependency
- Steeper learning curve than Tkinter
- Desktop-only (no web deployment)

**Alternative considered**: Web (React + Three.js) — rejected due to Python backend integration complexity.

### Why 4-16 Qubit Limit?

**Rationale**:
- 4 qubits: Enough to show multi-qubit entanglement
- 16 qubits: UI remains readable, memory manageable (~64K statevector)
- Educational focus: Not production-scale circuits

**Tradeoffs**:
- Cannot demonstrate some algorithms (Shor's requires 20+ qubits)
- Not realistic for "real" quantum computing

**Note**: This is intentional. QubitSim is a learning tool, not a research simulator.

---

## Contributing

### Code Style

- Follow PEP 8
- Docstrings for all public methods
- Type hints where beneficial
- Comments for complex quantum mechanics logic

### Commit Messages

Format: `<module>: <brief description>`

Examples:
- `core: add controlled-X gate implementation`
- `ui: fix circuit canvas drag-and-drop bug`
- `docs: update architecture diagram`
- `tests: add Bell state validation`

### Pull Request Process

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with tests
3. Run full test suite
4. Update documentation
5. Submit PR with description

---

## References

### Quantum Computing
- Nielsen & Chuang: *Quantum Computation and Quantum Information*
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computation Lecture Notes (Umesh Vazirani)](https://www.scottaaronson.com/qclec/)

### PyQt6
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt6 Documentation](https://doc.qt.io/qt-6/)

### Project-Specific
- [PAPER.md](PAPER.md) — Academic paper structure (for publication)
- [DOCS.md](DOCS.md) — Project scope and requirements
- [IMPLEMENTATION.md](../IMPLEMENTATION.md) — Qiskit integration notes

---

## Contact & Support

For questions about QubitSim development, please refer to project documentation or reach out to the development team.

**Status**: Active Development (Feb 2026)

