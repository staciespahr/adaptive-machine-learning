# Noise model helpers for the phase-flip channel.
#
# This file defines a builder for a phase-flip noise model that can be used by
# higher-level simulation code.

from typing import Optional, Sequence

from qiskit_aer.noise import NoiseModel, pauli_error


def create_phase_flip_noise(
    p: float,
    basis_gates: Optional[Sequence[str]] = None,
) -> NoiseModel:
    """Build a phase-flip noise model.

    The noise model applies a Pauli Z error with probability p.
    """
    if basis_gates is None:
        basis_gates = ["h", "x"]

    noise_model = NoiseModel()
    error = pauli_error([
        ("Z", p),
        ("I", 1 - p),
    ])
    noise_model.add_all_qubit_quantum_error(error, list(basis_gates))
    return noise_model