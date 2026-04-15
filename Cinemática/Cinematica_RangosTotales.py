import numpy as np
import matplotlib.pyplot as plt

# Longitudes de las falanges (en cm por ejemplo)
l1_val = 5.7  # falange proximal
l2_val = 3.2  # falange media
l3_val = 2.3  # falange distal

# Rango de ángulos para θ1 (abducción), θ2, θ3, θ4 (flexiones)
theta1_vals = np.deg2rad(np.linspace(0, 0, 100))   # abducción/adducción
theta2_vals = np.deg2rad(np.linspace(-10, 70, 10))      # flexión MCP
theta3_vals = np.deg2rad(np.linspace(-10, 100, 10))      # flexión PIP
theta4_vals = np.deg2rad(np.linspace(-10, 80, 10))      # flexión DIP

# Almacenar posiciones
positions = []

for theta1 in theta1_vals:
    for theta2 in theta2_vals:
        for theta3 in theta3_vals:
            for theta4 in theta4_vals:
                # Cinemática directa
                x = (l1_val * np.cos(theta2) + 
                     l2_val * np.cos(theta2 + theta3) + 
                     l3_val * np.cos(theta2 + theta3 + theta4)) * np.cos(theta1)
                
                y = (l1_val * np.cos(theta2) + 
                     l2_val * np.cos(theta2 + theta3) + 
                     l3_val * np.cos(theta2 + theta3 + theta4)) * np.sin(theta1)
                
                z = (l1_val * np.sin(theta2) + 
                     l2_val * np.sin(theta2 + theta3) + 
                     l3_val * np.sin(theta2 + theta3 + theta4))
                
                positions.append([x, y, z])

positions = np.array(positions)



# # Longitudes de las falanges (en cm por ejemplo)
# l1_val2 = 3.23  # falange proximal
# l2_val2 = 2.52  # falange media
# l3_val2 = 2.48  # falange distal

# # Rango de ángulos para θ1 (abducción), θ2, θ3, θ4 (flexiones)
# theta12_vals = np.deg2rad(np.linspace(0, 0, 100))   # abducción/adducción
# theta22_vals = np.deg2rad(np.linspace(0, 90, 10))      # flexión MCP
# theta32_vals = np.deg2rad(np.linspace(0, 100, 10))      # flexión PIP
# theta42_vals = np.deg2rad(np.linspace(0, 60, 10))      # flexión DIP

# # Almacenar posiciones
# positions2 = []

# for theta12 in theta12_vals:
#     for theta22 in theta22_vals:
#         for theta32 in theta32_vals:
#             for theta42 in theta42_vals:
#                 # Cinemática directa
#                 x2 = (l1_val2 * np.cos(theta22) + 
#                      l2_val2 * np.cos(theta22 + theta32) + 
#                      l3_val2 * np.cos(theta22 + theta32 + theta42)) * np.cos(theta12)
                
#                 y2 = (l1_val2 * np.cos(theta22) + 
#                      l2_val2 * np.cos(theta22 + theta32) + 
#                      l3_val2 * np.cos(theta22 + theta32 + theta42)) * np.sin(theta12)+1
                
#                 z2 = (l1_val2 * np.sin(theta2) + 
#                      l2_val2 * np.sin(theta22 + theta32) + 
#                      l3_val2 * np.sin(theta22 + theta32 + theta42))
                
#                 positions2.append([x2, y2, z2])

# positions2 = np.array(positions2)

# Visualización 3D del espacio alcanzable
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=5, c='blue', alpha=0.6)
ax.set_title("Espacio alcanzable de la punta del dedo medio")
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_zlabel("Z (cm)")
ax.view_init(elev=20, azim=45)
plt.tight_layout()
plt.show()

# Visualización 3D del espacio alcanzable


# ax.scatter(positions2[:, 0], positions2[:, 1], positions2[:, 2], s=5, c='cyan', alpha=0.6)
# ax.set_title("Espacio alcanzable de la punta del dedo índice")
# ax.set_xlabel("X (cm)")
# ax.set_ylabel("Y (cm)")
# ax.set_zlabel("Z (cm)")
# ax.view_init(elev=20, azim=45)
# plt.tight_layout()
# # plt.show()

