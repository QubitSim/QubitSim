"""

Available objects for circuit module

Standard Gates: 
- H
- X
- Y
- Z
- S
- T

Measurement:
- M

Rotational Gates:
- Rx
- Ry
- Rz

Control:
- Control qubit
- Anticontrol qubit

Swaps: 
- SWAP gate

"""

from qiskit.circuit import QuantumCircuit
from dataclasses import dataclass
import numpy as np

@dataclass
class GateOp:
    """
    Example: 
    
    ```python
    GateOp("H", targets=[0])
    GateOp("RX", targets=[1], params={"theta": 1.5708})
    GateOp("CNOT", targets=[1], controls=[0])
    GateOp("SWAP", targets=[0, 2])
    GateOp("M", targets=[0])
    ```
    """
    name: str                 # "H", "X", "RX", "SWAP", ...
    targets: list[int]        # qubit indices
    controls: list[int] = None
    anti_controls: list[int] = None
    params: dict[str, float] = None


def apply_h(qc: QuantumCircuit, op: GateOp): qc.h(op.targets[0])
def apply_x(qc: QuantumCircuit, op: GateOp): qc.x(op.targets[0])
def apply_y(qc: QuantumCircuit, op: GateOp): qc.y(op.targets[0])
def apply_z(qc: QuantumCircuit, op: GateOp): qc.z(op.targets[0])
def apply_s(qc: QuantumCircuit, op: GateOp): qc.s(op.targets[0])
def apply_t(qc: QuantumCircuit, op: GateOp): qc.t(op.targets[0])
def apply_sdg(qc: QuantumCircuit, op: GateOp): qc.sdg(op.targets[0])  # S†
def apply_tdg(qc: QuantumCircuit, op: GateOp): qc.tdg(op.targets[0])  # T†
def apply_i(qc: QuantumCircuit, op: GateOp): qc.id(op.targets[0])  # Identity gate

def apply_rx(qc: QuantumCircuit, op: GateOp):
    qc.rx(op.params["theta"], op.targets[0])

def apply_ry(qc: QuantumCircuit, op: GateOp):
    qc.ry(op.params["theta"], op.targets[0])

def apply_rz(qc: QuantumCircuit, op: GateOp):
    qc.rz(op.params["theta"], op.targets[0])

def apply_u3(qc: QuantumCircuit, op: GateOp):
    """Universal single-qubit gate U3(θ, φ, λ)"""
    qc.u(op.params["theta"], op.params["phi"], op.params["lam"], op.targets[0])

def apply_swap(qc: QuantumCircuit, op: GateOp):
    q0, q1 = op.targets
    qc.swap(q0, q1)

def apply_controlled(qc: QuantumCircuit, op: GateOp):
    # Generic controlled-U
    base_gate = op.name  # e.g. "X", "Z", "H", "S", "T", etc.
    ctrl = op.controls
    tgt = op.targets

    if base_gate == "X":
        qc.cx(ctrl[0], tgt[0])
    elif base_gate == "Y":
        qc.cy(ctrl[0], tgt[0])
    elif base_gate == "Z":
        qc.cz(ctrl[0], tgt[0])
    elif base_gate == "H":
        qc.ch(ctrl[0], tgt[0])
    elif base_gate == "S":
        qc.cs(ctrl[0], tgt[0])
    elif base_gate == "T":
        qc.ct(ctrl[0], tgt[0])
    elif base_gate == "Sdg":
        qc.csdg(ctrl[0], tgt[0])
    elif base_gate == "Tdg":
        qc.ctdg(ctrl[0], tgt[0])
    elif base_gate == "RX":
        qc.crx(op.params["theta"], ctrl[0], tgt[0])
    elif base_gate == "RY":
        qc.cry(op.params["theta"], ctrl[0], tgt[0])
    elif base_gate == "RZ":
        qc.crz(op.params["theta"], ctrl[0], tgt[0])
    else:
        raise ValueError(f"Unsupported controlled gate {base_gate}")
    
def apply_anticontrolled(qc: QuantumCircuit, op: GateOp):
    qc.x(op.controls[0])
    apply_controlled(qc, op)
    qc.x(op.controls[0])

# Advanced Multi-Qubit Gates
def apply_toffoli(qc: QuantumCircuit, op: GateOp):
    """Toffoli gate (CCNOT) - 3-qubit controlled-NOT
    Controls: 2 qubits, Target: 1 qubit"""
    if len(op.controls) != 2 or len(op.targets) != 1:
        raise ValueError("Toffoli gate requires 2 controls and 1 target")
    qc.ccx(op.controls[0], op.controls[1], op.targets[0])

