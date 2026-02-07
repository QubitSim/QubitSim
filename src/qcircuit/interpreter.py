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
from qcircuit.objects import GateOp, GATE_DISPATCH

class CircuitInterpreter:
    def __init__(self, steps: list[list[GateOp]], num_qubits: int) -> None:
        self.steps = steps

    def apply_step(self, step: int):
        for op in self.steps[step]:
            if op.name not in GATE_DISPATCH:
                raise ValueError(f"Unknown gate {op.name}")
            GATE_DISPATCH[op.name](self.qc, op)

    def apply_all(self):
        for step in range(len(self.steps)):
            self.apply_step(step)

    def get_circuit(self):
        return self.qc
