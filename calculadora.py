import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import math
from PIL import Image

st.set_page_config(layout="wide", page_title="Calculo de TCO",)
image = Image.open('Logo.png')
st.image(image, width=200)

st.title('Calculo de TCO')
st.markdown('AHORRO ECONOMICO ESTIMADO EN LEJANIA DE POZO')

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True


def calcular():
    costoManoObraResumenCHA = CostoRealMaximoCHA*12+3000+3000
    vehiculoResumenCHA = CostoRealVehiculoCHA*12
    pozoNoDeseadoResumenCHA = (user4/23.7*2.5*3)/3*4

    costoManoObraResumenMSAFE = CostoRealMaximoMSAFE*12+3000
    vehiculoResumenMSAFE = CostoRealVehiculoMSAFE*12
    pozoNoDeseadoResumenMSAFE = (user8/23.7*2.5*3)/3*0.5


    data = pd.DataFrame({
            "Dispositivo": ["CHA", "CHA", "CHA", "CHA", "CHA", "mSafe", "mSafe","mSafe","mSafe","mSafe"],
        "Precio": [15798, costoManoObraResumenCHA, vehiculoResumenCHA, 2800, pozoNoDeseadoResumenCHA, 19976, costoManoObraResumenMSAFE, vehiculoResumenMSAFE,1200,pozoNoDeseadoResumenMSAFE],
        "Seccion": ["5-Precio Equipo", "4-Costo Mano de Obra", "3-Costo vehiculo", "2-Repuestos/Spare parts", "1-Cierre de pozo no deseado", "5-Precio Equipo", "4-Costo Mano de Obra", "3-Costo vehiculo","2-Repuestos/Spare parts","1-Cierre de pozo no deseado"]
    })
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="Dispositivo:O",
        y="Precio:Q",
        color="Seccion"
    )
    st.altair_chart(bar_chart, use_container_width=True)

