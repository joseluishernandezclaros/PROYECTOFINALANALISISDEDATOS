from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


app = Flask(__name__)


# Configurar opciones de visualización
# Configura el número máximo de filas a mostrar
pd.set_option('display.max_rows', 10)
# Configura el número máximo de columnas a mostrar
pd.set_option('display.max_columns', 10)

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv('housing_fincaraiz_graf.csv', sep=";")
df2 = pd.read_csv('housing_fincaraiz.csv', sep=";")


# Ruta para la página principal


@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar el DataFrame en formato HTML


@app.route('/dataframe')
def show_dataframe():
    return render_template('dataframe.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


# Ruta para mostrar información sobre los datos faltantes


# Ruta para mostrar información sobre los datos faltantes
@app.route('/missing_data')
def show_missing_data():
    missing_data = df.isnull().mean() * 100

    # Convertir a DataFrame
    missing_data_df = missing_data.to_frame(
        name='Porcentaje de Datos Faltantes')

    # Convertir a HTML con opciones para manejar la codificación y saltos de línea
    html_content = missing_data_df.to_html(
        classes='data', escape=False, index=False)

    # Guardar contenido HTML en un archivo con codificación UTF-8
    with open('missing_data_html_content.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    return render_template('missing_data.html', missing_data=html_content)

# Ruta para mostrar el nombre de todas las columnas


@app.route('/column_names')
def show_column_names():
    column_names = df.columns
    num_columns = len(column_names)
    return render_template('column_names.html', column_names=column_names, num_columns=num_columns)


# Ruta para eliminar columnas innecesarias
@app.route('/eliminate_columns')
def eliminate_columns():
    # Lista de columnas a eliminar
    columns_to_drop = ['Circuito cerrado de TV', 'Parqueadero Visitantes', 'Barra estilo americano',
                       'Chimenea', 'Depósito / Bodega', 'Salón Comunal', 'Parques cercanos']

    # Eliminar las columnas
    df_filtered = df.drop(columns_to_drop, axis=1)

    # Convertir el DataFrame resultante a HTML
    dataframe_html = df_filtered.to_html(classes='data', index=False)

    return render_template('eliminate_columns.html', dataframe=dataframe_html)


# Ruta para observar todos los valores de la primera fila
@app.route('/first_row_values')
def first_row_values():
    # Seleccionar el DataFrame a usar (df o df2)
    current_df = df  # Puedes cambiar df2 por df según sea necesario

    # Obtener la primera fila
    first_row = current_df.iloc[0]

    # Convertir la primera fila a HTML
    first_row_html = first_row.to_frame(
        name='Valores de la Primera Fila').to_html(classes='data')

    return render_template('first_row_values.html', first_row_values=first_row_html)

# Ruta para el cambio de nombre de la columna


@app.route('/rename_column')
def rename_column():
    # Seleccionar el DataFrame a usar (df o df2)
    current_df = df  # Puedes cambiar df2 por df según sea necesario

    # Cambiar el nombre de la columna
    current_df.rename(columns={'nombre': 'Tipo de vivienda'}, inplace=True)

    # Convertir el DataFrame a HTML
    renamed_column_html = current_df.to_html(classes='data')

    return render_template('rename_column.html', renamed_column=renamed_column_html)

# Ruta para mostrar la gráfica del área privada y verificar cuántas viviendas tienen área privada de 0 metros cuadrados


@app.route('/area_privada_cero_chart')
def area_privada_cero_chart():
    # Verificar cuántas viviendas tienen área privada de 0 metros cuadrados
    viviendas_con_0_m2 = df[df['area_privada'] == '0 m²']
    num_viviendas_con_0_m2 = len(viviendas_con_0_m2)
    print("Número de viviendas con '0 m²':", num_viviendas_con_0_m2)

    # Graficar el área privada
    df['area_privada'] = df['area_privada'].str.extract('(\d+)').astype(float)
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df['area_privada'])
    plt.xlabel('Viviendas')
    plt.ylabel('Área Privada (m²)')
    plt.title('Área Privada de Viviendas')

    # Guardar la gráfica en un archivo BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convertir la gráfica a formato base64 para mostrarla en el HTML
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return render_template('area_privada_cero_chart.html', area_privada_chart=img_base64, num_viviendas_con_0_m2=num_viviendas_con_0_m2)

# Ruta para eliminar todas las filas con área privada igual a 0


# Ruta para eliminar áreas privadas iguales a 0
@app.route('/eliminar_area_privada_cero')
def eliminar_area_privada_cero():
    # Seleccionar el DataFrame a usar (df o df2)
    current_df = df2  # Puedes cambiar df2 por df según sea necesario

    # Eliminar áreas privadas igual a 0
    current_df = current_df[current_df['area_privada'] != '0 m²']

    # Convertir el DataFrame resultante a HTML
    df_html = current_df.to_html(classes='data')

    return render_template('eliminar_area_privada_cero.html', df=df_html)

# Ruta para volver a verificar cuántas viviendas tienen área privada de 0 metros cuadrados


@app.route('/verificar_area_privada_cero')
def verificar_area_privada_cero():
    # Filtrar viviendas con área privada de 0 metros cuadrados
    viviendas_con_0_m2 = df[df['area_privada'] == '0 m²']

    # Obtener el número de viviendas con área privada de 0 metros cuadrados
    num_viviendas_con_0_m2 = len(viviendas_con_0_m2)

    # Imprimir en la consola el número de viviendas con área privada de 0 metros cuadrados
    print("Número de viviendas con '0 m²':", num_viviendas_con_0_m2)

    # Convertir la información a HTML
    viviendas_con_0_m2_html = viviendas_con_0_m2.to_html(
        classes='data', index=False)

    return render_template('verificar_area_privada_cero.html',
                           viviendas_con_0_m2_html=viviendas_con_0_m2_html,
                           num_viviendas_con_0_m2=num_viviendas_con_0_m2)


# Ruta para agrupar viviendas por estratos y mostrar cuántas viviendas hay en cada estrato
@app.route('/conteo_por_estrato')
def conteo_por_estrato():
    # Agrupar viviendas por estrato y contar el número de viviendas en cada estrato
    conteo_por_estrato = df.groupby('estrato').size()

    # Mostrar el conteo de filas por estrato en la consola
    print("Conteo de filas por estrato:")
    print(conteo_por_estrato)

    # Convertir la información a HTML
    conteo_por_estrato_html = conteo_por_estrato.to_frame(
        name='Conteo de Viviendas').to_html(classes='data', escape=False)

    return render_template('conteo_por_estrato.html', conteo_por_estrato_html=conteo_por_estrato_html)

# Ruta para eliminar las filas con estrato 0 y volver a mostrar cuántas viviendas hay en cada estrato


# Ruta para eliminar las filas con estrato 0 y volver a mostrar cuántas viviendas hay en cada estrato
@app.route('/eliminar_estrato_cero')
def eliminar_estrato_cero():
    # Filtrar las filas con estrato diferente de 0
    df_filtrado = df[df['estrato'] != 0]

    # Contar el número de viviendas en cada estrato después de la eliminación
    conteo_por_estrato = df_filtrado.groupby('estrato').size()

    # Graficar los resultados
    conteo_por_estrato.plot(kind='bar')
    plt.xlabel('Estrato')
    plt.ylabel('Conteo de Filas')
    plt.title('Conteo de Filas por Estrato')

    # Guardar la gráfica en un archivo BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convertir la gráfica a formato base64 para mostrarla en el HTML
    img_base64 = base64.b64encode(img.getvalue()).decode()

    # Convertir la información de conteo a HTML
    conteo_por_estrato_html = conteo_por_estrato.to_frame(
        name='Conteo de Viviendas').to_html(classes='data', escape=False)

    return render_template('eliminar_estrato_cero.html', conteo_por_estrato_html=conteo_por_estrato_html, grafica_estrato=img_base64)


if __name__ == '__main__':
    app.run(debug=True)
