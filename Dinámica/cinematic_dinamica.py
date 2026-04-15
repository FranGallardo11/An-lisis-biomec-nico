#  Cinemática y dinámica

import numpy as np
import sympy as sp



# =============================================================================

# Para multiplicar las matrices, de forma simbólica ambas deben ser sympy
# Para multiplicar de forma numérica, sympy debe tener valores asignados para volverse numpy:
    
# Sustituimos valores simbólicos
# B_num = B.subs({x: 1, y: 2, z: 3, w: 4})

# Convertir a NumPy
# B_np = np.array(B_num.tolist(), dtype=float)

# convertir a radianes para dar valor a los ángulos
# R_90_grados = R.subs(theta, sp.rad(30)) 


# ==================== MATRIZ DE TRANSFORMACIÓN ===============================

# Definir las incógnitas (símbolos)
a, b, c, theta, alpha, phi = sp.symbols('a b c theta alpha phi')


Transx = np.array([[1, 0, 0, a],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

Transy = np.array([[1, 0, 0, 0],
                    [0, 1, 0, b],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

Transz = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, c],
                    [0, 0, 0, 1]])

Transx_sim = sp.Matrix(Transx)
Transy_sim = sp.Matrix(Transy)
Transz_sim = sp.Matrix(Transz)

Rotx_sim = sp.Matrix([[1, 0, 0, 0],
                      [0, sp.cos(alpha), -sp.sin(alpha), 0],
                      [0, sp.sin(alpha),  sp.cos(alpha), 0],
                      [0, 0, 0, 1]]) 

Roty_sim = sp.Matrix([[sp.cos(phi), 0, sp.sin(phi), 0],
                      [0, 1, 0, 0],
                      [-sp.sin(phi), 0,  sp.cos(phi), 0],
                      [0, 0, 0, 1]]) 

Rotz_sim = sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0, 0],
                      [sp.sin(theta), sp.cos(theta), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]]) 

# Rotx_num = Rotx_sim.subs({alpha: 1})
# Rotx = np.array(Rotx_num.tolist(), dtype=float)

# Roty_num = Roty_sim.subs({phi: 1})
# Roty = np.array(Roty_num.tolist(), dtype=float)

# Rotz_num = Rotz_sim.subs({theta: 1})
# Rotz = np.array(Rotz_num.tolist(), dtype=float)

print('Matriz de transformación total: ')
T = Rotz_sim @ Transz_sim @ Transx_sim @ Rotx_sim
sp.pprint(T)


# ==================== ECUACIONES DE VELOCIDAD ================================

L1, L2, t = sp.symbols('L1 L2 t ')

# Variables que dependen del tiempo
theta1 = sp.Function('theta1')(t)
theta2 = sp.Function('theta2')(t)

def dot(var, i):
    # Agrega punto arriba a cualquier variable (Unicode combinante)
    return sp.Symbol(var + '\u0307' + chr(0x2080 + i))

x1_dot = dot('x',1)
y1_dot = dot('y',1)
x2_dot = dot('x',2)
y2_dot = dot('y',2)

theta1_dot = sp.Symbol('θ̇₁')
theta2_dot = sp.Symbol('θ̇₂')

x1 = L1*sp.cos(theta1)
y1 = L1*sp.sin(theta1)
x2 = L1*sp.cos(theta1) + L2*sp.cos(theta1 + theta2)
y2 = L1*sp.sin(theta1) + L2*sp.sin(theta1 + theta2)

dx1_dt = sp.diff(x1, t)
dy1_dt = sp.diff(y1, t)
dx2_dt = sp.diff(x2, t)
dy2_dt = sp.diff(y2, t)

# Diccionario de reemplazo
subs_dict = {
    sp.Derivative(theta1, t): theta1_dot,
    sp.Derivative(theta2, t): theta2_dot
}

# Reemplazar en la expresión
dx1t = dx1_dt.subs(subs_dict)
dx2t = dx2_dt.subs(subs_dict)
dy1t = dy1_dt.subs(subs_dict)
dy2t = dy2_dt.subs(subs_dict)

ecx1 = sp.Eq(x1_dot, dx1t)
ecx2 = sp.Eq(x2_dot, dx2t)
ecy1 = sp.Eq(y1_dot, dy1t)
ecy2 = sp.Eq(y2_dot, dy2t)
print(' ')
print('Ecuaciones de velocidad')

sp.pprint(ecx1)
sp.pprint(ecy1)
sp.pprint(ecx2)
sp.pprint(ecy2)


# ==================== JACOBIANOS =============================================

theta1j, theta2j = sp.symbols('theta1 theta2')
x1j = L1*sp.cos(theta1j)
y1j = L1*sp.sin(theta1j)
x2j = L1*sp.cos(theta1j) + L2*sp.cos(theta1j + theta2j)
y2j = L1*sp.sin(theta1j) + L2*sp.sin(theta1j + theta2j)

pos1 = sp.Matrix([x1j, y1j])
# Variables articulares
q1 = sp.Matrix([theta1j, theta2j])

# Jacobiana
J1 = pos1.jacobian(q1)

print(' ')
print('Jacobiano 1er eslabón')
sp.pprint(J1)

pos2 = sp.Matrix([x2j, y2j])
# Variables articulares
q2 = sp.Matrix([theta1j, theta2j])

# Jacobiana
J2 = pos2.jacobian(q2)

print(' ')
print('Jacobiano 2do eslabón')
sp.pprint(J2)


# ==================== ENERGÍA CINÉTICA =======================================

dx1_dj = sp.diff(x1j, theta1j)
dy1_dj = sp.diff(y1j, theta1j)
dx2_dj = sp.diff(x2j, theta2j)
dy2_dj = sp.diff(y2j, theta2j)

Vc1 = sp.Matrix([dx1_dj, dy1_dj])
V1= sp.simplify(Vc1.T @ Vc1)

def superindices_unicode(expr):
    expr_str = str(expr)
    expr_str = expr_str.replace('**2', '²')
    expr_str = expr_str.replace('**3', '³')
    return expr_str

det_V1 = sp.simplify(V1.det())
det_VV_trig = sp.trigsimp(det_V1)

V1final = det_VV_trig * theta1_dot**2
print('\nVc1:')
print(superindices_unicode(V1final))




















