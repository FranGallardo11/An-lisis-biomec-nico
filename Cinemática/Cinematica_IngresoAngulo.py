import numpy as np
import matplotlib.pyplot as plt

# Longitudes de las falanges (en cm)
l1 = 5.7  # proximal
l2 = 3.2  # media
l3 = 2.3  # distal

# Ángulos en grados (pueden ser modificados)
theta1_deg = 0    # abducción/adducción (plano XY)
theta2_deg = 10    # flexión MCP (metacarpofalángica)
theta3_deg = 50    # flexión PIP (interfalángica proximal)
theta4_deg = 70    # flexión DIP (interfalángica distal)

# Conversión a radianes
theta1 = np.deg2rad(theta1_deg)
theta2 = np.deg2rad(theta2_deg)
theta3 = np.deg2rad(theta3_deg)
theta4 = np.deg2rad(theta4_deg)

# Posiciones articulaciones
x0, y0, z0 = 0, 0, 0
x1 = l1 * np.cos(theta2) * np.cos(theta1)
y1 = l1 * np.cos(theta2) * np.sin(theta1)
z1 = l1 * np.sin(theta2)

x2 = x1 + l2 * np.cos(theta2 + theta3) * np.cos(theta1)
y2 = y1 + l2 * np.cos(theta2 + theta3) * np.sin(theta1)
z2 = z1 + l2 * np.sin(theta2 + theta3)

x3 = x2 + l3 * np.cos(theta2 + theta3 + theta4) * np.cos(theta1)
y3 = y2 + l3 * np.cos(theta2 + theta3 + theta4) * np.sin(theta1)
z3 = z2 + l3 * np.sin(theta2 + theta3 + theta4)

# Visualización
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot([x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3],
        '-o', linewidth=3, markersize=6, color='purple')

# Etiquetas de huesos y ángulos
ax.text(x0, y0, z0, "Base MCP", color='black')
ax.text(x1, y1, z1, f"Proximal\nθ2={theta2_deg}°", color='blue')
ax.text(x2, y2, z2, f"Media\nθ3={theta3_deg}°", color='green')
ax.text(x3, y3, z3, f"Distal\nθ4={theta4_deg}°", color='red')

# Título y ejes
ax.set_title(f"Dedo pulgar con etiquetas de huesos y ángulos")
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_zlabel("Z (cm)")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(0, 10)
ax.view_init(elev=20, azim=45)
plt.tight_layout()
plt.show()
