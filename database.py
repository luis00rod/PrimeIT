#!/usr/bin/env python
# coding: utf-8

# ## Importacion de las librerias necesarias

# In[1]:


import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import MySQLdb
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import drange


# ## Parametros para establecer conexion con la base de datos

# In[2]:


db_data = 'mysql+mysqldb://' + 'root' + ':' + 'M4110rca' + '@' + 'localhost' + ':3306/'        + 'primeit' + '?charset=utf8mb4'


# ## Creacion de conexion con la base de datos

# In[3]:


engine = create_engine(db_data)


# ## Importacion a la base de datos  

# In[4]:


df = pd.read_csv('local_source/Prueba_AnalisisDatos.csv')


# In[24]:


df.to_sql("prueba_analisisdatos", engine)


# ## Carga de la tabla de la base de datos

# In[7]:


df_from_db = pd.read_sql_table('prueba_analisisdatos', engine)
df_from_db.head(5)


# ## Limpieza y transformacion de datos

# In[8]:


def clean_and_transform_data(data):
    data['fecha_reserva'] = pd.to_datetime(data['fecha_reserva'], errors ='coerce', format = "%d/%m/%Y")
    data['coste_reserva'] = data['coste_reserva'].apply(lambda x: float(x.split()[0].replace(',', '.')))
    data['pvp_reserva'] = data['pvp_reserva'].apply(lambda x: float(x.split()[0].replace(',', '.')))
    
    return data


# In[9]:


df_from_db = clean_and_transform_data(df_from_db)
df_from_db


# ## Propiedades estadisticas de la tabla df_from_db

# In[10]:


df_from_db.describe()


# ## Cantidad Vendida y Cantidad ganada durante el mes

# In[11]:


Ganancias_mes = df_from_db['pvp_reserva'].sum() - df_from_db['coste_reserva'].sum()
print('Cantidad Vendida:',df_from_db['pvp_reserva'].sum())
print('Cantidad ganada:',Ganancias_mes)


# ## Grafica de la evolucion temporal de la ventas

# In[12]:


xpoints = df_from_db['fecha_reserva']
ypoints = df_from_db['pvp_reserva']

plt.figure(figsize=(15,8))
plt.plot(xpoints, ypoints)
plt.show()


# ## Outliers encontrado en la columna pvp_reserva

# In[13]:


df_from_db[df_from_db['pvp_reserva'] == -248.21]


# ## Outliers encontrados en la columna coste_reserva 
# ## Vemos que hay valores negativos para los costes de reserva

# In[14]:


df_from_db[df_from_db['coste_reserva'] < 0]


# ## Filtros de la data por fines de semana

# In[15]:


df_primer_weekend = df_from_db[(df_from_db.fecha_reserva >= '2022-08-05') & (df_from_db.fecha_reserva <= '2022-08-07') ]


# In[16]:


df_segundo_weekend = df_from_db[(df_from_db.fecha_reserva >= '2022-08-12') & (df_from_db.fecha_reserva <= '2022-08-14') ]


# In[17]:


df_tercer_weekend = df_from_db[(df_from_db.fecha_reserva >= '2022-08-19') & (df_from_db.fecha_reserva <= '2022-08-21') ]


# In[18]:


df_cuarto_weekend = df_from_db[(df_from_db.fecha_reserva >= '2022-08-26') & (df_from_db.fecha_reserva <= '2022-08-28') ]


# ## Data historica de los fines de semana

# In[19]:


df_weekend = pd.concat([df_primer_weekend, df_segundo_weekend, df_tercer_weekend, df_cuarto_weekend])
df_weekend


# ## Ganancias los fines de semana

# In[20]:


ganancia_weekend = df_weekend.pvp_reserva.sum()-df_weekend.coste_reserva.sum()


# In[21]:


print(ganancia_weekend)


# ## Ganancias entre semana

# In[22]:


ganancias_non_weekend = Ganancias_mes - ganancia_weekend


# In[23]:


print(ganancias_non_weekend)


# ## El ejercicio numero tres no se pudo realizar por falta de datos

# In[ ]:




