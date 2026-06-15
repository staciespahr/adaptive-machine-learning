# -----------------------------
# BB84 Quantum Circuit Simulation with Scikit-learn
# -----------------------------

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# -----------------------------
# SETTINGS
# -----------------------------
N = 5000  # number of qubits / data points
EVE_PRESENT = True  # change to False to remove eavesdropper
np.random.seed(42)
random.seed(42)

backend = Aer.get_backend("qasm_simulator")


# -----------------------------
# RANDOM BB84 DATA
# -----------------------------

# Alice randomly chooses bits: 0 or 1
alice_bits = np.random.randint(2, size=N)

# Alice randomly chooses bases:
# 0 = Z basis
# 1 = X basis
alice_bases = np.random.randint(2, size=N)

# Bob randomly chooses bases:
# 0 = Z basis
# 1 = X basis
bob_bases = np.random.randint(2, size=N)

# Eve randomly chooses bases if present
eve_bases = np.random.randint(2, size=N) if EVE_PRESENT else np.full(N, -1)

bob_results = []
eve_results = []


# -----------------------------
# BB84 CIRCUIT SIMULATION
# -----------------------------
for i in range(N):
    q = QuantumRegister(1, "q")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q, c)

    # Alice prepares her bit
    if alice_bits[i] == 1:
        qc.x(q[0])

    # Alice prepares in X basis if chosen
    if alice_bases[i] == 1:
        qc.h(q[0])

    # Eve intercepts and measures
    if EVE_PRESENT:
        # Eve measures in X basis if chosen
        if eve_bases[i] == 1:
            qc.h(q[0])

        qc.measure(q[0], c[0])

        compiled_eve = transpile(qc, backend)
        eve_job = backend.run(compiled_eve, shots=1)
        eve_result = eve_job.result().get_counts()
        eve_bit = int(list(eve_result.keys())[0])
        eve_results.append(eve_bit)

        # Rebuild circuit after Eve measurement because Eve resends a new qubit
        qc = QuantumCircuit(q, c)

        # Eve resends measured bit
        if eve_bit == 1:
            qc.x(q[0])

        # Eve resends in her chosen basis
        if eve_bases[i] == 1:
            qc.h(q[0])

    else:
        eve_results.append(-1)

    # Bob measures in X basis if chosen
    if bob_bases[i] == 1:
        qc.h(q[0])

    qc.measure(q[0], c[0])

    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=1)
    result = job.result().get_counts()

    bob_bit = int(list(result.keys())[0])
    bob_results.append(bob_bit)


bob_results = np.array(bob_results)
eve_results = np.array(eve_results)


# -----------------------------
# BASIS COMPARISON
# -----------------------------
bases_match = alice_bases == bob_bases

alice_key = alice_bits[bases_match]
bob_key = bob_results[bases_match]

key_matches = alice_key == bob_key
key_accuracy = np.mean(key_matches) * 100

error_rate = 100 - key_accuracy


# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame({
    "index": np.arange(N),
    "alice_bit": alice_bits,
    "alice_basis": alice_bases,
    "bob_basis": bob_bases,
    "eve_basis": eve_bases,
    "eve_result": eve_results,
    "bob_result": bob_results,
    "bases_match": bases_match.astype(int),
})

df["alice_basis_label"] = df["alice_basis"].map({0: "Z", 1: "X"})
df["bob_basis_label"] = df["bob_basis"].map({0: "Z", 1: "X"})
df["eve_basis_label"] = df["eve_basis"].map({0: "Z", 1: "X", -1: "None"})

df["bob_correct"] = (df["alice_bit"] == df["bob_result"]).astype(int)

df.to_csv("bb84_full_dataset.csv", index=False)


# -----------------------------
# FINAL KEY DATAFRAME
# -----------------------------
key_df = pd.DataFrame({
    "alice_key_bit": alice_key,
    "bob_key_bit": bob_key,
    "match": key_matches.astype(int)
})

key_df.to_csv("bb84_final_key.csv", index=False)


# -----------------------------
# SCIKIT-LEARN MODEL
# Predict whether Alice and Bob used the same basis
# -----------------------------
features = df[[
    "alice_bit",
    "alice_basis",
    "bob_basis",
    "eve_basis",
    "eve_result",
    "bob_result"
]]

target = df["bases_match"]

X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.25,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

ml_accuracy = accuracy_score(y_test, predictions)


# -----------------------------
# PRINT SUMMARY
# -----------------------------
print("BB84 Simulation Complete")
print("------------------------")
print(f"Total qubits sent: {N}")
print(f"Eve present: {EVE_PRESENT}")
print(f"Matching bases: {np.sum(bases_match)}")
print(f"Final key length: {len(alice_key)}")
print(f"Alice/Bob key accuracy: {key_accuracy:.2f}%")
print(f"Quantum bit error rate: {error_rate:.2f}%")
print()
print("Scikit-learn Model Results")
print("--------------------------")
print(f"ML model accuracy predicting basis match: {ml_accuracy:.2f}")
print()
print("Classification Report:")
print(classification_report(y_test, predictions))
print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))
print()
print("First 20 BB84 data points:")
print(df.head(20))
print()
print("First 20 final key bits:")
print(key_df.head(20))


# -----------------------------
# BASIC VISUALIZATION
# -----------------------------
basis_counts = df["bases_match"].value_counts()

plt.figure(figsize=(6, 4))
basis_counts.plot(kind="bar")
plt.title("BB84 Basis Match Counts")
plt.xlabel("Bases Match? 0 = No, 1 = Yes")
plt.ylabel("Count")
plt.tight_layout()
plt.show()