#----------------------------------------------LIBRERIAS----------------------------------------------------------------------
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns 
import plotly.express as px




#----------------------------------------------CONFIGURACIÓN DE PÁGINA ----------------------------------------------------------------------

st.set_page_config(page_title="Los Pequeños del Titanic", layout="centered", page_icon="👋")


#---------------------------------------------- LECTURA DEL ARCHIVO CSV COMO DATAFRAME----------------------------------------------------------------------
df_titanic = pd.read_csv("C:/Users/objet/samplerepo/datos/titanic.csv")
columns=('col %d' % i for i in range(20))

# Eliminamos la columna cabin 
dft = df_titanic.drop(columns=["Cabin"])

# Rellenamos valores nulos de la columna age con la mediana 
#dft.describe()["Age"]
dft=dft.fillna(dft.mean())

# Cambiamos el dtype de la columna age a int
dft['Age']=dft['Age'].astype('int')

# Agregamos una nueva columna que específique las etiquetas de tratmiento según la edad 

def Label(Age):
    if Age <= 1:
        return "Baby"
    elif Age >= 2 and Age <= 3:
        return "Toddler"
    elif Age >= 4 and Age <= 12:
         return "Kid"
    elif Age >= 13 and Age <= 17:
        return "Teen"
    elif Age >= 18 and Age <= 65:
        return "Adult"
    else:
        return "Elderly"

dft["Label"] = dft["Age"].apply(lambda x: Label(x))

# Movemos la columna Label justo al lado de la edad
columnas = list(dft.columns)
columnas.insert(6, columnas.pop(columnas.index('Label')))
dft = dft.reindex(columns=columnas)

# Comprobamos que ya no tenemos valores nulos en la columna age
dft.isnull().sum().sort_values(ascending=False)

# Cambiamos el nombre de la columna embarked por port
dft = dft.rename(columns = {'Embarked':'Port'})

# Rellenamos valores nulos de la columna port
dft["Port"].fillna("No info", inplace = True)

# Colocamos los nombres enteros de los puertos 
dft = dft.replace({"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"})

# Especificamos en la columna fare el tipo de moneda
dft.rename(columns = { "Fare":"Fare £"}, inplace=True)

# En la columna survived cambiamos el número 0 por false indicando que no ha sobrevivido y el 1 por true indicando que ha sobrevivido
dft["Survived"] = dft["Survived"].replace({0: False, 1: True}) 

# Filtramos los datos de solo las muertes
dfm = dft[dft["Survived"] == False]
#dfm

# Filtramos valores para solo obtener resultados de los menores de edad que han fallecido
dfk = dfm[dfm["Label"].isin(["Baby", "Toddler", "Kid", "Teen"])]
#dfk

# Creamos una paleta de colores personalizada para nuestros gráficos
my_colors = sns.color_palette(["#66b3ff","#ff9999", "#99ff99","#9999ff"])
my_palette = sns.color_palette(my_colors)

#---------------------------------------------- EMPIEZA LA APP ----------------------------------------------------------------------
st.title('Los pequeños del Titanic') 
st.subheader('Gabriellys Gonzalez')
st.subheader('18 Febrero 2023')
texto = 'En 1907, los presidentes de la naviera White Star Line pusieron en marcha un ambicioso proyecto para construir un trío de transatlánticos que destacarían por ser los más grandes, rápidos y lujosos del mundo. Fue un desafío de la ingeniería de principios de siglo XX y decidieron bautizarlos con nombres inspirados en la mitología griega: Olympic, Titanic y Gigantic.\n\nEl segundo se convirtió en leyenda debido a su trágico destino y a que en su momento fue publicitado como un barco casi insumergible. Era el barco más grande y lujoso que se había construido nunca, pero naufragó en apenas tres horas durante su viaje inaugural.\n\nEsta tragedia sumergió no solo un barco de lujo, si no el futuro de familias con la muerte de niños y adolescentes aquella madrugada del 15 de abril de 1912. A pesar del famoso "niños y mujeres primero" la realidad es que no todos lograron salvarse.'
st.write(texto)
#---------------------------------------------- TABLAS QUE COMPONEN LA APP ----------------------------------------------------------------------

