#     Modelo Dinámico
#   Numérico 2 eslabones

import numpy as np

# ==================== VARIABLES =============================================



# =============================================================================
#                      MATRIZ DE INERCIA
# =============================================================================


# ==================== POSICIONES =============================================

def posicion(theta1, theta2, L1, L2):
    x = np.array([
        [L1 * np.cos(theta1)],
        [L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)]
    ])

    y = np.array([
        [L1 * np.sin(theta1)],
        [L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)]
    ])

    return x, y

L1 = 1
L2 = 1
q1 = np.deg2rad(-3.9650)
q2 = np.deg2rad(118.04)

(x, y) = posicion(q1, q2, L1, L2)

posiciones = np.array([ 
    [x[0],y[0]],
    [x[1],y[1]]
    ])
print('Posiciones S1 = ', posiciones[0])
print('Posiciones S2 = ', posiciones[1])
print('')

# ==================== VELOCIDADES ============================================

q_dot = np.array([
    [1],
    [1]
    ])

def velocidad(theta1, theta2, L1, L2, q_dot):
    s1_dot = np.array([
        [-L1 * np.sin(theta1) * q_dot[0]],
        [L1 * np.cos(theta1) * q_dot[0]]
    ])

    s2_dot = np.array([
        [-L1 * np.sin(theta1) * q_dot[0] -L2 * np.sin(theta1 + theta2) * (q_dot[0] + q_dot[1])],
        [L1 * np.cos(theta1) * q_dot[0] + L2 * np.cos(theta1 + theta2) * (q_dot[0] + q_dot[1])]
    ])

    return s1_dot, s2_dot

(Vc1,Vc2) = velocidad(q1, q2, L1, L2, q_dot)

print('Velocidades S1 = ', Vc1)
print('Velocidades S2 = ', Vc2)
print('')

# ==================== JACOBIANOS =============================================

def jacobianos(theta1, theta2, L1, L2):
    Jvc1 = np.array([
        [-L1 * np.sin(q1), 0],
        [L1 * np.cos(q1), 0]
        ])

    Jvc2 = np.array([
        [-L1 * np.sin(q1) -L2 * np.sin(q1 + q2), -L2 * np.sin(q1 + q2)],
        [L1 * np.cos(q1) +L2 * np.cos(q1 + q2), L2 * np.cos(q1 + q2)]
        ])
    
    return Jvc1, Jvc2

(Jvc1, Jvc2) = jacobianos(q1, q2, L1, L2)

print('Jacobiano S1 = ', Jvc1)
print('Jacobiano S2 = ', Jvc2)
print('')

# ==================== ENERGÍA CINÉTICA =======================================

def cinetica(Vc1, Jvc2):
    V1_c = np.array([
       [Vc1.T @ Vc1, 0],
       [0, 0]
       ])
        
    
    V2_c = Jvc2.T @ Jvc2    
    
    return V1_c, V2_c

(V1_c, V2_c) = cinetica(Vc1, Jvc2)


# ==================== IMATRIZ DE INERCIA =====================================

m1 = 1
m2 = 1

q_ddot = np.array([
    [1],
    [1]
    ])

def inercia(m1, m2, V1_c, V2_c):
    Mq_1 = m1 * V1_c
    
    Mq_2 = m2 * V2_c
    
    Mt = Mq_1 + Mq_2
    
    MT = Mt @ q_ddot
    
    return Mq_1, Mq_2, MT

(Mq_1, Mq_2, M) = inercia(m1, m2, V1_c, V2_c)

print('Matriz de inercia S1 = ', Mq_1)
print('Matriz de inercia S2 = ', Mq_2)
print('Matriz de inercia total = ', M)
print('')


# =============================================================================
#                      MATRIZ DE CORIOLIS
# =============================================================================


def coriolis(q1, q2, L1, L2, m1, m2, q_dot):
    C = np.array([
        [-L1 * L2 * m2 * np.sin(q2) * q_dot[1] * (2 * q_dot[0] + q_dot[1])],
        [L1 * L2 * m2 * np.sin(q2) * q_dot[0]]
        ])
    
    return C
    
C = coriolis(q1, q2, L1, L2, m1, m2, q_dot)


print('Matriz de coriolis = ', C)
print('')


# =============================================================================
#                      MATRIZ DE GRAVEDAD
# =============================================================================


g = 9.81

def gravedad(y, m1, m2, g):
    P1 = y[0] * m1 * g
    P2 = y[1] * m2 * g
    Pt = P1 + P2
    dPt_q1 = L1 * g * np.cos(q1) * (m1 + m2) + L2 * g * np.cos(q1 + q2) * m2
    dPt_q2 = L2 * g * np.cos(q1 + q2) * m2
    G = np.array([
        [dPt_q1],
        [dPt_q2]
        ])
    
    return G

G = gravedad(y, m1, m2, g)

print('Matriz de gravedad = ', G)
print('')


# =============================================================================
#                      TORQUE
# =============================================================================


def torque(M, C, G):
    t = M + C.T + G.T
    
    return t

t = torque(M, C, G)
print('El torque es = ', t.T)
print('')

