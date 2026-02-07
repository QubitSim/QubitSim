"""

Available objects for circuit module

Standard Gates: 
- H
- X
- Y
- Z
- S
- T

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

@dataclass
class GateOp:
    """
    Example: 
    
    ```python
    GateOp("H", targets=[0])
    GateOp("RX", targets=[1], params={"theta": 1.5708})
    GateOp("CNOT", targets=[1], controls=[0])
    GateOp("SWAP", targets=[0, 2])
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

def apply_rx(qc: QuantumCircuit, op: GateOp):
    qc.rx(op.params["theta"], op.targets[0])

def apply_ry(qc: QuantumCircuit, op: GateOp):
    qc.ry(op.params["theta"], op.targets[0])

def apply_rz(qc: QuantumCircuit, op: GateOp):
    qc.rz(op.params["theta"], op.targets[0])

def apply_swap(qc: QuantumCircuit, op: GateOp):
    q0, q1 = op.targets
    qc.swap(q0, q1)

def apply_controlled(qc: QuantumCircuit, op: GateOp):
    # Generic controlled-U
    base_gate = op.name  # e.g. "X", "Z", "H"
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
    else:
        raise ValueError(f"Unsupported controlled gate {base_gate}")
    
def apply_anticontrolled(qc: QuantumCircuit, op: GateOp):
    qc.x(op.controls[0])
    apply_controlled(qc, op)
    qc.x(op.controls[0])

GATE_DISPATCH: dict[str, callable] = {
    "H": apply_h,
    "X": apply_x,
    "Y": apply_y,
    "Z": apply_z,
    "RX": apply_rx,
    "RY": apply_ry,
    "RZ": apply_rz,
    "SWAP": apply_swap,
    "C": apply_controlled,
    "AC": apply_anticontrolled,
}