import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import math

st.title('Calculadora')
st.markdown('AHORRO ECONOMICO ESTIMADO EN LEJANIA DE POZO')

col1, col2 = st.columns(2)

with col1:
    user1 = st.number_input('Distancia pozo (km)')
    user2 = st.number_input('Frecuencia maniobra mensual (cant)')

with col2:
    user3 = st.number_input('Tiempo maniobra (mn)')
    user4 = st.number_input('Producción prom pozo (m³ / día)')

data= pd.DataFrame({
    "Dispositivo":["CHA","mSafe","CHA","mSafe","CHA","mSafe","CHA","mSafe","CHA","mSafe"],
    "Precio":[15786,3533,1260,1200,10549,19976,11000,630,2800,1319],
    "Seccion":["5-Precio Equipo","4-Costo Mano de Obra","3-Costo vehiculo","2-Repuestos/Spare parts","1-Cierre de pozo no deseado","5-Precio Equipo","4-Costo Mano de Obra","3-Costo vehiculo","2-Repuestos/Spare parts","1-Cierre de pozo no deseado"]

})

if st.button('Calcular'):
    bar_chart = alt.Chart(data).mark_bar().encode(
    x="Dispositivo:O",
    y="Precio:Q",
    color="Seccion"
    )
    st.altair_chart(bar_chart, use_container_width=True)

if user1 >= 1:
    user1 = math.floor(user1)
if user2 >= 1:
    user2 = math.floor(user2)
if user3 >= 1:
    user3 = math.floor(user3)
if user4 >= 1:
    user4 = math.floor(user4)

def functionsCHA():
    st.markdown('Calculando que un operador cuesta $4000')
    st.markdown('La cantidad de operadores fjios es de 2')
    st.markdown('Su vehiculo es Toyota Hilux Pick Up Cabina doble')
    st.markdown('Su velocidad prom es de 50km')
    #Datos Vehiculo
    kmsRecorridos = user1 * 2 * user2
    velocidaProm = 50
    tiempoViaje = kmsRecorridos/velocidaProm
    rendimientoCombustible = 0.1
    valorGasoil = 0.7
    CostoAsocVehiculo = valorGasoil*rendimientoCombustible*kmsRecorridos*30
    CostoRealVehiculo = 0

    if kmsRecorridos > 300:
        CostoRealVehiculo = 300*rendimientoCombustible*valorGasoil*30
    else:
        CostoRealVehiculo = CostoAsocVehiculo

    #Datos Operador
    Operadores = 2
    costoOperador = 4000
    horasUnit = 24*30
    usdHrsOp = costoOperador/horasUnit
    tiempoInvertidoManiobra = tiempoViaje*user2+(user3/60)*user2
    tiempoMaxInvertidoManiobra = tiempoInvertidoManiobra
    costoAsocOperadores = tiempoMaxInvertidoManiobra*usdHrsOp*Operadores*30
    CostoRealMaximo = 0

    if costoAsocOperadores > costoOperador*2+Operadores:
        CostoRealMaximo = Operadores*costoOperador,
    else:
        CostoRealMaximo = costoAsocOperadores

    constoFinal = CostoRealVehiculo + CostoRealMaximo

    st.write("DATOS DE LA OPERACIÓN")
    df_1ro = pd.DataFrame({
        "Operador Requeridos": [Operadores, Operadores, Operadores, Operadores, Operadores, Operadores, Operadores, Operadores, Operadores, Operadores, Operadores],
        "Distancia Pozo [Kms]": [user1, user1, user1, user1, user1, user1, user1, user1, user1, user1, user1],
        "Tiempo/ maniobra [min]": [user3, user3, user3, user3, user3, user3, user3, user3, user3, user3, user3],
        "Frecuencia de maniobra Manual/Diaria": [user2, user2, user2, user2, user2, user2, user2, user2, user2, user2, user2],
        "Produccion Diaria [m3/dia]": [user4, user4, user4, user4, user4, user4, user4, user4, user4, user4, user4]
    })
    st.write(df_1ro)
    st.write("COSTO OPERADOR")
    df_2da = pd.DataFrame({
        "Costo Operador [USD/MES]": [costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador, costoOperador],
        "Horas unit /mes/op": [horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit, horasUnit],
        "USD/hrs/op": [usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp, usdHrsOp],
        "Tiempo invertido en maniobra/dia": [tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra, tiempoInvertidoManiobra],
        "TIEMPO MAX. INVERTIDO": [tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra, tiempoMaxInvertidoManiobra],
        "COSTO ASOCIADO AL OPERADORES/mes": [costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores, costoAsocOperadores],
        "COSTO REAL MAXIMO OPERADOR/mes": [CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo, CostoRealMaximo],
    })
    st.write(df_2da)
    st.write("COSTO VEHICULO")
    df_3ro = pd.DataFrame({
        "Kms recorridos/dia": [kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos, kmsRecorridos],
        "Tiempo de Viaje": [tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje, tiempoViaje],
        "Velocidad Prom [km/h]": [velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm, velocidaProm],
        "Rendimiento combustible vehiculo [L/km]": [rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible, rendimientoCombustible],
        "Valor Gasoil [USD/L]": [valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil, valorGasoil],
        "COSTO ASOCIADO AL VEHICULO": [CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo, CostoAsocVehiculo],
        "COSTO REAL MAXIMO VEHICULO/mes": [CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo, CostoRealVehiculo],
    })
    st.write(df_3ro)
    st.write("COSTO MES")
    df_4to = pd.DataFrame({
        "OPEX/mes STD": [constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal, constoFinal],
    })
    st.write(df_4to)


    horasAhorradas = ((tiempoMaxInvertidoManiobra*2-(tiempoMaxInvertidoManiobra/10)*(2)/4)*30)*8.6

    st.write("BENEFICIOS DEL SISTEMA")
    df_5to = pd.DataFrame({
        "HORAS DE OPERACIÓN AHORRADAS/año": [horasAhorradas],
    })
    st.write(df_5to)

if st.button('Detalles de la operación'):
    st.write(functionsCHA())