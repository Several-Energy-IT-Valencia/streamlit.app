import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
dbname = os.getenv('DBNAME_MONGO')

def conectar_db():
    client = MongoClient(MONGO_URI)
    db = client[dbname]
    return db

def obtener_compañias_unicas(db):
    unicos = db['pruebas_alex'].distinct('company')
    return unicos

def obtener_compañias_unicas_metodo(db,metodo):
    unicos = db['pruebas_alex'].distinct('company',{'market':metodo})
    return unicos

def obtener_fees_unicos_productos(db,producto):
    unicos = db['pruebas_alex'].distinct('fee',{'product':producto})
    return unicos

def obtener_productos_unicos_por_compañia(db, compañia):
    productos = db['pruebas_alex'].distinct('product', {'company': compañia})
    return productos

def obtener_compañias_unicas_zone_rate_market_fecha(db, zone, rate, metodo,fecha):
    compañias = db['pruebas_alex'].distinct('company', {'zone': zone,'rate':rate,'market':metodo,'indexed_date':fecha})
    return compañias

def obtener_compañias_unicas_zone_rate_market_fijo(db, zone, rate, metodo):
    compañias = db['pruebas_alex'].distinct('company', {'zone': zone,'rate':rate,'market':metodo,'indexed_date':"-"})
    return compañias

def obtener_fechas_unicas(db):
    fechas = db['pruebas_alex'].distinct('indexed_date')
    return fechas

def obtener_productos_unicos_por_compañia_zone_rate(db, compania,zone,rate):
    productos = db['pruebas_alex'].distinct('product', {'company': compania,'zone': zone,'rate':rate})
    return productos

def obtener_fees_unicos_por_compañia_product_zone_fee(db,company,zone,rate,product):
    productos = db['pruebas_alex'].distinct('fee', {'company': company,'zone': zone,'rate':rate,'product':product})
    return productos

def obtener_fechas_unicas_por_compañia_product_zone_fee_fecha(db,company,zone,rate,product,fee):
    productos = db['pruebas_alex'].distinct('indexed_date', {'company': company,'zone': zone,'rate':rate,'product':product,'fee':fee})
    return productos

def obtener_fees_unicos_por_compañia_product_fee(db,company,product):
    productos = db['pruebas_alex'].distinct('fee', {'company': company,'product':product})
    return productos

def obtener_consumos_unicos_por_compañia_product_fee(db, company, product, fee,rate):
    consumos = db['pruebas_alex'].distinct('consumo', {'company': company, 'product': product, 'fee': fee, 'rate': rate})
    consumos = [int(consumo) for consumo in consumos]
    return consumos

def obtener_potencia_unica_consumos_compañia_product_fee(db,company,product,fee,rate,consumo):
    consumos = db['pruebas_alex'].distinct('potencia', {'company': company, 'product': product, 'fee': fee, 'rate': rate, 'consumo': consumo})
    return consumos


def obtener_precios_energia(db, metodo, zone, rate, company, product, fee):
    # Realizar la consulta en la colección 'pruebas_alex' con los filtros especificados
    cursor = db['pruebas_alex'].find(
        {'market': metodo, 'company': company, 'zone': zone, 'rate': rate, 'product': product, 'fee': fee},
        {
            'monthly_price_EP1': 1, 'monthly_price_EP2': 1, 'monthly_price_EP3': 1,
            'monthly_price_EP4': 1, 'monthly_price_EP5': 1, 'monthly_price_EP6': 1,
            '_id': 0  # Excluir el campo _id
        }
    )
    
    # Convertir el cursor en una lista de documentos
    precios_list = list(cursor)
    
    # Si la consulta devuelve resultados, extraer los precios del primer documento
    if precios_list:
        doc = precios_list[0]  # Tomamos el primer documento encontrado
        precios_energia = [
            doc.get('monthly_price_EP1', 0.0),
            doc.get('monthly_price_EP2', 0.0),
            doc.get('monthly_price_EP3', 0.0),
            doc.get('monthly_price_EP4', 0.0),
            doc.get('monthly_price_EP5', 0.0),
            doc.get('monthly_price_EP6', 0.0),
        ]
    else:
        # Si no hay resultados, devolver una lista de ceros
        precios_energia = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    return precios_energia

def obtener_precios_potencia(db, metodo, zone, rate, company, product, fee):
    # Realizar la consulta en la colección 'pruebas_alex' con los filtros especificados
    cursor = db['pruebas_alex'].find(
        {'market': metodo, 'company': company, 'zone': zone, 'rate': rate, 'product': product, 'fee': fee},
        {
            'monthly_price_PP1': 1, 'monthly_price_PP2': 1, 'monthly_price_PP3': 1,
            'monthly_price_PP4': 1, 'monthly_price_PP5': 1, 'monthly_price_PP6': 1,
            '_id': 0  # Excluir el campo _id
        }
    )
    
    # Convertir el cursor en una lista de documentos
    precios_list = list(cursor)
    
    # Si la consulta devuelve resultados, extraer los precios del primer documento
    if precios_list:
        doc = precios_list[0]  # Tomamos el primer documento encontrado
        precios_potencia = [
            doc.get('monthly_price_PP1', 0.0),
            doc.get('monthly_price_PP2', 0.0),
            doc.get('monthly_price_PP3', 0.0),
            doc.get('monthly_price_PP4', 0.0),
            doc.get('monthly_price_PP5', 0.0),
            doc.get('monthly_price_PP6', 0.0),
        ]
    else:
        # Si no hay resultados, devolver una lista de ceros
        precios_potencia = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    return precios_potencia


def convertir_a_float(valor):
    try:
        return float(valor)
    except ValueError:
        return 0.0
    

# Función para actualizar los precios en la base de datos
def actualizar_precios(db, filtros, nuevos_precios):
    result = db['pruebas_alex'].update_one(
        filtros,  # Filtros para encontrar el documento
        {'$set': nuevos_precios}  # Valores a actualizar
    )
    
    # Verificar el resultado de la actualización
    if result.matched_count > 0:
        if result.modified_count > 0:
            return "Los precios se han actualizado correctamente."
        else:
            return "No se han realizado cambios en los precios (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con los filtros proporcionados."
    
def actualizar_compañia(db, nombre_actual, nuevo_nombre):
    result = db['pruebas_alex'].update_many(
        {'company': nombre_actual},  # Filtro para encontrar los documentos con la compañía seleccionada
        {'$set': {'company': nuevo_nombre}}  # Nuevo nombre de la compañía
    )
    
    # Verificar el resultado de la actualización
    if result.matched_count > 0:
        if result.modified_count > 0:
            return f"Se han actualizado el nombre de la compañia {nombre_actual}, por {nuevo_nombre}"
        else:
            return "No se han realizado cambios en los nombres de las compañías (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con el nombre de la compañía proporcionado."
    

def actualizar_product(db, nombre_actual, nuevo_nombre):
    result = db['pruebas_alex'].update_many(
        {'product': nombre_actual}, 
        {'$set': {'product': nuevo_nombre}} 
    )
    
    # Verificar el resultado de la actualización
    if result.matched_count > 0:
        if result.modified_count > 0:
            return f"Se ha actualizado el nombre del producto {nombre_actual} por {nuevo_nombre}"
        else:
            return "No se han realizado cambios en los nombres de los productos (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con el nombre del producto proporcionado."
    
def actualizar_fee(db, nombre_actual, nuevo_nombre):
    result = db['pruebas_alex'].update_many(
        {'fee': nombre_actual}, 
        {'$set': {'fee': nuevo_nombre}} 
    )
    
    # Verificar el resultado de la actualización
    if result.matched_count > 0:
        if result.modified_count > 0:
            return f"Se ha actualizado el nombre del fee {nombre_actual} por {nuevo_nombre}"
        else:
            return "No se han realizado cambios en los nombres de los fees (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con el nombre del fee proporcionado."
    

def obtener_comisiones(db, metodo, rate, company, product, fee,consumo,potencia):
    # Realizar la consulta en la colección 'pruebas_alex' con los filtros especificados
    cursor = db['pruebas_alex'].find(
        {'market': metodo, 'company': company, 'rate': rate, 'product': product, 'fee': fee, 'consumo': consumo, 'potencia': potencia,},
        {
            'comision': 1
        }
    )

    # Convertir el cursor en una lista de documentos
    comision_list = list(cursor)


    return comision_list[0]['comision']

