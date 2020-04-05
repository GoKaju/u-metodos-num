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



import paho.mqtt.client as mqtt
import sqlite3

# Nombre de la base de datos
db_name='miguelito.db'

# enunciado SQL para crear tabla si no existe
sql='''
    CREATE TABLE IF NOT EXISTS "datos" (
        "numero"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "tiempo"	BLOB NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "radi"	REAL
    );
    '''    
# conectar a base de datos, ejecutar tarea y cerrar conexi\'on
db = sqlite3.connect(db_name)
cursor = db.cursor()
cursor.execute(sql)
db.commit()
db.close()

#datos del broker y t\'opico
MQTT_ADDRESS = 'mosquitto.poligran.edu.co'
MQTT_TOPIC = '[EMA]/[RADI]'
MQTT_PORT = 1883

#funci\'on que se ejecuta cuando hay conexi\'on
def on_connect(client, userdata, flags, rc):
    print ('Starting connection with '+MQTT_ADDRESS)
    print ('Starting subscription to '+MQTT_TOPIC)

#funci\'on que se ejecuta cuando llega mensaje
def on_message(client, userdata, msg):
    # ver mensaje que ha llegado
    print (str(msg.payload))
    # insertar en la base de datos
    sql='''INSERT INTO datos(radi) VALUES(?)'''
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    task=(float(msg.payload),)
    cursor.execute(sql,task)
    db.commit()
    cursor.close()
   
if __name__ == '__main__':
    #prepara la conexi\'on
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)
    #intentar la conexi\'on
    try:
        mqtt_client.loop_forever()
    except:
        print ("error general")
    mqtt_client.disconnect()

