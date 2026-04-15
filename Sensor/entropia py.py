#  ENTROPÍA POR PESOS

import numpy as np

# -----------------------------
# 1. Datos de sensores magnéticos
# -----------------------------
# Filas = sensores, columnas = criterios
# [Resolución, Ruido, Costo, ... ]

X = np.array([
    [12, 1, 2, 10, 6, 60, 2, 1, 2, 2, 5.2664],       # AS5600
    [14, 0.3, 0.7, 10, 16, 354, 2, 2, 1, 2, 2.55],   # AS5048A
    [16, 1, 2, 1, 2, 186, 1, 1, 1, 1, 6.4516]        # MLX90393
], dtype=float)


sensores = {
    0: "AS5600",
    1: "AS5048A",
    2: "MLX90393"
}

# Tipo de criterio:
# 1 = mayor es mejor
# 0 = menor es mejor
tipo = np.array([1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0])

# -----------------------------
# 2. Normalización min-max + 1
# -----------------------------
X_norm = np.zeros_like(X)

for j in range(X.shape[1]):
    col = X[:, j]
    xmin = np.min(col)
    xmax = np.max(col)

    if tipo[j] == 1:  # mayor es mejor
        X_norm[:, j] = (col - xmin) / (xmax - xmin) + 1
    else:  # menor es mejor
        X_norm[:, j] = (xmax - col) / (xmax - xmin) + 1

print("Matriz normalizada:\n", X_norm)

# -----------------------------
# 3. Probabilidades p_ij
# -----------------------------
P = X_norm / np.sum(X_norm, axis=0)
print("\nProbabilidades:\n", P)

# -----------------------------
# 4. Entropía
# -----------------------------
m = X.shape[0]
k = 1 / np.log(m)

P_log = np.where(P == 0, 1e-12, P)

E = -k * np.sum(P * np.log(P_log), axis=0)
print("\nEntropía:\n", E)

# -----------------------------
# 5. Diversidad y pesos
# -----------------------------
d = 1 - E
w = d / np.sum(d)

print("\nPesos por entropía:\n", w)

# -----------------------------
# 6. Puntaje integral
# -----------------------------
S = np.dot(X_norm, w)

print("\nPuntaje integral de cada sensor:\n", S)

# -----------------------------
# 7. Ranking
# -----------------------------
ranking = np.argsort(-S)

print("\nRanking (mejor a peor):")
for i in ranking:
    print(f"{sensores[i]} -> {S[i]:.3f}")

# 🔥 Sensor ganador
ganador = ranking[0]
print("\nEl sensor ganador es:", sensores[ganador])