def actualizar_comision(db, nombre_actual, nuevo_nombre):
    # Convertir nuevo_nombre a entero
    try:
        nuevo_nombre = int(nuevo_nombre)
    except ValueError:
        return "El nuevo nombre proporcionado no es un número entero válido."

    result = db['pruebas_alex'].update_many(
        {'comision': nombre_actual}, 
        {'$set': {'comision': nuevo_nombre}} 
    )
    
    # Verificar el resultado de la actualización
    if result.matched_count > 0:
        if result.modified_count > 0:
            return f"Se ha actualizado el valor de la comisión de {nombre_actual} por {nuevo_nombre}"
        else:
            return "No se han realizado cambios en los valores (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con el nombre de la comisión proporcionado."
    
def obtener_meses():
    # Crear una lista para almacenar los meses y años
    meses_y_años = []
    
    # Obtener el mes y año actual
    fecha_actual = datetime.now()
    
    # Diccionario para traducir los nombres de los meses
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    
    # Añadir el mes y año actual y los 11 meses anteriores
    for i in range(12):
        fecha = fecha_actual - relativedelta(months=i)
        mes_anio = f"{meses_es[fecha.month]} {fecha.year}"
        meses_y_años.append(mes_anio)
    
    # Invertir la lista para que el mes actual esté al final
    meses_y_años.reverse()
    
    return meses_y_años


def añadir_precios(db, metodo,fecha, company, product, fee, precios):
    if len(precios) != 12:
        return "La lista de precios debe contener 12 números."
    
    campos_ep = [f"monthly_price_EP{i+1}" for i in range(6)]
    campos_pp = [f"monthly_price_PP{i+1}" for i in range(6)]
    
    update_fields = {}
    for i in range(6):
        update_fields[campos_ep[i]] = precios[i]
        update_fields[campos_pp[i]] = precios[i+6]

    result = db['pruebas_alex'].update_many(
        {'metodo': metodo, 'company': company, 'indexed_date':fecha, 'product': product, 'fee': fee},
        {'$set': update_fields}
    )
    
    if result.matched_count > 0:
        if result.modified_count > 0:
            return f"Se han añadido los precios para los filtros proporcionados."
        else:
            return "No se han realizado cambios en los valores (los valores ya eran los mismos)."
    else:
        return "No se encontró ningún documento que coincida con los filtros proporcionados."
    

def meses_español(df):
    # Diccionario para el reemplazo de nombres de meses de inglés a español
    replacements = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
        'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
        'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
        'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    
    # Convertir la columna 'indexed_date' a string si aún no lo es
    df['indexed_date'] = df['indexed_date'].astype(str)
    
    # Aplicar reemplazos utilizando el método replace y pasando el diccionario
    df['indexed_date'] = df['indexed_date'].replace(replacements, regex=True)
    
    return df


def añadir_precios(db, df):
    # Preparar una lista para guardar los documentos a insertar
    documentos = []

    # Recorrer cada fila del DataFrame
    for index, row in df.iterrows():
        # Crear un diccionario para el documento actual
        documento = {
            "market": row['market'],
            "zone": row['zone'],
            "rate": row['rate'],
            "indexed_date": row['indexed_date'],
            "company": row['company'],
            "product": row['product'],
            "fee": row['fee'],
        }
        
        # Añadir los precios mensuales EP1 a EP6
        for i in range(1, 7):
            documento[f"monthly_price_EP{i}"] = row[f"monthly_price_EP{i}"]

        # Añadir los precios mensuales PP1 a PP6
        for i in range(1, 7):
            documento[f"monthly_price_PP{i}"] = row[f"monthly_price_PP{i}"]

        # Añadir el documento a la lista
        documentos.append(documento)

    # Insertar todos los documentos en la colección
    result = db['pruebas_alex'].insert_many(documentos)
    
    # Verificar el resultado de la inserción
    if result.acknowledged:
        return f"Se han insertado {len(result.inserted_ids)} documentos con éxito."
    else:
        return "No se pudo insertar los documentos."


def fetch_mongo():

    db = conectar_db()
    
    # Seleccionar la colección
    collection = db['pruebas_alex']
    
    # Traer todos los documentos de la colección
    documents = list(collection.find())
    
    # Convertir los documentos en un DataFrame de pandas
    dataframe = pd.DataFrame(documents)
    
    return dataframe





