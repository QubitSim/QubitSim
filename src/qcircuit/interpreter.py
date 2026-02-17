"""
The circuit is a grid. 
- Each column is a step in time.
- Each row is a qubit.

For example, the following circuit:

[
    [H,  , C,  , SW],
    [ , X,  ,  , SW],
    [H,  , X, Y,  ]
]

That is easier to access as:

[
    [H,  , H],
    [ , X,  ],
    [C,  , X],
    [ ,  , Y],
    [SW, SW,  ]
]

Means that: 
- at time step 0, H is applied to qubit 0, H to qubit 2, 
- at time step 1, X is applied to qubit 1,
- at time step 2, C (controlled gate) is applied to qubits 0 and 2,
- at time step 3, Y is applied to qubit 2,
- at time step 4, SWAP is applied to qubits 0 and 1

This makes sense.

Simultaneous operations exists. 

So we have a register of n qubits (System), with an initial state |ψ⟩.

Since I'm not carying about performance right now, I can just apply each gate in the column to the system one by one.

"""
from qiskit import QuantumCircuit
from qcircuit.objects import GateOp, GATE_DISPATCH

class CircuitInterpreter:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.qc = QuantumCircuit(num_qubits)

    def build_circuit(self, steps: list[list[GateOp | None]]) -> QuantumCircuit:
        self.qc = QuantumCircuit(self.num_qubits)
        for step in steps:
            self._apply_step(step)
        return self.qc

    def build_partial_circuit(self, steps: list[list[GateOp | None]], up_to_step: int) -> QuantumCircuit:
        self.qc = QuantumCircuit(self.num_qubits)
        for step in steps[:up_to_step]:
            self._apply_step(step)
        return self.qc

    def _apply_step(self, step: list[GateOp | None]):
        for op in step:
            if op is None:
                continue
            
            # Skip control markers themselves - they're attached to gates
            if op.name in {"C", "AC"}:
                continue
            
            if op.name not in GATE_DISPATCH:
                raise ValueError(f"Unknown gate {op.name}")
            
            # Handle controlled gates
            if op.controls:
                GATE_DISPATCH["C"](self.qc, op)
            # Handle anticontrolled gates
            elif op.anti_controls:
                # Create a modified op with controls instead of anti_controls
                # The apply_anticontrolled will flip the control bit
                modified_op = GateOp(
                    name=op.name,
                    targets=op.targets,
                    controls=op.anti_controls,
                    params=op.params
                )
                GATE_DISPATCH["AC"](self.qc, modified_op)
            else:
                # Regular gate
                GATE_DISPATCH[op.name](self.qc, op)
