import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. PERFIL QUÍNTICO (TRAYECTORIA)
# =============================================================================

tf = 0.6
dt = 0.001
t = np.arange(0, tf + dt, dt)
s = t / tf

q0 = np.array([0.0, 0.0, 0.0])
qf = np.array([
    np.deg2rad(40),
    np.deg2rad(60),
    np.deg2rad(35)
])

def quintic_profile(q0, qf, s, tf):
    dq = qf - q0
    q = q0 + dq * (10*s**3 - 15*s**4 + 6*s**5)
    q_dot = (dq/tf) * (30*s**2 - 60*s**3 + 30*s**4)
    q_ddot = (dq/tf**2) * (60*s - 180*s**2 + 120*s**3)
    return q, q_dot, q_ddot

q = np.zeros((len(t), 3))
q_dot = np.zeros((len(t), 3))
q_ddot = np.zeros((len(t), 3))

for i in range(3):
    q[:, i], q_dot[:, i], q_ddot[:, i] = quintic_profile(q0[i], qf[i], s, tf)

# =============================================================================
# 2. PARÁMETROS DINÁMICOS
# =============================================================================

L1, L2, L3 = 0.05, 0.03, 0.02
m1, m2, m3 = 0.02, 0.015, 0.01
Izz1, Izz2, Izz3 = 1e-5, 8e-6, 5e-6
g = 9.81

# =============================================================================
# 3. JACOBIANOS
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
# 4. MATRIZ DE INERCIA
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
# 5. CORIOLIS NUMÉRICO
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

                gamma = 0.5 * (dM[i,j] + dM[i,k] - dM[j,k])
                C[i] += gamma * q_dot[j] * q_dot[k]

    return C

# =============================================================================
# 6. GRAVEDAD
# =============================================================================

def gravedad(q):
    q1, q2, q3 = q.flatten()

    G1 = g*(m1*L1*np.cos(q1) +
            m2*(L1*np.cos(q1)) +
            m3*(L1*np.cos(q1)))

    G2 = g*(m2*L2*np.cos(q1+q2) +
            m3*(L2*np.cos(q1+q2)))

    G3 = g*(m3*L3*np.cos(q1+q2+q3))

    return np.array([[G1],[G2],[G3]])

# =============================================================================
# 7. TORQUE A LO LARGO DE LA TRAYECTORIA
# =============================================================================

tau_total = np.zeros((3, len(t)))

for k in range(len(t)):
    
    qk = q[k,:].reshape(3,1)
    qdk = q_dot[k,:].reshape(3,1)
    qddk = q_ddot[k,:].reshape(3,1)
    
    M = matriz_inercia(qk)
    C = coriolis(qk, qdk)
    G = gravedad(qk)
    
    tau = M @ qddk + C + G
    
    tau_total[:, k] = tau.flatten()

# =============================================================================
# 8. TORQUES MÁXIMOS Y MÍNIMOS
# =============================================================================

max_mcp = np.max(tau_total[0,:])
min_mcp = np.min(tau_total[0,:])
max_pip = np.max(tau_total[1,:])
min_pip = np.min(tau_total[1,:])
max_dip = np.max(tau_total[2,:])
min_dip = np.min(tau_total[2,:])

print("\n===== TORQUES =====")
print("MCP max:", max_mcp, "min:", min_mcp)
print("PIP max:", max_pip, "min:", min_pip)
print("DIP max:", max_dip, "min:", min_dip)

# Índices para graficar
i_max_mcp = np.argmax(tau_total[0,:])
i_min_mcp = np.argmin(tau_total[0,:])
i_max_pip = np.argmax(tau_total[1,:])
i_min_pip = np.argmin(tau_total[1,:])
i_max_dip = np.argmax(tau_total[2,:])
i_min_dip = np.argmin(tau_total[2,:])


# =============================================================================
# 9. GRÁFICA DE TORQUES
# =============================================================================

plt.figure(figsize=(10,6))

plt.plot(t, tau_total[0,:], label='Torque MCP')
plt.plot(t, tau_total[1,:], label='Torque PIP')
plt.plot(t, tau_total[2,:], label='Torque DIP')

# Puntos máximos y mínimos
plt.scatter(t[i_max_mcp], max_mcp, color='green')
plt.scatter(t[i_min_mcp], min_mcp, color='red')

plt.scatter(t[i_max_pip], max_pip, color='green')
plt.scatter(t[i_min_pip], min_pip, color='red')

plt.scatter(t[i_max_dip], max_dip, color='green')
plt.scatter(t[i_min_dip], min_dip, color='red')


plt.xlabel('Tiempo (s)')
plt.ylabel('Torque (Nm)')
plt.title('Torques articulares durante movimiento de pinza')
plt.grid()
plt.legend()
plt.show()

# =============================================================================
# 10. TORQUE RMS
# =============================================================================

tau_rms_mcp = np.sqrt(np.mean(tau_total[0,:]**2))
tau_rms_pip = np.sqrt(np.mean(tau_total[1,:]**2))
tau_rms_dip = np.sqrt(np.mean(tau_total[2,:]**2))

print("\n===== TORQUE RMS =====")
print("MCP:", tau_rms_mcp)
print("PIP:", tau_rms_pip)
print("DIP:", tau_rms_dip)

# Gráfica de barras
labels = ['MCP', 'PIP', 'DIP']
rms_values = [tau_rms_mcp, tau_rms_pip, tau_rms_dip]

plt.figure()
plt.bar(labels, rms_values)
plt.ylabel('Torque RMS (Nm)')
plt.title('Esfuerzo promedio de cada articulación')
plt.grid(axis='y')
plt.show()


# =============================================================================
# 10. TORQUE RMS acumulado en el tiempo
# =============================================================================


rms_time_mcp = np.sqrt(np.cumsum(tau_total[0,:]**2) / np.arange(1, len(t)+1))
rms_time_pip = np.sqrt(np.cumsum(tau_total[1,:]**2) / np.arange(1, len(t)+1))
rms_time_dip = np.sqrt(np.cumsum(tau_total[2,:]**2) / np.arange(1, len(t)+1))

plt.figure()
plt.plot(t, rms_time_mcp, label='MCP')
plt.plot(t, rms_time_pip, label='PIP')
plt.plot(t, rms_time_dip, label='DIP')

plt.xlabel('Tiempo (s)')
plt.ylabel('Torque RMS acumulado')
plt.title('Evolución del esfuerzo durante la pinza')
plt.legend()
plt.grid()
plt.show()

# =============================================================================
# 10. TORQUE a considerar
# =============================================================================

maxtorque = max_mcp * 1.3
maxrms = tau_rms_mcp * 1.3

print("\n===== TORQUES para motor =====")
print("Torque con 30% :   ", maxtorque)
print("Torque rms con 30::", maxrms)

