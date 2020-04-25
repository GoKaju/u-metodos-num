from math import *
import numpy as np
import sympy as sym

def CubicSplines(datos):
    n = len(datos)
    xi = [float(x[0]) for x in datos]
    yi = [float(x[1]) for x in datos]
    # Calcular h
    h = np.zeros(n-1, dtype = float)
    for j in range(0,n-1,1):
        h[j] = xi[j+1] - xi[j]
    
    # armar Sistema de ecuaciones
    A = np.zeros(shape=(n-2,n-2), dtype = float)
    B = np.zeros(n-2, dtype = float)
    S = np.zeros(n, dtype = float)
    A[0,0] = 2*(h[0]+h[1])
    A[0,1] = h[1]
    B[0] = 6*((yi[2]-yi[1])/h[1] - (yi[1]-yi[0])/h[0])
    for i in range(1,n-3,1):
        A[i,i-1] = h[i]
        A[i,i] = 2*(h[i]+h[i+1])
        A[i,i+1] = h[i+1]
        B[i] = 6*((yi[i+2]-yi[i+1])/h[i+1] - (yi[i+1]-yi[i])/h[i])
    A[n-3,n-4] = h[n-3]
    A[n-3,n-3] = 2*(h[n-3]+h[n-2])
    B[n-3] = 6*((yi[n-1]-yi[n-2])/h[n-2] - (yi[n-2]-yi[n-3])/h[n-3])
    
    # Resolver sistema 
    r = np.linalg.solve(A,B)
    # S
    for j in range(1,n-1,1):
        S[j] = r[j-1]
    S[0] = 0
    S[n-1] = 0
    
    #  sacar Coeficientes
    a = np.zeros(n-1, dtype = float)
    b = np.zeros(n-1, dtype = float)
    c = np.zeros(n-1, dtype = float)
    d = np.zeros(n-1, dtype = float)
    for j in range(0,n-1,1):
        a[j] = (S[j+1]-S[j])/(6*h[j])
        b[j] = S[j]/2
        c[j] = (yi[j+1]-yi[j])/h[j] - (2*h[j]*S[j]+h[j]*S[j+1])/6
        d[j] = yi[j]
    
    # armado de Polinomio trazador
    x = sym.Symbol('x')
    polinomio = []
    for j in range(0,n-1,1):
        ptramo = a[j]*(x-xi[j])**3 + b[j]*(x-xi[j])**2 + c[j]*(x-xi[j])+ d[j]
        ptramo = ptramo.expand()
        polinomio.append(ptramo)
        print(ptramo)
    
    return(polinomio)

def Integrar(datos,polinomios):
    n = len(datos)
    xi = [float(x[0]) for x in datos]
    acum = float(0.0)
    x = sym.Symbol('x') 
    print('Integrando Polinomios')
    for tramo in range(1,n,1):
        acum += sym.integrate(polinomios[tramo-1],(x,xi[tramo-1],xi[tramo]))
        print(xi[tramo])
    return acum

#Obtener datos desde Base de datos

import sqlite3

def Datosema():

    con = sqlite3.connect("Miguelito.db")
 
    cur = con.cursor()
 
    cur.execute("SELECT numero,radi from datos where  datetime(tiempo,'localtime') BETWEEN '2020-03-28 06:00:00' AND '2020-03-28 18:00:00';")
 
    rows = cur.fetchall()

    cur.close()

    con.close()


    return rows

Ema = Datosema()

# Datos de prueba
datos = (Ema)

#polinomios por tramos
polinomios = CubicSplines(datos)

#Integrar
acum  = Integrar(datos,polinomios)
print(acum)