tabs = st.tabs(["DataFrames", "Deceased","Profile","Comparison"]) 

# Botón de dataframes
tab_plots= tabs[0] 
with tab_plots: 
    tabs_data = st.tabs(["DataFrame Debug","Dataframe Children"])
    tab_plots = tabs_data[0]
    with tab_plots:
        st.write("Este es el DataFrame depurado") 
        st.dataframe(dft)
    tab_plots = tabs_data[1]
    with tab_plots:
        st.write("Este es el DataFrame de solo menores de edad fallecidos")
        st.dataframe(dfk)

# Botón de Death
tab_plots= tabs[1]  
with tab_plots: 
    tabs_deceased = st.tabs(["Muertes vs sobrevivientes", "Edades muertos","Edades niños muertos","Etiquetas niños muertos"])
    tab_plots = tabs_deceased[0]
    with tab_plots:
        st.write("En la tragedia del Titanic se contabilizan más muertes que sobrevivientes a pesar de los sacrificios hechos para salvar a los pasajeros.")
        st.image('a.png')
with tab_plots:  
    tab_plots = tabs_deceased[1]
    with tab_plots:
        st.write("Entre esos muertos se registra mayor número de personas en la franja de 20 - 30 años.")
        st.image('b.png')
    tab_plots = tabs_deceased[2]
    with tab_plots:
        st.write("A pesar del niños primero, vemos una incidencia de muertes en niños...")
        st.image('c.png')
    tab_plots = tabs_deceased[3]
    with tab_plots:
        st.write("¿Qué determinó la supervivencia de unos y otros?")
        st.image('d.png')

# Botón de Profile
tab_plots= tabs[2]  
with tab_plots:  
    tabs_profile = st.tabs(["Género","Precio Billete","Clase social","Puerto de embarque"])
    tab_plots = tabs_profile[0]
    with tab_plots:
        st.write("Género masculino")
        st.image('e.png')
    tab_plots = tabs_profile[1]
    with tab_plots:
        st.write("Una franja de coste de billetes entre 20 y 30 mil libras...")
        st.image('f.png')
    tab_plots = tabs_profile[2]
    with tab_plots:
        st.write("Gran mayoría de tercera clase...")
        st.image('z.png')
    tab_plots = tabs_profile[3]
    with tab_plots:
        st.write("Y su principal puerto de embarque fue de Southampton...")
        Port = dfk['Port'].value_counts()
        colores = ['#ff9999', '#66b3ff', '#99ff99']
        y = px.treemap(Port, path=[Port.index], values=Port, height=700,title='Puerto de Salida Víctimas', color_discrete_sequence=colores)
        st.plotly_chart(y)

# Botón de Comparison
tab_plots= tabs[3]  
with tab_plots:  
    tabs_comparison = st.tabs(["Comparación género","Comparación clase"])
    tab_plots = tabs_comparison[0]
    with tab_plots:
        st.write("En cambio, el género femenino tiene una cuantía superior en supervivencia...")
        st.image('h.png')
    tab_plots = tabs_comparison[1]
    with tab_plots:
        st.write("Pero la tercera clase sigue siendo clave en decesos y supervivientes.")
        st.image('i.png')

st.title('Conclusión') 
conclu = "No podemos confirmar qué factores eran determinantes a la hora de elegir quién subía al bote, sin embargo según los datos anteriormente vistos vemos una diferencia significativa de incidencias de fallecimientos en menores de edad cuyo perfil se inclina más hacia el género masculino y de tercera clase"
st.write(conclu)
       

   
#----------------------------------------------EMPIEZA EL SIDEBAR----------------------------------------------------------------

#ocultar errores
st.set_option('deprecation.showPyplotGlobalUse', False)   
st.sidebar.title('Escenas nunca vistas del Titanic') 
st.sidebar.video ("https://www.youtube.com/watch?v=Q_5M5CRTIHk")
st.sidebar.write("Sidebar Titanic") 
