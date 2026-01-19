import numpy as np
from core.gate import Gate, RotationGate

X: Gate = Gate(np.array([
    [0, 1],
    [1, 0]
    ]), "X")
Y: Gate = Gate(np.array([
    [0, -1j],
    [1j, 0]
    ]), "Y")
Z: Gate = Gate(np.array([
    [1, 0],
    [0, -1]
    ]), "Z")
H: Gate = Gate(np.array([
    [1, 1],
    [1, -1]
    ]) / np.sqrt(2), "H")

S: Gate = Gate(np.array([
    [1, 0],
    [0, 1j]
    ]), "S")

T: Gate = Gate(np.array([
    [1, 0],
    [0, np.exp(1j * np.pi / 4)]
    ]), "T")

Rx: RotationGate = lambda theta: RotationGate("X", theta)
Ry: RotationGate = lambda theta: RotationGate("Y", theta)
Rz: RotationGate = lambda theta: RotationGate("Z", theta)