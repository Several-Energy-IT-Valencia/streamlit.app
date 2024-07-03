import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as c
from pymongo.mongo_client import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
import os
import time
from functions import *
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
dbname = os.getenv('DBNAME_MONGO')
pruebas_alex = 'pruebas_alex'
user1 = os.getenv('user1')
pw1 = os.getenv('pw1')



# Configuración de la página
st.set_page_config(
    page_title="Actualizador", initial_sidebar_state="collapsed", layout="centered" 
)
db = conectar_db()

# Título y encabezados
st.divider()
st.header('Bienvenid@ al Actualizador')
st.divider()

# Entrada del nombre del usuario
st.write('¿Quién eres?')
user = st.text_input('Introduce tu nombre')

# Verificación del nombre y la contraseña
acceso = False
if user:
    # if user == "":
    #     st.write(f'Hola {user}, para confirmar que eres tú, por favor escribe aquí tu contraseña.')
    #     pw = st.text_input('Escribe aquí tu contraseña', type='password')
    #     if pw == "":
    #         acceso = True
    #         st.write('Acceso concedido.')
    #     elif pw:
    #         st.write('Contraseña incorrecta.')
    if user == user1:
        st.write(f'Hola {user}, para confirmar que eres tú, por favor escribe aquí tu contraseña.')
        pw = st.text_input('Escribe aquí tu contraseña', type='password')
        if pw == pw1:
            acceso = True
            st.write('Acceso concedido.')
        elif pw:
            acceso = 0
            st.write('Acceso denegado.')
            st.write('Contraseña incorrecta.')
    else:
        st.write('A ti no te conozco, por favor contacta con los admins.')



