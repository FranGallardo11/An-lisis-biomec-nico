import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# PARÁMETROS DEL SISTEMA
# =============================================================================

L1, L2, L3 = 1.0, 1.0, 1.0
m1, m2, m3 = 1.0, 1.0, 1.0
Izz1, Izz2, Izz3 = 0.2, 0.2, 0.2
g = 9.81

# Estados
q1_vals = np.linspace(-np.pi/2, np.pi/2, 10)
q2_vals = np.linspace(-np.pi/4, np.pi/4, 8)
q3_vals = np.linspace(-np.pi/6, np.pi/6, 6)

q_dot = np.array([[0.5],
                  [0.3],
                  [0.2]])

q_ddot = np.array([[0.1],
                   [0.05],
                   [0.02]])

# =============================================================================
# POSICIONES DE LOS CENTROS DE MASA
# =============================================================================

def posiciones(q):
    q1, q2, q3 = q.flatten()

    p1 = np.array([[L1*np.cos(q1)],
                   [L1*np.sin(q1)]])

    p2 = np.array([[L1*np.cos(q1)+L2*np.cos(q1+q2)],
                   [L1*np.sin(q1)+L2*np.sin(q1+q2)]])

    p3 = np.array([[L1*np.cos(q1)+L2*np.cos(q1+q2)+L3*np.cos(q1+q2+q3)],
                   [L1*np.sin(q1)+L2*np.sin(q1+q2)+L3*np.sin(q1+q2+q3)]])

    return p1, p2, p3

# =============================================================================
# JACOBIANOS LINEALES
# =============================================================================

def jacobianos(q):
    q1, q2, q3 = q.flatten()

    Jv1 = np.array([
        [-L1*np.sin(q1), 0, 0],
        [ L1*np.cos(q1), 0, 0]
    ])

    Jv2 = np.array([
        [-L1*np.sin(q1)-L2*np.sin(q1+q2), -L2*np.sin(q1+q2), 0],
        [ L1*np.cos(q1)+L2*np.cos(q1+q2),  L2*np.cos(q1+q2), 0]
    ])

    Jv3 = np.array([
        [-L1*np.sin(q1)-L2*np.sin(q1+q2)-L3*np.sin(q1+q2+q3),
         -L2*np.sin(q1+q2)-L3*np.sin(q1+q2+q3),
         -L3*np.sin(q1+q2+q3)],

        [ L1*np.cos(q1)+L2*np.cos(q1+q2)+L3*np.cos(q1+q2+q3),
          L2*np.cos(q1+q2)+L3*np.cos(q1+q2+q3),
          L3*np.cos(q1+q2+q3)]
    ])

    return Jv1, Jv2, Jv3

# =============================================================================
# MATRIZ DE INERCIA M(q)
# =============================================================================

def matriz_inercia(q):
    Jv1, Jv2, Jv3 = jacobianos(q)

    Jw1 = np.array([[1, 0, 0]])
    Jw2 = np.array([[1, 1, 0]])
    Jw3 = np.array([[1, 1, 1]])

    I1 = np.array([[Izz1]])
    I2 = np.array([[Izz2]])
    I3 = np.array([[Izz3]])

    M  = m1*(Jv1.T @ Jv1) + Jw1.T @ I1 @ Jw1
    M += m2*(Jv2.T @ Jv2) + Jw2.T @ I2 @ Jw2
    M += m3*(Jv3.T @ Jv3) + Jw3.T @ I3 @ Jw3

    return M

# =============================================================================
# CORIOLIS POR CHRISTOFFEL
# =============================================================================

def coriolis(q, q_dot, eps=1e-6):
    n = len(q)
    C = np.zeros((n,1))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                dq = np.zeros((n,1))
                dq[k] = eps

                dM = (matriz_inercia(q + dq) - matriz_inercia(q - dq)) / (2*eps)

                gamma = 0.5 * (
                    dM[i,j] + dM[i,k] - dM[j,k]
                )

                C[i] += gamma * q_dot[j] * q_dot[k]

    return C

# =============================================================================
# GRAVEDAD
# =============================================================================

def gravedad(q):
    _, p2, p3 = posiciones(q)
    q1, q2, q3 = q.flatten()

    G1 = g*(m1*L1*np.cos(q1) +
            m2*(L1*np.cos(q1)) +
            m3*(L1*np.cos(q1)))

    G2 = g*(m2*L2*np.cos(q1+q2) +
            m3*(L2*np.cos(q1+q2)))

    G3 = g*(m3*L3*np.cos(q1+q2+q3))

    return np.array([[G1],[G2],[G3]])

# =============================================================================
# TORQUE DINÁMICO
# =============================================================================

def torque(q, q_dot, q_ddot):
    M = matriz_inercia(q)
    C = coriolis(q, q_dot)
    G = gravedad(q)

    tau = M @ q_ddot + C + G
    
    return tau

# =============================================================================
# EJECUCIÓN
# =============================================================================


torques = []
# -----------------------------
# Ejecución del barrido
# -----------------------------
for q1 in q1_vals:
    for q2 in q2_vals:
        for q3 in q3_vals:

            q = np.array([[q1],
                          [q2],
                          [q3]])

            M = matriz_inercia(q)
            C = coriolis(q, q_dot)
            G = gravedad(q)
            tau = torque(q, q_dot, q_ddot)

            
            torques.append(tau)

T = np.hstack(torques)
print("Dimensión:", T.shape)


print("\nTorque total τ:\n", T)



# =============================================================================
# GRÁFICA
# =============================================================================


# Índice de muestras
n = T.shape[1]
x = np.arange(n)

plt.figure(figsize=(12, 6))

# Graficar los torques
plt.plot(x, T[0, :], 'b', label='Torque 1')
plt.plot(x, T[1, :], 'r', label='Torque 2')
plt.plot(x, T[2, :], 'g', label='Torque 3')

# Calcular máximos y mínimos
max_torques = np.max(T, axis=1)
min_torques = np.min(T, axis=1)

# Índices de máximos y mínimos por fila
idx_max = np.argmax(T, axis=1)
idx_min = np.argmin(T, axis=1)

# Marcar máximos y mínimos
plt.scatter(idx_max[0], max_torques[0], color='b', marker='o', s=80, label='Max Torque 1')
plt.scatter(idx_min[0], min_torques[0], color='b', marker='x', s=80, label='Min Torque 1')

plt.scatter(idx_max[1], max_torques[1], color='r', marker='o', s=80, label='Max Torque 2')
plt.scatter(idx_min[1], min_torques[1], color='r', marker='x', s=80, label='Min Torque 2')

plt.scatter(idx_max[2], max_torques[2], color='g', marker='o', s=80, label='Max Torque 3')
plt.scatter(idx_min[2], min_torques[2], color='g', marker='x', s=80, label='Min Torque 3')

# Etiquetas y leyenda
plt.xlabel('Índice de estado (barrido de q)')
plt.ylabel('Torque [Nm]')
plt.title('Torques articulares con máximos y mínimos')
plt.grid(True)
plt.legend(loc='upper right', fontsize=9)

plt.show()
