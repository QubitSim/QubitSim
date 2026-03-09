# Codebase Map

A guide to every significant file in the project, what it does, and key things to know when editing it.

---

## `src/main.py`
Entry point. Creates `QApplication`, instantiates `MainWindow`, starts event loop.
Nothing interesting here — start debugging from `MainWindow` instead.

---

## `src/core/`

These are quantum primitives. Currently they serve as data containers; the actual simulation runs through Qiskit via `backend.py`.

### `src/core/gates.py`
Gate matrix definitions as NumPy arrays.
- Standard matrices: H, X, Y, Z, S, T, Sdg, Tdg, I (Identity)
- Added in Plan 2: Sdg, Tdg, I gate definitions

### `src/core/operator.py`
`Operator` class wrapping unitary matrices.

### `src/core/system.py`
`System` class holding quantum state (statevector, probabilities, qubits).
This is what `QiskitBackend.convert_to_system()` returns and what `AppState.system` holds.

### `src/core/gate.py`
Base `Gate` class.

---

## `src/qcircuit/`

The bridge between the UI grid and Qiskit execution.

### `src/qcircuit/objects.py` ⭐ Most important in this package

Contains:
- **`GateOp` dataclass**: the unit of circuit data
  ```python
  @dataclass
  class GateOp:
      name: str                     # gate identifier string
      targets: list[int]            # qubit indices
      controls: list[int] = None    # control qubit indices
      anti_controls: list[int] = None
      params: dict[str, float] = None
  ```
- **`apply_*` functions**: one per gate type, each takes `(qc: QuantumCircuit, op: GateOp)`
- **`GATE_DISPATCH` dict**: maps gate name string → apply function (34+ entries)
- **`apply_controlled()`**: wraps any apply function with control/anti-control logic
- **`apply_measurement()`**: handles M gate

To **add a new gate**:
1. Write `apply_mygateX(qc, op)` function
2. Add entry to `GATE_DISPATCH`: `"MYGATE": apply_mygateX`
3. Optionally add alias: `"ALIAS": apply_mygateX`
4. Add button in `gate_palette.py`

### `src/qcircuit/interpreter.py`
`CircuitInterpreter` class:
- `build_circuit(steps)` → full Qiskit `QuantumCircuit`
- `build_partial_circuit(steps, up_to_step)` → circuit up to a given step  
- `_apply_step(qc, step_ops)` → processes one column of the grid

Key logic: handles control/anti-control routing. Multi-control gates (Toffoli, Fredkin, X3)
have special cases before falling through to `apply_controlled()`.

### `src/qcircuit/backend.py`
`QiskitBackend` class:
- `__init__(num_qubits)` — initializes
- `execute(steps, up_to_step=None)` → runs simulation, returns result dict
  - Result dict: `{"statevector": ..., "probabilities": {...}, "system": System}`
- `get_statevector(qc)` — Qiskit Statevector simulation
- `get_measurement_probabilities(sv)` — extracts prob dict
- `convert_to_system(sv, probs)` → `core.System`

---

## `src/ui/`

### `src/ui/main_window.py`
Top-level `MainWindow(QMainWindow)`. Lays out the 3-column UI:
- Left: `GatePalette`
- Center: `CircuitCanvas` + `ControlPanel`
- Right: `StateDisplay`

Creates `AppState` and passes it to all child widgets.

### `src/ui/app_state.py` ⭐
See project_overview.md — central hub, full description there.

### `src/ui/circuit_canvas.py` ⭐
The drag-and-drop circuit grid.
- Renders a 2D grid of qubit rows × step columns
- Gates appear as labeled cells; control markers (C, AC) as circles
- Handles mouse events: click to place selected gate, drag to move
- Reads `AppState.steps` and `AppState.selected_gate` on paint
- Calls `AppState.add_gate()` and `AppState.remove_gate()` on edits

Key internal state: `dragging_gate`, `hover_cell`. No quantum logic here.

