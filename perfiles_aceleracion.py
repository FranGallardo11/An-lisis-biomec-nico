import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Parámetros del movimiento
# ==========================================

tf = 0.6              # tiempo total (s)
dt = 0.001            # paso temporal
t = np.arange(0, tf + dt, dt)
s = t / tf            # tiempo normalizado

# ==========================================
# 2. Ángulos iniciales y finales (rad)
# Movimiento tipo pinza
# ==========================================

q0 = np.array([0.0, 0.0, 0.0])

qf = np.array([
    np.deg2rad(40),   # MCP
    np.deg2rad(60),   # PIP
    np.deg2rad(35)    # DIP
])

labels = ['MCP', 'PIP', 'DIP']

# ==========================================
# 3. Perfil mínimo jerk (quíntico)
# ==========================================

def quintic_profile(q0, qf, s, tf):
    dq = qf - q0
    
    q = q0 + dq * (10*s**3 - 15*s**4 + 6*s**5)
    q_dot = (dq/tf) * (30*s**2 - 60*s**3 + 30*s**4)
    q_ddot = (dq/tf**2) * (60*s - 180*s**2 + 120*s**3)
    
    return q, q_dot, q_ddot

# ==========================================
# 4. Generar trayectoria articular
# ==========================================

q = np.zeros((len(t), 3))
q_dot = np.zeros((len(t), 3))
q_ddot = np.zeros((len(t), 3))

for i in range(3):
    q[:, i], q_dot[:, i], q_ddot[:, i] = quintic_profile(q0[i], qf[i], s, tf)

# ==========================================
# 5. Gráficas articulares
# ==========================================

for i in range(3):
    plt.figure()
    plt.plot(t, np.rad2deg(q[:, i]))
    plt.title(f"Posición articular - {labels[i]}")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Ángulo (deg)")
    plt.grid()
    plt.show()

for i in range(3):
    plt.figure()
    plt.plot(t, np.rad2deg(q_dot[:, i]))
    plt.title(f"Velocidad articular - {labels[i]}")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Velocidad (deg/s)")
    plt.grid()
    plt.show()

for i in range(3):
    plt.figure()
    plt.plot(t, np.rad2deg(q_ddot[:, i]))
    plt.title(f"Aceleración articular - {labels[i]}")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Aceleración (deg/s²)")
    plt.grid()
    plt.show()

# ==========================================
# 6. Parámetros geométricos del dedo
# ==========================================

L1 = 0.05   # falange proximal (m)
L2 = 0.03   # falange media (m)
L3 = 0.02   # falange distal (m)

# ==========================================
# 7. Cinemática directa
# ==========================================

x = np.zeros(len(t))
y = np.zeros(len(t))

for k in range(len(t)):
    
    q1 = q[k, 0]
    q2 = q[k, 1]
    q3 = q[k, 2]
    
    x[k] = (L1*np.cos(q1) +
            L2*np.cos(q1 + q2) +
            L3*np.cos(q1 + q2 + q3))
    
    y[k] = (L1*np.sin(q1) +
            L2*np.sin(q1 + q2) +
            L3*np.sin(q1 + q2 + q3))

# ==========================================
# 8. Trayectoria cartesiana del extremo
# ==========================================

plt.figure()
plt.plot(x, y)
plt.title("Trayectoria cartesiana del extremo del dedo")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis('equal')
plt.grid()
plt.show()

# ==========================================
# 9. Visualización de posturas intermedias
# ==========================================

plt.figure()

steps = np.linspace(0, len(t)-1, 6, dtype=int)

for k in steps:
    
    q1 = q[k, 0]
    q2 = q[k, 1]
    q3 = q[k, 2]
    
    x1 = L1*np.cos(q1)
    y1 = L1*np.sin(q1)
    
    x2 = x1 + L2*np.cos(q1+q2)
    y2 = y1 + L2*np.sin(q1+q2)
    
    x3 = x2 + L3*np.cos(q1+q2+q3)
    y3 = y2 + L3*np.sin(q1+q2+q3)
    
    plt.plot([0, x1, x2, x3],
             [0, y1, y2, y3])

plt.title("Posturas del dedo durante movimiento de pinza")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis('equal')
plt.grid()
plt.show()