if acceso:
    st.divider()
    st.write(f'Hola {user}, ¿qué quieres hacer?')
    
    
    opcion = st.selectbox(
        'Selecciona una acción:',
        ['Seleccionar...', 'Añadir', 'Modificar', 'Borrar']
    )
    variables = ['Seleccionar...','Compañias','Producto','Fee','Precios','Comisión']
    # variables = ['Compañia', 'Producto', 'Fee', 'Fecha', 'Zona', 'Precios', 'Potencia', 'Consumo', 'Comisión']
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
########################################################              MODIFICAR              #####################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
    if opcion == 'Modificar':
        variable_seleccionada = st.selectbox('¿Qué quieres modificar?:', variables,key="001")

        if variable_seleccionada == 'Precios':
            
            # Selección de Método
            st.write('¿De qué método quieres modificar precios?')
            metodos = ['Seleccionar...', 'Indexado', 'Fijo']
            metodo = st.selectbox('Selecciona un método:', metodos)
            
            # Mostrar el siguiente paso solo si se ha seleccionado un método válido
            if metodo and metodo != 'Seleccionar...':
                if metodo == "Indexado":
                    st.write('Normalmente los precios indexados no se modifican, se añaden al histórico, a no ser que estén mal introducidos y necesitemos modificarlos.')
                    st.write('Por favor asegúrate de que estás haciendo la acción correcta.')
                    
                    # Fecha
                    st.write('Empecemos definiendo de que mes queremos modificar el precio.')
                    fechas_db = obtener_fechas_unicas(db)
                    fechas = ['Seleccionar...']
                    for i in fechas_db:
                        fechas.append(i)
                    fecha = st.selectbox('Selecciona la fecha:', fechas)
                
                    # Mostrar el mensaje final si se ha seleccionado un fee válido
                    if fecha and fecha != "Seleccionar...":

                        # Paso 2: Selección de Zona
                        st.write('¿De qué sistema vamos a modificar precios?')
                        zonas = ['Seleccionar...', 'Península', 'Baleares', 'Canarias']
                        zona_completa = st.selectbox('Selecciona un sistema:', zonas)
                        
                        # Convertir la zona completa a su abreviación
                        zone = ""
                        if zona_completa == "Península":
                            zone = "P"
                        elif zona_completa == "Baleares":
                            zone = "B"
                        elif zona_completa == "Canarias":
                            zone = "C"

                        # Mostrar el siguiente paso solo si se ha seleccionado una zona válida
                        if zona_completa and zona_completa != 'Seleccionar...':
                            # Paso 3: Selección de Tarifa
                            st.write('¿De qué tarifa quieres modificar?')
                            tarifas = ['Seleccionar...', '2.0TD', '3.0TD', '6.1TD', '6.2TD', '6.3TD', '6.4TD']
                            rate = st.selectbox('Selecciona una tarifa:', tarifas)
                            
                            # Mostrar el siguiente paso solo si se ha seleccionado una tarifa válida
                            if rate and rate != 'Seleccionar...':
                                # Paso 4: Selección de Compañía
                                st.write('Bien, ¿de qué compañía quieres modificar precios?')
                                compañias_db = obtener_compañias_unicas_zone_rate_market_fecha(db, zone, rate, metodo,fecha)
                                compañias = ['Seleccionar...']
                                for i in compañias_db:
                                    compañias.append(i)
                                company = st.selectbox('Selecciona una compañía:', compañias)
                                
                                # Mostrar el siguiente paso solo si se ha seleccionado una compañía válida
                                if company and company != "Seleccionar...":
                                    # Paso 5: Selección de Producto
                                    st.write(f'Genial, quieres modificar precios de {company}, ¿de qué producto quieres modificar precios?')
                                    productos_db = obtener_productos_unicos_por_compañia_zone_rate(db, company, zone, rate)
                                    productos = ['Seleccionar...']
                                    for i in productos_db:
                                        productos.append(i)
                                    product = st.selectbox('Selecciona el producto que quieres modificar:', productos)
                                    
                                    # Mostrar el siguiente paso solo si se ha seleccionado un producto válido
                                    if product and product != "Seleccionar...":
                                        # Paso 6: Selección de Fee
                                        st.write('Estupendo! Casi hemos terminado, necesitamos saber que fee quieres modificar.')
                                        fees_db = obtener_fees_unicos_por_compañia_product_zone_fee(db, company, zone, rate, product)
                                        fees = ['Seleccionar...']
                                        for i in fees_db:
                                            fees.append(i)
                                        fee = st.selectbox('Selecciona el fee:', fees)

                                        if fee and fee != 'Seleccionar...':
                                            precios_energia = obtener_precios_energia(db, metodo, zone, rate, company, product, fee)
                                            precios_potencia = obtener_precios_potencia(db, metodo, zone, rate, company, product, fee)
                                            st.write(f'Los precios del producto {product} de la compañía {company} para una tarifa {rate} en {zona_completa} con método {metodo} y el fee "{fee}"son:')
                                            indice = ['P1','P2','P3','P4','P5','P6']
                                            df = pd.DataFrame({'Energia': precios_energia, 'Potencia': precios_potencia}, index=indice)
                                            df_formatted = df.applymap(lambda x: f'{x:.6f}')
                                            precios_antiguos = [precios_energia,precios_potencia]
                                            st.write(df_formatted)
                                            
                                        
                                            st.divider()
                                            st.subheader('¿Quieres modificar estos precios?')
                                            respuestas = ['Selecciona...','Si','No']
                                            respuesta = st.selectbox('Selecciona una respuesta:',respuestas,key=1)
                                            if respuesta and respuesta == 'Si':
                                                # Energía
                                                st.write('Precios de energía')
                                                texto_precios_energia = st.text_input('Introduce los nuevos precios de energía (separados por espacios)')
                                                if texto_precios_energia:
                                                    # Procesar y convertir los precios de energía
                                                    respuesta_energia = texto_precios_energia.replace(',', '.')
                                                    respuesta_energia = respuesta_energia.split()
                                                    
                                                    monthly_price_EP1 = convertir_a_float(respuesta_energia[0]) if len(respuesta_energia) > 0 else 0.0
                                                    monthly_price_EP2 = convertir_a_float(respuesta_energia[1]) if len(respuesta_energia) > 1 else 0.0
                                                    monthly_price_EP3 = convertir_a_float(respuesta_energia[2]) if len(respuesta_energia) > 2 else 0.0
                                                    monthly_price_EP4 = convertir_a_float(respuesta_energia[3]) if len(respuesta_energia) > 3 else 0.0
                                                    monthly_price_EP5 = convertir_a_float(respuesta_energia[4]) if len(respuesta_energia) > 4 else 0.0
                                                    monthly_price_EP6 = convertir_a_float(respuesta_energia[5]) if len(respuesta_energia) > 5 else 0.0
                                                    precios_energia = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6]
                                                    # Potencia
                                                    
                                                st.write('Precios de potencia')
                                                texto_precios_potencia = st.text_input('Introduce los nuevos precios de potencia (separados por espacios)')
                                                if texto_precios_potencia:
                                                    # Procesar y convertir los precios de potencia
                                                    respuesta_potencia = texto_precios_potencia.replace(',', '.')
                                                    respuesta_potencia = respuesta_potencia.split()

                                                    monthly_price_PP1 = convertir_a_float(respuesta_potencia[0]) if len(respuesta_potencia) > 0 else 0.0
                                                    monthly_price_PP2 = convertir_a_float(respuesta_potencia[1]) if len(respuesta_potencia) > 1 else 0.0
                                                    monthly_price_PP3 = convertir_a_float(respuesta_potencia[2]) if len(respuesta_potencia) > 2 else 0.0
                                                    monthly_price_PP4 = convertir_a_float(respuesta_potencia[3]) if len(respuesta_potencia) > 3 else 0.0
                                                    monthly_price_PP5 = convertir_a_float(respuesta_potencia[4]) if len(respuesta_potencia) > 4 else 0.0
                                                    monthly_price_PP6 = convertir_a_float(respuesta_potencia[5]) if len(respuesta_potencia) > 5 else 0.0
                                                    precios_potencia = [monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]
                                                    
                                                    st.write('Vamos a visualizar que los precios que quieres modificar son correctos')
                                                    precios_nuevos = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6,
                                                            monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]
                                                    
                                                    df = pd.DataFrame({
                                                                    'Periodo': ['EP1', 'EP2', 'EP3', 'EP4', 'EP5', 'EP6', 'PP1', 'PP2', 'PP3', 'PP4', 'PP5', 'PP6'],
                                                                    'Precio_Antiguo': precios_antiguos,
                                                                    'Precio_Nuevo': precios_nuevos
                                                                })
                                                    df_long = df.melt(id_vars='Periodo', value_vars=['Precio_Antiguo', 'Precio_Nuevo'], var_name='Tipo', value_name='Precio')

                                                    fig = px.bar(df_long, x='Periodo', y='Precio', color='Tipo', barmode='group', title='Comparación de precios antiguos y nuevos') 

                                                    # Mostrar el gráfico en Streamlit
                                                    st.plotly_chart(fig)
                                                    st.write('Cambiar estos precios supone un efecto inmediato en nuestra base de datos y en la aplicación, comprueba por favor que sean correctos')
                                                    st.divider()
                                                    st.title('¿Estás seguro de que quieres modificar los precios de energía y potencia?')
                                                    respuestas = ['Selecciona...', 'Si', 'No']
                                                    respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_modificar')

                                                    # Si la respuesta es 'Si', mostrar el botón para modificar los precios
                                                    if respuesta == 'Si':
                                                        
                                                        # Nuevos precios definidos por el usuario
                                                        nuevos_precios = {
                                                            'monthly_price_EP1': precios_nuevos[0],
                                                            'monthly_price_EP2': precios_nuevos[1],
                                                            'monthly_price_EP3': precios_nuevos[2],
                                                            'monthly_price_EP4': precios_nuevos[3],
                                                            'monthly_price_EP5': precios_nuevos[4],
                                                            'monthly_price_EP6': precios_nuevos[5],
                                                            'monthly_price_PP1': precios_nuevos[6],
                                                            'monthly_price_PP2': precios_nuevos[7],
                                                            'monthly_price_PP3': precios_nuevos[8],
                                                            'monthly_price_PP4': precios_nuevos[9],
                                                            'monthly_price_PP5': precios_nuevos[10],
                                                            'monthly_price_PP6': precios_nuevos[11]
                                                        }
                                                        
                                                        # Filtros para encontrar el documento correcto
                                                        filtros = {
                                                            'market': metodo,
                                                            'company': company,
                                                            'zone': zone,
                                                            'rate': rate,
                                                            'product': product,
                                                            'fee': fee
                                                        }
                                                        
                                                        # Botón para realizar la actualización
                                                        if st.button('Modificar precios'):
                                                            # Solo se ejecuta esta parte si se presiona el botón
                                                            ingestar = actualizar_precios(db, filtros, nuevos_precios)
                                                            
                                                            if ingestar == "Los precios se han actualizado correctamente.":
                                                                st.success(ingestar)
                                                            else:
                                                                st.error(ingestar)
                elif metodo == "Fijo":

                    # Paso 2: Selección de Zona
                    st.write('¿De qué sistema vamos a modificar precios?')
                    zonas = ['Seleccionar...', 'Península', 'Baleares', 'Canarias']
                    zona_completa = st.selectbox('Selecciona un sistema:', zonas)
                    
                    # Convertir la zona completa a su abreviación
                    zone = ""
                    if zona_completa == "Península":
                        zone = "P"
                    elif zona_completa == "Baleares":
                        zone = "B"
                    elif zona_completa == "Canarias":
                        zone = "C"

                    # Mostrar el siguiente paso solo si se ha seleccionado una zona válida
                    if zona_completa and zona_completa != 'Seleccionar...':
                        # Paso 3: Selección de Tarifa
                        st.write('¿De qué tarifa quieres modificar?')
                        tarifas = ['Seleccionar...', '2.0TD', '3.0TD', '6.1TD', '6.2TD', '6.3TD', '6.4TD']
                        rate = st.selectbox('Selecciona una tarifa:', tarifas)
                        
                        # Mostrar el siguiente paso solo si se ha seleccionado una tarifa válida
                        if rate and rate != 'Seleccionar...':
                            # Paso 4: Selección de Compañía
                            st.write('Bien, ¿de qué compañía quieres modificar precios?')
                            compañias_db = obtener_compañias_unicas_zone_rate_market_fijo(db, zone, rate, metodo)
                            compañias = ['Seleccionar...']
                            for i in compañias_db:
                                compañias.append(i)
                            company = st.selectbox('Selecciona una compañía:', compañias)
                            
                            # Mostrar el siguiente paso solo si se ha seleccionado una compañía válida
                            if company and company != "Seleccionar...":
                                # Paso 5: Selección de Producto
                                st.write(f'Genial, quieres modificar precios de {company}, ¿de qué producto quieres modificar precios?')
                                productos_db = obtener_productos_unicos_por_compañia_zone_rate(db, company, zone, rate)
                                productos = ['Seleccionar...']
                                for i in productos_db:
                                    productos.append(i)
                                product = st.selectbox('Selecciona el producto que quieres modificar:', productos)
                                
                                # Mostrar el siguiente paso solo si se ha seleccionado un producto válido
                                if product and product != "Seleccionar...":
                                    # Paso 6: Selección de Fee
                                    st.write('Estupendo! Casi hemos terminado, necesitamos saber que fee quieres modificar.')
                                    fees_db = obtener_fees_unicos_por_compañia_product_zone_fee(db, company, zone, rate, product)
                                    fees = ['Seleccionar...']
                                    for i in fees_db:
                                        fees.append(i)
                                    fee = st.selectbox('Selecciona el fee:', fees)

                                    if fee and fee != 'Seleccionar...':
                                        precios_energia = obtener_precios_energia(db, metodo, zone, rate, company, product, fee)
                                        precios_potencia = obtener_precios_potencia(db, metodo, zone, rate, company, product, fee)
                                        st.write(f'Los precios del producto {product} de la compañía {company} para una tarifa {rate} en {zona_completa} con método {metodo} y el fee "{fee}"son:')
                                        indice = ['P1','P2','P3','P4','P5','P6']
                                        df = pd.DataFrame({'Energia': precios_energia, 'Potencia': precios_potencia}, index=indice)
                                        df_formatted = df.applymap(lambda x: f'{x:.6f}')
                                        st.write(df_formatted)
                                        
                                    
                                        st.divider()
                                        st.subheader('¿Quieres modificar estos precios?')
                                        respuestas = ['Selecciona...','Si','No']
                                        respuesta = st.selectbox('Selecciona una respuesta:',respuestas,key=1)
                                        if respuesta and respuesta == 'Si':
                                            # Energía
                                            st.write('Precios de energía')
                                            texto_precios_energia = st.text_input('Introduce los nuevos precios de energía (separados por espacios)')
                                            if texto_precios_energia:
                                                # Procesar y convertir los precios de energía
                                                respuesta_energia = texto_precios_energia.replace(',', '.')
                                                respuesta_energia = respuesta_energia.split()
                                                
                                                monthly_price_EP1 = convertir_a_float(respuesta_energia[0]) if len(respuesta_energia) > 0 else 0.0
                                                monthly_price_EP2 = convertir_a_float(respuesta_energia[1]) if len(respuesta_energia) > 1 else 0.0
                                                monthly_price_EP3 = convertir_a_float(respuesta_energia[2]) if len(respuesta_energia) > 2 else 0.0
                                                monthly_price_EP4 = convertir_a_float(respuesta_energia[3]) if len(respuesta_energia) > 3 else 0.0
                                                monthly_price_EP5 = convertir_a_float(respuesta_energia[4]) if len(respuesta_energia) > 4 else 0.0
                                                monthly_price_EP6 = convertir_a_float(respuesta_energia[5]) if len(respuesta_energia) > 5 else 0.0
                                                precios_energia = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6]
                                                # Potencia
                                                
                                            st.write('Precios de potencia')
                                            texto_precios_potencia = st.text_input('Introduce los nuevos precios de potencia (separados por espacios)')
                                            if texto_precios_potencia:
                                                # Procesar y convertir los precios de potencia
                                                respuesta_potencia = texto_precios_potencia.replace(',', '.')
                                                respuesta_potencia = respuesta_potencia.split()

                                                monthly_price_PP1 = convertir_a_float(respuesta_potencia[0]) if len(respuesta_potencia) > 0 else 0.0
                                                monthly_price_PP2 = convertir_a_float(respuesta_potencia[1]) if len(respuesta_potencia) > 1 else 0.0
                                                monthly_price_PP3 = convertir_a_float(respuesta_potencia[2]) if len(respuesta_potencia) > 2 else 0.0
                                                monthly_price_PP4 = convertir_a_float(respuesta_potencia[3]) if len(respuesta_potencia) > 3 else 0.0
                                                monthly_price_PP5 = convertir_a_float(respuesta_potencia[4]) if len(respuesta_potencia) > 4 else 0.0
                                                monthly_price_PP6 = convertir_a_float(respuesta_potencia[5]) if len(respuesta_potencia) > 5 else 0.0
                                                precios_potencia = [monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]
                                                st.write('Vamos a visualizar que los precios que quieres modificar son correctos')
                                                precios = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6,
                                                        monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]
                                                
                                                df = pd.DataFrame({'Periodo':['EP1', 'EP2', 'EP3', 'EP4', 'EP5', 'EP6','PP1', 'PP2', 'PP3', 'PP4', 'PP5', 'PP6'],
                                                                'Precio':precios})
                                                fig = px.bar(df, x='Periodo', y='Precio', title='Comparación de precios nuevos', color_discrete_sequence=['#E30613'])

                                                # Mostrar el gráfico en Streamlit
                                                st.plotly_chart(fig)
                                                st.write('Cambiar estos precios supone un efecto inmediato en nuestra base de datos y en la aplicación, comprueba por favor que sean correctos')
                                                st.divider()
                                                st.title('¿Estás seguro de que quieres modificar los precios de energía y potencia?')
                                                respuestas = ['Selecciona...', 'Si', 'No']
                                                respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_modificar')

                                                # Si la respuesta es 'Si', mostrar el botón para modificar los precios
                                                if respuesta == 'Si':
                                                    
                                                    # Nuevos precios definidos por el usuario
                                                    nuevos_precios = {
                                                        'monthly_price_EP1': precios[0],
                                                        'monthly_price_EP2': precios[1],
                                                        'monthly_price_EP3': precios[2],
                                                        'monthly_price_EP4': precios[3],
                                                        'monthly_price_EP5': precios[4],
                                                        'monthly_price_EP6': precios[5],
                                                        'monthly_price_PP1': precios[6],
                                                        'monthly_price_PP2': precios[7],
                                                        'monthly_price_PP3': precios[8],
                                                        'monthly_price_PP4': precios[9],
                                                        'monthly_price_PP5': precios[10],
                                                        'monthly_price_PP6': precios[11]
                                                    }
                                                    
                                                    # Filtros para encontrar el documento correcto
                                                    filtros = {
                                                        'market': metodo,
                                                        'company': company,
                                                        'zone': zone,
                                                        'rate': rate,
                                                        'product': product,
                                                        'fee': fee
                                                    }
                                                    
                                                    # Botón para realizar la actualización
                                                    if st.button('Modificar precios'):
                                                        # Solo se ejecuta esta parte si se presiona el botón
                                                        ingestar = actualizar_precios(db, filtros, nuevos_precios)
                                                        
                                                        if ingestar == "Los precios se han actualizado correctamente.":
                                                            st.success(ingestar)
                                                        else:
                                                            st.error(ingestar)
     
        if variable_seleccionada == 'Compañias':
            st.write('Vamos a modificar el nombre de una compañía, ¿qué compañía quieres modificar?')
            
            # Obtener la lista de compañías
            companys = obtener_compañias_unicas(db)
            respuesta_companys = ['Seleccionar...']
            for h in companys:
                respuesta_companys.append(h)

            # Primer selectbox para seleccionar la compañía
            company_seleccionada = st.selectbox('Selecciona la compañía:', respuesta_companys, key='company_select')

            # Verificar si se ha seleccionado una compañía
            if company_seleccionada != 'Seleccionar...':
                st.write('Modificar el nombre de una compañía es algo serio. ¿Estás segur@ de que quieres modificar el nombre de', company_seleccionada, '??') 
                
                # Segundo selectbox para confirmar la modificación
                respuestas = ['Selecciona...', 'Si', 'No']
                respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_modificar')

                # Si la respuesta es 'Si', mostrar el campo para ingresar el nuevo nombre
                if respuesta == 'Si':
                    st.write('De acuerdo')
                    st.write('Nombre actual de la compañía que quieres modificar:', company_seleccionada)
                    
                    # Campo de texto para el nuevo nombre
                    nuevo_nombre = st.text_input('Nuevo nombre de la compañía:')
                    
                    # Divider para separación visual
                    st.divider()
                    
                    # Verificar si el nuevo nombre ha sido ingresado
                    if len(nuevo_nombre) > 0:
                        st.write('El nombre por el que vamos a cambiar', company_seleccionada, 'es:', nuevo_nombre)
                        st.write('. . . cambiando nombre de la compañía . . .')
                        
                        # Actualizar el nombre de la compañía
                        cambiar_nombre = actualizar_compañia(db, company_seleccionada, nuevo_nombre)
                        
                        # Mostrar el resultado de la actualización
                        if cambiar_nombre == f"Se ha actualizado el nombre de la compañía {company_seleccionada} por {nuevo_nombre}":
                            st.success(cambiar_nombre)
                        else:
                            st.error(cambiar_nombre)

        elif variable_seleccionada == 'Producto':
            st.write('Vamos a modificar el nombre de un producto, ¿de qué compañía quieres modificar ese producto?')
            
            # Obtener la lista de compañías
            companys = obtener_compañias_unicas(db)
            respuesta_companys = ['Seleccionar...']
            for h in companys:
                respuesta_companys.append(h)

            # Primer selectbox para seleccionar la compañía
            company_seleccionada2 = st.selectbox('Selecciona la compañía:', respuesta_companys, key='company_select_product')

            # Verificar si se ha seleccionado una compañía
            if company_seleccionada2 != 'Seleccionar...':
                st.write('De acuerdo, ¿qué producto de', company_seleccionada2, 'quieres modificar?')
            
                # Obtener la lista de productos para la compañía seleccionada
                products = obtener_productos_unicos_por_compañia(db, company_seleccionada2)
                respuesta_products = ['Seleccionar...']
                for p in products:
                    respuesta_products.append(p)

                # Segundo selectbox para seleccionar el producto
                product_seleccionado = st.selectbox('Selecciona el producto:', respuesta_products, key='product_select')

                # Verificar si se ha seleccionado un producto
                if product_seleccionado != 'Seleccionar...':
                    st.write('Modificar el nombre de un producto es algo serio. ¿Estás segur@ de que quieres modificar el nombre de', product_seleccionado, '??') 
                    
                    # Tercer selectbox para confirmar la modificación
                    respuestas = ['Selecciona...', 'Si', 'No']
                    respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_modificar_producto')

                    # Si la respuesta es 'Si', mostrar el campo para ingresar el nuevo nombre
                    if respuesta == 'Si':
                        st.write('De acuerdo')
                        st.write('Nombre actual del producto que quieres modificar:', product_seleccionado)
                        
                        # Campo de texto para el nuevo nombre
                        nuevo_nombre = st.text_input('Nuevo nombre del producto:')
                        
                        # Divider para separación visual
                        st.divider()
                        
                        # Verificar si el nuevo nombre ha sido ingresado
                        if len(nuevo_nombre) > 0:
                            st.write('El nombre por el que vamos a cambiar', product_seleccionado, 'es:', nuevo_nombre)
                            st.write('. . . cambiando nombre del producto . . .')
                            
                            # Actualizar el nombre del producto
                            cambiar_nombre = actualizar_product(db, product_seleccionado, nuevo_nombre)
                            
                            # Mostrar el resultado de la actualización
                            if cambiar_nombre == f"Se ha actualizado el nombre del producto {product_seleccionado} por {nuevo_nombre}":
                                st.success(cambiar_nombre)
                            else:
                                st.error(cambiar_nombre)

        elif variable_seleccionada == 'Fee':
            st.write('Vamos a modificar el nombre de un Fee, ¿de qué compañía quieres modificar ese fee?')
            
            # Obtener la lista de compañías
            companys = obtener_compañias_unicas(db)
            respuesta_companys = ['Seleccionar...']
            for h in companys:
                respuesta_companys.append(h)

            # Primer selectbox para seleccionar la compañía
            company_seleccionada3 = st.selectbox('Selecciona la compañía:', respuesta_companys, key='company_select_product')

            # Verificar si se ha seleccionado una compañía
            if company_seleccionada3 != 'Seleccionar...':
                st.write('De acuerdo, ¿El fee de qué producto quieres modificar?')
            
                # Obtener la lista de productos para la compañía seleccionada
                products = obtener_productos_unicos_por_compañia(db, company_seleccionada3)
                respuesta_products = ['Seleccionar...']
                for p in products:
                    respuesta_products.append(p)

                # Segundo selectbox para seleccionar el producto
                product_seleccionado = st.selectbox('Selecciona el producto:', respuesta_products, key='product_select')
                if respuesta_products != 'Seleccionar...':
                
                    # Obtener la lista de productos para la compañía seleccionada
                    fees = obtener_fees_unicos_por_compañia_product_fee(db,company_seleccionada3,product_seleccionado)
                    respuesta_fees = ['Seleccionar...']
                    for f in fees:
                        respuesta_fees.append(f)

                    # Segundo selectbox para seleccionar el producto
                    fee_seleccionado = st.selectbox('Selecciona el fee:', respuesta_fees, key='fee_select')
                    # Verificar si se ha seleccionado un feeo
                    if fee_seleccionado != 'Seleccionar...':
                        st.write('Modificar el nombre de un fee es algo serio. ¿Estás segur@ de que quieres modificar el nombre de', fee_seleccionado, '??') 
                        
                        # Tercer selectbox para confirmar la modificación
                        respuestas = ['Selecciona...', 'Si', 'No']
                        respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_modificar_fee')

                        # Si la respuesta es 'Si', mostrar el campo para ingresar el nuevo nombre
                        if respuesta == 'Si':
                            st.write('De acuerdo')
                            st.write('Nombre actual del fee que quieres modificar:', fee_seleccionado)
                            
                            # Campo de texto para el nuevo nombre
                            nuevo_nombre = st.text_input('Nuevo nombre del fee:')
                            
                            # Divider para separación visual
                            st.divider()
                            
                            # Verificar si el nuevo nombre ha sido ingresado
                            if len(nuevo_nombre) > 0:
                                st.write('El nombre por el que vamos a cambiar', product_seleccionado, 'es:', nuevo_nombre)
                                st.write('. . . cambiando nombre del producto . . .')
                                
                                # Actualizar el nombre del producto
                                cambiar_nombre = actualizar_fee(db, fee_seleccionado, nuevo_nombre)
                                
                                # Mostrar el resultado de la actualización
                                if cambiar_nombre == f"Se ha actualizado el nombre del producto {product_seleccionado} por {nuevo_nombre}":
                                    st.success(cambiar_nombre)
                                else:
                                    st.error(cambiar_nombre)

        elif variable_seleccionada == 'Comisión':
            st.write('Vamos a modificar las comisiones, de que método quieres modificarlas?')
            metodos = ['Seleccionar...','Fijo','Indexado']
            metodo_seleccionado = st.selectbox('Selececiona el método :', metodos, key='metodo_select')
            if metodo_seleccionado != 'Seleccionar...':
                st.write('¿De qué tarifa las quieres modificar las comisiones?')
                tarifas = ['Seleccionar...', '2.0TD', '3.0TD', '6.1TD', '6.2TD', '6.3TD', '6.4TD']
                rate = st.selectbox('Selecciona la tarifa: ', tarifas, key='rate_select')
                if rate != 'Seleccionar...':
                    st.write('Vamos a modificar comisiones de una tarifa', rate)
                    st.write('En que compañia vamos a modificarlas?')
                    # Obtener la lista de compañías
                    companys = obtener_compañias_unicas_metodo(db,metodo_seleccionado)
                    respuesta_companys = ['Seleccionar...']
                    for h in companys:
                        respuesta_companys.append(h)

                    # Primer selectbox para seleccionar la compañía
                    company_seleccionada3 = st.selectbox('Selecciona la compañía:', respuesta_companys, key='company_select_product')

                    # Verificar si se ha seleccionado una compañía
                    if company_seleccionada3 != 'Seleccionar...':
                        st.write('Okey, ¿De que producto quieres modificar las comisiones?')
                    
                        # Obtener la lista de productos para la compañía seleccionada
                        products = obtener_productos_unicos_por_compañia(db, company_seleccionada3)
                        respuesta_products = ['Seleccionar...']
                        for p in products:
                            respuesta_products.append(p)

                        # Segundo selectbox para seleccionar el producto
                        product_seleccionado = st.selectbox('Selecciona el producto:', respuesta_products, key='product_select')
                        if product_seleccionado != 'Seleccionar...':
                            st.write('Estupendo quieres modificar las comisiones de ',product_seleccionado,' ,ahora dime, las comisiones de que fee quieres modificar?')
                            # Obtener la lista de productos para la compañía seleccionada
                            fees = obtener_fees_unicos_por_compañia_product_fee(db,company_seleccionada3,product_seleccionado)
                            respuesta_fees = ['Seleccionar...']
                            for f in fees:
                                respuesta_fees.append(f)

                            # Segundo selectbox para seleccionar el producto
                            fee_seleccionado = st.selectbox('Selecciona el fee:', respuesta_fees, key='fee_select')
                            # Verificar si se ha seleccionado un feeo
                            if fee_seleccionado != 'Seleccionar...':
                                st.write('De acuerdo, vamos a modificar las comisiones del fee ', fee_seleccionado,'del producto', product_seleccionado,' ')
                                consumos = obtener_consumos_unicos_por_compañia_product_fee(db,company_seleccionada3,product_seleccionado,fee_seleccionado,rate)
                                respuesta_consumos = ['Seleccionar...']
                                for c in consumos:
                                    respuesta_consumos.append(c)
                                consumo_seleccionado = st.selectbox('Selecciona el consumo asociado a la comision que quieres modificar', respuesta_consumos, key='consumo_select')
                                if consumo_seleccionado != 'Seleccionar...':
                                    st.write('Por ultimo necesitamos saber la potencia contrata asociada a la comision')
                                    potencias = obtener_potencia_unica_consumos_compañia_product_fee(db,company_seleccionada3,product_seleccionado,fee_seleccionado,rate,consumo_seleccionado)
                                    respuesta_potencias = ['Seleccionar...']
                                    for p in potencias:
                                        respuesta_potencias.append(p)
                                    potencia_seleccionada = st.selectbox('Selecciona la potencia asociada a la comision que quieres modificar', respuesta_potencias, key='potencia_select')
                                    if potencia_seleccionada != 'Seleccionar...':
                                        comision = obtener_comisiones(db, metodo_seleccionado, rate, company_seleccionada3, product_seleccionado, fee_seleccionado,consumo_seleccionado,potencia_seleccionada)
                                        st.write('La comision actual de ',product_seleccionado,'con tarifa ', rate,' con consumo ',consumo_seleccionado,'y potencia', potencia_seleccionada, 'es de ', comision ,' €')
                                        st.write('Modificar una comision es algo muy serio y que afecta directamente a la elección comercial de un producto u otro en las propuestas.')
                                        st.write('Estás segur@ de que quieres modificar esta comisión?')
                                        respuestas = ['Selecciona...', 'Si', 'No']
                                        respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_comision')

                                        # Si la respuesta es 'Si', mostrar el campo para ingresar el nuevo nombre
                                        if respuesta == 'Si':
                                            st.write('De acuerdo')
                                            st.write('Comision actual del producto elegido:', comision ,'€')
                                            nueva_comision = comision
                                            nueva_comision = st.text_input('Ingresa el nuevo valor de la comisión', key='nueva_comision')
                                            st.divider()
                                            if nueva_comision != comision:
                                                st.write('El valor por el que vamos a sustituir  :' ,comision ,'€, es : ', nueva_comision,'€')
                                                cambiar_comision = actualizar_comision(db, comision, nueva_comision)
                                                if cambiar_comision == f"Se ha actualizado el valor de la comision de {comision} por {nueva_comision}":
                                                    st.success(cambiar_comision)
                                                else:
                                                    st.error(cambiar_comision)
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ########################################################              MODIFICAR 2            #####################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################

    if opcion == 'Añadir':
        st.write('Genial !! que quieres añadir a la base de datos?')
        variables = ['Seleccionar...','Precio','Compañia','Producto','Fee','Consumo','Potencia','Comisión']
        opcion_añadir = st.selectbox('Selecciona una opción', variables, key='opcion_añadir')
        if opcion_añadir == "Precio":
            st.write('Genial!! Hoy toca actualización de precios! Yuju!!')
            # df = fetch_mongo()
            with st.expander('Filtros'):
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    metodo = st.selectbox('Metodo ', ['Seleccionar...','Fijo','Indexado'])
                with col2:
                    zone = st.selectbox('Sistema', ['Seleccionar...','Península','Baleares','Canarias'])
                with col3:
                    rates = ['Selecionar...','2.0TD','3.0TD','6.1TD','6.2TD','6.3TD','6.4TD']
                    rate = st.selectbox('Tarifa', rates)
                with col4:
                    fechas = ['Seleccionar...']
                    fechas_unicas = obtener_fechas_unicas(db)
                    for i in fechas_unicas:
                        fechas.append(i)
                    indexed_date = st.selectbox('Fecha', fechas)

                col5,col6,col7 = st.columns(3)
                with col5:
                    compañias = ['Seleccionar...']
                    compañias_unicas = obtener_compañias_unicas_metodo(db,metodo)
                    for i in compañias_unicas:
                        compañias.append(i)
                    compañia = st.selectbox('Compañia', compañias)
                with col6:
                    productos = ['Seleccionar...']
                    productos_unicos = obtener_productos_unicos_por_compañia(db,compañia)
                    for i in productos_unicos:
                        productos.append(i)
                    producto = st.selectbox('Producto', productos)
                with col7:
                    fees = ['Seleccionar...']
                    fees_unicos = obtener_fees_unicos_productos(db,producto)
                    for i in fees_unicos:
                        fees.append(i)
                    fee = st.selectbox('Fee', fees)
                filtros = []
                colA,colB,colC = st.columns(3)
                with colA:
                    pass
                with colB:
                    if st.button('Aplicar filtros'):
                        market = metodo
                        zone = zone
                        rate = rate
                        indexed_date = indexed_date
                        company = compañia
                        product = producto
                        fee = fee
                        filtros = [market,zone,rate,indexed_date,company,product,fee]
                with colC:
                    pass
            # if len(filtros) == 0:
            #     st.write(df)
            # else:
            #     df = df[(df['market'] == market) &
            #             (df['zone'] == zone) &
            #             (df['rate'] == rate) &
            #             (df['indexed_date'] == indexed_date) &
            #             (df['company'] == company) &
            #             (df['product'] == product) &
            #             (df['fee'] == fee)]
            



# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ########################################################              AÑADIR                 #####################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################

#     if opcion == 'Añadir':
#         st.write('Genial!! que quieres añadir a la base de datos?')
#         variables = ['Seleccionar...','Precio','Compañia','Producto','Fee','Consumo','Potencia','Comisión']
#         opcion_añadir = st.selectbox('Selecciona una opción', variables, key='opcion_añadir')
#         if opcion_añadir == "Precio":
#             st.write('Genial!! Hoy toca actualización de precios! Yuju!!')
#             subir_archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])
#             if subir_archivo is not None:
#                 # column_names = ['market','zone','indexed_date','company','rate','product','fee','monthly_price_EP1','monthly_price_EP2','monthly_price_EP3','monthly_price_EP4','monthly_price_EP5','monthly_price_EP6','monthly_price_PP1','monthly_price_PP2','monthly_price_PP3','monthly_price_PP4','monthly_price_PP5','monthly_price_PP6']
#                 df = pd.read_excel('añadir_precios.xlsx', sheet_name='añadir_precios',header=3)
#                 # df['indexed_date'] = df['indexed_date'].dt.strftime('%B %Y')
#                 # df['indexed_date'] = df['indexed_date'].astype(str)
#                 with st.expander('Mostrar la tabla de excel'):
#                     # nuevo_df = meses_español(df)
#                     st.dataframe(df) 

