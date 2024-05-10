import datetime
import math
from flask import Flask, render_template, request
import numpy_financial as npf 

app = Flask(__name__, static_folder="static", template_folder="templates")

def calcular_time(fecha_inicio, fecha_fin):
    # Calcula la diferencia entre las fechas en segundos
    diferencia_segundos = (fecha_fin - fecha_inicio).total_seconds()
    # Calcula la diferencia en años (considerando años bisiestos)
    diferencia_anios = diferencia_segundos / (365.25 * 24 * 3600)  # Aproximadamente 365.25 días en un año
    return diferencia_anios

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_valor_futuro', methods=['GET', 'POST'])
def calcular_valor_futuro():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        fecha_inicio = datetime.datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')

        # Convertir la tasa de interés a su equivalente decimal
        tasa_interes_decimal = tasa_interes_porcentaje / 100

        # Calcular el tiempo en años
        tiempo = calcular_time(fecha_inicio, fecha_fin)

        # Calcular el valor futuro
        valor_futuro = round(capital * (1 + (tasa_interes_decimal * tiempo)),2)

        # Renderizar la plantilla con el resultado
        return render_template('simple/resultado_valor_futuro.html', capital=capital, tasa_interes=tasa_interes_porcentaje, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, valor_futuro=valor_futuro)
    else:
        return render_template('simple/calcular_valor_futuro.html')

@app.route('/calcular_interes', methods=['GET', 'POST'])
def calcular_interes():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo_anios = int(request.form['tiempo_anios'])
        tiempo_meses = int(request.form['tiempo_meses'])
        tiempo_dias = int(request.form['tiempo_dias'])

        # Convertir el tiempo a años
        tiempo_total = tiempo_anios + (tiempo_meses / 12) + (tiempo_dias / 360)
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Calcular el interés
        interes = round ((capital*tasa_interes_decimal*tiempo_total),2)

        # Renderizar la plantilla con el resultado
        return render_template('simple/resultado_interes.html', capital=capital, tasa_interes=tasa_interes_porcentaje, tiempo_anios=tiempo_anios, tiempo_meses=tiempo_meses, tiempo_dias=tiempo_dias, interes=interes)
    else:
        return render_template('simple/calcular_interes.html')
    
