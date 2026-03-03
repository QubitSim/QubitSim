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

# Conjugate/Dagger versions of S and T
Sdg: Gate = Gate(np.array([
    [1, 0],
    [0, -1j]
    ]), "Sdg")  # S†

Tdg: Gate = Gate(np.array([
    [1, 0],
    [0, np.exp(-1j * np.pi / 4)]
    ]), "Tdg")  # T†

# Identity gate
I: Gate = Gate(np.array([
    [1, 0],
    [0, 1]
    ]), "I")

# Rotation gates
Rx: RotationGate = lambda theta: RotationGate("X", theta)
Ry: RotationGate = lambda theta: RotationGate("Y", theta)
Rz: RotationGate = lambda theta: RotationGate("Z", theta)

# Universal single-qubit gate U3(θ, φ, λ)
# U3(θ, φ, λ) = [[cos(θ/2), -e^(iλ)sin(θ/2)], [e^(iφ)sin(θ/2), e^(i(φ+λ))cos(θ/2)]]
class U3Gate(Gate):
    def __init__(self, theta: float, phi: float, lam: float):
        op = np.array([
            [np.cos(theta/2), -np.exp(1j * lam) * np.sin(theta/2)],
            [np.exp(1j * phi) * np.sin(theta/2), np.exp(1j * (phi + lam)) * np.cos(theta/2)]
        ])
        name = f"U3({theta:.3f},{phi:.3f},{lam:.3f})"
        super().__init__(op, name)

U3 = U3Gate  # Alias for convenience