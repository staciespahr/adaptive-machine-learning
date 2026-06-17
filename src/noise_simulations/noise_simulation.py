# Top-level noise simulation utilities.
#
# This module exposes a simple API for building Qiskit Aer noise models and
# running noisy circuit simulations. It delegates the actual noise-model
# construction to the helper modules in noise_simulations.noise

from typing import Optional, Sequence

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from noise_simulations.noise.bit_flip_noise import create_bit_flip_noise
from noise_simulations.noise.depolarizing_noise import create_depolarizing_noise
from noise_simulations.noise.phase_flip_noise import create_phase_flip_noise

# Map a friendly noise type name to the helper that builds that noise model.
NOISE_CREATORS = {
    "bit_flip": create_bit_flip_noise,
    "phase_flip": create_phase_flip_noise,
    "depolarizing": create_depolarizing_noise,
}


def create_noise_model(
    noise_type: str,
    p: float,
    basis_gates: Optional[Sequence[str]] = None,
):
    """Create a Qiskit noise model for the requested noise type.

    Args:
        noise_type: One of 'bit_flip', 'phase_flip', or 'depolarizing'.
        p: Error probability for the noise channel.
        basis_gates: Optional list of gates the noise should apply to.

    Returns:
        A qiskit_aer NoiseModel instance.
    """
    noise_type = noise_type.lower()
    if noise_type not in NOISE_CREATORS:
        supported = ", ".join(sorted(NOISE_CREATORS))
        raise ValueError(
            f"Unsupported noise type {noise_type!r}. Supported types: {supported}"
        )

    return NOISE_CREATORS[noise_type](p=p, basis_gates=basis_gates)


def simulate_noise(
    circuit: QuantumCircuit,
    noise_type: str = "bit_flip",
    p: float = 0.1,
    shots: int = 1024,
    basis_gates: Optional[Sequence[str]] = None,
):
    """Run a noisy simulation on the given quantum circuit.

    Args:
        circuit: The QuantumCircuit to simulate.
        noise_type: The noise model to apply.
        p: Noise probability parameter.
        shots: Number of measurement samples.
        basis_gates: Optional gates to which the noise applies.

    Returns:
        A dictionary of measurement counts from the simulation.
    """
    noise_model = create_noise_model(noise_type, p, basis_gates=basis_gates)
    simulator = AerSimulator(noise_model=noise_model)
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled, shots=shots).result()
    return result.get_counts()


def sample_bb84_circuit() -> QuantumCircuit:
    """Create a simple one-qubit BB84-style test circuit.

    This circuit uses a Hadamard gate to place the qubit in the X basis,
    then measures it into a classical bit.
    """
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit


