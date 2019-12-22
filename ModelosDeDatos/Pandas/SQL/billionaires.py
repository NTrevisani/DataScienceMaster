#!/usr/bin/env python
# coding: utf-8

# # Billionaires
# 
# `conda install sqlite sqlalchemy`
# 
# Source: https://corgis-edu.github.io/corgis/csv/billionaires/
# 
# SQLAlchemy: https://docs.sqlalchemy.org/en/13/core/connections.html

# In[3]:


import numpy as np
import pandas as pd


# In[4]:


# Cargo el dataset
df = pd.read_csv('billionaires.csv', delimiter = ',')
df.head(7)


# ## All rows where company is Microsoft or Zara

# In[5]:


df[(df['company.name'] == "Zara") | (df['company.name'] == "Microsoft")] 


# ## Number of times each person appears in the database in descending order

# In[6]:


df.groupby('name').size().sort_values(ascending = False)


# In[7]:


# equivalente a
df['name'].value_counts(ascending = False)


# ## Top ten sectors (by frequency appereance in the dataset)

# In[8]:


df.groupby('company.sector').size().sort_values(ascending = False)[0:10]


# ## SQL IO
# 
# Create a database called 'billionaries' using sqlite and save the data from the dataframe using the appropiate tables. Save the information of people, companies and the relationship between people and companies (ie. company.relationship). Use the functions viewed in class.

# In[181]:


from sqlalchemy import create_engine

engine = create_engine('sqlite:///billionaries.db', echo = True)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


# Extract necessary information:

# In[182]:


df.head()


# In[183]:


# Tabla de personas
df_people = df[['name','location.region','year','demographics.age']]

# Introduzco el año de nacimiento para disminuir la posibilidad de 
# eliminar omonimos que no son la misma persona
df_people['born'] = df['year'] - df['demographics.age']
df_people = df_people.drop(columns = ['year','demographics.age'])

# Ahora borro los duplicados
df_people.drop_duplicates(keep = 'first', inplace = True)

df_people = df_people.reset_index()
people_columns_name = ["people_number","person_name","region","born"] 
df_people.columns = people_columns_name

df_people['id_people'] = df_people.index
#df_people = df_people[0:10]
#df_people


# In[184]:


# Tabla de empresas
df_company = df[['company.founded','company.name','company.sector', 'company.type','company.relationship']]

df_company.drop_duplicates(keep = 'first', inplace = True)

df_company= df_company.reset_index()

company_columns_name = ["id_people","founded","company_name","sector","type","company_relationship"] 
df_company.columns = company_columns_name

df_company['id_company'] = df_company.index
#df_company = df_company[0:10]
#df_company


# In[185]:


# Construyo la tabla de relaciones entre personas y empresas 
# a través de un merge de las dos tablas anteriores

df_relationship = pd.merge(df_people, df_company, left_on='people_number', right_on='id_people')
#df_relationship


# In[186]:


# Ahora 'limpio' las tablas para que tengan solo las informaciones necesarias
people_columns = ['people_number','person_name', 'region', 'born']
df_people = df_people[people_columns]
df_people.columns = ['id_people','person_name', 'region', 'born']
#print(df_people)

company_columns = ['id_people','founded', 'company_name', 'sector', 'type', 'id_company']
df_company = df_company[company_columns]
#print(df_company)

relationship_columns = ['people_number','id_company','company_relationship']
df_relationship = df_relationship[relationship_columns]
df_relationship.columns = ['id_people','id_company','company_relationship']
#print(df_relationship)


# In[187]:


# Paso los data_frames a tablas de SQL
df_people.to_sql('people', con = engine, if_exists = 'replace', index = False)
df_company.to_sql('company', con = engine, if_exists = 'replace', index = False)
df_relationship.to_sql('relationship', con = engine, if_exists = 'replace', index = False)


# Reference I used to add primary key:
# 
# https://stackoverflow.com/questions/39407254/how-to-set-the-primary-key-when-writing-a-pandas-dataframe-to-a-sqlite-database?rq=1
# 
# The idea is to:
# 
# "create a new table with the same column names and types while
#     defining a primary key for the desired column"
# 

# In[203]:


import sqlite3

# Modifico las tablas para definir primary key, foreign keys, etc.
conn = sqlite3.connect('billionaries.db')
c = conn.cursor()
    
c.executescript('''
    
    
    /* Table people */
    BEGIN TRANSACTION;
    ALTER TABLE people RENAME TO old_table;

    CREATE TABLE people (id_people int not null primary key,
                        person_name char not null,
                        region char,
                        born char); 
    
    INSERT INTO people SELECT * FROM old_table;

    DROP TABLE old_table;
    COMMIT TRANSACTION;
    
    
    /* Table company */
    BEGIN TRANSACTION;
    ALTER TABLE company RENAME TO old_table;

    CREATE TABLE company (id_people,
                         founded, 
                         company_name, 
                         sector, 
                         type, 
                         id_company); 
    
    INSERT INTO people SELECT * FROM old_table;

    DROP TABLE old_table;
    COMMIT TRANSACTION;

''')
    
#close out the connection
c.close()
conn.close()


# In[189]:


# Miro el contenido de la tabla people
engine.execute("SELECT * FROM people").fetchall()


# In[12]:


metadata = MetaData()

# Tabla people
people = Table('people', metadata,
    Column('person_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('location.region', String, nullable=False),
)

# Tabla companies
companies = Table('companies', metadata,
    Column('company_id', Integer, primary_key=True),
    Column('company.name', String, nullable=False),
)

# Tabla companies
companies = Table('companies', metadata,
    Column('company_id', Integer, primary_key=True),
    Column('company.name', String, nullable=False),
)


# Save to the database:

# In[ ]:





# Test query
# 
# ```
# sqlite> 
# 
# select count(*) from people 
#     inner join positions on people."index" = positions.person_id 
#     inner join companies on positions.company_id=companies."index";
# 
# count(*)
# 2102
# ```

# In[ ]:




