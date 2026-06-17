# Depolarizing noise model helper.
#
# This module builds a Qiskit Aer depolarizing NoiseModel. The helper is
# intended for use by a higher-level noise simulator, such as
# noise_simulations.noise_simulation.

from typing import Optional, Sequence

from qiskit_aer.noise import NoiseModel, depolarizing_error


def create_depolarizing_noise(
    p: float,
    basis_gates: Optional[Sequence[str]] = None,
) -> NoiseModel:
    """Build a depolarizing noise model.

    The noise model applies a depolarizing error with probability p.
    """
    if basis_gates is None:
        basis_gates = ["h", "x"]

    noise_model = NoiseModel()
    error = depolarizing_error(p, 1)
    noise_model.add_all_qubit_quantum_error(error, list(basis_gates))
    return noise_model