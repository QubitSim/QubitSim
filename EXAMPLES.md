# Guided Example: Flipping a Qubit with the X Gate

This example shows how the **X gate works like a classical NOT gate**: it flips the state of a qubit.

### Instructions

1. **Set up the canvas with 1 qubit**

2. **Place an X gate on qubit 0 at time step 0**

   * Drag the **"X"** gate from the left panel
   * Drop it on the first qubit (top line) at the first column

3. **Click "Run All"**

4. **Check the results in the Probabilities tab**

You should see:

* |1⟩ with **100% probability**

The qubit started in the default state **|0⟩**, and the X gate flipped it to **|1⟩**.

### Try This

Click **Reset**, then add **two X gates**:

* X at time step 0
* X at time step 1

Run the circuit again.

Now you should see:

* |0⟩ with **100% probability**

The qubit was flipped **twice**, returning to its original state.

### Why This Matters

The **X gate** is the quantum version of a **classical bit flip**.

* |0⟩ → |1⟩
* |1⟩ → |0⟩

This gate is often used to **prepare specific states** before applying more interesting quantum operations.

---

# Guided Example: Creating Superposition with the Hadamard Gate

This example demonstrates **superposition**, one of the most important ideas in quantum computing.

### Instructions

1. **Set up the canvas with 1 qubit**

2. **Place an H (Hadamard) gate on qubit 0 at time step 0**

   * Drag **"H"** from the gate palette
   * Drop it on the first qubit at the first time column

3. **Click "Run All"**

4. **Check the results in the Probabilities tab**

You should see:

* |0⟩ with **50% probability**
* |1⟩ with **50% probability**

The Hadamard gate transformed the qubit into a **superposition state**.

### Use the Step Button

Click **Reset**, then:

1. Place the **H gate**
2. Press **Step**

Watch the **Amplitudes** and **Probabilities** tabs update immediately.

### Why This Matters

Before the gate:

* The qubit was definitely **|0⟩**

After the Hadamard:

* The qubit is **not 0 or 1**
* It is **both at the same time** until measured

This ability to exist in **multiple states simultaneously** is one of the key differences between classical and quantum computing.

---

# Guided Example: Undoing a Superposition

In quantum computing, some operations can **reverse each other**. This circuit shows that applying the **Hadamard gate twice returns the qubit to its original state**.

### Instructions

1. **Set up the canvas with 1 qubit**

2. **Place an H gate on qubit 0 at time step 0**

3. **Place another H gate on qubit 0 at time step 1**

Your circuit should look like:

```
Qubit 0:  H  →  H
```

4. **Click "Run All"**

5. **Check the Probabilities tab**

You should see:

* |0⟩ with **100% probability**

The second Hadamard **canceled the effect of the first**.

### Try Using Step

Click **Reset**, then:

1. Add both H gates
2. Press **Step** once

You will see the **50/50 superposition**.

3. Press **Step** again

The qubit returns to **|0⟩**.

### Why This Matters

Quantum gates are **reversible operations**.

In this example:

* First H → creates superposition
* Second H → returns to the original state

Understanding reversibility is important because **most quantum algorithms rely on carefully reversing intermediate operations**.

