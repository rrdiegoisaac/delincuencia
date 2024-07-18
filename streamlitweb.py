import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import numpy as np

df = pd.read_csv('dbdelitoschile.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Fecha'] = df['Fecha'].dt.date

color_set = px.colors.qualitative.G10[::-1]

# Configuración de la página
st.set_page_config(page_title='Delitos Chile',
                   layout='wide')


# Usar Markdown para formatear el título
st.title('Historial de delitos en Chile (2005-2023)')


# Iconos sociales
linkedin_icon_url = "https://cdn-icons-png.freepik.com/256/174/174857.png?semt=ais_hybrid"
github_icon_url = "https://www.svgrepo.com/show/475654/github-color.svg"

def social_icon(link, icon_url, name):
    icon_markdown = f'<a href="{link}" target="_blank"><img src="{icon_url}" width="30" style="vertical-align: bottom;"> {name}</a>'
    st.sidebar.markdown(icon_markdown, unsafe_allow_html=True)


st.write(df) 

# Barra lateral con controles interactivos
st.sidebar.header("Control interactivo para visualizar delitos en regiones")
st.sidebar.write("""
- Se pueden seleccionar regiones y delitos, hay gráficos que les afecta este filtro, y otros que no.
- Se puede hacer zoom seleccionando un área del gráfico. Para regresar del zoom, se puede realizar un doble click en el gráfico.
- En la esquina superior derecha de un gráfico, se ofrece la opción de colocar el gráfico en pantalla completa.
""")
regiones_unique = df['Región'].unique().tolist()
delitos_unique = df['Delitos'].unique().tolist()

regiones_predeterminadas = ['Valparaíso', 'Biobío']
delitos_predeterminados = ['Amenazas', 'Violencia intrafamiliar a mujer']

regiones_seleccionadas = st.sidebar.multiselect('Seleccionar Regiones', regiones_unique, default=regiones_predeterminadas)
delitos_seleccionados = st.sidebar.multiselect('Seleccionar Tipos de Delito', delitos_unique, default=delitos_predeterminados)

fecha_min = df['Fecha'].min()
fecha_max = df['Fecha'].max()
fecha_seleccionada = st.sidebar.slider('Seleccionar Rango de Fechas', fecha_min, fecha_max, (fecha_min, fecha_max))


# Gráfico de delitos totales en Chile

total_delitos_por_año = df.groupby('Fecha')['Cantidad'].sum().reset_index()
total_delitos_por_año = total_delitos_por_año[(total_delitos_por_año['Fecha'] >= fecha_seleccionada[0]) & (total_delitos_por_año['Fecha'] <= fecha_seleccionada[1])]
fig1 = px.area(total_delitos_por_año, x='Fecha', y='Cantidad', title='Delitos en Chile por Mes y Año',
              color_discrete_sequence=color_set, height=600, width=800)





# Crear combinaciones de fechas, regiones y delitos
combinaciones = pd.MultiIndex.from_product([df['Fecha'].unique(), regiones_seleccionadas, delitos_seleccionados], names=['Fecha', 'Región', 'Delitos'])
df_combinado = pd.DataFrame(index=combinaciones).reset_index()

# Filtrar y preparar datos para el gráfico de líneas
df_filtrado = pd.merge(df_combinado, df, on=['Fecha', 'Región', 'Delitos'], how='left').fillna(0)
df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_seleccionada[0]) & (df_filtrado['Fecha'] <= fecha_seleccionada[1])]

# Crear gráfico de líneas facetado por región y tipo de delito
fig2 = px.line(df_filtrado, x='Fecha', y='Cantidad', color='Delitos',
              facet_row='Región', facet_col_wrap=2,
              title='Delitos por Año en Regiones y Tipos de Delito Seleccionados',
              labels={'Cantidad': 'Cantidad de Delitos'},
              height=600, width=800)  # Ajusta el ancho del gráfico aquí