def apply_fredkin(qc: QuantumCircuit, op: GateOp):
    """Fredkin gate (CSWAP) - Controlled SWAP
    Control: 1 qubit, Targets: 2 qubits to swap"""
    if len(op.controls) != 1 or len(op.targets) != 2:
        raise ValueError("Fredkin gate requires 1 control and 2 targets")
    qc.cswap(op.controls[0], op.targets[0], op.targets[1])

def apply_iswap(qc: QuantumCircuit, op: GateOp):
    """iSWAP gate - Interaction SWAP
    Targets: 2 qubits"""
    if len(op.targets) != 2:
        raise ValueError("iSWAP gate requires 2 targets")
    qc.iswap(op.targets[0], op.targets[1])

def apply_x3(qc: QuantumCircuit, op: GateOp):
    """3-Control X gate (CCCX)
    Controls: 3 qubits, Target: 1 qubit"""
    if len(op.controls) != 3 or len(op.targets) != 1:
        raise ValueError("3-Control X gate requires 3 controls and 1 target")
    # Implement using Qiskit's mcx (multi-control-X)
    qc.mcx(op.controls, op.targets[0])

def apply_anticontrolled(qc: QuantumCircuit, op: GateOp):
    qc.x(op.controls[0])
    apply_controlled(qc, op)
    qc.x(op.controls[0])

# Algorithm Components

def apply_hadamard_layer(qc: QuantumCircuit, op: GateOp):
    """Apply Hadamard gate to all specified qubits (or all qubits if not specified)
    targets: list of qubits to apply H, or empty list for all qubits"""
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    for q in qubits:
        qc.h(q)

def apply_grover_diffusion(qc: QuantumCircuit, op: GateOp):
    """Grover's diffusion operator: D = 2|s⟩⟨s| - I
    Targets: list of qubits to apply diffusion, or empty list for all qubits
    
    Implementation:
    - Apply Hadamards to all qubits
    - Apply X to all qubits
    - Apply multi-control-Z
    - Apply X to all qubits
    - Apply Hadamards to all qubits
    """
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    n = len(qubits)
    
    # Step 1: Hadamards
    for q in qubits:
        qc.h(q)
    
    # Step 2: X gates
    for q in qubits:
        qc.x(q)
    
    # Step 3: Multi-control-Z using mcx decomposition
    # MCZ(controls, target) = H(target) - MCX(controls, target) - H(target)
    if n > 1:
        qc.h(qubits[-1])
        qc.mcx(qubits[:-1], qubits[-1])
        qc.h(qubits[-1])
    elif n == 1:
        qc.z(qubits[0])
    
    # Step 4: X gates
    for q in qubits:
        qc.x(q)
    
    # Step 5: Hadamards
    for q in qubits:
        qc.h(q)

def apply_qft(qc: QuantumCircuit, op: GateOp):
    """Quantum Fourier Transform
    Targets: list of qubits (or all qubits if empty)
    
    Standard QFT decomposition:
    - Controlled rotations on qubits
    - Final swap operations
    """
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    n = len(qubits)
    
    # Apply QFT decomposition
    for j in range(n):
        # Apply Hadamard to qubit j
        qc.h(qubits[j])
        
        # Apply controlled rotations
        for k in range(j + 1, n):
            angle = 2 * np.pi / (2**(k - j + 1))
            qc.crz(angle, qubits[k], qubits[j])
    
    # Swap qubits to reverse order
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])

def apply_qft_dagger(qc: QuantumCircuit, op: GateOp):
    """Inverse Quantum Fourier Transform (QFT†)
    Targets: list of qubits (or all qubits if empty)"""
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    n = len(qubits)
    
    # Swap qubits to reverse order
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    
    # Apply inverse QFT decomposition
    for j in range(n - 1, -1, -1):
        # Apply controlled rotations
        for k in range(j):
            angle = -2 * np.pi / (2**(j - k + 1))
            qc.crz(angle, qubits[k], qubits[j])
        
        # Apply Hadamard to qubit j
        qc.h(qubits[j])

# Oracle Components

def apply_oracle_mark_state(qc: QuantumCircuit, op: GateOp):
    """Oracle that marks a specific basis state with a phase flip (-1)
    
    Parameters:
    - targets: list of qubits
    - params["state"]: the basis state to mark (string of 0s and 1s or integer)
    
    Implementation: Apply X gates to qubits that should be 0 in the target state,
    then apply a multi-control-Z, then apply X gates again.
    """
    qubits = op.targets
    target_state = op.params.get("state", "0" * len(qubits))
    
    # Convert integer to binary string if needed
    if isinstance(target_state, int):
        target_state = format(target_state, f'0{len(qubits)}b')
    
    # Apply X gates to qubits where target state is 0
    for i, q in enumerate(qubits):
        if target_state[i] == '0':
            qc.x(q)
    
    # Apply multi-control-Z to mark the state (MCZ = H - MCX - H)
    if len(qubits) > 1:
        qc.h(qubits[-1])
        qc.mcx(qubits[:-1], qubits[-1])
        qc.h(qubits[-1])
    elif len(qubits) == 1:
        qc.z(qubits[0])
    
    # Apply X gates again to restore
    for i, q in enumerate(qubits):
        if target_state[i] == '0':
            qc.x(q)

