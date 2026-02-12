# QubitSim: Project Definition and Scope

**Last Updated**: February 11, 2026  
**Status**: Active Development  
**Version**: 0.2.0-alpha

---

## Project Type

Educational **quantum circuit simulator** with explicit, step-by-step quantum state visualization.

**Core Value Proposition**: Make quantum circuit execution transparent and observable for learning, not production use.

---

## Target Audience

### Primary Users
- **Undergraduate Computer Science students**
- **Undergraduate Physics students** (non-physics majors)

### Assumed Background
- Linear algebra familiarity (vectors, matrices, tensor products)
- Basic quantum mechanics concepts:
  - Superposition and entanglement
  - Quantum probability
  - Dirac notation
  - State vectors
  - Measurement postulate
- **No prior experience** with quantum SDKs (Qiskit, Cirq, etc.)

### Learning Goals
Students should be able to:
1. Construct quantum circuits visually
2. Observe state evolution at each gate application
3. Understand how entanglement emerges
4. See amplitude redistribution in real-time
5. Grasp the difference between quantum state and measurement outcomes

---

## Core Purpose

> **Enable students to explicitly observe how a quantum circuit transforms a quantum system over time, instead of treating the circuit as a black box.**

This is QubitSim's **unique value proposition** compared to production frameworks.

