# Gate Reference

Complete reference for all 34+ gate types registered in `GATE_DISPATCH` (`src/qcircuit/objects.py`).

---

## Basic Single-Qubit Gates (9)

| Name | `GateOp.name` | Matrix | Notes |
|------|--------------|--------|-------|
| Hadamard | `"H"` | (H+V)/√2 superposition | |
| Pauli-X | `"X"` | Bit flip | |
| Pauli-Y | `"Y"` | |
| Pauli-Z | `"Z"` | Phase flip | |
| Phase S | `"S"` | 90° phase | |
| T-gate | `"T"` | 45° phase | |
| S-dagger | `"Sdg"` | S†, inverse S | |
| T-dagger | `"Tdg"` | T†, inverse T | |
| Identity | `"I"` | No-op | |

---

## Rotation Gates (3)

All require `params={"theta": angle}`.

| Name | `GateOp.name` | Description |
|------|--------------|-------------|
| Rotate X | `"RX"` | Rotation around X-axis by θ |
| Rotate Y | `"RY"` | Rotation around Y-axis by θ |
| Rotate Z | `"RZ"` | Rotation around Z-axis by θ |

---

## Universal Parametric Gate (1)

| Name | `GateOp.name` | Params | Description |
|------|--------------|--------|-------------|
| Universal | `"U3"` | `theta`, `phi`, `lam` | Full single-qubit unitary |

---

## Multi-Qubit Gates (5 + aliases)

| Name | `GateOp.name` | Aliases | Qubits | Description |
|------|--------------|---------|--------|-------------|
| SWAP | `"SWAP"` | — | 2 targets | Exchange states |
| Toffoli | `"Toffoli"` | `"CCNOT"` | 2 controls + 1 target | Controlled-controlled-NOT |
| Fredkin | `"Fredkin"` | `"CSWAP"` | 1 control + 2 targets | Controlled SWAP |
| iSWAP | `"iSWAP"` | — | 2 targets | Interaction SWAP |
| 3-Control X | `"X3"` | `"CCCX"` | 3 controls + 1 target | Multi-control NOT |

---

## Controlled Versions of Standard Gates

These are not separate dispatch entries — any gate can be made controlled by adding `controls=[...]`
to the `GateOp`. The interpreter calls `apply_controlled()` automatically.

Special convenience names registered in dispatch:
- `"CNOT"` → controlled-X (c: controls[0], t: targets[0])
- `"CY"`, `"CZ"`, `"CH"` → controlled variants

---

## Algorithm Components (4)

| Name | `GateOp.name` | Targets | Description |
|------|--------------|---------|-------------|
| Hadamard Layer | `"H_LAYER"` | list of qubits | Apply H to all listed qubits |
| Grover Diffusion | `"GROVER_DIFFUSION"` | list of qubits | D = 2\|s⟩⟨s\| - I |
| QFT | `"QFT"` | list of qubits | Quantum Fourier Transform |
| Inverse QFT | `"QFT_DAG"` | list of qubits | QFT† |

**Grover Diffusion decomposition**: H — X — MCX (multi-control) — X — H

**QFT implementation**: standard decomposition with CRZ gates + SWAP reordering

---

## Oracle Components (3)

| Name | `GateOp.name` | Params | Description |
|------|--------------|--------|-------------|
| Mark State | `"ORACLE_MARK_STATE"` | `state` (binary str or int) | Phase-flip target basis state |
| Parity Oracle | `"ORACLE_PARITY"` | `parity` ("even"/"odd") | Phase-flip states with given parity |
| Phase Oracle | `"ORACLE_PHASE"` | `angle` (radians, default π) | Apply custom phase to qubits |

---

## Visualization / Annotation Components (2)

| Name | `GateOp.name` | Params | Description |
|------|--------------|--------|-------------|
| Barrier | `"BARRIER"` | — | Visual separator, no quantum effect |
| Label | `"LABEL"` | `text` (str) | Circuit annotation |

---

## Control Modifiers

These are placed as independent cells on the grid to modify adjacent gates:

| Name | `GateOp.name` | Description |
|------|--------------|-------------|
| Control | `"C"` | Control qubit (gate fires when qubit = \|1⟩) |
| Anti-control | `"AC"` | Anti-control (gate fires when qubit = \|0⟩) |

---

## Usage Examples

```python
from qcircuit.objects import GateOp

# Single-qubit
GateOp(name="H", targets=[0])
GateOp(name="Sdg", targets=[1])
GateOp(name="U3", targets=[0], params={"theta": 1.5708, "phi": 0.0, "lam": 0.0})

# Rotation
GateOp(name="RX", targets=[0], params={"theta": 3.14159})

# Controlled
GateOp(name="X", targets=[1], controls=[0])   # CNOT
GateOp(name="Z", targets=[1], controls=[0])   # CZ

# Toffoli
GateOp(name="Toffoli", targets=[2], controls=[0, 1])

# Fredkin
GateOp(name="Fredkin", targets=[1, 2], controls=[0])

# iSWAP
GateOp(name="iSWAP", targets=[0, 1])

# 3-Control X
GateOp(name="X3", targets=[3], controls=[0, 1, 2])

# Algorithm components
GateOp(name="H_LAYER", targets=[0, 1, 2])
GateOp(name="GROVER_DIFFUSION", targets=[0, 1, 2])
GateOp(name="QFT", targets=[0, 1, 2])
GateOp(name="QFT_DAG", targets=[0, 1, 2])

# Oracles
GateOp(name="ORACLE_MARK_STATE", targets=[0, 1, 2], params={"state": "101"})
GateOp(name="ORACLE_PARITY", targets=[0, 1, 2], params={"parity": "odd"})
GateOp(name="ORACLE_PHASE", targets=[0, 1], params={"angle": 3.14159})

# Annotations
GateOp(name="BARRIER", targets=[])
GateOp(name="LABEL", targets=[0], params={"text": "Superposition"})
```

---

## Algorithm Patterns

### Grover's Search (3-qubit, searching |101⟩)
```python
steps = [
    [GateOp("H_LAYER", targets=[0, 1, 2])],
    [GateOp("ORACLE_MARK_STATE", targets=[0, 1, 2], params={"state": "101"})],
    [GateOp("GROVER_DIFFUSION", targets=[0, 1, 2])],
    # Repeat oracle + diffusion for more iterations
]
```

### Bell State
```python
steps = [
    [GateOp("H", targets=[0])],
    [GateOp("X", targets=[1], controls=[0])],
]
# Result: (|00⟩ + |11⟩)/√2
```

### QFT
```python
steps = [
    [GateOp("QFT", targets=[0, 1, 2])],
    [GateOp("QFT_DAG", targets=[0, 1, 2])],  # inverse → returns to original
]
```

---

## Adding a New Gate (quick checklist)

1. **`src/qcircuit/objects.py`**: write `apply_mygate(qc: QuantumCircuit, op: GateOp)`
2. **`src/qcircuit/objects.py`**: add `"MYGATE": apply_mygate` to `GATE_DISPATCH`
3. **`src/core/gates.py`**: optionally add the numpy matrix if needed by core layer
4. **`src/ui/gate_palette.py`**: add a button in the appropriate tab
   - Call `state.selected_gate = "MYGATE"` on click
5. Write a test in `test_new_gates.py`