#                 # metodos_unicos = nuevo_df['market'].unique().tolist()
#                 # metodos_unicos_str = ', '.join(metodos_unicos)

#                 # fechas_unicas = nuevo_df['indexed_date'].unique().tolist()
#                 # fechas_unicas_str = ', '.join(fechas_unicas)

#                 # compañias_unicas = nuevo_df['company'].unique().tolist()
#                 # compañias_unicas_str = ', '.join(compañias_unicas)

#                 # zonas_unicas = nuevo_df['zone'].unique().tolist()
#                 # zonas_unicas_str = ', '.join(zonas_unicas)

#                 # tarifas_unicas = nuevo_df['rate'].unique().tolist()
#                 # tarifas_unicas_str = ', '.join(tarifas_unicas)

#                 # productos_unicos = nuevo_df['product'].unique().tolist()
#                 # productos_unicos_str = ', '.join(productos_unicos)

#                 # df['fee'] = df['fee'].astype(str)
#                 # fees_unicos = nuevo_df['fee'].unique().tolist()
#                 # fees_unicos_str = ', '.join(fees_unicos)

#                 advertencia = "<div style='color: red;'>Por favor lee el resumen de los precios que vas a añadir.</div>"
#                 st.markdown(advertencia, unsafe_allow_html=True)

