"""Example usage of the noise simulator module.

This file demonstrates how to:
1. Build a quantum circuit
2. Add noise to the simulation
3. Run the simulation and inspect results
"""

from qiskit import QuantumCircuit

# Import from the parent package
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from noise_simulations.noise_simulation import simulate_noise, sample_bb84_circuit


def example_1_simple_circuit():
    """Example 1: Simulate a simple one-qubit circuit with bit-flip noise."""
    print("\n" + "=" * 60)
    print("Example 1: Simple circuit with bit-flip noise")
    print("=" * 60)

    circuit = sample_bb84_circuit()
    print(f"Circuit:\n{circuit}")

    # Run with bit-flip noise (p=0.1 means 10% error probability)
    counts = simulate_noise(
        circuit,
        noise_type="bit_flip",
        p=0.1,
        shots=1000,
    )
    print(f"\nResults (1000 shots, p=0.1):\n{counts}")


def example_2_different_noise_types():
    """Example 2: Compare different noise models on the same circuit."""
    print("\n" + "=" * 60)
    print("Example 2: Compare noise types")
    print("=" * 60)

    circuit = sample_bb84_circuit()

    noise_types = ["bit_flip", "phase_flip", "depolarizing"]
    p = 0.05

    for noise_type in noise_types:
        counts = simulate_noise(circuit, noise_type=noise_type, p=p, shots=1000)
        print(f"\n{noise_type.upper()} (p={p}):")
        print(f"  {counts}")


def example_3_varying_error_rates():
    """Example 3: See how error rate affects measurement results."""
    print("\n" + "=" * 60)
    print("Example 3: Varying error probability")
    print("=" * 60)

    circuit = sample_bb84_circuit()
    error_rates = [0.0, 0.05, 0.1, 0.2, 0.5]

    print("\nBit-flip noise with varying error rates (p):")
    for p in error_rates:
        counts = simulate_noise(circuit, noise_type="bit_flip", p=p, shots=1000)
        print(f"  p={p}: {counts}")


def example_4_custom_circuit():
    """Example 4: Create a custom circuit and simulate it."""
    print("\n" + "=" * 60)
    print("Example 4: Custom circuit (2-qubit)")
    print("=" * 60)

    # Build a 2-qubit circuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)  # CNOT gate
    circuit.measure([0, 1], [0, 1])

    print(f"Circuit:\n{circuit}")

    counts = simulate_noise(
        circuit,
        noise_type="depolarizing",
        p=0.1,
        shots=1000,
    )
    print(f"\nResults with depolarizing noise:\n{counts}")


if __name__ == "__main__":
    print("Noise Simulator Examples")
    print("=" * 60)

    example_1_simple_circuit()
    example_2_different_noise_types()
    example_3_varying_error_rates()
    example_4_custom_circuit()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
