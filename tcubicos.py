#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Compendio de programas.
# Matemáticas para Ingeniería. Métodos numéricos con Python.
# Copyright (C) 2017  Los autores del texto.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# ---------------------------------------------------------------------

# Trazadores cúbicos naturales y algunos casos de salida.

from math import *


def CubicSplines(datos):
    n = len(datos)-1
    # Inicializar vectores auxiliares
    A = [float(x[1]) for x in datos]
    X = [float(x[0]) for x in datos]
    H = [0.0 for x in range(n)]
    B = [0.0 for x in range(n+1)]
    C = [0.0 for x in range(n+1)]
    D = [0.0 for x in range(n+1)]
    alpha = [0.0 for x in range(n)]
    mu = [0.0 for x in range(n+1)]
    l = [1.0 for x in range(n+1)]
    z = [0.0 for x in range(n+1)]

    # Crear vector $H$
    for i in range(n):
        H[i] = X[i+1]-X[i]

    # Crear vector $\alpha$
    for i in range(1, n):
        alpha[i] = (3.0/H[i])*(A[i+1]-A[i])-(3.0/H[i-1])*(A[i]-A[i-1])

    # Solucionar sistema tridiagonal
    for i in range(1, n):
        l[i] = 2.0*(X[i+1]-X[i-1])-H[i-1]*mu[i-1]
        mu[i] = float(H[i])/l[i]
        z[i] = (alpha[i]-H[i-1]*z[i-1])/float(l[i])

    # Solucionar sistema tridiagonal
    for j in range(n-1, -1, -1):
        C[j] = z[j]-mu[j]*C[j+1]
        B[j] = (A[j+1]-A[j])/float(H[j])-H[j]*(C[j+1]+2*C[j])/3.0
        D[j] = (C[j+1]-C[j])/(3.0*H[j])

    # Retornar vectores $A$, $B$, $C$, $D$
    return A[:-1], B[:-1], C[:-1], D[:-1]

# Datos de prueba $(1,2)$, $(2,3)$, $(3,5)$
datosPrueba = [(1, 2), (2, 3), (3, 5)]
a, b, c, d = CubicSplines(datosPrueba)
print ("\nVectores de coeficientes:")
print ("A =", a)
print ("B =", b)
print ("C =", c)
print ("D =", d)

# Datos de prueba $(0,1)$, $(1,e)$, $(2,e^2)$ y $(3,e^3)$
datosPrueba = [(0, exp(0)), (1, exp(1)),
               (2, exp(2)), (3, exp(3))]
a, b, c, d = CubicSplines(datosPrueba)
print ("\nVectores de coeficientes:")
print ("A =", a)
print ("B =", b)
print ("C =", c)
print ("D =", d)
