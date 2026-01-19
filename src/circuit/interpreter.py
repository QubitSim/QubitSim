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

from core.system import System
from circuit.objects import gates
from core.gate import ControlledGate

class CircuitInterpreter:
    def __init__(self, circuit: list[list[str]], system: System):
        self.circuit = circuit
        self.system = system

    def apply_step(self, step: int) -> None:
        """
        Apply all gates in a given time step to the system.
        """
        controls: dict[int, int] = {}
        targets: list[int] = []
        for i, obj in enumerate(self.circuit[step]):
            if obj == "C": 
                controls[i] = 1
            elif obj == "A":
                controls[i] = 0
            elif obj in gates.GATE_MAP:
                targets.append(i)

            if not controls:
                # No control qubits, apply gates directly
                for i, obj in enumerate(self.circuit[step]):
                    if obj in gates.GATE_MAP:
                        gate = gates.GATE_MAP[obj]
                        gate._apply(self.system, target=i)
            else:
                # There are control qubits, build controlled gates
                # One controlled gate per target
                # This is not optimal, but it works for now
                # Optimization can be done later
                for i, obj in enumerate(self.circuit[step]):
                    if obj in gates.GATE_MAP:
                        gate = gates.GATE_MAP[obj]
                        controlled_gate = ControlledGate(
                            base_gate=gate,
                            controls=controls,
                            targets=[i]
                        )
                        controlled_gate._apply(self.system)

    def run(self) -> System:
        """
        Run the circuit on the system.
        """
        num_steps = len(self.circuit[0])
        for step in range(num_steps):
            self.apply_step(step)
        return self.system