def apply_oracle_parity(qc: QuantumCircuit, op: GateOp):
    """Oracle that marks even or odd parity states
    
    Parameters:
    - targets: list of qubits
    - params["parity"]: "even" or "odd" (default "even")
    
    Even parity: number of 1s is even
    Odd parity: number of 1s is odd
    """
    qubits = op.targets
    parity = op.params.get("parity", "even")
    
    # For parity detection, we can use a multi-control gate
    # Even parity: apply Z to last qubit when even number of others are 1
    # Odd parity: apply Z to last qubit when odd number of others are 1
    
    if parity == "odd":
        # Mark odd parity: use multi-control-Z on all qubits (MCZ = H - MCX - H)
        if len(qubits) > 1:
            qc.h(qubits[-1])
            qc.mcx(qubits[:-1], qubits[-1])
            qc.h(qubits[-1])
    else:
        # Mark even parity: apply X to all, then multi-control-Z, then X to all
        for q in qubits:
            qc.x(q)
        if len(qubits) > 1:
            qc.h(qubits[-1])
            qc.mcx(qubits[:-1], qubits[-1])
            qc.h(qubits[-1])
        for q in qubits:
            qc.x(q)

def apply_custom_phase_oracle(qc: QuantumCircuit, op: GateOp):
    """Custom phase oracle that applies a phase to marked qubits
    
    Parameters:
    - targets: list of qubits to mark
    - params["angle"]: phase angle (default π)
    
    Applies e^(iθ)|target⟩⟨target|
    """
    qubits = op.targets
    angle = op.params.get("angle", np.pi)
    
    # Apply global phase using RZ on a single control qubit
    # This is simplified - in a full implementation, would use proper phase marker
    for q in qubits:
        qc.rz(angle, q)

# Visualization Components (Barrier and Label)

def apply_barrier(qc: QuantumCircuit, op: GateOp):
    """Barrier for circuit visualization and grouping
    
    Parameters:
    - targets: list of qubits (or all if empty)
    
    Barrier does not affect quantum computation, only visualization.
    It groups preceding operations together visually.
    """
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    qc.barrier(*qubits)

def apply_label(qc: QuantumCircuit, op: GateOp):
    """Label/annotation for teaching purposes
    
    Parameters:
    - params["text"]: label text
    - targets: qubits to attach label to (optional)
    
    Labels don't affect quantum computation, only add annotations for clarity.
    In Qiskit, we can use barrier with a label as a workaround.
    """
    label_text = op.params.get("text", "Label")
    qubits = op.targets if op.targets else list(range(qc.num_qubits))
    # Qiskit doesn't have native labels, but we can add metadata
    # For now, we'll just add as a comment in the circuit
    qc.global_phase = qc.global_phase  # Placeholder - would be improved in full impl
    qc.barrier(*qubits)

GATE_DISPATCH: dict[str, callable] = {
    "H": apply_h,
    "X": apply_x,
    "Y": apply_y,
    "Z": apply_z,
    "S": apply_s,
    "T": apply_t,
    "Sdg": apply_sdg,
    "Tdg": apply_tdg,
    "I": apply_i,
    "RX": apply_rx,
    "RY": apply_ry,
    "RZ": apply_rz,
    "U3": apply_u3,
    "SWAP": apply_swap,
    "Toffoli": apply_toffoli,
    "CCNOT": apply_toffoli,  # Alias
    "Fredkin": apply_fredkin,
    "CSWAP": apply_fredkin,  # Alias
    "iSWAP": apply_iswap,
    "X3": apply_x3,
    "CCCX": apply_x3,  # Alias
    # Algorithm components
    "H_LAYER": apply_hadamard_layer,
    "GROVER_DIFFUSION": apply_grover_diffusion,
    "QFT": apply_qft,
    "QFT_DAG": apply_qft_dagger,
    # Oracle components
    "ORACLE_MARK_STATE": apply_oracle_mark_state,
    "ORACLE_PARITY": apply_oracle_parity,
    "ORACLE_PHASE": apply_custom_phase_oracle,
    # Visualization components
    "BARRIER": apply_barrier,
    "LABEL": apply_label,
    "C": apply_controlled,
    "AC": apply_anticontrolled,
}