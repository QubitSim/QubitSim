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

def main():
    print("=" * 50)
    print("Qiskit Backend Integration Tests")
    print("=" * 50)
    
    tests = [
        test_hadamard,
        test_pauli_x,
        test_rotation,
        test_two_qubit,
        test_partial_execution
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