### Design Philosophy
- **Surface complexity intentionally** (don't hide math)
- **Transparency over optimization** (show tensor products explicitly)
- **Pedagogical correctness** (faithful to quantum mechanics)
- **Limited scope** (focus on core concepts, not scalability)

---

## Functional Scope

### 1. Circuit Construction

**Circuit Representation**: Standard quantum circuit diagram
- Horizontal wires = qubits
- Vertical columns = time steps
- Gates placed at discrete positions

**Supported Gates**:

| Category | Gates | Status |
|----------|-------|--------|
| Single-qubit Pauli | X, Y, Z | ✅ Implemented |
| Hadamard | H | ✅ Implemented |
| Phase gates | S, T | ✅ Implemented |
| Rotation gates | RX(θ), RY(θ), RZ(θ) | ✅ Implemented |
| Controlled gates | Control, Anti-control | ✅ Implemented |
| Multi-qubit | SWAP | ✅ Implemented |
| Measurement | Measurement operator | 📋 Planned |

**Qubit Limit**: 4-16 qubits
- **4 qubits**: Minimum to demonstrate multi-qubit entanglement
- **16 qubits**: Maximum for readable UI and manageable memory (~64K statevector)
- Rationale: Pedagogically optimal range without overwhelming visualization

**Interface**: Drag-and-drop gate placement from palette to circuit canvas

---

### 2. Execution Model

**Primary Mode**: Step-by-step execution
- Each time step is a discrete event
- User controls execution pace
- State updates after each step are visible

**Execution Controls**:
- **Step**: Execute next time step
- **Run To**: Execute to specific step
- **Run All**: Execute entire circuit at once
- **Reset**: Return to |0...0⟩ initial state

**Current Step Indicator**: Visual highlight showing execution position in circuit

---

### 3. State Representation

**Internal Canonical Form**: State vector (column vector of complex amplitudes)
- Stored as: `numpy.ndarray` with shape `(2^n, 1)`
- Initialized to: `|0...0⟩` (all qubits in ground state)
- Updated via: Matrix multiplication with gate operators

**Exposed Views**:

| View | Status | Description |
|------|--------|-------------|
| State vector | ✅ Implemented | Complex amplitudes for each basis state |
| Probabilities | ✅ Implemented | Measurement probabilities per basis state |
| System details | ✅ Implemented | Metadata (num_qubits, norm, shape) |
| Density matrix | 📋 Planned | Matrix representation (derivable from state vector) |

**Design Decision**: 
- Store state vector internally (simple, memory-efficient for pure states)
- Derive density matrix on demand: ρ = |ψ⟩⟨ψ|
- Rationale: Educational circuits are primarily pure states; mixed states not needed initially

---

### 4. Visualization

**State Display Panel** (Right side of UI):

**Tab 1 - Amplitudes**: ✅ Implemented
```
State Vector:

|000⟩: 0.7071 + 0.0000i
|111⟩: 0.7071 + 0.0000i
```
Shows complex amplitudes (real + imaginary parts) for non-zero basis states.

**Tab 2 - Probabilities**: ✅ Implemented
```
Measurement Probabilities:

|000⟩: 50.00%
|111⟩: 50.00%
```
Shows |amplitude|² for each basis state.

**Tab 3 - Details**: ✅ Implemented
- Number of qubits
- State vector dimension
- Norm (should be 1.0 for valid states)

**Tab 4 - Density Matrix**: 📋 Planned
- Matrix view (real/imaginary components)
- Option for magnitude/phase representation
- Comparison with state vector view for pedagogical purposes

**What is NOT visualized** (intentional exclusions):
- ❌ **Bloch sphere per qubit**: Tempting but distracts from multi-qubit circuits; only works for single qubits
- ❌ **Noise models**: Out of scope (learning tool, not hardware simulator)
- ❌ **Decoherence effects**: Not relevant for mathematical understanding
- ❌ **Error correction codes**: Advanced topic beyond core scope

---

## Implementation Status

### ✅ Currently Implemented

**Frontend (UI Layer)**:
- [x] PyQt6 application framework
- [x] Main window with splitter layout
- [x] Circuit canvas (drag-and-drop, grid-based)
- [x] Gate palette (single-qubit, rotation, multi-qubit gates)
- [x] Control panel (step, run, reset controls)
- [x] State display (amplitudes, probabilities, details)
- [x] Reactive state management (AppState signals)

**Backend (Quantum Simulation)**:
- [x] Qiskit-based temporary backend (`qcircuit/backend.py`)
- [x] Circuit interpreter (UI grid → Qiskit circuit)
- [x] GateOp dispatch system
- [x] Partial circuit execution (for stepping)
- [x] State extraction and probability calculation

**Testing**:
- [x] Backend unit tests (5/5 passing)
- [x] Integration tests (3/3 passing)
- [x] UI smoke tests (all passing)

### 🚧 In Progress

**Custom Backend** (`core/` module):
- [x] `System` class (quantum state vector)
- [x] `Operator` class (unitarity validation)
- [x] `Gate` class (single-qubit gates, tensor product generation)
- [x] `ControlledGate` class (controlled operations)
- [ ] Complete integration with `qcircuit/interpreter.py`
- [ ] Validation against Qiskit results
- [ ] Replace Qiskit backend

### 📋 Planned (Short-term)

- [ ] Density matrix view in UI
- [ ] Export/import circuit to JSON
- [ ] Circuit examples library (Bell state, GHZ, etc.)
- [ ] Measurement operator support
- [ ] Improved controlled gate visualization (connect lines)
- [ ] Complete custom backend integration

### 🔮 Planned (Long-term)

- [ ] C++ backend for performance optimization
- [ ] Performance benchmarks (Python vs C++ vs Qiskit)
- [ ] Quantum algorithm demonstrations (Deutsch-Jozsa, Grover)
- [ ] Interactive tutorials
- [ ] Circuit optimization suggestions
- [ ] End-user documentation and public release

---

## What This Project Is NOT

### Explicitly Out of Scope

- ❌ **Not a quantum compiler**: No optimization, transpilation, or gate decomposition
- ❌ **Not performance-oriented**: Correctness and transparency over speed
- ❌ **Not scalable**: Limited to 4-16 qubits by design
- ❌ **Not a Qiskit/Cirq replacement**: Production frameworks serve different purposes
- ❌ **No noise modeling**: No decoherence, gate errors, or readout errors
- ❌ **No hardware effects**: No T1/T2 times, crosstalk, or calibration data
- ❌ **No quantum error correction**: Advanced topic beyond scope
- ❌ **Not a scientific research tool**: Educational focus only

### Scope Boundaries Rationale

**Why no noise?**  
Noise models obscure the clean mathematical structure we want students to see. Understanding ideal quantum mechanics comes first.

**Why limited qubits?**  
Beyond 16 qubits, visualization becomes unreadable and defeats the transparency goal. This is a learning tool, not a simulation platform.

**Why no optimization?**  
Circuit optimization is an advanced topic. We want students to understand what gates *do*, not how to make them run faster.

---

## Backend Architecture

### Current Architecture (Temporary)

```
┌──────────────────────────────────────┐
│          UI Layer (PyQt6)            │
│     MainWindow, Canvas, Display      │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│     AppState (State Management)      │
│      Signals, Circuit Grid           │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│   Circuit Execution (qcircuit/)      │
│   Interpreter → GateOp → Dispatch    │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│   Temporary: QiskitBackend           │
│   (qcircuit/backend.py)              │
└──────────────────────────────────────┘
```

**Current Status**: Using Qiskit for quantum simulation while custom backend is in development.

**Rationale**:
- Qiskit provides correct, validated quantum simulation
- Allows frontend development to proceed independently
- Serves as reference for validating custom backend
- Easy to swap via backend abstraction layer

### Target Architecture (Planned)

```
┌──────────────────────────────────────┐
│          UI Layer (PyQt6)            │
│     MainWindow, Canvas, Display      │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│     AppState (State Management)      │
│      Signals, Circuit Grid           │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│   Circuit Execution (qcircuit/)      │
│   Interpreter → GateOp → Dispatch    │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│     Custom Backend (core/)           │
│   System → Gate → Operator           │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│  Linear Algebra Backend              │
│  Phase 1: NumPy                      │
│  Phase 2: C++ (pybind11)             │
└──────────────────────────────────────┘
```

### Backend Abstraction Design

**Goal**: Enable backend substitution without changing UI code.

**Interface** (`qcircuit/backend.py` or future `core/backend.py`):
```python
class Backend:
    def __init__(self, num_qubits: int)
    def execute(self, steps: list[list[GateOp]], up_to_step: int) -> dict
    def get_statevector(self) -> System
    def get_measurement_probabilities(self) -> dict
```

**This abstraction allows**:
- Python backend (Phase 1: current development)
- C++ backend (Phase 2: performance optimization)
- Zero UI redesign when swapping backends
- Side-by-side comparison for validation

### Custom Backend Design (core/)

**Philosophy**: Make tensor products and matrix operations explicit.

#### `core/system.py`
```python
class System:
    """Quantum state vector representation."""
    num_qubits: int
    state: np.ndarray  # Shape: (2^n, 1), complex amplitudes
```
- Represents |ψ⟩ as column vector
- Supports matrix multiplication: `system @ gate_matrix`
- Validates norm ≈ 1.0 (quantum state normalization)

#### `core/operator.py`
```python
class Operator:
    """Base class for quantum operators."""
    op: np.ndarray  # Unitary matrix
    name: str
    
    def _check_unitary(self) -> None  # Validates U @ U† = I
    def _check_shape(self) -> None     # Validates 2^n × 2^n
```

#### `core/gate.py`
```python
class Gate(Operator):
    """Single-qubit and multi-qubit gates."""
    def __generate_gate(self, n, target) -> np.ndarray
        # Generate full 2^n × 2^n matrix via tensor products:
        # I ⊗ I ⊗ ... ⊗ U ⊗ ... ⊗ I
    
class RotationGate(Gate):
    """RX(θ), RY(θ), RZ(θ)"""
    
class ControlledGate(Operator):
    """Controlled-U with multiple controls/targets."""
    def __generate_gate(self, n, U, controls, targets) -> np.ndarray
        # Build controlled gate from computational basis:
        # Apply U only when control qubits match conditions
```

**Key Implementation Detail**: 
The `__generate_gate()` methods make tensor product construction *explicit* and *traceable* for educational transparency.

#### `core/gates.py`
```python
# Predefined gate instances
X = Gate(...)  # Pauli-X
Y = Gate(...)  # Pauli-Y
Z = Gate(...)  # Pauli-Z
H = Gate(...)  # Hadamard
S = Gate(...)  # Phase gate
T = Gate(...)  # π/8 gate
Rx = lambda theta: RotationGate("X", theta)
Ry = lambda theta: RotationGate("Y", theta)
Rz = lambda theta: RotationGate("Z", theta)
```

### Linear Algebra Backend Progression

#### Phase 1: NumPy (Current)
- **Pros**: Easy to implement, well-documented, sufficient for 4-16 qubits
- **Cons**: Slower than specialized implementations
- **Status**: ✅ Implemented in `core/` (integration pending)

#### Phase 2: C++ Backend (Future)
- **Technology**: C++ with pybind11 bindings
- **Scope**: Replace `core/` linear algebra operations with optimized C++
- **Goals**:
  - Faster tensor product computation
  - Efficient matrix-vector multiplication
  - Better memory management for larger states
- **Non-goals**: 
  - Not GPU acceleration (overkill for educational scope)
  - Not distributed computing (not needed for 16 qubits)

**Benchmark targets** (16-qubit state):
- NumPy: Baseline
- C++: 5-10× faster matrix operations
- Still prioritize correctness over raw speed

---

## Academic Contribution

### Why This Is Valid Academic Work

Most quantum computing tools optimize for **usage**, not **understanding**.

**QubitSim's Unique Contribution**:
1. **Makes tensor products explicit** → Students see how multi-qubit gates are constructed
2. **Shows amplitude redistribution after each gate** → Superposition becomes observable, not abstract
3. **Makes measurement collapse visible** → Probabilistic nature of QM is experienced directly
4. **Forces confrontation with exponential state growth** → Students grasp why quantum computing is hard

This directly addresses a **well-documented learning barrier** in quantum computing education.

### What the Paper Will Argue

**Thesis**: Students struggle with quantum circuits because existing simulators hide state evolution; explicit step-by-step visualization improves conceptual understanding.

**Claims**:
- Black-box quantum simulators create pedagogical barriers
- Explicit state visualization reduces abstraction gaps
- Carefully limited scope (4-16 qubits) enables transparency without overwhelm
- Interactive step-by-step execution supports self-paced learning

**Evidence**:
- Correct reproduction of known quantum states (Bell, GHZ, W states)
- Step-wise state transformation visualization
- Entanglement emergence demonstration
- Measurement collapse observation

### What the Paper Will NOT Claim

- ❌ **Performance gains**: This is not faster than Qiskit
- ❌ **Hardware realism**: No noise, no error correction
- ❌ **Large-scale simulation**: Intentionally limited to 16 qubits
- ❌ **Novel algorithms**: Uses standard quantum gates
- ❌ **Research tool**: Educational focus only

**Positioning**: Pedagogical tool demonstrating transparency-first design for quantum circuit education.

---

## Development Phases

### Phase 1: Custom Backend Implementation (Current)
**Timeline**: 2-4 weeks  
**Status**: 🚧 In Progress

**Goals**:
- [x] Complete `core/gate.py` controlled gate implementation
- [ ] Add comprehensive unit tests for `core/` module
- [ ] Validate against known quantum states (Bell, GHZ, W)
- [ ] Integrate `core/` backend with `qcircuit/interpreter.py`
- [ ] Side-by-side validation: custom backend vs Qiskit
- [ ] Remove Qiskit dependency

**Success Criteria**:
- All backend tests pass with custom implementation
- State evolution matches Qiskit results to 1e-10 precision
- No regression in UI functionality

### Phase 2: Feature Completion
**Timeline**: 2-3 weeks  
**Status**: 📋 Planned

**Goals**:
- [ ] Implement density matrix view in UI
- [ ] Add measurement operator support
- [ ] Create circuit examples library (Bell, GHZ, Deutsch-Jozsa)
- [ ] Export/import circuit JSON format
- [ ] Improve multi-qubit gate visualization (CNOT lines)
- [ ] Add circuit validation (detect invalid operations)

**Success Criteria**:
- Students can visualize both state vector and density matrix
- Example circuits demonstrate key quantum concepts
- Circuits can be saved and shared

### Phase 3: Optimization & Performance
**Timeline**: 4-6 weeks  
**Status**: 🔮 Future

**Goals**:
- [ ] Profile Python backend performance bottlenecks
- [ ] Implement C++ backend with pybind11
- [ ] Benchmark: NumPy vs C++ vs Qiskit
- [ ] Optimize UI rendering for large circuits
- [ ] Add performance metrics display (optional dev mode)

**Success Criteria**:
- C++ backend 5-10× faster than NumPy for 16-qubit states
- UI remains responsive during circuit execution
- All tests pass with C++ backend

### Phase 4: Educational Content & Polish
**Timeline**: 3-4 weeks  
**Status**: 🔮 Future

**Goals**:
- [ ] Write end-user documentation (setup, usage, examples)
- [ ] Create interactive tutorials (in-app or video)
- [ ] Implement quantum algorithm demonstrations
- [ ] Add tooltips and help text throughout UI
- [ ] Create demo video for presentations
- [ ] Public release preparation

**Success Criteria**:
- A complete novice can install and use QubitSim
- Tutorials cover basic quantum concepts using QubitSim
- Academic paper draft complete

---

## Key Design Rationales

### Why Qiskit as Temporary Backend?
- ✅ Battle-tested correctness (industry standard)
- ✅ Allows parallel UI and backend development
- ✅ Provides validation reference for custom backend
- ✅ Easy to remove via clean abstraction layer
- ⚠️ Tradeoff: Extra dependency, black-box simulation (temporary)

### Why Grid-Based Circuit Representation?
- ✅ Matches standard quantum circuit diagrams
- ✅ Intuitive for students
- ✅ Simple indexing: `steps[time][qubit]`
- ✅ Natural for drag-and-drop UI
- ⚠️ Tradeoff: Sparse for large circuits (many `None` cells)

### Why State Vector Over Density Matrix as Primary?
- ✅ Simpler for pure states (90% of educational examples)
- ✅ Less memory: O(2^n) vs O(2^2n)
- ✅ Easier to explain to undergraduates
- ✅ Density matrix derivable: ρ = |ψ⟩⟨ψ|
- ⚠️ Tradeoff: Cannot represent mixed states (not needed for current scope)

### Why No Bloch Sphere Visualization?
- ⚠️ Only works for single qubits
- ⚠️ Distracts from multi-qubit circuit understanding
- ⚠️ Amplitude redistribution across 2^n basis states is more important
- ✅ Alternative: Could add as optional per-qubit view (future)

### Why 4-16 Qubit Limit?
- ✅ 4 qubits: Minimum for interesting multi-qubit entanglement
- ✅ 16 qubits: Maximum for readable state visualization
- ✅ Memory manageable: 2^16 = 65,536 complex numbers ≈ 1 MB
- ⚠️ Tradeoff: Cannot run Shor's algorithm (needs 20+ qubits)
- ✅ Intentional: This is a learning tool, not a research simulator

---

## Testing Strategy

### Unit Tests (`test_backend.py`)
**Scope**: Quantum mechanics correctness

**Tests**:
- Single-qubit gates (H, X, Y, Z, S, T)
- Rotation gates with various angles
- Two-qubit gates (CNOT, SWAP)
- Partial circuit execution
- State vector normalization

**Validation**: Compare against analytically known states

### Integration Tests (`test_integration.py`)
**Scope**: AppState ↔ Backend integration

**Tests**:
- Circuit execution through AppState
- Step, run_all, run_to functionality
- Backend reinitialization (qubit count change)
- Probability calculation
- Reset functionality

**Validation**: State evolution through complete workflows

### UI Tests (`test_ui_*.py`)
**Scope**: Widget functionality and rendering

**Tests**:
- Widget creation and initialization
- Signal emission and handling
- Drag-and-drop gate placement
- State display updates
- Control panel interactions

**Validation**: No crashes, signals emitted correctly

### Future Test Additions
- [ ] Controlled gate tests (multiple controls)
- [ ] Custom backend validation suite
- [ ] Performance benchmarks
- [ ] UI regression tests (screenshot comparison)
- [ ] End-to-end user workflows

---

## Dependencies

### Current Dependencies
```
PyQt6 >= 6.4.0          # UI framework
numpy >= 1.24.0          # Linear algebra
qiskit >= 1.0.0          # Temporary backend (will be removed)
qiskit-aer >= 0.13.0     # Qiskit statevector simulator
```

### Future Dependencies (Phase 3)
```
pybind11                 # C++ Python bindings
Eigen3                   # C++ linear algebra library (optional)
```

### Development Dependencies
```
pytest                   # Testing framework
black                    # Code formatting
mypy                     # Type checking
sphinx                   # Documentation generation
```

---

## References

### Quantum Computing Education Research
- IEEE Transactions on Education (QC curriculum papers)
- Physics Education journals (quantum pedagogy)
- Existing educational simulators (academic papers)

### Technical References
- Nielsen & Chuang: *Quantum Computation and Quantum Information*
- Qiskit documentation and tutorials
- Cirq documentation

### Project Documentation
- [README.md](README.md) — Comprehensive developer documentation
- [PAPER.md](PAPER.md) — Academic paper structure (DO NOT MODIFY)
- [IMPLEMENTATION.md](../IMPLEMENTATION.md) — Qiskit integration notes

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-11 | 0.2.0 | Updated to reflect current implementation status; added detailed architecture; clarified roadmap |
| 2025-XX-XX | 0.1.0 | Initial project definition |

---

**Status**: This document reflects the current project state as of February 11, 2026. Refer to [README.md](README.md) for detailed developer documentation.

