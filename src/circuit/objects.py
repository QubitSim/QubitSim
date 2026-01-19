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

from core.gates import X, Y, Z, H, S, T, Rx, Ry, Rz
from core.gates import Gate

gates: dict[str, Gate] = {
    "H": H,
    "X": X,
    "Y": Y,
    "Z": Z,
    "S": S,
    "T": T,
    "Rx": Rx,
    "Ry": Ry,
    "Rz": Rz
}