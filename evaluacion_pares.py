import pandas as pd
import csv
import math

df = pd.read_csv('respuestas.csv')

df = df.drop(columns=['Marca temporal'])
df.columns = ['grupo', 'lista', 'lista1', 'nota1', 'lista2', 'nota2', 'lista3', 'nota3', 'lista4', 'nota4', 'lista5', 'nota5']

#Muestra del dataframe
# print(df.head())

#Eliminamos las respuestas duplicadas de formulario
alumnos_set = set()
alumnos_repetidos = []
errores = []


for index, row in df.iterrows():
    if row['lista'] in alumnos_set:
        alumnos_repetidos.append(index)
    alumnos_set.add(row['lista'])

df = df.drop(alumnos_repetidos, axis=0)


#Buscamos aquellos que asignaron más puntos de lo debido
for index, row in df.iterrows():
    total = 0
    max = 20
    if row['nota5'] < 1:
        max = 16
    total += row['nota1']
    total += row['nota2']
    total += row['nota3']
    total += row['nota4']
    total += row['nota5']
    if total > max:
        errores.append(row['lista'])
# print(errores)


#Buscamos aquellos que no respondieron la evaluación
todos = {i for i in range(1, 227)}
faltantes = todos - alumnos_set
#print(faltantes)



#Diccionario con key el número de lista del alumno, y value una lista con sus calificaciones.
alumnos = {i: [] for i in range(1, 227)}

for index, row in df.iterrows():
    alumnos[row['lista1']].append(row['nota1'])
    alumnos[row['lista2']].append(row['nota2'])
    alumnos[row['lista3']].append(row['nota3'])
    if row['lista4'] >= 1:
        alumnos[row['lista4']].append(row['nota4'])
    if row['lista5'] >= 1:
        alumnos[row['lista5']].append(row['nota5'])



for key in alumnos:
    if len(alumnos[key]) < 1:
        alumnos[key] = 0.0
    else:
        alumnos[key] = sum(alumnos[key]) / len(alumnos[key])

alumnos_items = alumnos.items()
alumnos_sorted= sorted(alumnos_items)

with open('resultados.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Numero de Lista", "Nota Evaluacion de Pares"])
    for key, value in alumnos_sorted:
        writer.writerow([key, round(value, 1)])