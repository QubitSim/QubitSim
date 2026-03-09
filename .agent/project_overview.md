# QubitSim — Project Overview

## What It Is

QubitSim is an **educational quantum circuit simulator** with a drag-and-drop GUI built in PyQt6.
Target audience: students and teachers learning quantum computing concepts interactively.

Key capabilities:
- Build quantum circuits visually on a 2D grid (qubits × steps)
- Step through circuit execution or run all at once
- Visualize quantum state in real-time (amplitudes, probabilities, Bloch sphere, phase, statistics)
- Drag gates from a categorized palette and drop them on the circuit canvas

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| GUI | PyQt6 (Qt 6 bindings for Python) |
| Quantum simulation | Qiskit Statevector + qiskit-aer |
| Numerics | NumPy, SciPy |
| Plotting | Matplotlib (embedded in PyQt6 via FigureCanvasQTAgg) |
| Python | 3.10+ |

Dependencies are in `requirements.txt`:
```
PyQt6>=6.4.0
numpy>=1.24.0
qiskit>=1.0.0
qiskit-aer>=0.13.0
matplotlib>=3.5.0
pyqtgraph>=0.13.0
scipy
```

---

## High-Level Architecture

```
src/
├── main.py                   Entry point — creates QApplication + MainWindow
├── core/                     Core quantum primitives (mostly stubs/wrappers)
│   ├── gate.py               Gate base class
│   ├── gates.py              Gate matrix definitions (numpy arrays)
│   ├── operator.py           Operator/unitary wrappers
│   └── system.py             QuantumSystem state container
├── qcircuit/                 Circuit building + Qiskit execution layer
│   ├── objects.py            GateOp dataclass + all apply_* functions + GATE_DISPATCH
│   ├── interpreter.py        Translates AppState grid → Qiskit QuantumCircuit
│   └── backend.py            QiskitBackend: executes circuits, returns System
└── ui/                       PyQt6 UI layer
    ├── main_window.py         Top-level MainWindow widget
    ├── app_state.py           AppState: single source of truth (QObject)
    ├── circuit_canvas.py      Drag-and-drop circuit grid widget
    ├── gate_palette.py        Left panel: tabbed gate buttons
    ├── control_panel.py       Step/Run/Reset buttons
    ├── state_display.py       Right panel: 7-tab quantum state visualization
    ├── visualization_utils.py Quantum math utilities (Bloch, entropy, purity…)
    ├── visualization_widgets.py PyQt6 matplotlib widgets for visual tabs
    ├── themes.py              Light/dark theme stylesheets
    └── app_state.py           (see below)
```

---

## AppState — Central Hub

`AppState` (in `src/ui/app_state.py`) is a `QObject` and the **single source of truth**. All UI components read from and write to it.

### Key fields

| Field | Type | Description |
|-------|------|-------------|
| `num_qubits` | int | Number of qubits in current circuit |
| `num_steps` | int | Number of time steps (columns) |
| `steps` | `list[list[GateOp\|None]]` | Grid: `steps[step][qubit]` → GateOp |
| `current_step` | int | Execution cursor |
| `selected_gate` | str\|None | Currently selected gate name from palette |
| `selected_theta` | float | Angle parameter for rotation gates |
| `backend` | QiskitBackend | Quantum simulator instance |
| `system` | System | Latest quantum state after execution |
| `statevector` | ndarray | Raw Qiskit statevector |
| `measurement_probs` | dict | Basis state → probability |
| `theme` | str | "light" or "dark" |

### Key signals

| Signal | When emitted |
|--------|-------------|
| `circuit_changed` | Gate added, removed, or circuit resized |
| `state_changed` | current_step changes |
| `system_changed` | Circuit executed, new quantum state available |
| `selection_changed` | User selects a new gate in palette |
| `theme_changed(str)` | Theme toggled |

### Key methods

| Method | Description |
|--------|-------------|
| `add_gate(step, gate_op)` | Place a gate on the grid |
| `remove_gate(step, qubit)` | Remove gate + any dependent control markers |
| `step()` | Advance one step and execute |
| `run_all()` | Execute full circuit |
| `run_to(n)` | Execute through step n |
| `reset()` | Reset cursor and quantum state |
| `set_num_qubits(n)` | Resize circuit and reinitialize backend |
| `execute_circuit_to_current_step()` | Internal: triggers backend execution |

---

## Data Flow

```
User drops gate → CircuitCanvas → AppState.add_gate()
                      ↓ circuit_changed
               UI re-renders canvas

User clicks Step → ControlPanel → AppState.step()
                      ↓
               current_step++
               execute_circuit_to_current_step()
                      ↓
               QiskitBackend.execute(steps, up_to_step)
                      ↓
               CircuitInterpreter.build_partial_circuit()
                      ↓
               Qiskit Statevector simulation
                      ↓
               System object produced
                      ↓ system_changed
               StateDisplay refreshes all 7 tabs
```

---

## Qubit Ordering

Qiskit uses **little-endian** ordering: basis states are indexed as |q_{n-1}...q_1 q_0⟩.
- Applying H to qubit 0 on a 2-qubit system: (|00⟩ + |01⟩)/√2
- This differs from big-endian notation (|00⟩ + |10⟩)/√2
The UI consistently follows Qiskit's convention.

---

## Migration Path (Future)

The `QiskitBackend` interface is intentionally decoupled so a custom backend using `core/` primitives
can replace it without any UI changes:
1. Create `CustomBackend` in `src/qcircuit/backend.py` with the same API
2. Swap the instantiation in `AppState.__init__()`
3. No UI changes needed

---

## Practical Limits

- Exact statevector simulation: practical up to ~20–25 qubits (exponential memory)
- Execution is synchronous (may block UI for large circuits)
- No noise modeling (ideal quantum computer)
