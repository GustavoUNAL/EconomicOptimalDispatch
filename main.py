import numpy as np
from scipy.optimize import minimize

# Función de costo para la generación local, la generación solar y la importación
def costo_total(x):
    P_gen, P_import, P_solar = x
    C_local = 184.5 * P_gen * 1000  # Costo de generación local en COP/MWh
    C_import = 820 * P_import * 1000  # Costo de importación en COP/MWh
    C_solar = 200.9 * P_solar * 1000  # Costo de generación solar en COP/MWh
    return C_local + C_import + C_solar

# Restricción de igualdad (demanda total)
def restriccion_eq(x):
    P_gen, P_import, P_solar = x
    return P_gen + P_import + P_solar - (P_carga + P_perdidas)

# Restricción de desigualdad (potencia generada >= demanda total)
def restriccion_ineq(x):
    P_gen, P_import, P_solar = x
    return P_gen + P_import + P_solar - (P_carga + P_perdidas)

# Valores obtenidos del archivo
P_carga = 9.017  # MW (potencia cargada)
P_perdidas = 1.821  # MW (pérdidas)
demanda_total = P_carga + P_perdidas  # Demanda total que debe ser cubierta

# Límites de generación (supuestos)
P_gen_min, P_gen_max = 3, 5.4  # MW
P_import_min, P_import_max = 0, 3.5  # MW
P_solar_min, P_solar_max = 0, 1.91  # MW

# Inicialización ajustada más cercana a la demanda total
x0 = [P_gen_max, P_import_max, P_solar_max]

# Límites para P_gen, P_import, y P_solar
bounds = [(P_gen_min, P_gen_max), (P_import_min, P_import_max), (P_solar_min, P_solar_max)]

# Solución usando el optimizador
solucion = minimize(costo_total, x0=x0, bounds=bounds, constraints=[
    {'type': 'eq', 'fun': restriccion_eq},
    {'type': 'ineq', 'fun': restriccion_ineq}
], options={'ftol': 1e-9})  # Aumentar precisión con 'ftol'

P_gen_opt, P_import_opt, P_solar_opt = solucion.x

print(f'Potencia óptima generada localmente: {P_gen_opt:.2f} MW')
print(f'Potencia óptima importada: {P_import_opt:.2f} MW')
print(f'Potencia óptima generada por el sistema solar: {P_solar_opt:.2f} MW')
print(f'Costo total mínimo: {costo_total([P_gen_opt, P_import_opt, P_solar_opt]):,.2f} COP')

# Verificación
potencia_total_generada = P_gen_opt + P_import_opt + P_solar_opt
print(f'Demanda total del sistema: {demanda_total:.2f} MW')
print(f'Potencia total generada: {potencia_total_generada:.2f} MW')