#                 # st.write('Vamos a actualizar precios ', metodos_unicos_str)
#                 # st.write('De la/s compañia/s:', compañias_unicas_str)
#                 # st.write('En ', zonas_unicas_str)
#                 # st.write('Con fecha ', fechas_unicas_str)
#                 # st.write('Con tarifas ', tarifas_unicas_str)
#                 # st.write('En los productos', productos_unicos_str)
#                 # st.write('Con fees', fees_unicos_str)
#                 st.subheader('Añadir estos precios en nuestra base de datos es algo muy importante, afecta directamente al funcionamiento de la aplicaicón.')
#                 st.subheader('¿Estas seguro de que quieres añadir estos precios?')
#                 respuestas = ['Selecciona...', 'Si', 'No']
#                 respuesta = st.selectbox('Selecciona una respuesta:', respuestas, key='respuesta_comision')
#                 if respuesta == 'Si':
#                      st.write('Pulsa el botón para confirmar')
#                      if st.button('Añadir precios'):
#                         # Solo se ejecuta esta parte si se presiona el botón
#                         precios = añadir_precios(db,nuevo_df)
                        
#                         if "éxito" in precios:
#                             st.success(precios)
#                         else:
#                             st.error(precios)




  





        # if opcion_añadir == "Compañia":
        # if opcion_añadir == "Producto":
        # if opcion_añadir == "Fee":
        # if opcion_añadir == "Consumo":
        # if opcion_añadir == "Potencia":
        # if opcion_añadir == "Comisión":

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
########################################################              AÑADIR                 #####################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################

    # if opcion == 'Añadir':
    #     st.write('Genial!! que quieres añadir a la base de datos?')
    #     variables = ['Seleccionar...','Precio','Compañia','Producto','Fee','Consumo','Potencia','Comisión']
    #     opcion_añadir = st.selectbox('Selecciona una opción', variables, key='opcion_añadir')
    #     if opcion_añadir == "Precio":
    #         st.write('Para añadir un precio necesitamos saber algunas cosas más.')
    #         st.write('En que método quieres añadir el precio?')
    #         metodos = ['Seleccionar...','Fijo','Indexado']
    #         metodo_seleccionado = st.selectbox('Selececiona un método', metodos, key='seleccion_metodo')
    #         if metodo_seleccionado == 'Fijo':
    #             st.write('ATENCION!')
    #             st.write('Añadir un precio fijo solo lo hariamos en situaciones en las que se haya creado una compañia nueva, un producto o un fee nuevo, si es ese el caso continua, si no por favor asegúrate de estár haciendo la acción correcta.')
    #             st.divider()
    #             st.write('Añadir precios fijos está en "STAND BY" por el momento, por favor espera nuevos cambios.')
    #             st.divider()

    #         elif metodo_seleccionado == 'Indexado':
    #             st.write('A que mes corresponde el precio que quieres añadir?')
    #             meses = obtener_meses()
    #             respuesta_meses = ['Seleccionar...']
    #             for i in meses:
    #                 respuesta_meses.append(i)
    #             mes_seleccionado = st.selectbox('Selecciona un mes', respuesta_meses, key='mes_seleccionado')
    #             if mes_seleccionado != 'Seleccionar...':
    #                 st.write('Genial vamos a añadir precios a', mes_seleccionado)
    #                 st.write('A que zona corresponden los precios que quieres añadir?')
    #                 zonas = ['Seleccionar...', 'Península', 'Baleares', 'Canarias']
    #                 zona_completa = st.selectbox('Selecciona un sistema:', zonas)
                    
    #                 # Convertir la zona completa a su abreviación
    #                 zone = ""
    #                 if zona_completa == "Península":
    #                     zone = "P"
    #                 elif zona_completa == "Baleares":
    #                     zone = "B"
    #                 elif zona_completa == "Canarias":
    #                     zone = "C"

    #                 # Mostrar el siguiente paso solo si se ha seleccionado una zona válida
    #                 if zona_completa != 'Seleccionar...':
    #                     st.write('Y... en que tarifa quieres añadir precios?')
    #                     tarifas = ['Seleccionar...', '2.0TD', '3.0TD', '6.1TD', '6.2TD', '6.3TD', '6.4TD']
    #                     rate = st.selectbox('Selecciona una tarifa:', tarifas)
                        
    #                     # Mostrar el siguiente paso solo si se ha seleccionado una tarifa válida
    #                     if rate != 'Seleccionar...':
    #                         st.write('A que compañia le quieres añadir precios?')
    #                         compañias_añadir = obtener_compañias_unicas_metodo(db,metodo_seleccionado)
    #                         respuesta_compañias = ['Seleccionar...']
    #                         for i in compañias_añadir:
    #                             respuesta_compañias.append(i)
    #                         compañia_seleccionada = st.selectbox('Selecciona una compañia', respuesta_compañias, key='compañia_seleccionada')
    #                         if compañia_seleccionada != 'Seleccionar...':
    #                             st.write('Estupendo vamos a añadir precios a ', compañia_seleccionada,'en ', mes_seleccionado)
    #                             st.write('A que producto le quieres añadir los precios?')
    #                             productos_añadir = obtener_productos_unicos_por_compañia(db, compañia_seleccionada)
    #                             respuesta_productos = ['Seleccionar...']
    #                             for i in productos_añadir:
    #                                 respuesta_productos.append(i)
    #                             producto_seleccionado = st.selectbox('Selecciona un producto', respuesta_productos, key='producto_seleeccionado')
    #                             if producto_seleccionado != 'Seleccionar...':
    #                                 st.write('Wow!!', producto_seleccionado, ' va a recibir una actualización de precios!! Genial!!!')
    #                                 fees = obtener_fees_unicos_por_compañia_product_fee(db,compañia_seleccionada,producto_seleccionado)
    #                                 respuesta_fees = ['Seleccionar...']
    #                                 for f in fees:
    #                                     respuesta_fees.append(f)
    #                                 fee_seleccionado = st.selectbox('Selecciona un fee', respuesta_fees, key='fee_seleccionado')
    #                                 st.write('Vamos a añadir precios a ', fee_seleccionado,'en ', mes_seleccionado)
    #                                 if fee_seleccionado != 'Seleccionar...':
    #                                     st.write('Introduce los nuevos precios separados por espacios, por ejemplo "0.212314  0.181645  0.151201 ..."')
    #                                     precios_energia = st.text_input('Introduce los precios de energia')
    #                                     precios_potencia = st.text_input('Introduce los precios de potencia')
    #                                     if precios_energia:
    #                                         # Procesar y convertir los precios de energía
    #                                         respuesta_energia = precios_energia.replace(',', '.')
    #                                         respuesta_energia = precios_energia.split()
                                            
    #                                         monthly_price_EP1 = convertir_a_float(respuesta_energia[0]) if len(respuesta_energia) > 0 else 0.0
    #                                         monthly_price_EP2 = convertir_a_float(respuesta_energia[1]) if len(respuesta_energia) > 1 else 0.0
    #                                         monthly_price_EP3 = convertir_a_float(respuesta_energia[2]) if len(respuesta_energia) > 2 else 0.0
    #                                         monthly_price_EP4 = convertir_a_float(respuesta_energia[3]) if len(respuesta_energia) > 3 else 0.0
    #                                         monthly_price_EP5 = convertir_a_float(respuesta_energia[4]) if len(respuesta_energia) > 4 else 0.0
    #                                         monthly_price_EP6 = convertir_a_float(respuesta_energia[5]) if len(respuesta_energia) > 5 else 0.0
    #                                         precios_energia = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6]

    #                                     if precios_potencia:
    #                                         # Procesar y convertir los precios de energía
    #                                         respuesta_potencia = precios_potencia.replace(',', '.')
    #                                         respuesta_potencia = precios_potencia.split()
                                            
    #                                         monthly_price_PP1 = convertir_a_float(respuesta_potencia[0]) if len(respuesta_potencia) > 0 else 0.0
    #                                         monthly_price_PP2 = convertir_a_float(respuesta_potencia[1]) if len(respuesta_potencia) > 1 else 0.0
    #                                         monthly_price_PP3 = convertir_a_float(respuesta_potencia[2]) if len(respuesta_potencia) > 2 else 0.0
    #                                         monthly_price_PP4 = convertir_a_float(respuesta_potencia[3]) if len(respuesta_potencia) > 3 else 0.0
    #                                         monthly_price_PP5 = convertir_a_float(respuesta_potencia[4]) if len(respuesta_potencia) > 4 else 0.0
    #                                         monthly_price_PP6 = convertir_a_float(respuesta_potencia[5]) if len(respuesta_potencia) > 5 else 0.0
    #                                         precios_potencia = [monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]

    #                                         st.write('Vamos a visualizar que los precios que quieres añadir son correctos y tienen sentido')

    #                                         precios = [monthly_price_EP1, monthly_price_EP2, monthly_price_EP3, monthly_price_EP4, monthly_price_EP5, monthly_price_EP6,
    #                                                 monthly_price_PP1, monthly_price_PP2, monthly_price_PP3, monthly_price_PP4, monthly_price_PP5, monthly_price_PP6]
                                            
    #                                         df = pd.DataFrame({'Periodo':['EP1', 'EP2', 'EP3', 'EP4', 'EP5', 'EP6','PP1', 'PP2', 'PP3', 'PP4', 'PP5', 'PP6'],
    #                                                         'Precio':precios})
                                            
    #                                         fig = px.bar(df, x='Periodo', y='Precio', title='Comparación de precios', color_discrete_sequence=['#E30613'])

    #                                         # Mostrar el gráfico en Streamlit
    #                                         st.plotly_chart(fig)
    #                                         st.write('Añadir estos precios supone un efecto inmediato en nuestra base de datos y en la aplicación, comprueba por favor que sean correctos')
    #                                         st.divider()
    #                                         st.title('¿Estás seguro de que quieres añadir estos precios de energía y potencia?')
    #                                         respuesta_ingestar_precios = ['Seleccionar...','Si','No']
    #                                         respuesta_seleccionada = st.selectbox('Selecciona una respuesta:', respuesta_ingestar_precios, key='respuest_ingestar_precios')
    #                                         if respuesta_seleccionada == 'Si':
                                                            
    #                                                         # Nuevos precios definidos por el usuario
    #                                                         nuevos_precios = {
    #                                                             'monthly_price_EP1': precios[0],
    #                                                             'monthly_price_EP2': precios[1],
    #                                                             'monthly_price_EP3': precios[2],
    #                                                             'monthly_price_EP4': precios[3],
    #                                                             'monthly_price_EP5': precios[4],
    #                                                             'monthly_price_EP6': precios[5],
    #                                                             'monthly_price_PP1': precios[6],
    #                                                             'monthly_price_PP2': precios[7],
    #                                                             'monthly_price_PP3': precios[8],
    #                                                             'monthly_price_PP4': precios[9],
    #                                                             'monthly_price_PP5': precios[10],
    #                                                             'monthly_price_PP6': precios[11]
    #                                                         }
                                                            
    #                                                         # Filtros para encontrar el documento correcto
    #                                                         filtros = {
    #                                                             'market': metodo_seleccionado,
    #                                                             'company': compañia_seleccionada,
    #                                                             'zone': zone,
    #                                                             'rate': rate,
    #                                                             'product': producto_seleccionado,
    #                                                             'fee': fee_seleccionado
    #                                                         }
                                                            
    #                                                         # Botón para realizar la actualización
    #                                                         if st.button('Modificar precios'):
    #                                                             # Solo se ejecuta esta parte si se presiona el botón
    #                                                             ingestar = añadir_precios(db, metodo,fecha, company, product, fee, precios)
                                                                
    #                                                             if ingestar == "Los precios se han actualizado correctamente.":
    #                                                                 st.success(ingestar)
    #                                                             else:
    #                                                                 st.error(ingestar)





        # if opcion_añadir == "Compañia":
        # if opcion_añadir == "Producto":
        # if opcion_añadir == "Fee":
        # if opcion_añadir == "Consumo":
        # if opcion_añadir == "Potencia":
        # if opcion_añadir == "Comisión":