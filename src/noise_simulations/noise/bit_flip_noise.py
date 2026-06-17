# Noise model helpers for the bit-flip channel.
#
# This file defines a builder for a bit-flip noise model that can be used by
# higher-level simulation code.


from typing import Optional, Sequence

from qiskit_aer.noise import NoiseModel, pauli_error


def create_bit_flip_noise(
    p: float,
    basis_gates: Optional[Sequence[str]] = None,
) -> NoiseModel:
    """Build a bit-flip noise model.

    The noise model flips qubits with probability p using the Pauli X error.
    """
    if basis_gates is None:
        basis_gates = ["h", "x"]

    noise_model = NoiseModel()
    error = pauli_error([
        ("X", p),
        ("I", 1 - p),
    ])
    noise_model.add_all_qubit_quantum_error(error, list(basis_gates))
    return noise_model