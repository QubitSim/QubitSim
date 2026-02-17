"""
Test script for Qiskit backend integration
Tests the circuit interpreter and backend execution
"""

import sys
import numpy as np
from qcircuit.objects import GateOp
from qcircuit.backend import QiskitBackend

def test_hadamard():
    """Test H gate creates |+> state"""
    print("Testing H gate...")
    backend = QiskitBackend(num_qubits=1)
    
    steps = [[GateOp("H", targets=[0])]]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # |+> = (|0> + |1>) / sqrt(2)
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ H gate test passed")
        return True
    else:
        print(f"✗ H gate test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_pauli_x():
    """Test X gate creates |1> state"""
    print("Testing X gate...")
    backend = QiskitBackend(num_qubits=1)
    
    steps = [[GateOp("X", targets=[0])]]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # |1>
    expected = np.array([0, 1])
    
    if np.allclose(state, expected):
        print("✓ X gate test passed")
        return True
    else:
        print(f"✗ X gate test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_rotation():
    """Test RX gate with pi/2"""
    print("Testing RX(π/2) gate...")
    backend = QiskitBackend(num_qubits=1)
    
    steps = [[GateOp("RX", targets=[0], params={"theta": np.pi/2})]]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # RX(π/2)|0> = (|0> - i|1>) / sqrt(2)
    expected = np.array([1/np.sqrt(2), -1j/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ RX gate test passed")
        return True
    else:
        print(f"✗ RX gate test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_two_qubit():
    """Test 2-qubit circuit with H on both qubits"""
    print("Testing 2-qubit H gates...")
    backend = QiskitBackend(num_qubits=2)
    
    steps = [
        [GateOp("H", targets=[0]), GateOp("H", targets=[1])]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # |++> = (|00> + |01> + |10> + |11>) / 2
    expected = np.array([0.5, 0.5, 0.5, 0.5])
    
    if np.allclose(state, expected):
        print("✓ 2-qubit test passed")
        return True
    else:
        print(f"✗ 2-qubit test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_partial_execution():
    """Test partial circuit execution (stepping)"""
    print("Testing partial execution...")
    backend = QiskitBackend(num_qubits=1)
    
    steps = [
        [GateOp("H", targets=[0])],
        [GateOp("X", targets=[0])],
        [None]
    ]
    
    # Execute only first step
    result = backend.execute(steps, up_to_step=1)
    system = result['system']
    state = system.state[:, 0]
    
    # Should be |+> after just H
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ Partial execution test passed")
        return True
    else:
        print(f"✗ Partial execution test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_s_gate():
    """Test S gate (phase gate)"""
    print("Testing S gate...")
    backend = QiskitBackend(num_qubits=1)
    
    # S gate on |0> should give |0> (diagonal matrix with [1, i])
    steps = [[GateOp("S", targets=[0])]]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # S|0> = |0>
    expected = np.array([1, 0])
    
    if np.allclose(state, expected):
        print("✓ S gate test passed")
        return True
    else:
        print(f"✗ S gate test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_t_gate():
    """Test T gate (π/8 phase gate)"""
    print("Testing T gate...")
    backend = QiskitBackend(num_qubits=1)
    
    # T gate on |0> should give |0> (diagonal matrix with [1, e^(iπ/4)])
    steps = [[GateOp("T", targets=[0])]]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # T|0> = |0>
    expected = np.array([1, 0])
    
    if np.allclose(state, expected):
        print("✓ T gate test passed")
        return True
    else:
        print(f"✗ T gate test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_st_sequence():
    """Test S and T gates in sequence with H"""
    print("Testing H-S-T sequence...")
    backend = QiskitBackend(num_qubits=1)
    
    # Create |+> with H, then apply S and T
    steps = [
        [GateOp("H", targets=[0])],
        [GateOp("S", targets=[0])],
        [GateOp("T", targets=[0])]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # H creates (|0> + |1>)/sqrt(2)
    # S doesn't change |0>, adds phase i to |1>: (|0> + i|1>)/sqrt(2)
    # T doesn't change |0>, adds phase e^(iπ/4) to |1>: (|0> + e^(iπ/4)|1>)/sqrt(2)
    # Note: phase accumulates: i * e^(iπ/4) = e^(iπ/2) * e^(iπ/4) = e^(i3π/4)
    expected = np.array([1/np.sqrt(2), np.exp(1j * 3 * np.pi / 4) / np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ H-S-T sequence test passed")
        return True
    else:
        print(f"✗ H-S-T sequence test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_controlled_x():
    """Test CNOT (controlled-X) gate"""
    print("Testing CNOT gate...")
    backend = QiskitBackend(num_qubits=2)
    
    # Create |+> on qubit 0, |0> on qubit 1
    # Then apply CNOT with control=0, target=1
    # Initial superposition: (|00> + |10>)/sqrt(2)
    # After CNOT (flips target when control=|1>): (|00> + |11>)/sqrt(2)
    steps = [
        [GateOp("H", targets=[0]), None],
        [GateOp("X", targets=[1], controls=[0]), None]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # In Qiskit little-endian ordering:
    # |00> is index 0, |10> is index 2, |01> is index 1, |11> is index 3
    # Initial after H on qubit 0: (|00> + |10>)/sqrt(2) = indices [1/sqrt(2), 0, 1/sqrt(2), 0]
    # After CNOT with control=0, target=1: (|00> + |11>)/sqrt(2) = indices [1/sqrt(2), 0, 0, 1/sqrt(2)]
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ CNOT test passed")
        return True
    else:
        print(f"✗ CNOT test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_controlled_h():
    """Test controlled-H gate"""
    print("Testing controlled-H gate...")
    backend = QiskitBackend(num_qubits=2)
    
    # Apply X to qubit 0 (makes it |1>), then CH with control=0, target=1
    # H on target creates superposition only when control is |1>
    steps = [
        [GateOp("X", targets=[0]), None],
        [GateOp("H", targets=[1], controls=[0]), None]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # Initial: X on qubit 0 → |01> (little-endian) at index 1
    # After CH with control=0: H on target → (|01> + |11>)/sqrt(2)
    # In little-endian: indices [0, 1/sqrt(2), 0, 1/sqrt(2)]
    expected = np.array([0, 1/np.sqrt(2), 0, 1/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ Controlled-H test passed")
        return True
    else:
        print(f"✗ Controlled-H test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_anticontrolled_x():
    """Test anticontrolled-X gate (X with anticontrol)"""
    print("Testing anticontrolled-X gate...")
    backend = QiskitBackend(num_qubits=2)
    
    # Start with |00>
    # Apply anticontrolled-X: flips qubit 1 only if qubit 0 is |0>
    # Result: |10>
    steps = [
        [None, None],
        [GateOp("X", targets=[1], anti_controls=[0]), None]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # Initial: |00> (index 0)
    # After anticontrolled-X (flips q1 when q0 is |0>): |10> (index 2)
    expected = np.array([0, 0, 1, 0])
    
    if np.allclose(state, expected):
        print("✓ Anticontrolled-X test passed")
        return True
    else:
        print(f"✗ Anticontrolled-X test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_controlled_s():
    """Test controlled-S gate"""
    print("Testing controlled-S gate...")
    backend = QiskitBackend(num_qubits=2)
    
    # Apply X to qubit 0 (makes it |1>), then CS with control=0, target=1
    # S on target (qubit 1 in |0> state) doesn't change anything
    steps = [
        [GateOp("X", targets=[0]), None],
        [GateOp("S", targets=[1], controls=[0]), None]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # Initial after X on q0: |01> (index 1)
    # After CS: S is applied to q1 (which is |0>), so no change: |01> (index 1)
    expected = np.array([0, 1, 0, 0])
    
    if np.allclose(state, expected):
        print("✓ Controlled-S test passed")
        return True
    else:
        print(f"✗ Controlled-S test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def test_controlled_rotation():
    """Test controlled rotation gate (CRY)"""
    print("Testing controlled rotation gate...")
    backend = QiskitBackend(num_qubits=2)
    
    # Apply X to qubit 0 (|1>), then CRY with control=0, target=1, theta=π/2
    # RY(π/2)|0> = (|0> + |1>)/sqrt(2)
    steps = [
        [GateOp("X", targets=[0]), None],
        [GateOp("RY", targets=[1], controls=[0], params={"theta": np.pi/2}), None]
    ]
    result = backend.execute(steps)
    
    system = result['system']
    state = system.state[:, 0]
    
    # Initial after X on q0: |01> (index 1)
    # After CRY(π/2): RY on q1 produces (|0> + |1>)/sqrt(2)
    # Result: (|01> + |11>)/sqrt(2) = indices [0, 1/sqrt(2), 0, 1/sqrt(2)]
    expected = np.array([0, 1/np.sqrt(2), 0, 1/np.sqrt(2)])
    
    if np.allclose(state, expected):
        print("✓ Controlled rotation test passed")
        return True
    else:
        print(f"✗ Controlled rotation test failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {state}")
        return False

def main():
    print("=" * 50)
    print("Qiskit Backend Integration Tests")
    print("=" * 50)
    
    tests = [
        test_hadamard,
        test_pauli_x,
        test_rotation,
        test_two_qubit,
        test_partial_execution,
        test_s_gate,
        test_t_gate,
        test_st_sequence,
        test_controlled_x,
        test_controlled_h,
        test_anticontrolled_x,
        test_controlled_s,
        test_controlled_rotation,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
