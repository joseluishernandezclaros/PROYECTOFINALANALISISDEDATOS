from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import io


def crear_app():

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
        df['area_privada'] = df['area_privada'].str.extract(
            '(\d+)').astype(float)
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

    # Ruta para mostrar la información del DataFrame

    @app.route('/show_info')
    def show_info():
        # Capturar la salida de la consola en un objeto StringIO
        buffer = io.StringIO()
        df.info(buf=buffer)

        # Obtener la información como cadena de texto
        df_info = buffer.getvalue()
        # Renderiza la plantilla y pasa la información del DataFrame
        return render_template('show_info.html', df_info=df_info)

    # Ruta para agrupar viviendas por estratos y mostrar cuántas viviendas hay en cada estrato

    # Ruta para transformar y mostrar información actualizada

    # Ruta para transformar datos

    @app.route('/transformar_datos')
    def transformar_datos():
        # Copia del DataFrame original para no modificar el original
        df_transformado = df.copy()

        # Convierte las columnas a numérico, maneja valores no esperados
        df_transformado['habitaciones'] = pd.to_numeric(
            df_transformado['habitaciones'], errors='coerce')
        df_transformado['baños'] = pd.to_numeric(
            df_transformado['baños'], errors='coerce')
        df_transformado['parqueaderos'] = pd.to_numeric(
            df_transformado['parqueaderos'], errors='coerce')
        df_transformado['precio'] = pd.to_numeric(
            df_transformado['precio'], errors='coerce')

        # Convierte "No definida" a NaN
        df_transformado.replace('No definida', pd.NA, inplace=True)

        # Rellena los valores NaN con 0
        df_transformado.fillna(0, inplace=True)

        # Convierte 'area_construida' y 'area_privada' a numérico, maneja valores no esperados
        df_transformado['area_construida'] = pd.to_numeric(
            df_transformado['area_construida'].astype(str).str.replace(' m²', ''), errors='coerce')
        df_transformado['area_privada'] = pd.to_numeric(
            df_transformado['area_privada'].astype(str).str.replace(' m²', ''), errors='coerce')

        # Convierte 'area_construida' y 'area_privada' a Int64
        df_transformado['area_construida'] = df_transformado['area_construida'].round(
        ).astype('Int64')
        df_transformado['area_privada'] = df_transformado['area_privada'].round(
        ).astype('Int64')

        # Luego, convierte las demás columnas a int64
        df_transformado['habitaciones'] = df_transformado['habitaciones'].astype(
            'int64')
        df_transformado['baños'] = df_transformado['baños'].astype('int64')
        df_transformado['parqueaderos'] = df_transformado['parqueaderos'].astype(
            'int64')
        df_transformado['precio'] = df_transformado['precio'].astype('int64')

        # Capturar la salida de la consola en un objeto StringIO
        buffer = io.StringIO()
        df_transformado.info(buf=buffer)

        # Obtener la información como cadena de texto
        df_info = buffer.getvalue()

        # Renderiza la plantilla y pasa la información del DataFrame
        return render_template('transformar_datos.html', df_info=df_info)

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

    # Ruta para ver valores de un estrato en específico, del 1 al 6

    # Variable para almacenar el estrato deseado, inicializada en 2 por defecto
    estrato_deseado = 1

    @app.route('/ver_valores_estrato', methods=['GET', 'POST'])
    def ver_valores_estrato():
        global estrato_deseado

        if request.method == 'POST':
            # Si el formulario se envió, actualiza el estrato deseado
            estrato_deseado = int(request.form['nuevo_estrato'])

        # Filtrar el DataFrame para el estrato deseado
        grupo_estrato = df[df['estrato'] == estrato_deseado]

        # Mostrar los datos del estrato en la consola (puedes comentar estas líneas si no deseas imprimir en la consola)
        print(f'Datos del Estrato {estrato_deseado}:')
        print(grupo_estrato)

        # Convertir los datos del estrato a HTML
        grupo_estrato_html = grupo_estrato.to_html(classes='data', index=False)

        return render_template('ver_valores_estrato.html', estrato_deseado=estrato_deseado, grupo_estrato_html=grupo_estrato_html)

    # Ruta para calcular el promedio del precio por cantidad de habitaciones

    # Ruta para calcular el promedio del precio por cantidad de habitaciones

    @app.route('/promedio_precio_por_habitaciones')
    def promedio_precio_por_habitaciones():
        # Seleccionar el DataFrame a usar (df o df2)
        current_df = df  # Puedes cambiar df2 por df según sea necesario

        # Seleccionar las columnas 'precio' y 'habitaciones'
        a = current_df['precio']
        b = current_df['habitaciones']

        # Crear un nuevo DataFrame con las columnas 'precio' y 'habitaciones'
        df_calculo = pd.DataFrame({'precio': a, 'habitaciones': b})

        # Convertir las columnas a tipos numéricos si no lo están ya
        df_calculo['precio'] = pd.to_numeric(
            df_calculo['precio'], errors='coerce')
        df_calculo['habitaciones'] = pd.to_numeric(
            df_calculo['habitaciones'], errors='coerce')

        # Eliminar filas con valores nulos
        df_calculo = df_calculo.dropna()

        # Agrupar por la cantidad de habitaciones
        grouped = df_calculo.groupby('habitaciones')

        # Inicializar listas para almacenar los resultados
        habitaciones_values = []
        promedio_precios = []

        # Iterar sobre los grupos y calcular el promedio del precio para cada grupo de habitaciones
        for habitaciones, group in grouped:
            habitaciones_values.append(habitaciones)
            promedio_precio = group['precio'].sum() / len(group)
            promedio_precios.append(promedio_precio)

        # Crear un nuevo DataFrame con los resultados
        resultados = pd.DataFrame(
            {'habitaciones': habitaciones_values, 'promedio_precio': promedio_precios})

        # Ordenar los resultados por la cantidad de habitaciones de manera ascendente
        resultados = resultados.sort_values(by='habitaciones')

        # Convertir el DataFrame de resultados a formato HTML
        resultados_html = resultados.to_html(classes='data', index=False)

        # Graficar los resultados
        plt.figure(figsize=(10, 6))
        plt.plot(resultados['habitaciones'],
                 resultados['promedio_precio'], marker='o', linestyle='-')
        plt.xlabel('Cantidad de Habitaciones')
        plt.ylabel('Promedio del Precio')
        plt.title('Promedio del Precio por Cantidad de Habitaciones')
        plt.grid(True)

        # Guardar la gráfica en un archivo BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Convertir la gráfica a formato base64 para mostrarla en el HTML
        img_base64 = base64.b64encode(img.getvalue()).decode()

        return render_template('promedio_precio_por_habitaciones.html', resultados_html=resultados_html, grafica_promedio_precio=img_base64)

    # Ruta para mostrar el conteo de habitaciones y su gráfica

    @app.route('/conteo_habitaciones')
    def conteo_habitaciones():
        # Leer el DataFrame desde el archivo CSV
        df = pd.read_csv('housing_fincaraiz_graf.csv', sep=";")

        # Filtrar las filas que no sean "No definida" y que no sean 0 habitaciones
        df = df[(df['habitaciones'] != "No definida")
                & (df['habitaciones'] != 0)]

        # Convertir la columna "habitaciones" a tipo entero
        df['habitaciones'] = df['habitaciones'].astype(int)

        # Agrupar por la columna "habitaciones"
        grupos = df.groupby('habitaciones')

        # Contar cuántos elementos hay en cada grupo
        conteo = grupos.size()

        # Ordenar en orden ascendente por la columna "habitaciones"
        conteo = conteo.sort_index()

        # Graficar los resultados
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.xlabel('Habitaciones')
        plt.ylabel('Conteo')
        plt.title('Conteo de Habitaciones')

        # Guardar la gráfica en un archivo BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Convertir la gráfica a formato base64 para mostrarla en el HTML
        img_base64 = base64.b64encode(img.getvalue()).decode()

        # Convertir el conteo a formato HTML
        conteo_html = conteo.to_frame(name='Conteo de Habitaciones').to_html(
            classes='data', escape=False)

        return render_template('conteo_habitaciones.html', conteo_html=conteo_html, grafica_conteo=img_base64)

    # Ruta para mostrar el conteo de baños y su gráfica

    @app.route('/conteo_banos')
    def conteo_banos():
        # Leer el DataFrame desde el archivo CSV
        df = pd.read_csv('housing_fincaraiz_graf.csv', sep=";")

        # Eliminar filas con 'No definida' en la columna 'baños'
        df = df[df['baños'] != 'No definida']

        # Convertir la columna "baños" a tipo entero
        df['baños'] = df['baños'].astype(int)

        # Agrupar por la columna "baños"
        grupos = df.groupby('baños')

        # Contar cuántos elementos hay en cada grupo
        conteo = grupos.size()

        # Ordenar en orden ascendente por la columna "baños"
        conteo = conteo.sort_index()

        # Graficar los resultados
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.xlabel('Baños')
        plt.ylabel('Conteo')
        plt.title('Conteo de Baños')

        # Guardar la gráfica en un archivo BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Convertir la gráfica a formato base64 para mostrarla en el HTML
        img_base64 = base64.b64encode(img.getvalue()).decode()

        # Convertir el conteo a formato HTML
        conteo_html = conteo.to_frame(name='Conteo de Baños').to_html(
            classes='data', escape=False)

        return render_template('conteo_banos.html', conteo_html=conteo_html, grafica_conteo=img_base64)

    # Nueva ruta para la matriz de correlación

    @app.route('/correlation_matrix')
    def correlation_matrix():
        # Seleccionar solo las variables numéricas para la matriz de correlación
        numeric_columns = df.select_dtypes(include=['int64', 'Int64']).columns
        numeric_data = df[numeric_columns]

        # Calcular la matriz de correlación
        correlation_matrix = numeric_data.corr()

        # Crear un mapa de calor con la matriz de correlación
        plt.figure(figsize=(15, 10))
        sns.heatmap(correlation_matrix, annot=True,
                    cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title('Matriz de Correlación')

        # Guardar la gráfica en un archivo BytesIO
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Convertir la gráfica a formato base64 para mostrarla en el HTML
        img_base64 = base64.b64encode(img.getvalue()).decode()

        return render_template('correlation_matrix.html', correlation_matrix=img_base64)

    def detectar_valores_atipicos(df, columns_to_check, umbral_atipico):
        informe_html = ""

        for column_to_check in columns_to_check:
            try:
                numeric_values = pd.to_numeric(
                    df[column_to_check], errors='coerce')
                numeric_values = numeric_values.dropna()
            except pd.errors.OutOfBoundsDatetime:
                informe_html += f'<p>No se puede convertir la columna {column_to_check} a valores numéricos.</p>'
                continue

            mean_value = numeric_values.mean()
            std_dev = numeric_values.std()

            umbral_superior = mean_value + umbral_atipico * std_dev
            umbral_inferior = mean_value - umbral_atipico * std_dev

            bool_index = numeric_values.index
            bool_series = (numeric_values > umbral_superior) | (
                numeric_values < umbral_inferior)

            outliers = df.loc[bool_index][bool_series]

            informe_html += f'<h2>Valores atípicos en {column_to_check} (umbral={umbral_atipico}):</h2>'
            informe_html += outliers.to_html(index=False, classes='data')

        return informe_html

    # Nueva ruta para verificar valores atípicos

    @app.route('/verificar_atipicos')
    def verificar_atipicos():
        # Lista de columnas para verificar
        columns_to_check = ['habitaciones', 'baños', 'parqueaderos', 'area_construida', 'area_privada', 'estrato', 'estado',
                            'antiguedad', 'administracion', 'precio_m2', 'nombre', 'ubicacion', 'precio']

        # Ajustar el umbral a 2
        umbral_atipico = 8  # Puedes ajustar este valor según tus necesidades

        # Almacenar resultados
        resultados_atipicos = {}

        # Iterar sobre las columnas y verificar valores atípicos
        for column_to_check in columns_to_check:
            # Intentar convertir la columna a valores numéricos y manejar los errores
            try:
                numeric_values = pd.to_numeric(
                    df[column_to_check], errors='coerce')
                numeric_values = numeric_values.dropna()
            except pd.errors.OutOfBoundsDatetime:
                print(
                    f'No se puede convertir la columna {column_to_check} a valores numéricos.')
                continue

            # Calcular el promedio y la desviación estándar
            mean_value = numeric_values.mean()
            std_dev = numeric_values.std()

            # Establecer umbrales para valores atípicos en ambas direcciones
            umbral_superior = mean_value + umbral_atipico * std_dev
            umbral_inferior = mean_value - umbral_atipico * std_dev

            # Asegurarse de que las series booleanas tengan el mismo índice
            bool_index = numeric_values.index
            bool_series = (numeric_values > umbral_superior) | (
                numeric_values < umbral_inferior)

            # Identificar valores atípicos
            outliers = df.loc[bool_index][bool_series]

            # Almacenar los resultados
            resultados_atipicos[column_to_check] = {
                'umbral': umbral_atipico,
                'outliers': outliers.to_html(classes='data', index=False)
            }

        # Renderizar la plantilla y pasar los resultados
        return render_template('verificar_atipicos.html', resultados_atipicos=resultados_atipicos)
    return app


if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)