### `src/ui/gate_palette.py`
Left panel with a `QTabWidget` containing 8 tabs:
1. **Single** — H, X, Y, Z, S, T, M
2. **Rotation** — RX, RY, RZ (with theta slider)
3. **Control** — C (control), AC (anti-control), CNOT, CZ, CH, SWAP
4. **Pauli & Phase** — I, Sdg, Tdg, U3
5. **Advanced** — Toffoli, Fredkin, iSWAP, X3 (3-Control X)
6. **Algorithm** — H_LAYER, GROVER_DIFFUSION, QFT, QFT_DAG
7. **Oracle** — ORACLE_MARK_STATE, ORACLE_PARITY, ORACLE_PHASE
8. **Tools** — BARRIER, LABEL

Buttons call `AppState.selected_gate = name` + `AppState.selection_changed.emit()`.

### `src/ui/control_panel.py`
Buttons: Step, Run All, Run To (step number), Reset, Qubit count selector, Theme toggle.
Wired directly to `AppState` methods — no logic here.

### `src/ui/state_display.py`
Right panel — 7-tab `QTabWidget` showing quantum state:
1. **Amplitudes** — text: complex amplitudes
2. **Probabilities** — text: measurement probabilities
3. **Details** — text: system properties
4. **Prob. Chart** — `ProbabilityChartWidget` (matplotlib bar chart)
5. **Bloch Sphere** — `BlochSphereWidget` (matplotlib 3D)
6. **Phase Plot** — `StateVectorPhaseWidget` (matplotlib phase coloring)
7. **Statistics** — `EnhancedStatisticsWidget` (entropy, purity)

Refreshes on `AppState.system_changed` signal.

### `src/ui/visualization_utils.py`
Pure-function quantum math utilities (no Qt, no Qiskit):
- `partial_trace(statevector, keep_qubit, n_qubits)` → reduced density matrix
- `get_single_qubit_state(statevector, qubit_index, n_qubits)` → single-qubit density matrix
- `density_matrix_to_bloch_vector(rho)` → (x, y, z)
- `bloch_vector_to_angles(bv)` → (theta, phi)
- `phase_to_color(phase)` → RGB tuple
- `get_probability_data(system)` → sorted list of (state_label, prob)
- `get_amplitude_data(system)` → list of (label, magnitude, phase)
- `calculate_entropy(probs)` → von Neumann entropy (bits)
- `calculate_purity(statevector)` → purity scalar
- `filter_probabilities(prob_data, threshold)` → filtered list
- `get_statistics_text(system)` → formatted string

### `src/ui/visualization_widgets.py`
PyQt6 widgets backed by matplotlib:
- `ProbabilityChartWidget` — bar chart, threshold slider, log scale toggle
- `BlochSphereWidget` — 3D Bloch sphere, qubit selector
- `StateVectorPhaseWidget` — phase-colored bar chart
- `EnhancedStatisticsWidget` — entropy, purity, distribution analysis

Each widget has an `update_display(system)` method called by `StateDisplay`.

### `src/ui/themes.py`
`LIGHT_THEME` and `DARK_THEME` stylesheet strings.
Applied via `QApplication.setStyleSheet()` on theme toggle.

---

## Test Files (root level)

| File | What it tests |
|------|--------------|
| `test_backend.py` | `QiskitBackend` unit tests (5 tests) |
| `test_integration.py` | AppState + backend integration (3 tests) |
| `test_new_gates.py` | All Plan 2 gates: 27 tests covering dispatch + correctness |
| `test_ui_smoke.py` | MainWindow instantiation + widget presence |
| `test_ui_updates.py` | Signal/slot wiring, UI refresh after circuit changes |
| `test_visualizations.py` | `visualization_utils.py` math correctness (9 tests) |

Run all tests:
```bash
source venv/bin/activate
PYTHONPATH=src python test_backend.py
PYTHONPATH=src python test_integration.py
PYTHONPATH=src python test_new_gates.py
PYTHONPATH=src python test_visualizations.py
python test_ui_smoke.py
```

---

## `examples/`

`example_circuit.py` — demonstrates programmatic circuit construction using `GateOp` and `QiskitBackend`.
Good template for writing integration tests or debugging backend logic.

---

## `docs/`

User-facing documentation (DOCS.md, PAPER.md, README.md). Not agent context.