df_filtrado = df[df['Delitos'].isin(delitos_seleccionados)]
df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_seleccionada[0]) & (df_filtrado['Fecha'] <= fecha_seleccionada[1])]

# Crear histograma de distribución de delitos por región
fig3 = px.histogram(df_filtrado, x='Cantidad', y='Región', color='Delitos',
                   title='Distribución de Delitos por Región en Chile',
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   labels={'Región': 'Región', 'Cantidad': 'Cantidad de Delitos', 'Delitos': 'Tipo de Delito'},
                   orientation='h', height=600)

regiones_ordenadas = df_filtrado.groupby('Región')['Cantidad'].sum().sort_values(ascending=True).index.tolist()
fig3.update_yaxes(categoryorder='array', categoryarray=regiones_ordenadas)


# Gráfico de líneas con delitos totales por región


total_delitos_por_año = df.groupby(['Región', 'Fecha'])['Cantidad'].sum().reset_index()
df_filtrado = total_delitos_por_año[total_delitos_por_año['Región'].isin(regiones_seleccionadas)]
df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_seleccionada[0]) & (df_filtrado['Fecha'] <= fecha_seleccionada[1])]

# Crear gráfico de area facetado por región

fig4 = px.area(df_filtrado, x='Fecha', y='Cantidad', title='Delitos por Año en Regiones Seleccionadas',
              color='Región', color_discrete_sequence=color_set, height=600, width=1200)
fig4.update_layout(
    xaxis_title='Año',
    yaxis_title='Total de Delitos',
    legend_title='Región'
)


frecuencia_delitos_por_region = df.groupby(['Región', 'Delitos'])['Cantidad'].sum().reset_index()
fig5 = px.treemap(data_frame=frecuencia_delitos_por_region, path=['Región', 'Delitos'], values='Cantidad',
                 color_discrete_sequence=color_set, title='Frecuencia de Delitos por Región', height=1200, width=1200)
fig5.update_traces(textinfo='label+value')


# Mapa de calor de delitos por mes y año
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Mes'] = df['Fecha'].dt.month
df['Año'] = df['Fecha'].dt.year

fig6 = px.density_heatmap(df, x='Mes', y='Año', z='Cantidad', 
                         histfunc='sum', title='Mapa de Calor de Delitos por Mes',
                         height=800, width=1200,
                         labels={'Cantidad': 'Cantidad de Delitos'},
                         color_continuous_scale='Blues')
fig6.update_layout(xaxis_title='Mes', yaxis_title='Año', yaxis_type='category')
fig6.update_xaxes(tickvals=list(range(1, 13)))  
fig6.update_coloraxes(colorbar_title='Total de Delitos')  


# MOSTRAR GRÁFICOS


# Mostrar los gráficos en columnas
col1, col2 = st.columns(2)
with col1:
    st.header("Delitos totales por Región")
    st.write('Muestra la suma de los delitos cometidos en las regiones seleccionadas')
    st.plotly_chart(fig1, use_container_width=True)  
with col2:
    st.header("Suma de delitos por Región")
    st.write('Muestra la suma total de los delitos seleccionados, en todas las regiones del país')
    st.plotly_chart(fig4, use_container_width=True) 

st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)
st.plotly_chart(fig6, use_container_width=True)
# Mostrar mapa
# Código del iframe
iframe_code = '''
<iframe title="Distribución de total de delitos en Chile (2005-2023)" aria-label="Mapa" id="datawrapper-chart-rMD4T" src="https://datawrapper.dwcdn.net/rMD4T/2/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="1132" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>
'''

# Mostrar el iframe en Streamlit
st.components.v1.html(iframe_code, height=1200)  # Ajusta la altura según sea necesario

# Pie de página y contacto
st.sidebar.markdown("---")
st.sidebar.markdown("### Puedes contactarme en:")
social_icon("https://www.linkedin.com/in/rrdiegoisaac/", linkedin_icon_url, "Diego Isaac")
social_icon("https://github.com/rrdiegoisaac?tab=repositories", github_icon_url, "Diego Isaac")
