#!/usr/bin/env python
# coding: utf-8

# # ANALISE EXPLORATÓRIA DA PRODUÇÃO DE SOJA BRASILEIRA 

# In[22]:


#Importando as bibliotecas necessárias

import folium
import geojson
import pandas as pd
import plotly.express as px
import json
from urllib.request import urlopen
import plotly as plt


# In[23]:


#Importando mapa do google

mapa = folium.Map(location = [-13.6599529,-69.6827802])
mapa


# In[24]:


#Plotando o mapa com visão de satelite.
folium.Map(location = [-13.6599529,-69.6827802], tiles = 'Stamen Terrain', zoom_start = 4)


# In[25]:


#exibindo coordenadas de tatitude e longitude no evento de click no mapa
#Ajuda a encontrar a latitude para futuras coordenadas

mapa.add_child(folium.LatLngPopup())


# In[26]:


df = pd.read_csv("dadosgovbr.csv",sep = ';', encoding="latin-1")
df.UF.unique()


# In[27]:


#Instanciando o GeoJson para atrelar as informações de estados aos dados

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
 Brazil = json.load(response) 
Brazil


# In[28]:


#Amarrando as informções de geolocalização dos estados para serem plotados nos graficos
state_id_map = {}
for feature in Brazil ['features']:
 feature['id'] = feature['properties']['name']
 state_id_map[feature['properties']['sigla']] = feature['id']


# In[29]:


#Importando os dados referente a produção de soja.

soybean = pd.read_csv('https://raw.githubusercontent.com/nayanemaia/Dataset_Soja/main/soja%20sidra.csv')
print(soybean)


# In[30]:


#Gerando o gráfico.

fig = px.choropleth(
 soybean, #soybean database
 locations = "Estado", #define the limits on the map/geography
 geojson = Brazil, #shape information
 color = "Produção", #defining the color of the scale through the database
 hover_name = "Estado", #the information in the box
 hover_data =["Produção","Longitude","Latitude"],
 title = "Produtividade da soja (Toneladas)", #title of the map
 animation_frame = "ano" #creating the application based on the year
)
fig.update_geos(fitbounds = "locations", visible = False)
fig.show()


# In[31]:


#Salvando o resultado em um arquivo HTML

plt.offline.plot(fig, filename = 'map1.html')