@app.route('/calcular_capital', methods=['GET', 'POST'])
def calcular_capital():
    if request.method == 'POST':
        interes = float(request.form['interes'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo_anios = int(request.form['tiempo_anios'])
        tiempo_meses = int(request.form['tiempo_meses'])
        tiempo_dias = int(request.form['tiempo_dias'])

        # Convertir el tiempo a años
        tiempo_total = tiempo_anios + (tiempo_meses / 12) + (tiempo_dias / 360)
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Calcular el capital
        capital = round((interes / (tasa_interes_decimal * tiempo_total)),2)

        # Renderizar la plantilla con el resultado
        return render_template('simple/resultado_capital.html', interes=interes, tasa_interes=tasa_interes_porcentaje, tiempo_anios=tiempo_anios, tiempo_meses=tiempo_meses, tiempo_dias=tiempo_dias, capital=capital)
    else:
        return render_template('simple/calcular_capital.html')
    
@app.route('/calcular_tiempo', methods=['GET', 'POST'])
def calcular_tiempo():
    if request.method == 'POST':
        interes = float(request.form['interes'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        capital = float(request.form['capital'])
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Convertir el tiempo a años
        tiempo_total= interes/(capital * tasa_interes_decimal)

        # Obtener la parte entera y decimal de los años
        años_enteros = int(tiempo_total)
        meses_decimales = (tiempo_total - años_enteros) * 12

        # Obtener la parte entera y decimal de los meses
        meses_enteros = int(meses_decimales)
        dias_decimales = (meses_decimales - meses_enteros) * 30  # Estimado de 30 días por mes

        # Obtener la parte entera de los días
        dias_enteros = int(dias_decimales)


        # Renderizar la plantilla con el resultado
        return render_template('simple/resul_tiempo.html', interes=interes, tasa_interes=tasa_interes_porcentaje, años=años_enteros, meses=meses_enteros, dias=dias_enteros, capital=capital)
    else:
        return render_template('simple/calcular_tiempo.html')

@app.route('/calcular_tasa_interes', methods=['GET', 'POST'])
def calcular_tasa_interes():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        tiempo_anios = int(request.form['tiempo_anios'])
        tiempo_meses = int(request.form['tiempo_meses'])
        tiempo_dias = int(request.form['tiempo_dias'])
        interes = int(request.form['interes'])

        # Convertir el tiempo a años
        tiempo_total = tiempo_anios + (tiempo_meses / 12) + (tiempo_dias / 360)
        
        # Calcular tasa interés
        tasa = (interes / (capital*tiempo_total)) * 100
        tasa_interes = "{0:.2f}".format(tasa)

        # Renderizar la plantilla con el resultado
        return render_template('simple/resul_tasa_interes.html', capital=capital, tasa_interes=tasa_interes, tiempo_anios=tiempo_anios, tiempo_meses=tiempo_meses, tiempo_dias=tiempo_dias, interes=interes)
    else:
        return render_template('simple/calcular_tasa_interes.html')
    
@app.route('/monto_compuesto', methods=['GET', 'POST'])
def calcular_monto_compuesto():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = int(request.form['tiempo'])
        capi = request.form.get("capi")

        time = {
    "1": "Dias",
    "2": "Meses",
    "3": "Trimestres",
    "4": "Cuatrimestres",
    "5": "Semestres",
    "6": "Años",
}
        
        capitali = time.get(capi)


        # Convertir el tiempo a años
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Calcular el interés
        monto = round (((capital*((1 + tasa_interes_decimal))**tiempo)),2)

        # Renderizar la plantilla con el resultado
        return render_template('compuesto/resul_monto_compuesto.html', capitali=capitali, capital=capital, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=monto)
    else:
        return render_template('compuesto/monto_compuesto.html')
    
@app.route('/tiempo_compuesto', methods=['GET', 'POST'])
def calcular_tiempo_compuesto():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        monto = float(request.form['monto'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        capi = request.form.get("capi")

        time = {
    "1": "Dias",
    "2": "Meses",
    "3": "Trimestres",
    "4": "Cuatrimestres",
    "5": "Semestres",
    "6": "Años",
}
        
        capitali = time.get(capi)


        # Convertir el tiempo a años
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Calcular el interés
        tiempo = round( (math.log(monto) - math.log(capital)) / math.log(1 + tasa_interes_decimal),2)

        # Renderizar la plantilla con el resultado
        return render_template('compuesto/resul_tiempo_compuesto.html', capitali=capitali, capital=capital, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=monto)
    else:
        return render_template('compuesto/tiempo_compuesto.html')
    

@app.route('/tasa_compuesta', methods=['GET', 'POST'])
def calcular_tasa_compuesta():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        monto = float(request.form['monto'])
        tiempo = float(request.form['tiempo'])
        capi = request.form.get("capi")

        if capi == "1":
                valor=365
                tiempo2=tiempo*valor
                capitali="Diaria"
               
        elif capi == "2":
                valor=12
                tiempo2=tiempo * valor
                capitali="Mensual"
                
        elif capi=="3":
                valor=4
                tiempo2=tiempo * valor
                capitali="Trimestral"
                
        elif capi == "4":
                valor=3
                tiempo2=tiempo * valor
                capitali="Cuatrimestral"
                
        elif capi=="5":
                valor=2
                tiempo2=tiempo * valor
                capitali="Semestral"
                
        elif capi=="6":
                valor=1
                tiempo2=tiempo * valor
                capitali="Anual"

  # Calcular el interés
        tasa_interes_decimal = (((monto/capital)**(1/tiempo2))-1)
        tasa_interes=round((tasa_interes_decimal * 100),2)



        # Renderizar la plantilla con el resultado
        return render_template('compuesto/resul_tasa_compuesta.html', capitali=capitali, capital=capital, tasa_interes=tasa_interes, tiempo=tiempo, monto=monto)
    else:
        return render_template('compuesto/tasa_compuesta.html')
    
@app.route('/capital_compuesto', methods=['GET', 'POST'])
def calcular_capital_compuesto():
    if request.method == 'POST':
        monto = float(request.form['monto'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = int(request.form['tiempo'])
        capi = request.form.get("capi")

        time = {
    "1": "Dias",
    "2": "Meses",
    "3": "Trimestres",
    "4": "Cuatrimestres",
    "5": "Semestres",
    "6": "Años",
}
        
        capitali = time.get(capi)


        # Convertir el tiempo a años
        tasa_interes_decimal = tasa_interes_porcentaje / 100
        # Calcular el interés
        capital = round ((monto/((1+tasa_interes_decimal)**tiempo)),2)

        # Renderizar la plantilla con el resultado
        return render_template('compuesto/resul_capital_compuesto.html', capitali=capitali, capital=capital, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=monto)
    else:
        return render_template('compuesto/capital_compuesto.html')
    

@app.route('/interes_compuesto', methods=['GET', 'POST'])
def calcular_interes_compuesto():
    if request.method == 'POST':
        capital = float(request.form['capital'])
        monto = float(request.form['monto'])
        
      

      
        # Calcular el interés
        interes = round(monto - capital,2)

        # Renderizar la plantilla con el resultado
        return render_template('compuesto/resul_interes_compuesto.html', capital=capital, monto=monto, ic=interes)
    else:
        return render_template('compuesto/interes_compuesto.html')
    
    

@app.route('/anual_valor_futuro', methods=['GET', 'POST'])
def calcular_anual_futuro():
    if request.method == 'POST':
        monto = float(request.form['monto'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = float(request.form['tiempo'])
        capi = request.form.get("capi")

    
        
        if capi == "1":
                valor=365
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Diaria"
                
        elif capi == "2":
                valor=12
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Mensual"
               
        elif capi=="3":
                valor=4
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Trimestral"
                
        elif capi == "4":
                valor=3
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Cuatrimestral"
               
        elif capi=="5":
                valor=2
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Semestral"
                
        elif capi=="6":
                valor=1
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Anual"
                

        valor_final=valor*tiempo
        tasa_interes_decimal = tasa_tiempo/ 100

        
        valor_fu = round (monto * ((((1 + tasa_interes_decimal)**valor_final) - 1) / tasa_interes_decimal),2)
       

        # Renderizar la plantilla con el resultado
        return render_template('anualidad/resul_anual_futuro.html', capitali=capitali, vf=valor_fu, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=monto)
    else:
        return render_template('anualidad/anual_valor_futuro.html')
    

@app.route('/anual_valor_presente', methods=['GET', 'POST'])
def calcular_anual_presente():
    if request.method == 'POST':
        futuro = float(request.form['monto'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = float(request.form['tiempo'])
        capi = request.form.get("capi")

    
        
        if capi == "1":
                valor=365
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Diaria"
               
        elif capi == "2":
                valor=12
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Mensual"
                
        elif capi=="3":
                valor=4
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Trimestral"
                
        elif capi == "4":
                valor=3
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Cuatrimestral"
                
        elif capi=="5":
                valor=2
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Semestral"
                
        elif capi=="6":
                valor=1
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Anual"

        valor_final=valor*tiempo
        tasa_interes_decimal = tasa_tiempo/ 100

        
        valor_p = round(futuro * ((1-((1 + tasa_interes_decimal)**-valor_final)) / tasa_interes_decimal),2)
       

        # Renderizar la plantilla con el resultado
        return render_template('anualidad/resul_anual_presente.html', capitali=capitali, vp=valor_p, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=futuro)
    else:
        return render_template('anualidad/anual_valor_presente.html')
    
@app.route('/anual_pago', methods=['GET', 'POST'])
def calcular_anual_pago():
    if request.method == 'POST':
        monto = float(request.form['vf'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = float(request.form['tiempo'])
        capi = request.form.get("capi")

    
        
        if capi == "1":
                valor=365
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Diaria"
                
        elif capi == "2":
                valor=12
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Mensual"
               
        elif capi=="3":
                valor=4
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Trimestral"
                
        elif capi == "4":
                valor=3
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Cuatrimestral"
               
        elif capi=="5":
                valor=2
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Semestral"
                
        elif capi=="6":
                valor=1
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Anual"
                

        valor_final=valor*tiempo
        tasa_interes_decimal = tasa_tiempo/ 100

        
        depo = round (monto * (tasa_interes_decimal / (((1 + tasa_interes_decimal)**valor_final) - 1) ),2)
       

        # Renderizar la plantilla con el resultado
        return render_template('anualidad/resul_anual_pago.html', capitali=capitali, pago=depo, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=monto)
    else:
        return render_template('anualidad/anual_pago.html')
    


@app.route('/anual_venci', methods=['GET', 'POST'])
def calcular_anual_venci():
    if request.method == 'POST':
        futuro = float(request.form['monto'])
        tasa_interes_porcentaje = float(request.form['tasa_interes'])
        tiempo = float(request.form['tiempo'])
        capi = request.form.get("capi")

    
        
        if capi == "1":
                valor=365
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Diaria"
               
        elif capi == "2":
                valor=12
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Mensual"
                
        elif capi=="3":
                valor=4
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Trimestral"
                
        elif capi == "4":
                valor=3
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Cuatrimestral"
                
        elif capi=="5":
                valor=2
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Semestral"
                
        elif capi=="6":
                valor=1
                tasa_tiempo=tasa_interes_porcentaje / valor
                capitali="Anual"

        valor_final=valor*tiempo
        tasa_interes_decimal = tasa_tiempo/ 100

        
        valor_v = round(futuro * ( tasa_interes_decimal / (1-((1 + tasa_interes_decimal)**-valor_final))),2)
       

        # Renderizar la plantilla con el resultado
        return render_template('anualidad/resul_anual_venci.html', capitali=capitali, vv=valor_v, tasa_interes=tasa_interes_porcentaje, tiempo=tiempo, monto=futuro)
    else:
        return render_template('anualidad/anual_venci.html')
    
  
def calcular_tasa_efectiva(tasa, perio):
    # Calcula la tasa de interés efectiva trimestral a partir de la tasa nominal
    if perio == "1":
                valor=12
                tasa_real= tasa / valor
               
               
    elif perio == "2":
                valor=4
                tasa_real= tasa / valor
                
                
    elif perio=="3":
                valor=3
                tasa_real= tasa / valor
                
                
    elif perio == "4":
                valor=2
                tasa_real= tasa / valor
                
                
    elif perio=="5":
                valor=1
                tasa_real= tasa / valor

                
    return tasa_real

def calcular_cuota_capital(pres, pagos):
    # Calcula la cuota de amortización de capital constante
    cuota_capital = pres / pagos
    return cuota_capital
    
def tabla_aleman(pres, pagos, tasa, perio):
    # Inicializar la tabla de amortización
    tabla_amortizacion = []

    # Calcular la tasa de interés efectiva trimestral
    tasa = calcular_tasa_efectiva(tasa,perio)

    # Calcular la cuota de amortización de capital constante
    cuota_capital = calcular_cuota_capital(pres, pagos)

    # Inicializar el saldo de capital
    saldo_capital = pres

    # Calcular la tabla de amortización para cada período
    for k in range(1, pagos + 1):
        # Calcular los intereses
        intereses = saldo_capital * tasa

        # Calcular el pago mensual
        pago_mensual = cuota_capital + intereses

        # Actualizar el saldo de capital
        saldo_capital -= cuota_capital

        # Agregar los valores a la tabla de amortización
        tabla_amortizacion.append([k, pago_mensual, intereses, cuota_capital, saldo_capital])

    return tabla_amortizacion

def tabla_frances(pres, pagos, tasa, perio):
    tabla_amortizacion = []
    tasa_real = calcular_tasa_efectiva(tasa,perio)  # Convertir tasa anual a tasa periódica mensual
    cuota_capital = (pres * tasa) / (1 - (1 + tasa) ** -pagos)
    
    saldo_capital = pres
    
    
    for k in range(1, pagos + 1):
        intereses = saldo_capital * tasa_real
        pago_mensual = cuota_capital - intereses
        saldo_capital -= pago_mensual

        tabla_amortizacion.append([k, pago_mensual, intereses, cuota_capital, saldo_capital])

    return tabla_amortizacion

@app.route('/aleman', methods=['GET', 'POST'])
def aleman():
    if request.method == 'POST':
        pres = int(request.form['pres'])
        interes = float(request.form['tasa_interes'])
        pagos = int(request.form['pagos'])
        perio = request.form.get("perio")
        tasa = interes / 100

        tabla = tabla_aleman(pres, pagos, tasa, perio)

        # Convertir la tabla de amortización a formato HTML
        tabla_html = "<table border='1'><tr><th>Periodo</th><th>Cuota</th><th>Intereses</th><th>Amortización Capital</th><th>Saldo de Capital</th></tr>"
        for fila in tabla:
            tabla_html += "<tr>"
            for dato in fila:
                tabla_html += "<td>{}</td>".format(dato)
            tabla_html += "</tr>"
        tabla_html += "</table>"

        # Renderizar la plantilla con el resultado
        return render_template('amortizacion/resul_aleman.html', tabla=tabla_html)
    else:
        return render_template('amortizacion/aleman.html')
    

@app.route('/frances', methods=['GET', 'POST'])
def frances():
    if request.method == 'POST':
        pres = int(request.form['pres'])
        interes = float(request.form['tasa_interes'])
        pagos = int(request.form['pagos'])
        perio = request.form.get("perio")
        tasa = interes / 100

        tabla = tabla_frances(pres, pagos, tasa, perio)

        # Convertir la tabla de amortización a formato HTML
        tabla_html = "<table border='1'><tr><th>Periodo</th><th>Amortización Capital</th><th>Intereses</th><th>Cuota</th><th>Saldo de Capital</th></tr>"
        for fila in tabla:
            tabla_html += "<tr>"
            for dato in fila:
                tabla_html += "<td>{}</td>".format(dato)
            tabla_html += "</tr>"
        tabla_html += "</table>"

        # Renderizar la plantilla con el resultado
        return render_template('amortizacion/resul_frances.html', tabla=tabla_html)
    else:
        return render_template('amortizacion/frances.html')
    
def calcular_tasa_americano(tasa, perio):
    # Calcula la tasa de interés efectiva trimestral a partir de la tasa nominal
    if perio == "1":
                valor=12
                tasa_real= tasa / valor
               
               
    elif perio == "2":
                valor=4
                tasa_real= tasa / valor
                
                
    elif perio=="3":
                valor=3
                tasa_real= tasa / valor
                
                
    elif perio == "4":
                valor=2
                tasa_real= tasa / valor
                
                
    elif perio=="5":
                valor=1
                tasa_real= tasa / valor

                
    return valor
    

def tabla_americano(pres, pagos, tasa, perio):
    tabla_amortizacion = []
    # Calcular la tasa de interés efectiva
    tasa_efectiva = calcular_tasa_efectiva(tasa, perio)
    
    # Inicializar el saldo pendiente
    saldo_pendiente = pres

    # Calcular la tabla de amortización para cada periodo
    for k in range(1, pagos + 1):
        # Calcular los intereses
        intereses = saldo_pendiente * tasa_efectiva

        pago_mensual = (pres * tasa_efectiva) / calcular_tasa_americano(tasa, perio)

        amortizacion = pago_mensual - intereses

        if k == pagos:
            pago_mensual = saldo_pendiente + intereses
            amortizacion = saldo_pendiente
        
        saldo_pendiente -= amortizacion
        
        # Append the data for this period to the table
        tabla_amortizacion.append([k, pago_mensual, intereses, amortizacion, saldo_pendiente])

    return tabla_amortizacion


    


@app.route('/americano', methods=['GET', 'POST'])
def americano():
    if request.method == 'POST':

        pres = int(request.form['pres'])
        interes = float(request.form['tasa_interes'])
        pagos = int(request.form['pagos'])
        perio = request.form.get("perio")
        tasa = interes / 100

        tabla = tabla_americano(pres, pagos, tasa, perio)

        # Convertir la tabla de amortización a formato HTML
        tabla_html = "<table border='1'><tr><th>Periodo</th><th>Cuota</th><th>Intereses</th><th>Amortización Capital</th><th>Saldo de Capital</th></tr>"
        for fila in tabla:
            tabla_html += "<tr>"
            for dato in fila:
                tabla_html += "<td>{}</td>".format(dato)
            tabla_html += "</tr>"
        tabla_html += "</table>"

         
        return render_template('amortizacion/resul_americano.html', tabla=tabla_html)
    else:
        return render_template('amortizacion/americano.html')



@app.route('/calcular_tir', methods=['GET', 'POST'])
def calcular_tir():
    if request.method == 'POST':
    
        inversion = float(request.form['inversion_ini'])
        tipo_interes = float(request.form['tipo_int'])
        flujos_caja = list(map(float, request.form.getlist('flujos_caja[]')))

        vanresul = calcular_van(flujos_caja, inversion, tipo_interes)
        tirresul = calcular_tir(flujos_caja, inversion)

        return render_template('tir/resul_tir.html', vanresul=vanresul, tirresul=tirresul)
    else:
        return render_template('tir/calcular_tir.html') 

def calcular_van(flujos, inversion, tipo_interes):
    tipo_interes_decimal = tipo_interes / 100  # Convertir de porcentaje a decimal
    flujos = [-inversion] + flujos
    van = npf.npv(tipo_interes_decimal, flujos)
    return van

def calcular_tir(flujos, inversion):
    tir = npf.irr([-inversion] + flujos)
    return tir * 100


if __name__ == '__main__':
    app.run(debug=True)



    
    
    