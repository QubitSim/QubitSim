# **QubitSim: An Educational Quantum Circuit Simulator with Explicit State Evolution**

## **Abstract**
- Context: educational problem
- Gap (existing tools are insufficient)
- Contribution: what is being built
- Outcome: what it demonstrates and enables
    - What not to include:
    - How quantum circuits are tought
    - Not a list

## **Introduction**

- Importance of quantum circuits (dominant as computational model)
- Pedagogical difficulty
    - Abstract math
    - Hidden state
    - "Black box" simulators
- Why is important for CS and Physics students
- What am I presenting in this paper
- Contribution
- Outline of the paper

## **Background and related work**

- Overview of:
    - QC as computational model
    - State vector vs density matrix
- Overview of current tools:
    - Qiskit
    - Cirq
    - Educational simulators (research)
- The limitations for teaching 
    - Abstractions 
    - Batch
    - Limited introspection

## **System Design and Methodology**

- Overall system architecture:
	- Frontend
	- Backend
- Circuit representation model
- Execution model (step-by-step vs batch)
- Quantum state representation
	- Internal canonical form
	- Derived views (state vector, density matrix)
- Backend-agnostic linear algebra abstraction
- Design constraints:
	- 5-qubit limit
	- Educational trade-offs

## **Visualizations and interaction**

- Circuit construction interface
- State visualization strategy
- How users observe:
    - Amplitude redistribution
    - Entanglement emergence
    - Measurement collapse
- Why certain visualizations were chosen
- Why others were intentionally excluded

## **Results**

- Step-by-step evolution of:
    - Superposition creation
    - Bell state generation
    - Multi-qubit entanglement

- Comparison:
    - State before and after measurement
    - State vector vs density matrix views

- Correctness validation:
    - Known analytical results reproduced

## **Discussion**

- Acknowledge scalability limits
- Explain why noise and hardware effects are excluded
- Discuss cognitive trade-offs
- Mention backend substitution as future work (HPC hook)

## **Conclusions and Future Work**

- Restate contribution, emphazise educational impact. 
- Future extensions: 
    - C++ backend
    - Performance studies
    - More visualizations

