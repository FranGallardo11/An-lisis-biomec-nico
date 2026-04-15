import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

grados = np.arange(0, 361, 5)

raw = np.array([
0,57,114,171,228,285,342,399,456,513,
569,626,683,740,797,854,911,968,1025,1081,
1138,1195,1252,1309,1366,1423,1480,1537,1594,1651,
1707,1764,1821,1878,1935,1992,2049,2106,2163,2220,
2276,2333,2390,2447,2504,2561,2618,2675,2732,2789,
2845,2902,2959,3016,3073,3130,3187,3244,3301,3358,
3414,3471,3528,3585,3642,3699,3756,3813,3870,3927,
3983,4040,4095
])

# -----------------------------
# Ajuste lineal (calibración)
# -----------------------------
coef = np.polyfit(grados, raw, 1)
modelo = np.poly1d(coef)

# -----------------------------
# Gráfica
# -----------------------------
plt.figure(figsize=(8,6))

plt.scatter(grados, raw, label="Datos medidos")
plt.plot(grados, modelo(grados), 'r', linestyle="--", label="Ajuste lineal")

plt.xlabel("Grados (°)")
plt.ylabel("RAW del sensor")
plt.title("Caracterización del sensor magnético AS5600")
plt.grid(True)
plt.legend()

plt.show()

# -----------------------------
# Ecuación de calibración
# -----------------------------
print("Ecuación de calibración:")
print(f"RAW = {coef[0]:.3f} * grados + {coef[1]:.3f}")