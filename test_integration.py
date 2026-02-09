"""
Test the full integration with AppState
Tests that the backend works correctly with the UI state management
"""

import sys
import numpy as np
from ui.app_state import AppState
from qcircuit.objects import GateOp

def test_appstate_integration():
    """Test that AppState correctly executes circuits"""
    print("Testing AppState integration...")
    
    # Create app state with 2 qubits and 3 steps
    app_state = AppState(num_qubits=2, num_steps=3)
    
    # Initial state should be |00>
    assert app_state.system is not None
    assert app_state.system.num_qubits == 2
    assert np.allclose(app_state.system.state[0, 0], 1.0)
    print("✓ Initial state is |00>")
    
    # Add H gate to qubit 0 at step 0
    app_state.add_gate(0, GateOp("H", targets=[0]))
    
    # Step forward (should execute step 0)
    app_state.step()
    
    # After H on qubit 0, state should be |+> ⊗ |0>
    # In Qiskit ordering (q1,q0): (|00> + |01>) / sqrt(2)
    state = app_state.system.state[:, 0]
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0, 0])
    assert np.allclose(state, expected), f"Expected {expected}, got {state}"
    print("✓ After H gate on q0: state is correct")
    
    # Add X gate to qubit 1 at step 1
    app_state.add_gate(1, GateOp("X", targets=[1]))
    
    # Step forward again
    app_state.step()
    
    # After X on qubit 1, state should be: H(q0) ⊗ X(q1)
    # In Qiskit ordering (q1,q0): (|10> + |11>) / sqrt(2)
    state = app_state.system.state[:, 0]
    expected = np.array([0, 0, 1/np.sqrt(2), 1/np.sqrt(2)])
    assert np.allclose(state, expected), f"Expected {expected}, got {state}"
    print("✓ After X gate on q1: state is correct")
    
    # Test reset
    app_state.reset()
    assert app_state.current_step == 0
    assert np.allclose(app_state.system.state[0, 0], 1.0)
    print("✓ Reset works correctly")
    
    # Test run_all
    app_state.run_all()
    assert app_state.current_step == app_state.num_steps
    # Should be at step 2 now (H then X)
    state = app_state.system.state[:, 0]
    expected = np.array([0, 0, 1/np.sqrt(2), 1/np.sqrt(2)])
    assert np.allclose(state, expected), f"Expected {expected}, got {state}"
    print("✓ run_all() executes full circuit")
    
    # Test run_to
    app_state.reset()
    app_state.run_to(1)
    assert app_state.current_step == 1
    state = app_state.system.state[:, 0]
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0, 0])
    assert np.allclose(state, expected), f"Expected {expected}, got {state}"
    print("✓ run_to() works correctly")
    
    return True

def test_qubit_count_change():
    """Test changing number of qubits resets backend"""
    print("\nTesting qubit count change...")
    
    app_state = AppState(num_qubits=2, num_steps=2)
    
    # Add a gate and execute
    app_state.add_gate(0, GateOp("H", targets=[0]))
    app_state.step()
    
    # Change qubit count
    app_state.set_num_qubits(3)
    
    # Should be reset to |000>
    assert app_state.system.num_qubits == 3
    assert app_state.current_step == 0
    assert np.allclose(app_state.system.state[0, 0], 1.0)
    print("✓ Changing qubit count resets system")
    
    return True

def test_measurement_probabilities():
    """Test that measurement probabilities are calculated correctly"""
    print("\nTesting measurement probabilities...")
    
    app_state = AppState(num_qubits=1, num_steps=1)
    
    # Add H gate
    app_state.add_gate(0, GateOp("H", targets=[0]))
    app_state.step()
    
    # Check probabilities
    probs = app_state.measurement_probs
    assert probs is not None
    
    # Should have 50/50 for |0> and |1>
    assert '0' in probs or '0' in str(probs)
    assert '1' in probs or '1' in str(probs)
    
    print("✓ Measurement probabilities calculated")
    
    return True

def main():
    print("=" * 60)
    print("AppState Integration Tests")
    print("=" * 60)
    
    tests = [
        test_appstate_integration,
        test_qubit_count_change,
        test_measurement_probabilities
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
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All integration tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