with st.container():
    col1, col2 = st.columns([1, 3])

    with col1:
        user1 = st.number_input('Distancia pozo (km)', min_value=0)
        user3 = st.number_input('Tiempo maniobra (min)', min_value=0)
        user2 = st.number_input('Frecuencia maniobra mensual (cant)', min_value=0)
        user4 = st.number_input('Producción prom pozo (m³ / día)', min_value=0)
        result = st.button('Calcular', on_click=callback) or st.session_state.button_clicked

    with col2:
        user5 = 25
        user6 = 2
        user7 = 0.50
        user8 = 25000

        #Caculos CHA
        kmsRecorridosCHA = user1 * 2 * user2
        velocidaPromCHA = 50
        tiempoViajeCHA = kmsRecorridosCHA/velocidaPromCHA
        rendimientoCombustibleCHA = 0.1
        valorGasoilCHA = 0.7
        CostoAsocVehiculoCHA = valorGasoilCHA*rendimientoCombustibleCHA*kmsRecorridosCHA*30
        CostoRealVehiculoCHA = 0

        if kmsRecorridosCHA > 300:
            CostoRealVehiculoCHA = 300*rendimientoCombustibleCHA*valorGasoilCHA*30
        else:
            CostoRealVehiculoCHA = CostoAsocVehiculoCHA

        # Datos Operador
        OperadoresCHA = 2
        costoOperadorCHA = 4000
        horasUnitCHA = 24*30
        usdHrsOpCHA = costoOperadorCHA/horasUnitCHA
        tiempoInvertidoManiobraCHA = tiempoViajeCHA*user2+(user3/60)*user2
        tiempoMaxInvertidoManiobraCHA = tiempoInvertidoManiobraCHA
        costoAsocOperadoresCHA = tiempoMaxInvertidoManiobraCHA*usdHrsOpCHA*OperadoresCHA*30
        CostoRealMaximoCHA = 0

        if costoAsocOperadoresCHA > costoOperadorCHA*2+OperadoresCHA:
            CostoRealMaximoCHA = OperadoresCHA*costoOperadorCHA
        else:
            CostoRealMaximoCHA = costoAsocOperadoresCHA

        constoFinalCHA = CostoRealVehiculoCHA + CostoRealMaximoCHA

        #Calculos msafe
        kmsRecorridosMSAFE = user5 * 2 * user6
        velocidaPromMSAFE = 50
        tiempoViajeMSAFE = kmsRecorridosMSAFE/velocidaPromMSAFE
        rendimientoCombustibleMSAFE = 0.1
        valorGasoilMSAFE = 0.7
        CostoAsocVehiculoMSAFE = valorGasoilMSAFE*rendimientoCombustibleMSAFE*kmsRecorridosMSAFE*30
        CostoRealVehiculoMSAFE = 0

        if kmsRecorridosMSAFE > 300:
            CostoRealVehiculoMSAFE = 300*rendimientoCombustibleMSAFE*valorGasoilMSAFE*30
        else:
            CostoRealVehiculoMSAFE = CostoAsocVehiculoMSAFE

        # Datos Operador
        OperadoresMSAFE = 1
        costoOperadorMSAFE = 4000
        horasUnitMSAFE = 24*30
        usdHrsOpMSAFE = costoOperadorMSAFE/horasUnitMSAFE
        tiempoInvertidoManiobraMSAFE = tiempoViajeMSAFE*user6+(user7/60)*user6
        tiempoMaxInvertidoManiobraMSAFE = 0
        if tiempoInvertidoManiobraMSAFE > 24:
            tiempoMaxInvertidoManiobraMSAFE = 24
        else:
            tiempoMaxInvertidoManiobraMSAFE =+ tiempoInvertidoManiobraMSAFE
        costoAsocOperadoresMSAFE =+ tiempoMaxInvertidoManiobraMSAFE*usdHrsOpMSAFE*OperadoresMSAFE*30
        CostoRealMaximoMSAFE = 0
        if costoAsocOperadoresMSAFE > costoOperadorMSAFE*2+OperadoresMSAFE:
            CostoRealMaximoMSAFE = OperadoresMSAFE*costoOperadorMSAFE,
        else:
            CostoRealMaximoMSAFE = costoAsocOperadoresMSAFE
        constoFinalMSAFE = CostoRealVehiculoMSAFE + CostoRealMaximoMSAFE


        if result:
            calcular()

    
    if result:
        if st.button('Detalles de la operación'):
            st.title('Detalle de operación CHA')
            st.markdown('Calculando que un operador cuesta $4000')
            st.markdown('La cantidad de operadores fjios es de 2')
            st.markdown('Su vehiculo es Toyota Hilux Pick Up Cabina doble')
            st.markdown('Su velocidad prom es de 50km')
            # Datos Vehiculo
            

            st.write("DATOS DE LA OPERACIÓN")
            df_1ro = pd.DataFrame({
                    "Operador Requeridos": [OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA, OperadoresCHA],
                    "Distancia Pozo [Kms]": [user1, user1, user1, user1, user1, user1, user1, user1, user1, user1, user1],
                    "Tiempo/ maniobra [min]": [user3, user3, user3, user3, user3, user3, user3, user3, user3, user3, user3],
                    "Frecuencia de maniobra Manual/Diaria": [user2, user2, user2, user2, user2, user2, user2, user2, user2, user2, user2],
                    "Produccion Diaria [m3/dia]": [user4, user4, user4, user4, user4, user4, user4, user4, user4, user4, user4]
            })
            st.write(df_1ro)
            st.write("COSTO OPERADOR")
            df_2da = pd.DataFrame({
                    "Costo Operador [USD/MES]": [costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA, costoOperadorCHA],
                    "Horas unit /mes/op": [horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA, horasUnitCHA],
                    "USD/hrs/op": [usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA, usdHrsOpCHA],
                    "Tiempo invertido en maniobra/dia": [tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA, tiempoInvertidoManiobraCHA],
                    "TIEMPO MAX. INVERTIDO": [tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA, tiempoMaxInvertidoManiobraCHA],
                    "COSTO ASOCIADO AL OPERADORES/mes": [costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA, costoAsocOperadoresCHA],
                    "COSTO REAL MAXIMO OPERADOR/mes": [CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA, CostoRealMaximoCHA],
            })
            st.write(df_2da)
            st.write("COSTO VEHICULO")
            df_3ro = pd.DataFrame({
                    "Kms recorridos/dia": [kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA, kmsRecorridosCHA],
                    "Tiempo de Viaje": [tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA, tiempoViajeCHA],
                    "Velocidad Prom [km/h]": [velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA, velocidaPromCHA],
                    "Rendimiento combustible vehiculo [L/km]": [rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA, rendimientoCombustibleCHA],
                    "Valor Gasoil [USD/L]": [valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA, valorGasoilCHA],
                    "COSTO ASOCIADO AL VEHICULO": [CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA, CostoAsocVehiculoCHA],
                    "COSTO REAL MAXIMO VEHICULO/mes": [CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA, CostoRealVehiculoCHA],
            })
            st.write(df_3ro)
            st.write("COSTO MES")
            df_4to = pd.DataFrame({
                    "OPEX/mes STD": [constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA, constoFinalCHA],
            })
            st.write(df_4to)

            ###########################################################################

            st.title('Detalle de operación mSafe')
            st.markdown('Calculando que un operador cuesta $4000')
            st.markdown('La cantidad de operadores fjios es de 1')
            st.markdown('El nuevo tiempo de Maniobra es de 1 Minuto')
            st.markdown('La nueva frecuencia mensual es de 0.5 Veces')
            st.markdown('Su vehiculo es Toyota Hilux Pick Up Cabina doble')
            st.markdown('Su velocidad prom es de 50km')
            # Datos Vehiculo

            st.write("DATOS DE LA OPERACIÓN")
            df_1ro = pd.DataFrame({
                            "Operador Requeridos": [OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE, OperadoresMSAFE],
                            "Distancia Pozo [Kms]": [user5, user5, user5, user5, user5, user5, user5, user5, user5, user5, user5],
                            "Tiempo/ maniobra [min]": [user7, user7, user7, user7, user7, user7, user7, user7, user7, user7, user7],
                            "Frecuencia de maniobra Manual/Diaria": [user6, user6, user6, user6, user6, user6, user6, user6, user6, user6, user6],
                            "Produccion Diaria [m3/dia]": [user8, user8, user8, user8, user8, user8, user8, user8, user8, user8, user8]
            })
            st.write(df_1ro)
            st.write("COSTO OPERADOR")
            df_2da = pd.DataFrame({
                            "Costo Operador [USD/MES]": [costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE, costoOperadorMSAFE],
                            "Horas unit /mes/op": [horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE, horasUnitMSAFE],
                            "USD/hrs/op": [usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE, usdHrsOpMSAFE],
                            "Tiempo invertido en maniobra/dia": [tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE, tiempoInvertidoManiobraMSAFE],
                            "TIEMPO MAX. INVERTIDO": [tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE, tiempoMaxInvertidoManiobraMSAFE],
                            "COSTO ASOCIADO AL OPERADORES/mes": [costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE, costoAsocOperadoresMSAFE],
                            "COSTO REAL MAXIMO OPERADOR/mes": [CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE, CostoRealMaximoMSAFE],
            })
            st.write(df_2da)
            st.write("COSTO VEHICULO")
            df_3ro = pd.DataFrame({
                            "Kms recorridos/dia": [kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE, kmsRecorridosMSAFE],
                            "Tiempo de Viaje": [tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE, tiempoViajeMSAFE],
                            "Velocidad Prom [km/h]": [velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE, velocidaPromMSAFE],
                            "Rendimiento combustible vehiculo [L/km]": [rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE, rendimientoCombustibleMSAFE],
                            "Valor Gasoil [USD/L]": [valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE, valorGasoilMSAFE],
                            "COSTO ASOCIADO AL VEHICULO": [CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE, CostoAsocVehiculoMSAFE],
                            "COSTO REAL MAXIMO VEHICULO/mes": [CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE, CostoRealVehiculoMSAFE],
            })
            st.write(df_3ro)
            st.write("COSTO MES")
            df_4to = pd.DataFrame({
                            "OPEX/mes STD": [constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE, constoFinalMSAFE],
            })
            st.write(df_4to)

if user1 >= 1:
    user1 = math.floor(user1)
if user2 >= 1:
    user2 = math.floor(user2)
if user3 >= 1:
    user3 = math.floor(user3)
if user4 >= 1:
    user4 = math.floor(user4)


    


