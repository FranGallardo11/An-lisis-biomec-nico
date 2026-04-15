import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt

# Longitudes de las falanges (cm)
l1 = 0.15   # proximal
l2 = 0.10  # media
# l3 = 2.3  # distal

# Ángulos articulares (en grados)
theta1_deg = 0  # abducción
theta2_deg = 30  # flexión MCP
theta3_deg = 45  # flexión PIP
# theta4_deg = 50  # flexión DIP

# Convertir a radianes
theta1 = np.deg2rad(theta1_deg)
theta2 = np.deg2rad(theta2_deg)
theta3 = np.deg2rad(theta3_deg)
# theta4 = np.deg2rad(theta4_deg)

# Función para matriz de transformación D-H
def dh_matrix(theta, d, a, alpha):
    return np.array([
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,           sin(alpha),             cos(alpha),            d],
        [0,           0,                      0,                     1]
    ])

# Matrices de cada articulación
# T1 = dh_matrix(theta1, 0,     0,  np.pi/2)  # abducción
T2 = dh_matrix(theta2, 0,    l1,  0)        # flexión MCP
T3 = dh_matrix(theta3, 0,    l2,  0)        # flexión PIP
# T4 = dh_matrix(theta4, 0,    l3,  0)        # flexión DIP

# Transformación total
T = T2 @ T3 #@ T4

# Posición de la punta del dedo (x, y, z)
position = T[:3, 3]
print("Posición de la punta del dedo (cm):")
print(f"x = {position[0]:.2f}, y = {position[1]:.2f}, z = {position[2]:.2f}")
