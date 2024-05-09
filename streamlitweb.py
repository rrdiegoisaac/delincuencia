import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import numpy as np

df = pd.read_csv('C:/Users/Diego/Desktop/Accesos/Python Files/ProyectoDelincuencia/dbdelitoschile.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
df['Fecha'] = pd.to_datetime(df['Fecha'])
color_set = px.colors.qualitative.G10[::-1]

st.set_page_config(page_title='Delitos Chile')
st.title('Historial de delitos en Chile (2005-2023)')
####################
# URL del ícono de LinkedIn
linkedin_icon_url = "https://cdn-icons-png.freepik.com/256/174/174857.png?semt=ais_hybrid"

# URL del ícono de GitHub
github_icon_url = "https://www.svgrepo.com/show/475654/github-color.svg"

# Función para mostrar el ícono y el enlace
def social_icon(link, icon_url, name):
    icon_markdown = f'<a href="{link}" target="_blank"><img src="{icon_url}" width="30" style="vertical-align: bottom;"> {name}</a>'
    st.markdown(icon_markdown, unsafe_allow_html=True)

# Llamar a la función con tu link de LinkedIn y tu nombre
social_icon("https://www.linkedin.com/in/rrdiegoisaac/", linkedin_icon_url, "Diego Isaac")

# Llamar a la función con tu link de GitHub y tu nombre
social_icon("https://github.com/rrdiegoisaac?tab=repositories", github_icon_url, "Diego Isaac")



########################################################################

st.header("Base de datos de Delitos")
st.write("""
Extraída del Centro de Estudios y Análisis del Delito (CEAD) a través de web scraping
""")
st.write(df)  # visualize the dataframe



########################################################################
st.header("Delitos totales en Chile")
st.write("""
El gráfico a continuación muestra el total de delitos reportados por mes y año.
""")
total_delitos_por_año = df.groupby('Fecha')['Cantidad'].sum().reset_index()
fig = px.line(total_delitos_por_año, x='Fecha', y='Cantidad', title='Delitos en Chile por Mes y Año', color_discrete_sequence=color_set,
height=600, width=1200)

st.plotly_chart(fig, use_container_width=True)
########################################################################
st.sidebar.header("Control interactivo para visualizar delitos en regiones")

# Definir los controles interactivos para seleccionar las regiones y los delitos
regiones_unique = df['Región'].unique().tolist()
regiones_seleccionadas = st.sidebar.multiselect('Seleccionar Regiones', regiones_unique)

delitos_unique = df['Delitos'].unique().tolist()
delitos_seleccionados = st.sidebar.multiselect('Seleccionar Tipos de Delito', delitos_unique)

########################################################################
st.title("Mapas interactivos de delitos (Utilizar control interactivo de la izquierda)")
st.header('Regiones y Delitos')
st.write('Seleccionar Región(es) y Delito(s)')
# Definir los controles interactivos para seleccionar las regiones y los delitos
#regiones_unique = df['Región'].unique().tolist()
#regiones_seleccionadas = st.multiselect('Seleccionar Regiones', regiones_unique)

#delitos_unique = df['Delitos'].unique().tolist()
#delitos_seleccionados = st.multiselect('Seleccionar Tipos de Delito', delitos_unique)

# Crear un DataFrame con todas las combinaciones de fecha, región y delito
combinaciones = pd.MultiIndex.from_product([df['Fecha'].unique(), regiones_seleccionadas, delitos_seleccionados], names=['Fecha', 'Región', 'Delitos'])
df_combinado = pd.DataFrame(index=combinaciones).reset_index()

# Combinar el DataFrame completo con los datos filtrados
df_filtrado = pd.merge(df_combinado, df, on=['Fecha', 'Región', 'Delitos'], how='left').fillna(0)

# Configurar y mostrar el gráfico
fig = px.line(df_filtrado, x='Fecha', y='Cantidad', color='Delitos',
              facet_row='Región', facet_col_wrap=2,
              title='Delitos por Año en Regiones y Tipos de Delito Seleccionados',
              labels={'Cantidad': 'Cantidad de Delitos'},
              height=600, width=1200)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

########################################################################
st.header("Suma de delitos por Región")
st.write('Muestra la suma total de los delitos seleccionados, en todas las regiones del país')

# Obtener la lista única de delitos
delitos_unique = df['Delitos'].unique()

# Widget de selección para los delitos
#delitos_seleccionados = st.multiselect('Seleccionar delitos', delitos_unique)
df_filtrado = df[df['Delitos'].isin(delitos_seleccionados)]
fig = px.bar(df_filtrado, x='Región', y='Cantidad', title='Delitos por región en Chile',
             color='Delitos', color_discrete_sequence=px.colors.qualitative.Pastel,
             labels={'Región': 'Región', 'Cantidad': 'Cantidad de Delitos', 'Delitos': 'Tipo de Delito'},
             height=600)
st.plotly_chart(fig, use_container_width=True)


########################################################################
#st.header('Delitos totales por Región')
#st.write('Muestra la cantidad de delitos que se cometieron por región')
# Filtrar el DataFrame según las regiones y los delitos seleccionados
df_filtrado = df[(df['Región'].isin(regiones_seleccionadas)) & (df['Delitos'].isin(delitos_seleccionados))]

# Agrupar y sumar los delitos por año
total_delitos_por_año = df_filtrado.groupby(['Fecha', 'Región'])['Cantidad'].sum().reset_index()

# Configurar y mostrar el gráfico
#fig = px.line(total_delitos_por_año, x='Fecha', y='Cantidad', color='Región',
             # title='Delitos por Año en Regiones y Tipos de Delito Seleccionados',
             # labels={'Cantidad': 'Total de Delitos'},
              #height=600, width=1200)


# Mostrar el gráfico en Streamlit
#st.plotly_chart(fig, use_container_width=True)


########################################################################

st.header("Delitos totales por Región")
st.write('Muestra la suma de los delitos cometidos en las regiones seleccionadas')
# Calcular la suma de delitos por año para todas las regiones
total_delitos_por_año = df.groupby(['Región', 'Fecha'])['Cantidad'].sum().reset_index()

# Crear controles interactivos para seleccionar las regiones
regiones_unique = df['Región'].unique().tolist()
#regiones_seleccionadas = st.multiselect('Seleccionar Regiones', regiones_unique, default=regiones_unique)

# Filtrar el DataFrame según las regiones seleccionadas
df_filtrado = total_delitos_por_año[total_delitos_por_año['Región'].isin(regiones_seleccionadas)]

# Configurar y mostrar el gráfico
fig = px.line(df_filtrado, x='Fecha', y='Cantidad', title='Delitos por Año en Regiones Seleccionadas',
              color='Región', color_discrete_sequence=px.colors.qualitative.Plotly, height=600, width=1200)
fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Total de Delitos',
    legend_title='Región'
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

########################################################################
st.markdown("## Distribución de delitos en las regiones")

frecuencia_delitos_por_region = df.groupby(['Región', 'Delitos'])['Cantidad'].sum().reset_index()
fig = px.treemap(data_frame=frecuencia_delitos_por_region, path=['Región', 'Delitos'], values='Cantidad',
                 color_discrete_sequence=color_set, title='Frecuencia de Delitos por Región', height=600, width=1200)
fig.update_traces(textinfo='label+value')
st.plotly_chart(fig, use_container_width=True)

########################################################################
st.markdown("## Frecuencia de delitos por Mes y Año")
df['Mes'] = df['Fecha'].dt.month
df['Año'] = df['Fecha'].dt.year

# Crear el mapa de calor
fig = px.density_heatmap(df, x='Mes', y='Año', z='Cantidad', 
                         histfunc='sum', title='Mapa de Calor de Delitos por Mes',
                         height=600, width=1200,
                         labels={'Cantidad': 'Cantidad de Delitos'},
                         color_continuous_scale='Blues')
fig.update_layout(xaxis_title='Mes', yaxis_title='Año', yaxis_type='category')
fig.update_xaxes(tickvals=list(range(1, 13)))  # Esto muestra todos los meses del año
fig.update_coloraxes(colorbar_title='Total de Delitos')  # Cambia el título de la barra de colores
st.plotly_chart(fig, use_container_width=True)
########################################################################


# Footer
st.write("""
El propósito detrás de la creación de esta página web es proporcionar una plataforma para presentar un proyecto personal. 
El proyecto nació debido a la poca flexibilidad que muestra el CEAD para presentar sus estadísticas.
Pueden contactarme en mis redes sociales compartidas al principio de esta página. Espero que les sea útil.
""")
