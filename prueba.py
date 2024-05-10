def calcular_tasa_efectiva(anual_nominal):
    # Calcula la tasa de interés efectiva trimestral a partir de la tasa nominal
    i_t = anual_nominal / 1
    return i_t

def calcular_cuota_capital(Vp, n):
    # Calcula la cuota de amortización de capital constante
    cuota_capital = Vp / n
    return cuota_capital

def generar_tabla_amortizacion(Vp, n, trimestral_nominal):
    # Inicializar la tabla de amortización
    tabla_amortizacion = []

    # Calcular la tasa de interés efectiva trimestral
    i_t = calcular_tasa_efectiva(trimestral_nominal)

    # Calcular la cuota de amortización de capital constante
    cuota_capital = calcular_cuota_capital(Vp, n)

    # Inicializar el saldo de capital
    saldo_capital = Vp

    # Calcular la tabla de amortización para cada período
    for k in range(1, n + 1):
        # Calcular los intereses
        intereses = saldo_capital * i_t

        # Calcular el pago mensual
        pago_mensual = cuota_capital + intereses

        # Actualizar el saldo de capital
        saldo_capital -= cuota_capital

        # Agregar los valores a la tabla de amortización
        tabla_amortizacion.append([k, pago_mensual, intereses, cuota_capital, saldo_capital])

    return tabla_amortizacion

# Parámetros del préstamo
Vp = 20000 # Valor del préstamo
n = 4          # Número de pagos trimestrales
trimestral_nominal = 0.06  # Tasa de interés nominal trimestral (20% N-t)

# Generar la tabla de amortización
tabla = generar_tabla_amortizacion(Vp, n, trimestral_nominal)

# Imprimir la tabla de amortización
print("Periodo (k)  Pago Mensual (Ak)  Intereses (Ik)  Cuota de Capital (Vk)  Saldo de Capital")
for fila in tabla:
    print("{:<12}  {:<19,.2f}  {:<14,.2f}  {:<21,.2f}  {:<17,.2f}".format(*fila))
