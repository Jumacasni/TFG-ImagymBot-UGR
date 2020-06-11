#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

# para el servidor
# db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")

# --- Start Configuration dependencies
import os
import json
import codecs
# --- End Configuration dependencies
import logging
import pymysql
import datetime
import dateutil
import time
import random
import string
import pytz
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import os.path
from os import path
from datetime import date, timedelta, datetime, timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters
from dateutil import tz

print(time.tzname)
os.environ["TZ"] = "Europe/Madrid"
time.tzset()
print(time.tzname)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# POSSIBLE STATES
WELCOME, WELCOME_PRESS_START, INICIO, INICIO_FICHA, INICIO_FICHA_ALTURA,\
INICIO_FICHA_NACIMIENTO, INICIO_FICHA_GENERO, INICIO_FICHA_EMAIL, INICIO_PESO,\
INICIO_PESO_ANOTAR, INICIO_PESO_ANOTAR_PESO, INICIO_PESO_ANOTAR_GRASA,\
INICIO_PESO_ANOTAR_MUSCULO, INICIO_PESO_ESTABLECER, INICIO_PESO_ESTABLECER_PESO, INICIO_PESO_ESTABLECER_PESO_TIEMPO,\
INICIO_PESO_ESTABLECER_GRASA, INICIO_PESO_ESTABLECER_GRASA_TIEMPO,\
INICIO_PESO_ESTABLECER_MUSCULO, INICIO_PESO_ESTABLECER_MUSCULO_TIEMPO,\
INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR, INICIO_PESO_ELIMINAR, INICIO_PESO_EVOLUCION,\
INICIO_PESO_EVOLUCION_PESO, INICIO_PESO_VALORACION, INICIO_PESO_EVOLUCION_GRASA, INICIO_PESO_EVOLUCION_MUSCULO,\
INICIO_PESO_EVOLUCION_IMC, INICIO_CARDIO, INICIO_CARDIO_REGISTRAR, INICIO_CARDIO_REGISTRAR_ACTIVIDAD,\
INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR, INICIO_CARDIO_VER, INICIO_CARDIO_ESTABLECER, INICIO_CARDIO_ESTABLECER_ACTIVIDAD,\
INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR, INICIO_CARDIO_ELIMINAR, INICIO_FICHA_PESO, INICIO_RETOS,\
INICIO_PESO_ANOTAR_PESO_ALTURA, INICIO_FICHA_PESO_ALTURA, INICIO_RETOS_VER, INICIO_RETOS_VER_RETO,\
INICIO_RETOS_ELIMINAR, INICIO_RETOS_ELIMINAR_CONFIRMAR, INICIO_RETOS_ANOTAR_CONFIRMAR, INICIO_RETOS_CALENDARIO,\
INICIO_RETOS_DESCALIFICAR, INICIO_RETOS_DESCALIFICAR_CONFIRMAR, INICIO_RETOS_HISTORIAL, INICIO_RETOS_HISTORIAL_CLASIFICACION,\
 = range(51)

db = pymysql.connect("localhost", "root", "password", "Imagym")

global current_state, conv_handler, updater

############# INICIO #############
def start(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	global current_state 

	name_user = update.message.from_user.first_name
	username_user = update.message.from_user.username

	cur = db.cursor()
	cur.execute("SELECT id_usuario FROM Usuarios where id_usuario='"+username_user+"';")
	resultado = cur.fetchall()
	cur.close()
	db.close()

	if not resultado:
		msg = update.message.reply_text(
			text="¡Bienvenido/a a Imagym! Introduce la contraseña de tu gimnasio para hablar conmigo.")

		# Le decimos al bot que estamos en el estado WELCOME
		current_state = 'WELCOME'
		return WELCOME

	else:
		msg = update.message.reply_text(
			text="¡Bienvenido/a de nuevo, "+name_user)
		keyboard = [
			[InlineKeyboardButton("Empezar Imagym ➡", callback_data='start_menu')]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text(
			text="Pulsa el botón para empezar",
			reply_markup=reply_markup
		)

		current_state = 'WELCOME_PRESS_START'
		return WELCOME_PRESS_START

def mandar_mensaje(update, context):
	global current_state 
	bot = context.bot

	n_params = context.args
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("SELECT chat_id FROM Usuarios;")
	resultado = cur.fetchall()

	if len(n_params) == 0:
		if username == 'Jumacasni':
			for i in range(len(resultado)):
				bot.send_message(
					chat_id=resultado[i][0],
					text="Hola, soy Juanma! Acabo de actualizar el bot.\n\n Si queréis usarlo de nuevo, usad /start\n\nMuchas gracias por ayudarme! :)"
				)

	else:
		user_msg = update.message.text
		if username == 'Jumacasni':
			for i in range(len(resultado)):
				bot.send_message(
					chat_id=resultado[i][0],
					text=user_msg.split(' ', 1)[1]
				)

	cur.close()
	db.close()

def any_message_start(update, context):
	update.message.reply_text(
		text="Usa /start para iniciar el bot",
	)

def any_message(update, context):
	global current_state
	
	if current_state == "WELCOME":	
		user_msg = update.message.text
		user_msg_split = user_msg.split()
		n_params = len(user_msg_split)

		if n_params == 1:
			# Comprobar si la clave coincide con algún gimnasio
			user_msg = user_msg_split[0]

			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()
			cur = db.cursor()
			cur.execute("SELECT id_gym,nombre FROM Gimnasios where BINARY clave_clientes='"+user_msg+"';")

			resultado = cur.fetchall();

			if not resultado:
				update.message.reply_text(
					text="No encuentro ningún gimnasio con esa clave. Prueba a poner otra clave."
				)
				cur.close()
				db.close()

			else:
				name_user = update.message.from_user.first_name
				last_name_user = update.message.from_user.last_name
				username_user = update.message.from_user.username
				password_user = randomPassword(10)
				chat_id_user = update.message.chat_id
				id_gym = resultado[0][0]
				name_gym = resultado[0][1]
				update.message.reply_text(
					text="¡Bienvenido a "+name_gym+", "+name_user+"! Tu contraseña para acceder a la web es:\n\n"+password_user+"\n\nPuedes cambiar tu contraseña desde la web."
				)
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("INSERT INTO Usuarios(id_usuario,nombre,apellidos,chat_id,clave_web,date_add,id_gym) VALUES (%s, %s, %s, %s, %s, %s, %s)",(username_user,name_user,last_name_user,chat_id_user,password_user,date_today,id_gym))
				db.commit()
				cur.close()
				db.close()

				update.message.reply_text(
					text="¡Aquí empieza tu experiencia en Imagym! 💪"
				)
				keyboard = [
					[InlineKeyboardButton("Empezar Imagym ➡", callback_data='start_menu')]
				]
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="Pulsa el botón para empezar",
					reply_markup=reply_markup
				)

				current_state = "WELCOME_PRESS_START"
				return WELCOME_PRESS_START

		else:
			update.message.reply_text(
				text="No te entiendo. Introduce la clave de tu gimnasio para hablar conmigo."
			)


	if current_state == "WELCOME_PRESS_START":
		keyboard = [
			[InlineKeyboardButton("Empezar Imagym ➡", callback_data='start_menu')]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text(
			text="Pulsa el botón para empezar",
			reply_markup=reply_markup
		)

	else:
		update.message.reply_text(
			text="No te he entendido. Si es necesario, puedes reiniciarme usando /start"
		)

def show_inicio(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando inicio..."
	)
	time.sleep(.8)
	keyboard = [
		[InlineKeyboardButton("Mi objetivo de peso ⚖", callback_data='inicio_peso')],
		[InlineKeyboardButton("Mi objetivo de actividades cardio 🏃", callback_data='inicio_cardio')],
		[InlineKeyboardButton("Retos 🏁", callback_data='inicio_retos')],
		[InlineKeyboardButton("Ejercicio del mes 🎯", callback_data='inicio_ejercicio')],
		[InlineKeyboardButton("Rutinas y entrenamiento 💪", callback_data='inicio_rutinas')],
		[InlineKeyboardButton("Mi ficha personal 🧑", callback_data='inicio_ficha')],
		[InlineKeyboardButton("Soporte ❓", callback_data='inicio_soporte')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio",
		reply_markup = reply_markup
	)

	current_state = "INICIO"
	return INICIO

############# MI FICHA PERSONAL #############
def show_inicio_ficha(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Mi ficha personal... "
	)

	# Obtener datos
	username_user = query.from_user.username

	cur = db.cursor()
	cur.execute("SELECT altura, fecha_nacimiento, genero, email FROM Usuarios where id_usuario='"+username_user+"';")
	resultado = cur.fetchall()

	altura = resultado[0][0]
	fecha_nacimiento = resultado[0][1]
	genero = resultado[0][2]
	email = resultado[0][3]

	if altura is None or not altura:
		altura = "✏"
	else:
		altura = str(altura) + " cm"

	if fecha_nacimiento is None or not fecha_nacimiento:
		fecha_nacimiento = "✏"
	else:
		fecha_nacimiento = fecha_nacimiento.strftime("%d-%b-%Y")

	if genero is None or not genero:
		genero = "✏"
	else:
		if genero == "m":
			genero = "👩"
		elif genero == "v":
			genero = "👨"
		elif genero == "o":
			genero = "otro"

	if email is None or not email:
		email = "✏"

	# Peso más reciente
	cur.execute("SELECT peso,fecha FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL)")
	resultado = cur.fetchall()

	if not resultado:
		peso = " ✏"
		fecha = ""
	else:
		if resultado[0][0] is None or not resultado[0][0]:
			peso = " ✏"
			fecha = ""
		else:
			peso = str(resultado[0][0]).rstrip('0').rstrip('. ')+"kg 👉 "
			fecha = resultado[0][1]
			if fecha == date.today():
				fecha = "Registrado hoy"
			else:
				fecha = "Registrado el día "+fecha.strftime("%d-%B-%Y")

	cur.close()
	db.close()

	time.sleep(.8)
	keyboard = [
		[InlineKeyboardButton("Peso: "+peso+fecha, callback_data='inicio_ficha_peso')],
		[InlineKeyboardButton("Altura: "+altura, callback_data='inicio_ficha_altura')],
		[InlineKeyboardButton("Fecha nacimiento: "+fecha_nacimiento, callback_data='inicio_ficha_nacimiento')],
		[InlineKeyboardButton("Género: "+genero, callback_data='inicio_ficha_genero')],
		[InlineKeyboardButton("Correo electrónico: "+email, callback_data='inicio_ficha_email')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Pulsa un botón para cambiar la información"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Mi ficha personal",
		reply_markup = reply_markup
	)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def modify_altura(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT altura FROM Usuarios WHERE id_usuario='"+username_user+"';")
	hay_altura = cur.fetchall()

	cur.close()
	db.close()

	if hay_altura[0][0] is None:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_ficha')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar la altura 🔙", callback_data='back_inicio_ficha')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuánto mides (en cm)?"
	)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Por ejemplo, 170.",
		reply_markup=reply_markup
	)

	current_state = "INICIO_FICHA_ALTURA"
	return INICIO_FICHA_ALTURA

def check_altura(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT altura FROM Usuarios WHERE id_usuario='"+username+"';")
	hay_altura = cur.fetchall()

	if hay_altura is None:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_ficha')]
		]
		if current_state == "INICIO_PESO_ANOTAR_PESO_ALTURA":
			keyboard = [
				[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_peso_anotar')]
			]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar la altura 🔙", callback_data='back_inicio_ficha')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	cur.close()
	db.close()

	if is_int(user_msg):

		numero = int(user_msg)
		if numero < 0:
			update.message.reply_text(
				text="No puedes usar números negativos para registrar tu altura. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			if numero > 220:
				update.message.reply_text(
					text="No puedes usar un número más grande de 220. Prueba de nuevo.",
					reply_markup=reply_markup
				)
			else:
				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()

				cur = db.cursor()
				cur.execute("UPDATE Usuarios SET altura="+str(numero)+" WHERE id_usuario='"+username+"'")
				db.commit()

				update.message.reply_text(
					text="Has cambiado tu altura con éxito ✔"
				)

				# Peso más reciente
				cur.execute("SELECT peso,id_peso FROM Peso WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username+"' AND peso IS NOT NULL)")
				resultado = cur.fetchall()
				peso = float(resultado[0][0])
				id_peso = resultado[0][1]
				altura = numero
				altura_m2 = pow(altura/100,2)
				imc = peso/altura_m2
				imc = round(imc,2)

				cur.execute("UPDATE Peso SET imc="+str(imc)+" WHERE id_peso="+str(id_peso)+";")
				db.commit()

				if current_state == "INICIO_PESO_ANOTAR_PESO_ALTURA":
					update.message.reply_text(
						text="¡Genial! Puedes comprobar tu IMC desde <b>👣 Inicio > Mi objetivo de peso</b>",
						parse_mode='HTML'
					)

					inicio_peso_anotar(update, context)

					current_state = "INICIO_PESO_ANOTAR"
					return INICIO_PESO_ANOTAR

				elif current_state == "INICIO_FICHA_PESO_ALTURA":
					update.message.reply_text(
						text="¡Genial! Puedes comprobar tu IMC desde <b>👣 Inicio > Mi objetivo de peso</b>",
						parse_mode='HTML'
					)

				cur.close()
				db.close()

				inicio_ficha(update, context)

				current_state = "INICIO_FICHA"
				return INICIO_FICHA

	else:
		update.message.reply_text(
			text="No te entiendo. Escríbeme tu altura en cm.",
			reply_markup=reply_markup
		)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Escríbeme solo un número. Por ejemplo, 170.",
			reply_markup=reply_markup
		)

def modify_nacimiento(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT fecha_nacimiento FROM Usuarios WHERE id_usuario='"+username_user+"';")
	hay_nacimiento = cur.fetchall()

	cur.close()
	db.close()
	if hay_nacimiento[0][0] is None:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar mi fecha de nacimiento 🔙", callback_data='back_inicio_ficha')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar mi fecha de nacimiento 🔙", callback_data='back_inicio_ficha')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu fecha de nacimiento? Utiliza el formato dd-mm-yyyy",
		reply_markup=reply_markup
	)

	current_state = "INICIO_FICHA_NACIMIENTO"
	return INICIO_FICHA_NACIMIENTO

def check_nacimiento(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT fecha_nacimiento FROM Usuarios WHERE id_usuario='"+username+"';")
	hay_nacimiento = cur.fetchall()

	cur.close()
	db.close()

	if hay_nacimiento is None:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar mi fecha de nacimiento 🔙", callback_data='back_inicio_ficha')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar mi fecha de nacimiento 🔙", callback_data='back_inicio_ficha')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	if is_valid_date(user_msg):
		fecha_len = len(user_msg)

		if fecha_len != 10:
			update.message.reply_text(
				text="Utiliza el formato dd-mm-yyyy.",
				reply_markup=reply_markup
			)

		else:
			birthday_date = datetime.strptime(user_msg, '%d-%m-%Y')
			birthday_sql_format = user_msg[6:10] +'-'+ user_msg[3:5] +'-'+ user_msg[0:2] # Formato YYYY-mm-dd

			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			cur = db.cursor()
			cur.execute("UPDATE Usuarios SET fecha_nacimiento='"+birthday_sql_format+"' WHERE id_usuario='"+username+"'")
			db.commit()

			cur.close()
			db.close()

			update.message.reply_text(
				text="Has cambiado tu fecha de nacimiento con éxito ✔"
			)

			inicio_ficha(update, context)

			current_state = "INICIO_FICHA"
			return INICIO_FICHA

	else:
		update.message.reply_text(
			text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy. Por ejemplo, 01-01-1990",
			reply_markup=reply_markup
		)

def modify_genero(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT genero FROM Usuarios WHERE id_usuario='"+username_user+"';")
	hay_genero = cur.fetchall()

	cur.close()
	db.close()

	keyboard = []


	keyboard.append([InlineKeyboardButton("Hombre 👨", callback_data='select_genero_hombre')])
	keyboard.append([InlineKeyboardButton("Mujer 👩", callback_data='select_genero_mujer')])
	keyboard.append([InlineKeyboardButton("Otro", callback_data='select_genero_otro')])
	keyboard.append([InlineKeyboardButton("Sin especificar", callback_data='select_genero_sin')])

	if hay_genero[0][0] is None:
		keyboard.append([InlineKeyboardButton("No quiero anotar mi género 🔙", callback_data='back_inicio_ficha')])
	else:
		keyboard.append([InlineKeyboardButton("No quiero modificar mi género 🔙", callback_data='back_inicio_ficha')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Elige tu género:",
		reply_markup=reply_markup
	)

	current_state = "INICIO_FICHA_GENERO"
	return INICIO_FICHA_GENERO

def check_genero_hombre(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("UPDATE Usuarios SET genero='v' WHERE id_usuario='"+username+"'")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has cambiado tu género con éxito ✔"
	)

	show_inicio_ficha(update, context)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def check_genero_mujer(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("UPDATE Usuarios SET genero='m' WHERE id_usuario='"+username+"'")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has cambiado tu género con éxito ✔"
	)

	show_inicio_ficha(update, context)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def check_genero_otro(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("UPDATE Usuarios SET genero='o' WHERE id_usuario='"+username+"'")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has cambiado tu género con éxito ✔"
	)

	show_inicio_ficha(update, context)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def check_genero_sin(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("UPDATE Usuarios SET genero=NULL WHERE id_usuario='"+username+"'")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has cambiado tu género con éxito ✔"
	)

	show_inicio_ficha(update, context)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def modify_email(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT email FROM Usuarios WHERE id_usuario='"+username_user+"';")
	hay_email = cur.fetchall()

	cur.close()
	db.close()

	if hay_email[0][0] is None:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar mi email 🔙", callback_data='back_inicio_ficha')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar mi email 🔙", callback_data='back_inicio_ficha')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Dime tu correo electrónico",
		reply_markup=reply_markup
	)

	current_state = "INICIO_FICHA_EMAIL"
	return INICIO_FICHA_EMAIL

def check_email(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("UPDATE Usuarios SET email='"+user_msg+"' WHERE id_usuario='"+username+"'")
	db.commit()

	update.message.reply_text(
		text="Has cambiado tu correo electrónico con éxito ✔"
	)

	cur.close()
	db.close()

	inicio_ficha(update, context)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

############# MI OBJETIVO DE PESO #############
def show_inicio_peso(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username
	cur = db.cursor()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Mi objetivo de peso... "
	)
	time.sleep(.8)

	# Peso más reciente
	cur.execute("SELECT peso,grasa,musculo,fecha,hora,imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
	resultado = cur.fetchall()


	if not resultado:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="📌 Aún no tienes registrado ningún dato.\n\nPodrás establecer un objetivo de peso/grasa/músculo cuando anotes algún dato por primera vez."
		)
		time.sleep(1.5)
		show_inicio_peso_anotar(update, context)

		current_state = "INICIO_PESO_ANOTAR"
		return INICIO_PESO_ANOTAR

	else:	
		peso = resultado[0][0]
		grasa = resultado[0][1]
		musculo = resultado[0][2]
		imc = resultado[0][5]
		fecha = resultado[0][3]

		if fecha == date.today():
			fecha = "hoy"
		else:
			fecha = fecha.strftime("%d-%b-%Y")

		text="📌 Última vez que anotaste datos: "+fecha
		if peso is not None:
			text=text+"\n\nPeso: "+str(peso).rstrip('0').rstrip('. ')+"kg"
		else:
			text=text+"\n\nPeso: sin datos"

		if grasa is not None:
			text=text+"\nGrasa: "+str(grasa).rstrip('0').rstrip('. ')+"%"
		else:
			text=text+"\nGrasa: sin datos"

		if musculo is not None:
			text=text+"\nMúsculo: "+str(musculo).rstrip('0').rstrip('. ')+"%"
		else:
			text=text+"\nMúsculo: sin datos"

		if imc is not None:
			text=text+"\nIMC: "+str(imc).rstrip('0').rstrip('. ')

		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text
		)

		cur.execute("SELECT tipo,objetivo,fecha_fin,fecha_inicio FROM Objetivo_peso WHERE id_usuario='"+username_user+"' AND fecha_fin>CURDATE();")
		resultado = cur.fetchall()

		keyboard = [
			[InlineKeyboardButton("Anotar datos 📝", callback_data='inicio_peso_anotar')]
		]

		if not resultado:
			keyboard.append([InlineKeyboardButton("Establecer objetivo 🏁", callback_data='inicio_peso_establecer')])
			keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])
			time.sleep(.8)
			bot.send_message(
				chat_id = query.message.chat_id,
				text="📌 Actualmente no tienes ningún objetivo establecido."
			)
		else:
			tipo = resultado[0][0]
			peso_objetivo = resultado[0][1]
			fecha_fin = resultado[0][2]
			fecha_inicio = resultado[0][3]

			if tipo == "peso":
				medida = "kg"
			else:
				medida = "%"

			cur.execute("SELECT "+tipo+" FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND "+tipo+" IS NOT NULL);")
			resultado = cur.fetchall()
			peso = resultado[0][0]
			diferencia_peso = peso_objetivo - peso


			fecha_fin = fecha_fin.strftime("%d-%b-%Y")
			if fecha_inicio == date.today():
				fecha_inicio = "hoy"
			else:
				fecha_inicio = fecha_inicio.strftime("%d-%b-%Y")

			text="📌 Actualmente tienes un <b>objetivo de "+tipo+"</b>.\n\nÚltimo registro de "+tipo+": "+str(peso).rstrip('0').rstrip('. ')+medida+"\nTu objetivo: "+str(peso_objetivo).rstrip('0').rstrip('. ')+medida
			text=text+"\nTe queda: "+str(diferencia_peso).rstrip('0').rstrip('. ')+medida
			text=text+"\nFecha inicio: "+fecha_inicio+"\nFecha fin: "+fecha_fin

			keyboard.append([InlineKeyboardButton("Eliminar objetivo 🏁", callback_data='inicio_peso_eliminar')])
			keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])

			time.sleep(.8)
			bot.send_message(
				chat_id = query.message.chat_id,
				text=text,
				parse_mode='HTML'
			)

		cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL")
		resultado = cur.fetchall()

		if resultado:
			keyboard.append([InlineKeyboardButton("Valoración del IMC 🗨", callback_data='inicio_peso_valoracion')])
			keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
		else:
			keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

		cur.close()
		db.close()

		time.sleep(.8)
		reply_markup = InlineKeyboardMarkup(keyboard)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="👣 Inicio > Mi objetivo de peso",
			reply_markup = reply_markup
		)

		current_state = "INICIO_PESO"
		return INICIO_PESO

def show_inicio_peso_anotar(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Mi objetivo de peso > Anotar datos... "
	)

	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso,grasa,musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
	resultado = cur.fetchall()

	time.sleep(.8)

	if not resultado:
		text="No has registrado ningún dato aún."
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text
		)
		keyboard = [
			[InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')],
			[InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')],
			[InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
		]
	else:
		# Comprobar si ya hay datos registrados de hoy
		cur.execute("SELECT peso,grasa,musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=CURDATE();")
		resultado = cur.fetchall()

		# Si no hay nada registrado hoy
		if not resultado:
			text="Hoy no has registrado nada aún."
			bot.send_message(
				chat_id = query.message.chat_id,
				text=text
			)
			keyboard = [
				[InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')],
				[InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')],
				[InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')],
				[InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')],
				[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
			]
		# Si ya hay algo registrado hoy
		else:
			keyboard = []
			text="Hoy ya has registrado lo siguiente:\n"

			if resultado[0][0] is not None:
				peso = resultado[0][0]
				text=text+"\nPeso: "+str(peso).rstrip('0').rstrip('. ')+"kg"
				keyboard.append([InlineKeyboardButton("Modificar peso", callback_data='inicio_peso_anotar_peso')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')])


			if resultado[0][1] is not None:
				grasa = resultado[0][1]
				text=text+"\nGrasa: "+str(grasa).rstrip('0').rstrip('. ')+"%"
				keyboard.append([InlineKeyboardButton("Modificar grasa", callback_data='inicio_peso_anotar_grasa')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')])

			if resultado[0][2] is not None:
				musculo = resultado[0][2]
				text=text+"\nMúsculo: "+str(musculo).rstrip('0').rstrip('. ')+"%"
				keyboard.append([InlineKeyboardButton("Modificar músculo", callback_data='inicio_peso_anotar_musculo')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')])

			keyboard.append([InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')])
			keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

			bot.send_message(
				chat_id = query.message.chat_id,
				text=text
			)

	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Qué quieres anotar?"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Mi objetivo de peso > Anotar datos",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR"
	return INICIO_PESO_ANOTAR

def anotar_peso(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	username_user = query.from_user.username

	cur = db.cursor()

	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=CURDATE() AND peso IS NOT NULL;")
	hay_peso = cur.fetchall()

	if current_state == "INICIO_PESO_ANOTAR":
		if not hay_peso:
			keyboard = [
				[InlineKeyboardButton("No quiero anotar el peso 🔙", callback_data='back_inicio_peso_anotar')]
			]
		else:
			keyboard = [
				[InlineKeyboardButton("No quiero modificar el peso 🔙", callback_data='back_inicio_peso_anotar')]
			]

	elif current_state == "INICIO_FICHA":
		if not hay_peso:
			keyboard = [
				[InlineKeyboardButton("No quiero anotar el peso 🔙", callback_data='back_inicio_ficha')]
			]
		else:
			keyboard = [
				[InlineKeyboardButton("No quiero modificar el peso 🔙", callback_data='back_inicio_ficha')]
			]

	reply_markup = InlineKeyboardMarkup(keyboard)

	if not hay_peso:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="¿Cuál es tu peso de hoy (en kg)?"
		)
	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Vas a modificar tu peso de hoy: "+str(hay_peso[0][0]).rstrip('0').rstrip('. ')+"kg\n\n¿Cuál es tu peso de hoy (en kg)?"
		)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 75.5",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	if current_state == "INICIO_PESO_ANOTAR":
		current_state = "INICIO_PESO_ANOTAR_PESO"
		return INICIO_PESO_ANOTAR_PESO

	elif current_state == "INICIO_FICHA":
		current_state = "INICIO_FICHA_PESO"
		return INICIO_FICHA_PESO

def check_anotar_peso(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE() AND peso IS NOT NULL;")
	hay_peso = cur.fetchall()

	if current_state == "INICIO_PESO_ANOTAR_PESO":
		if not hay_peso:
			keyboard = [
				[InlineKeyboardButton("No quiero anotar el peso 🔙", callback_data='back_inicio_peso_anotar')]
			]
		else:
			keyboard = [
				[InlineKeyboardButton("No quiero modificar el peso 🔙", callback_data='back_inicio_peso_anotar')]
			]

	elif current_state == "INICIO_FICHA_PESO":
		if not hay_peso:
			keyboard = [
				[InlineKeyboardButton("No quiero anotar el peso 🔙", callback_data='back_inicio_ficha')]
			]
		else:
			keyboard = [
				[InlineKeyboardButton("No quiero modificar el peso 🔙", callback_data='back_inicio_ficha')]
			]

	reply_markup = InlineKeyboardMarkup(keyboard)

	cur.close()
	db.close()

	if is_float(user_msg):

		peso = float(user_msg)
		if peso < 0:
			update.message.reply_text(
				text="No puedes usar números negativos.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			cur = db.cursor()
			cur.execute("SELECT * FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE();")
			resultado = cur.fetchall()

			# Si no ha registrado un peso hoy
			if not resultado:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				# Cálculo del IMC
				cur = db.cursor()
				cur.execute("SELECT altura FROM Usuarios where id_usuario='"+username+"';")
				resultado = cur.fetchall()

				if not resultado or resultado[0][0] is None:
					cur.execute("INSERT INTO Peso(peso,fecha,hora,id_usuario) VALUES (%s, %s, %s, %s)",(peso,date_today,current_time,username))
					db.commit()

					update.message.reply_text(
						text="Has registrado tu peso de hoy con éxito ✔"
					)
					update.message.reply_text(
						text="¡Es momento de registrar tu altura! Con tu altura podré calcular tu IMC y podré valorarlo desde el menú 👣 <b>Inicio > Mi objetivo de peso</b>",
						parse_mode='HTML'
					)
					update.message.reply_text(
						text="¿Cuánto mides (en cm)?"
					)

					if current_state == "INICIO_PESO_ANOTAR_PESO":
						keyboard = [
							[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_peso_anotar')]
						]
					elif current_state == "INICIO_FICHA_PESO":
						keyboard = [
							[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_ficha')]
						]

					reply_markup = InlineKeyboardMarkup(keyboard)

					update.message.reply_text(
						text="Escríbeme solo un número. Por ejemplo, 170.",
						reply_markup=reply_markup
					)

					if current_state == "INICIO_PESO_ANOTAR_PESO":
						current_state = "INICIO_PESO_ANOTAR_PESO_ALTURA"
						return INICIO_PESO_ANOTAR_PESO_ALTURA

					elif current_state == "INICIO_FICHA_PESO":
						current_state = "INICIO_FICHA_PESO_ALTURA"
						return INICIO_FICHA_PESO_ALTURA

				else:
					altura = resultado[0][0]
					altura_m2 = pow(altura/100,2)
					imc = peso/altura_m2
					imc = round(imc,2)

					cur.execute("INSERT INTO Peso(peso,imc,fecha,hora,id_usuario) VALUES (%s, %s, %s, %s, %s)",(peso,imc,date_today,current_time,username))
					db.commit()
					update.message.reply_text(
						text="Has registrado tu peso de hoy con éxito ✔"
					)

			else:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				# Cálculo del IMC
				cur = db.cursor()
				cur.execute("SELECT altura FROM Usuarios where id_usuario='"+username+"';")
				resultado = cur.fetchall()

				if not resultado or resultado[0][0] is None:
					cur.execute("UPDATE Peso SET peso="+user_msg+",hora='"+str(current_time)+"' WHERE id_usuario='"+username+"' and fecha=CURDATE();")
					db.commit()
					update.message.reply_text(
						text="He modificado tu peso de hoy correctamente ✔"
					)
					update.message.reply_text(
						text="¿Quieres registrar tu altura? Con tu altura podré calcular tu IMC y podré valorarlo desde el menú 👣 <b>Inicio > Mi objetivo de peso</b>",
						parse_mode='HTML'
					)
					update.message.reply_text(
						text="¿Cuánto mides (en cm)?"
					)

					if current_state == "INICIO_PESO_ANOTAR_PESO":
						keyboard = [
							[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_peso_anotar')]
						]
					elif current_state == "INICIO_FICHA_PESO":
						keyboard = [
							[InlineKeyboardButton("No quiero anotar la altura 🔙", callback_data='back_inicio_ficha')]
						]

					reply_markup = InlineKeyboardMarkup(keyboard)

					update.message.reply_text(
						text="Escríbeme solo un número. Por ejemplo, 170.",
						reply_markup=reply_markup
					)

					if current_state == "INICIO_PESO_ANOTAR_PESO":
						current_state = "INICIO_PESO_ANOTAR_PESO_ALTURA"
						return INICIO_PESO_ANOTAR_PESO_ALTURA

					elif current_state == "INICIO_FICHA_PESO":
						current_state = "INICIO_FICHA_PESO_ALTURA"
						return INICIO_FICHA_PESO_ALTURA

				else:
					altura = resultado[0][0]
					altura_m2 = pow(altura/100,2)
					imc = peso/altura_m2
					imc = round(imc,2)

					cur.execute("UPDATE Peso SET peso="+user_msg+",imc="+str(imc)+",hora='"+str(current_time)+"' WHERE id_usuario='"+username+"' and fecha=CURDATE();")
					db.commit()
					update.message.reply_text(
						text="He modificado tu peso de hoy correctamente ✔"
					)
			# Si tiene un objetivo de peso
			cur.execute("SELECT id_objetivo_peso,diferencia,fecha_inicio,fecha_fin,objetivo FROM Objetivo_peso WHERE id_usuario='"+username+"' AND tipo='peso' AND fecha_fin>CURDATE();")
			resultado = cur.fetchall()

			if resultado:
				id_objetivo_peso = resultado[0][0]
				diferencia = resultado[0][1]
				fecha_inicio = resultado[0][2]
				fecha_inicio = fecha_inicio.strftime("%Y-%m-%d")
				fecha_fin = resultado[0][3]
				fecha_fin = fecha_fin.strftime("%Y-%m-%d")
				objetivo = resultado[0][4]

				cur.execute("SELECT COUNT(*) FROM Peso WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"';")
				resultado = cur.fetchall()

				# Si hay más de un peso entre las fechas, calcular el último peso y hacer la diferencia
				if resultado[0][0] > 1:
					cur.execute("SELECT peso,fecha FROM Peso WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"' AND fecha!=CURDATE());")
					resultado = cur.fetchall()
					peso_ultimo = float(resultado[0][0])
					fecha = resultado[0][1]
					fecha = fecha.strftime("%d-%B-%Y")
					diferencia_peso = peso - peso_ultimo
					diferencia_peso = round(diferencia_peso, 3)

					if diferencia > 0:
						if peso >= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()

							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR

					if diferencia < 0:
						if peso <= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()

							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR


					time.sleep(.8)
					# Si el objetivo era ganar peso
					if diferencia > 0:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Pesas lo mismo que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso > 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nPesas <b>"+str(diferencia_peso).rstrip('0').rstrip('. ')+"kg más</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2)).rstrip('0').rstrip('. ')+" kg el día "+fecha,
								parse_mode = 'HTML'
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nPesas <b>"+str(diferencia_peso).rstrip('0').rstrip('. ')+"kg menos</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2)).rstrip('0').rstrip('. ')+" kg el día "+fecha,
								parse_mode = 'HTML'
							)
					else:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Pesas lo mismo que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso < 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nPesas <b>"+str(diferencia_peso).rstrip('0').rstrip('. ')+"kg menos</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2)).rstrip('0').rstrip('. ')+" kg el día "+fecha,
								parse_mode = 'HTML'
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nPesas <b>"+str(diferencia_peso).rstrip('0').rstrip('. ')+"kg más</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2)).rstrip('0').rstrip('. ')+" kg el día "+fecha,
								parse_mode = 'HTML'
							)

			cur.close()
			db.close()

			if current_state == "INICIO_PESO_ANOTAR_PESO":
				inicio_peso_anotar(update, context)
				current_state = "INICIO_PESO_ANOTAR"
				return INICIO_PESO_ANOTAR

			elif current_state == "INICIO_FICHA_PESO":
				inicio_ficha(update, context)
				current_state = "INICIO_FICHA"
				return INICIO_FICHA


	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Escríbeme tu peso de hoy (en kg)"
		)
		time.sleep(.8)
		update.message.reply_text(
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 75.5",
			reply_markup=reply_markup
		)

def anotar_grasa(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	query = update.callback_query
	bot = context.bot

	username_user = query.from_user.username
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=CURDATE() AND grasa IS NOT NULL;")
	hay_peso = cur.fetchall()

	cur.close()
	db.close()
	if not hay_peso:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar la grasa 🔙", callback_data='back_inicio_peso_anotar')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar la grasa 🔙", callback_data='back_inicio_peso_anotar')]
		]

	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu porcentaje de grasa de hoy?"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR_GRASA"
	return INICIO_PESO_ANOTAR_GRASA

def check_anotar_grasa(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE() AND grasa IS NOT NULL;")
	hay_peso = cur.fetchall()

	if not hay_peso:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar la grasa 🔙", callback_data='back_inicio_peso_anotar')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar la grasa 🔙", callback_data='back_inicio_peso_anotar')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)

	cur.close()
	db.close()

	if is_float(user_msg):

		grasa = float(user_msg)
		if grasa < 0:
			update.message.reply_text(
				text="No puedes usar números negativos. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			cur = db.cursor()
			cur.execute("SELECT * FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE();")
			resultado = cur.fetchall()

			if not resultado:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				cur.execute("INSERT INTO Peso(grasa,fecha,hora,id_usuario) VALUES (%s, %s, %s, %s)",(grasa,date_today,current_time,username))
				db.commit()
				time.sleep(.8)
				update.message.reply_text(
					text="Has registrado tu porcentaje de grasa de hoy con éxito ✔"
				)

			else:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				cur.execute("UPDATE Peso SET grasa="+user_msg+",hora='"+str(current_time)+"' WHERE id_usuario='"+username+"' and fecha=CURDATE();")
				db.commit()
				time.sleep(.8)
				update.message.reply_text(
					text="He modificado tu porcentaje de grasa de hoy correctamente ✔"
				)

			# Si tiene un objetivo de grasa
			cur.execute("SELECT id_objetivo_peso,diferencia,fecha_inicio,fecha_fin,objetivo FROM Objetivo_peso WHERE id_usuario='"+username+"' AND tipo='grasa' AND fecha_fin>CURDATE();")
			resultado = cur.fetchall()

			if resultado:
				id_objetivo_peso = resultado[0][0]
				diferencia = resultado[0][1]
				fecha_inicio = resultado[0][2]
				fecha_inicio = fecha_inicio.strftime("%Y-%m-%d")
				fecha_fin = resultado[0][3]
				fecha_fin = fecha_fin.strftime("%Y-%m-%d")
				objetivo = resultado[0][4]

				cur.execute("SELECT COUNT(*) FROM Peso WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"';")
				resultado = cur.fetchall()

				# Si hay más de una grasa entre las fechas, calcular la última grasa y hacer la diferencia
				if resultado[0][0] > 1:
					cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"' AND fecha!=CURDATE());")
					resultado = cur.fetchall()
					peso_ultimo = float(resultado[0][0])
					diferencia_peso = peso - peso_ultimo
					diferencia_peso = round(diferencia_peso, 3)

					if diferencia > 0:
						if peso >= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()

							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR

					if diferencia < 0:
						if peso <= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()
							
							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR


					time.sleep(.8)
					# Si el objetivo era ganar grasa
					if diferencia > 0:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Tienes el mismo porcentaje de grasa que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso > 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% menos que la última vez"
							)
					else:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Tienes el mismo porcentaje de grasa que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso < 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% menos que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que la última vez"
							)

			cur.close()
			db.close()

			inicio_peso_anotar(update, context)

			current_state = "INICIO_PESO_ANOTAR"
			return INICIO_PESO_ANOTAR

	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Dime tu porcentaje de grasa de hoy."
		)
		time.sleep(.8)
		update.message.reply_text(
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
			reply_markup=reply_markup
		)

def anotar_musculo(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	query = update.callback_query
	bot = context.bot

	username_user = query.from_user.username
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=CURDATE() AND musculo IS NOT NULL;")
	hay_peso = cur.fetchall()

	cur.close()
	db.close()
	if not hay_peso:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar el músculo 🔙", callback_data='back_inicio_peso_anotar')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar el músculo 🔙", callback_data='back_inicio_peso_anotar')]
		]

	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu porcentaje de músculo de hoy?"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR_MUSCULO"
	return INICIO_PESO_ANOTAR_MUSCULO

def check_anotar_musculo(update, context):
	global current_state 

	user_msg = update.message.text
	username = update.message.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si ya hay datos registrados de hoy
	cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE() AND musculo IS NOT NULL;")
	hay_peso = cur.fetchall()

	if not hay_peso:
		keyboard = [
			[InlineKeyboardButton("No quiero anotar el músculo 🔙", callback_data='back_inicio_peso_anotar')]
		]
	else:
		keyboard = [
			[InlineKeyboardButton("No quiero modificar el músculo 🔙", callback_data='back_inicio_peso_anotar')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)

	cur.close()
	db.close()

	if is_float(user_msg):

		musculo = float(user_msg)
		if musculo < 0:
			update.message.reply_text(
				text="No puedes usar números negativos. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			cur = db.cursor()
			cur.execute("SELECT * FROM Peso WHERE id_usuario='"+username+"' AND fecha=CURDATE();")
			resultado = cur.fetchall()

			if not resultado:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				cur.execute("INSERT INTO Peso(musculo,fecha,hora,id_usuario) VALUES (%s, %s, %s, %s)",(musculo,date_today,current_time,username))
				db.commit()
				time.sleep(.8)
				update.message.reply_text(
					text="Has registrado tu porcentaje de musculo de hoy con éxito ✔"
				)

			else:
				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("SELECT CURTIME();")
				resultado = cur.fetchall()
				current_time = resultado[0][0]

				cur.execute("UPDATE Peso SET musculo="+user_msg+",hora='"+str(current_time)+"' WHERE id_usuario='"+username+"';")
				db.commit()
				time.sleep(.8)
				update.message.reply_text(
					text="He modificado tu porcentaje de músculo de hoy correctamente ✔"
				)

			# Si tiene un objetivo de musculo
			cur.execute("SELECT id_objetivo_peso,diferencia,fecha_inicio,fecha_fin,objetivo FROM Objetivo_peso WHERE id_usuario='"+username+"' AND tipo='musculo' AND fecha_fin>CURDATE();")
			resultado = cur.fetchall()

			if resultado:
				id_objetivo_peso = resultado[0][0]
				diferencia = resultado[0][1]
				fecha_inicio = resultado[0][2]
				fecha_inicio = fecha_inicio.strftime("%Y-%m-%d")
				fecha_fin = resultado[0][3]
				fecha_fin = fecha_fin.strftime("%Y-%m-%d")
				objetivo = resultado[0][4]

				cur.execute("SELECT COUNT(*) FROM Peso WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"';")
				resultado = cur.fetchall()

				# Si hay más de un musculo entre las fechas, calcular la última grasa y hacer la diferencia
				if resultado[0][0] > 1:
					cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username+"' AND fecha>='"+fecha_inicio+"' AND fecha<='"+fecha_fin+"' AND fecha!=CURDATE());")
					resultado = cur.fetchall()
					peso_ultimo = float(resultado[0][0])
					diferencia_peso = peso - peso_ultimo
					diferencia_peso = round(diferencia_peso, 3)

					if diferencia > 0:
						if peso >= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()

							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR

					if diferencia < 0:
						if peso <= objetivo:
							time.sleep(.8)
							update.message.reply_text(
								text="¡HAS ALCANZADO TU OBJETIVO!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="🥳🥳🥳🥳🥳🥳🥳🥳🥳"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="¡ENHORABUENA!"
							)
							time.sleep(.8)
							update.message.reply_text(
								text="Aquí has acabado tu objetivo, pero puedes seguir proponiéndote más 🥳"
							)
							cur.execute("DELETE FROM Objetivo_peso WHERE id_objetivo_peso="+str(id_objetivo_peso)+";")
							resultado = cur.fetchall()
							db.commit()
							
							cur.close()
							db.close()

							inicio_peso_anotar(update, context)

							current_state = "INICIO_PESO_ANOTAR"
							return INICIO_PESO_ANOTAR


					time.sleep(.8)
					# Si el objetivo era ganar grasa
					if diferencia > 0:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Tienes el mismo porcentaje de musculo que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso > 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% menos que la última vez"
							)
					else:
						if diferencia_peso == 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Tienes el mismo porcentaje de musculo que la última vez, con lo cual tu objetivo sigue igual. ¡Ánimo!"
							)
						elif diferencia_peso < 0:
							time.sleep(.8)
							update.message.reply_text(
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% menos que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que la última vez"
							)

			cur.close()
			db.close()

			inicio_peso_anotar(update, context)

			current_state = "INICIO_PESO_ANOTAR"
			return INICIO_PESO_ANOTAR

	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Dime tu porcentaje de músculo de hoy."
		)
		time.sleep(.8)
		update.message.reply_text(
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
			reply_markup=reply_markup
		)

def show_inicio_peso_establecer(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Mi objetivo de peso > Establecer objetivo..."
	)

	username_user = query.from_user.username
	cur = db.cursor()
	time.sleep(.8)

	# Eliminar objetivos de peso con fecha_fin NULL
	cur.execute("SELECT * FROM Objetivo_peso WHERE id_usuario='"+username_user+"' AND fecha_fin IS NULL;")
	resultado = cur.fetchall()
	if resultado:
		cur.execute("DELETE FROM Objetivo_peso WHERE id_usuario='"+username_user+"' AND fecha_fin IS NULL;")
		db.commit()


	# Comprobar si hay datos registrados
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL;")
	hay_peso = cur.fetchall()
	cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username_user+"' AND grasa IS NOT NULL;")
	hay_grasa = cur.fetchall()
	cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username_user+"' AND musculo IS NOT NULL;")
	hay_musculo = cur.fetchall()

	cur.close()
	db.close()
	# Si no hay nada registrado
	keyboard = []
	if hay_peso:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de peso", callback_data='inicio_peso_establecer_peso')])

	if hay_grasa:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de grasa", callback_data='inicio_peso_establecer_grasa')])

	if hay_musculo:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de músculo", callback_data='inicio_peso_establecer_musculo')])

	keyboard.append([InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Selecciona un tipo de objetivo"
	)

	time.sleep(.8)
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Mi objetivo de peso > Establecer objetivo",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER"
	return INICIO_PESO_ESTABLECER

def objetivo_peso(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot

	# Peso más reciente
	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL)")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Tu último peso registrado es: "+str(peso).rstrip('0').rstrip('. ')+"kg"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu peso objetivo (en kg)?"
	)

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de peso 🔙", callback_data='back_inicio_peso_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 75.5",
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_PESO"
	return INICIO_PESO_ESTABLECER_PESO

def check_objetivo_peso(update, context):
	global current_state 

	user_msg = update.message.text
	username_user = update.message.from_user.username

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de peso 🔙", callback_data='back_inicio_peso_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if is_float(user_msg):

		peso = float(user_msg)
		if peso < 0:
			update.message.reply_text(
				text="No puedes usar números negativos. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			# Peso más reciente
			cur = db.cursor()
			cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL)")
			resultado = cur.fetchall()
			ultimo_peso = resultado[0][0]

			diferencia_peso = round(peso-float(ultimo_peso),1)

			if diferencia_peso != 0:
				if(diferencia_peso >= 0):
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(diferencia_peso).rstrip('0').rstrip('. ')+"kg más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso)).rstrip('0').rstrip('. ')+"kg menos que actualmente."
					)

				keyboard = [
					[InlineKeyboardButton("1 mes", callback_data='objetivo_peso_1'), InlineKeyboardButton("2 meses", callback_data='objetivo_peso_2')],
					[InlineKeyboardButton("3 meses", callback_data='objetivo_peso_3'), InlineKeyboardButton("6 meses", callback_data='objetivo_peso_4')],
					[InlineKeyboardButton("1 año", callback_data='objetivo_peso_5')],
					[InlineKeyboardButton("No quiero establecer un objetivo de peso 🔙", callback_data='back_inicio_peso_establecer')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				time.sleep(.8)
				update.message.reply_text(
					text="¿Cuál es tu fecha objetivo?",
					reply_markup=reply_markup
				)

				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("INSERT INTO Objetivo_peso(tipo,objetivo,diferencia,fecha_inicio,date_add,id_usuario) VALUES (%s, %s, %s, %s, %s, %s)",("peso",peso,diferencia_peso,date_today,date_today,username_user))
				db.commit()

				cur.close()
				db.close()

				current_state="INICIO_PESO_ESTABLECER_PESO_TIEMPO"
				return INICIO_PESO_ESTABLECER_PESO_TIEMPO

			else:
				time.sleep(.8)
				update.message.reply_text(
					text="Tu objetivo no puede ser tu peso actual. Prueba de nuevo.",
					reply_markup=reply_markup
				)

	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Escríbeme tu objetivo de peso (en kg)."
		)
		time.sleep(.8)
		update.message.reply_text(
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 75.5",
			reply_markup=reply_markup
		)

def objetivo_peso_tiempo(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username
	plazo = query.data
	plazo = plazo[-1:]
	
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	if plazo == "1":
		cur.execute("SELECT CURDATE() + INTERVAL 1 MONTH;")

	elif plazo == "2":
		cur.execute("SELECT CURDATE() + INTERVAL 2 MONTH;")

	elif plazo == "3":
		cur.execute("SELECT CURDATE() + INTERVAL 3 MONTH;")

	elif plazo == "4":
		cur.execute("SELECT CURDATE() + INTERVAL 6 MONTH;")

	elif plazo == "5":
		cur.execute("SELECT CURDATE() + INTERVAL 1 YEAR;")

	resultado = cur.fetchall()
	fecha = resultado[0][0]
	fecha_fin = fecha
	fecha = fecha.strftime("%d-%b-%Y")

	cur.execute("SELECT objetivo,diferencia FROM Objetivo_peso WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	if resultado[0][1] > 0:
		diferencia = "+"+str(resultado[0][1])
	else:
		diferencia = str(resultado[0][1])

	cur.execute("UPDATE Objetivo_peso SET fecha_fin='"+str(fecha_fin)+"' WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	db.commit()

	cur.close()
	db.close()

	text = "RESUMEN DEL OBJETIVO:\n\nPeso objetivo: "+str(peso).rstrip('0').rstrip('. ')+"kg\nDiferencia de peso: "+diferencia+"kg\nFecha fin: "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text
	)
	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='objetivo_peso_tiempo_si')],
		[InlineKeyboardButton("No ❌", callback_data='objetivo_peso_tiempo_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Confirmas este nuevo objetivo?",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR"
	return INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR

def objetivo_grasa(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot

	# Peso más reciente
	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND grasa IS NOT NULL)")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Tu último porcentaje de grasa registrado es: "+str(peso).rstrip('0').rstrip('. ')+"%"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu porcentaje de grasa objetivo?"
	)

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de grasa 🔙", callback_data='back_inicio_peso_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_GRASA"
	return INICIO_PESO_ESTABLECER_GRASA

def check_objetivo_grasa(update, context):
	global current_state 

	user_msg = update.message.text
	username_user = update.message.from_user.username

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de grasa 🔙", callback_data='back_inicio_peso_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if is_float(user_msg):

		peso = float(user_msg)
		if peso < 0:
			update.message.reply_text(
				text="No puedes usar números negativos. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			# Peso más reciente
			cur = db.cursor()
			cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND grasa IS NOT NULL)")
			resultado = cur.fetchall()
			ultimo_peso = resultado[0][0]

			diferencia_peso = round(peso-float(ultimo_peso),1)

			if diferencia_peso != 0:
				if(diferencia_peso >= 0):
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso)).rstrip('0').rstrip('. ')+"% menos que actualmente."
					)

				keyboard = [
					[InlineKeyboardButton("1 mes", callback_data='objetivo_grasa_1'), InlineKeyboardButton("2 meses", callback_data='objetivo_grasa_2')],
					[InlineKeyboardButton("3 meses", callback_data='objetivo_grasa_3'), InlineKeyboardButton("6 meses", callback_data='objetivo_grasa_4')],
					[InlineKeyboardButton("1 año", callback_data='objetivo_grasa_5')],
					[InlineKeyboardButton("No quiero establecer un objetivo de grasa 🔙", callback_data='back_inicio_peso_establecer')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				time.sleep(.8)
				update.message.reply_text(
					text="¿Cuál es tu fecha objetivo?",
					reply_markup=reply_markup
				)

				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("INSERT INTO Objetivo_peso(tipo,objetivo,diferencia,fecha_inicio,date_add,id_usuario) VALUES (%s, %s, %s, %s, %s, %s)",("grasa",peso,diferencia_peso,date_today,date_today,username_user))
				db.commit()

				cur.close()
				db.close()

				current_state="INICIO_PESO_ESTABLECER_GRASA_TIEMPO"
				return INICIO_PESO_ESTABLECER_GRASA_TIEMPO

			else:
				time.sleep(.8)
				update.message.reply_text(
					text="Tu objetivo no puede ser tu porcentaje de grasa actual. Prueba de nuevo.",
					reply_markup=reply_markup
				)

	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Escríbeme tu objetivo de porcentaje de grasa."
		)
		time.sleep(.8)
		update.message.reply_text(
			chat_id = query.message.chat_id,
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
			reply_markup=reply_markup
		)

def objetivo_grasa_tiempo(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username
	plazo = query.data
	plazo = plazo[-1:]
	
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	if plazo == "1":
		cur.execute("SELECT CURDATE() + INTERVAL 1 MONTH;")

	elif plazo == "2":
		cur.execute("SELECT CURDATE() + INTERVAL 2 MONTH;")

	elif plazo == "3":
		cur.execute("SELECT CURDATE() + INTERVAL 3 MONTH;")

	elif plazo == "4":
		cur.execute("SELECT CURDATE() + INTERVAL 6 MONTH;")

	elif plazo == "5":
		cur.execute("SELECT CURDATE() + INTERVAL 1 YEAR;")

	resultado = cur.fetchall()
	fecha = resultado[0][0]
	fecha_fin = fecha
	fecha = fecha.strftime("%d-%b-%Y")

	cur.execute("SELECT objetivo,diferencia FROM Objetivo_peso WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	if resultado[0][1] > 0:
		diferencia = "+"+str(resultado[0][1])
	else:
		diferencia = str(resultado[0][1])

	cur.execute("UPDATE Objetivo_peso SET fecha_fin='"+str(fecha_fin)+"' WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	db.commit()

	cur.close()
	db.close()

	text = "RESUMEN DEL OBJETIVO:\n\nPorcentaje de grasa objetivo: "+str(peso).rstrip('0').rstrip('. ')+"kg\nDiferencia de porcentaje: "+diferencia+"%\nFecha fin: "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text
	)
	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='objetivo_peso_tiempo_si')],
		[InlineKeyboardButton("No ❌", callback_data='objetivo_peso_tiempo_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Confirmas este nuevo objetivo?",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR"
	return INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR

def objetivo_musculo(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot

	# Peso más reciente
	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username_user+"' AND musculo IS NOT NULL AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND musculo IS NOT NULL)")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Tu último porcentaje de músculo registrado es: "+str(peso).rstrip('0').rstrip('. ')+"%"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Cuál es tu porcentaje de músculo objetivo?"
	)

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de músculo 🔙", callback_data='back_inicio_peso_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_MUSCULO"
	return INICIO_PESO_ESTABLECER_MUSCULO

def check_objetivo_musculo(update, context):
	global current_state 

	user_msg = update.message.text
	username_user = update.message.from_user.username

	keyboard = [
		[InlineKeyboardButton("No quiero establecer un objetivo de músculo 🔙", callback_data='back_inicio_peso')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if is_float(user_msg):

		peso = float(user_msg)
		if peso < 0:
			update.message.reply_text(
				text="No puedes usar números negativos. Prueba de nuevo.",
				reply_markup=reply_markup
			)
		else:
			db = pymysql.connect("localhost", "root", "password", "Imagym")
			db.begin()

			# Peso más reciente
			cur = db.cursor()
			cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND musculo IS NOT NULL)")
			resultado = cur.fetchall()
			ultimo_peso = resultado[0][0]

			diferencia_peso = round(peso-float(ultimo_peso),1)

			if diferencia_peso != 0:
				if(diferencia_peso >= 0):
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(diferencia_peso).rstrip('0').rstrip('. ')+"% más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso)).rstrip('0').rstrip('. ')+"% menos que actualmente."
					)

				keyboard = [
					[InlineKeyboardButton("1 mes", callback_data='objetivo_musculo_1'), InlineKeyboardButton("2 meses", callback_data='objetivo_musculo_2')],
					[InlineKeyboardButton("3 meses", callback_data='objetivo_musculo_3'), InlineKeyboardButton("6 meses", callback_data='objetivo_musculo_4')],
					[InlineKeyboardButton("1 año", callback_data='objetivo_musculo_5')],
					[InlineKeyboardButton("No quiero establecer un objetivo de músculo 🔙", callback_data='back_inicio_peso_establecer')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				time.sleep(.8)
				update.message.reply_text(
					text="¿Cuál es tu fecha objetivo?",
					reply_markup=reply_markup
				)

				cur.execute("SELECT CURDATE();")
				resultado = cur.fetchall()
				date_today = resultado[0][0]
				cur.execute("INSERT INTO Objetivo_peso(tipo,objetivo,diferencia,fecha_inicio,date_add,id_usuario) VALUES (%s, %s, %s, %s, %s, %s)",("musculo",peso,diferencia_peso,date_today,date_today,username_user))
				db.commit()

				cur.close()
				db.close()

				current_state="INICIO_PESO_ESTABLECER_MUSCULO_TIEMPO"
				return INICIO_PESO_ESTABLECER_MUSCULO_TIEMPO

			else:
				time.sleep(.8)
				update.message.reply_text(
					text="Tu objetivo no puede ser tu porcentaje de músculo actual. Prueba de nuevo.",
					reply_markup=reply_markup
				)

	else:
		time.sleep(.8)
		update.message.reply_text(
			text="No te entiendo. Dime tu objetivo de porcentaje de músculo."
		)
		time.sleep(.8)
		update.message.reply_text(
			text="Escríbeme solo un número. Si usas decimales, sepáralos por un punto. Por ejemplo, 15.8",
			reply_markup=reply_markup
		)

def objetivo_musculo_tiempo(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	username = query.from_user.username
	plazo = query.data
	plazo = plazo[-1:]
	
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	if plazo == "1":
		cur.execute("SELECT CURDATE() + INTERVAL 1 MONTH;")

	elif plazo == "2":
		cur.execute("SELECT CURDATE() + INTERVAL 2 MONTH;")

	elif plazo == "3":
		cur.execute("SELECT CURDATE() + INTERVAL 3 MONTH;")

	elif plazo == "4":
		cur.execute("SELECT CURDATE() + INTERVAL 6 MONTH;")

	elif plazo == "5":
		cur.execute("SELECT CURDATE() + INTERVAL 1 YEAR;")

	resultado = cur.fetchall()
	fecha = resultado[0][0]
	fecha_fin = fecha
	fecha = fecha.strftime("%d-%b-%Y")

	cur.execute("SELECT objetivo,diferencia FROM Objetivo_peso WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	resultado = cur.fetchall()
	peso = resultado[0][0]

	if resultado[0][1] > 0:
		diferencia = "+"+str(resultado[0][1])
	else:
		diferencia = str(resultado[0][1])

	cur.execute("UPDATE Objetivo_peso SET fecha_fin='"+str(fecha_fin)+"' WHERE id_usuario='"+username+"' and fecha_fin IS NULL;")
	db.commit()

	cur.close()
	db.close()

	text = "RESUMEN DEL OBJETIVO:\n\nPorcentaje de músculo objetivo: "+str(peso).rstrip('0').rstrip('. ')+"kg\nDiferencia de porcentaje: "+diferencia+"%\nFecha fin: "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text
	)
	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='objetivo_peso_tiempo_si')],
		[InlineKeyboardButton("No ❌", callback_data='objetivo_peso_tiempo_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Confirmas este nuevo objetivo?",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR"
	return INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR

def objetivo_peso_tiempo_si(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has establecido tu objetivo con éxito ✔",
	)

	time.sleep(.8)
	show_inicio_peso(update, context)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def objetivo_peso_tiempo_no(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("DELETE FROM Objetivo_peso WHERE id_usuario='"+username+"' and date_add=CURDATE();")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="No has establecido el objetivo ❌",
	)

	time.sleep(.8)
	show_inicio_peso(update, context)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def show_inicio_peso_eliminar(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='objetivo_peso_eliminar_si')],
		[InlineKeyboardButton("No ❌", callback_data='objetivo_peso_eliminar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Deseas eliminar tu objetivo actual?",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ELIMINAR"
	return INICIO_PESO_ELIMINAR

def objetivo_peso_eliminar_si(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("DELETE FROM Objetivo_peso WHERE id_usuario='"+username+"' and fecha_fin>CURDATE();")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has eliminado tu objetivo. Puedes proponerte otro siempre que quieras.",
	)

	time.sleep(.8)
	show_inicio_peso(update, context)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def objetivo_peso_eliminar_no(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="De acuerdo, no eliminaré tu objetivo actual.",
	)

	time.sleep(.8)
	show_inicio_peso(update, context)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def show_inicio_peso_evolucion(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Mi objetivo de peso > Evolución... "
	)

	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' and peso IS NOT NULL;")
	peso = cur.fetchall()
	cur.execute("SELECT grasa FROM Peso WHERE id_usuario='"+username_user+"' AND grasa IS NOT NULL;")
	grasa = cur.fetchall()
	cur.execute("SELECT musculo FROM Peso WHERE id_usuario='"+username_user+"' AND musculo IS NOT NULL;")
	musculo = cur.fetchall()
	cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL;")
	imc = cur.fetchall()

	time.sleep(.8)

	keyboard = []

	if peso:
		keyboard.append([InlineKeyboardButton("Evolución de peso", callback_data='inicio_peso_evolucion_peso')])

	if grasa:
		keyboard.append([InlineKeyboardButton("Evolución de grasa", callback_data='inicio_peso_evolucion_grasa')])

	if musculo:
		keyboard.append([InlineKeyboardButton("Evolución de músculo", callback_data='inicio_peso_evolucion_musculo')])

	if imc:
		keyboard.append([InlineKeyboardButton("Evolución del IMC", callback_data='inicio_peso_evolucion_imc')])

	keyboard.append([InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Mi objetivo de peso > Evolución",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_EVOLUCION"
	return INICIO_PESO_EVOLUCION

def evolucion_peso(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando gráfica..."
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/peso/"+image_name_plot

	# image_name_bar = current_user+"_"+current_date[0][0]+"_"+current_time[0][0]+"_bar.png"
	# image_path_bar = "/home/jumacasni/Documentos/ingenieria_informatica/curso1920/TFG/graphs/"+image_name_bar

	cur.execute("SELECT fecha,peso FROM Peso WHERE id_usuario='"+username+"' ORDER BY DATE(fecha) ASC;")
	user_date_weight = cur.fetchall()
	x_axis = []
	y_axis = []
	numbers = []
	for i in range(len(user_date_weight)):
		numbers.append(i)
		fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
		x_axis.append(fecha)

	for i in range(len(user_date_weight)):
		y_axis.append(user_date_weight[i][1])

	plt.clf()
	plt.plot(x_axis, y_axis, 'g--d')
	plt.xticks(rotation=25)
	plt.ylabel("Peso (kg)")
	plt.xlabel("Fecha")
	plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

	keyboard = [
		[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	plot = open(image_path_plot, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = plot
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí está tu evolución desde que empezaste hasta hoy."
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución entre dos fechas, usa /rango <fecha_1> <fecha_2>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución desde una fecha hasta hoy, usa /rango <fecha>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el formato DD-MM-YYYY\n\nEjemplo: /rango 01-01-2019 31-12-2019"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = 'INICIO_PESO_EVOLUCION_PESO'
	return INICIO_PESO_EVOLUCION_PESO

def evolucion_peso_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	if len(n_params) < 1 or len(n_params) > 2:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /rango 01-01-2019 01-12-2019\nEjemplo 2: /rango 01-01-2019"
		)
	elif len(n_params) == 1:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy"
				)
			else:
				update.message.reply_text(
					text="⏳ Generando gráfica..."
				)
				time.sleep(.8)

				fecha_date = datetime.strptime(fecha_string, '%d-%m-%Y')
				fecha1 = fecha_string[6:10] +'-'+ fecha_string[3:5] +'-'+ fecha_string[0:2] # Formato YYYY-mm-dd

				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/peso/"+image_name_plot
				
				cur.execute("SELECT fecha,peso FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' ORDER BY DATE(fecha) ASC;")
				user_date_weight = cur.fetchall()
				x_axis = []
				y_axis = []
				numbers = []
				for i in range(len(user_date_weight)):
					numbers.append(i)
					fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
					x_axis.append(fecha)

				for i in range(len(user_date_weight)):
					y_axis.append(user_date_weight[i][1])

				plt.clf()
				plt.plot(x_axis, y_axis, 'g--d')
				plt.xticks(rotation=25)
				plt.ylabel("Peso (kg)")
				plt.xlabel("Fecha")
				plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

				keyboard = [
					[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				plot = open(image_path_plot, 'rb')
				update.message.reply_photo(
					photo = plot,
					text="Aquí está tu evolución desde el día "+fecha1+" hasta hoy."
				)
				time.sleep(.8)
				update.message.reply_text(
					text="Puedes continuar generando más gráficas con /rango",
				)
				time.sleep(.8)
				update.message.reply_text(
					text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso",
					reply_markup=reply_markup
				)
		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy"
			)

	elif len(n_params) == 2:
		fecha1_string = context.args[0]
		fecha2_string = context.args[1]

		if is_valid_date(fecha1_string) and is_valid_date(fecha2_string):
			fecha1_len = len(fecha1_string)
			fecha2_len = len(fecha2_string)
			if fecha1_len != 10 and fecha2_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy para ambas fechas"
				)
			else:
				fecha1_date = datetime.strptime(fecha1_string, '%d-%m-%Y')
				fecha1 = fecha1_string[6:10] +'-'+ fecha1_string[3:5] +'-'+ fecha1_string[0:2] # Formato YYYY-mm-dd
				fecha2_date = datetime.strptime(fecha2_string, '%d-%m-%Y')
				fecha2 = fecha2_string[6:10] +'-'+ fecha2_string[3:5] +'-'+ fecha2_string[0:2] # Formato YYYY-mm-dd

				if fecha1 > fecha2:
					update.message.reply_text(
						text="La primera fecha no puede ser posterior a la segunda fecha. Prueba de nuevo."
					)
				else:
					update.message.reply_text(
						text="⏳ Generando gráfica..."
					)
					time.sleep(.8)

					db = pymysql.connect("localhost", "root", "password", "Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/peso/"+image_name_plot
					
					cur.execute("SELECT fecha,peso FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' and fecha<='"+fecha2+"' ORDER BY DATE(fecha) ASC;")
					user_date_weight = cur.fetchall()
					x_axis = []
					y_axis = []
					numbers = []
					for i in range(len(user_date_weight)):
						numbers.append(i)
						fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
						x_axis.append(fecha)

					for i in range(len(user_date_weight)):
						y_axis.append(user_date_weight[i][1])

					plt.clf()
					plt.plot(x_axis, y_axis, 'g--d')
					plt.xticks(rotation=25)
					plt.ylabel("Peso (kg)")
					plt.xlabel("Fecha")
					plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

					keyboard = [
						[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
					]

					reply_markup = InlineKeyboardMarkup(keyboard)
					plot = open(image_path_plot, 'rb')
					update.message.reply_photo(
						photo = plot,
						text="Aquí está tu evolución desde el día "+fecha1+" hasta el día "+fecha2+"."
					)
					time.sleep(.8)
					update.message.reply_text(
						text="Puedes continuar generando más gráficas con /rango",
					)
					time.sleep(.8)
					update.message.reply_text(
						text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso",
						reply_markup=reply_markup
					)
		else:
			update.message.reply_text(
				text="No has introducido dos fechas. Recuerda usar el formato dd-mm-yyyy."
			)

def evolucion_grasa(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando gráfica..."
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/grasa/"+image_name_plot

	cur.execute("SELECT fecha,grasa FROM Peso WHERE id_usuario='"+username+"' ORDER BY DATE(fecha) ASC;")
	user_date_weight = cur.fetchall()
	x_axis = []
	y_axis = []
	numbers = []
	for i in range(len(user_date_weight)):
		numbers.append(i)
		fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
		x_axis.append(fecha)

	for i in range(len(user_date_weight)):
		y_axis.append(user_date_weight[i][1])

	plt.clf()
	plt.plot(x_axis, y_axis, 'g--d')
	plt.xticks(rotation=25)
	plt.ylabel("Grasa (%)")
	plt.xlabel("Fecha")
	plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

	keyboard = [
		[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	plot = open(image_path_plot, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = plot
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí está tu evolución de tu porcentaje de grasa desde que empezaste hasta hoy."
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución entre dos fechas, usa /rango <fecha_1> <fecha_2>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución desde una fecha hasta hoy, usa /rango <fecha>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el formato DD-MM-YYYY\n\nEjemplo: /rango 01-01-2019 31-12-2019"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = 'INICIO_PESO_EVOLUCION_GRASA'
	return INICIO_PESO_EVOLUCION_GRASA

def evolucion_grasa_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	if len(n_params) < 1 or len(n_params) > 2:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /rango 01-01-2019 01-12-2019\nEjemplo 2: /rango 01-01-2019"
		)
	elif len(n_params) == 1:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy"
				)
			else:
				update.message.reply_text(
					text="⏳ Generando gráfica..."
				)
				time.sleep(.8)

				fecha_date = datetime.strptime(fecha_string, '%d-%m-%Y')
				fecha1 = fecha_string[6:10] +'-'+ fecha_string[3:5] +'-'+ fecha_string[0:2] # Formato YYYY-mm-dd

				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/grasa/"+image_name_plot
				
				cur.execute("SELECT fecha,grasa FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' ORDER BY DATE(fecha) ASC;")
				user_date_weight = cur.fetchall()
				x_axis = []
				y_axis = []
				numbers = []
				for i in range(len(user_date_weight)):
					numbers.append(i)
					fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
					x_axis.append(fecha)

				for i in range(len(user_date_weight)):
					y_axis.append(user_date_weight[i][1])

				plt.clf()
				plt.plot(x_axis, y_axis, 'g--d')
				plt.xticks(rotation=25)
				plt.ylabel("Grasa (%)")
				plt.xlabel("Fecha")
				plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

				keyboard = [
					[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				plot = open(image_path_plot, 'rb')
				update.message.reply_photo(
					photo = plot,
					text="Aquí está tu evolución del procentaje de grasa desde el día "+fecha1+" hasta hoy."
				)
				time.sleep(.8)
				update.message.reply_text(
					text="Puedes continuar generando más gráficas con /rango",
				)
				time.sleep(.8)
				update.message.reply_text(
					text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa",
					reply_markup=reply_markup
				)
		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy"
			)

	elif len(n_params) == 2:
		fecha1_string = context.args[0]
		fecha2_string = context.args[1]

		if is_valid_date(fecha1_string) and is_valid_date(fecha2_string):
			fecha1_len = len(fecha1_string)
			fecha2_len = len(fecha2_string)
			if fecha1_len != 10 and fecha2_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy para ambas fechas"
				)
			else:
				fecha1_date = datetime.strptime(fecha1_string, '%d-%m-%Y')
				fecha1 = fecha1_string[6:10] +'-'+ fecha1_string[3:5] +'-'+ fecha1_string[0:2] # Formato YYYY-mm-dd
				fecha2_date = datetime.strptime(fecha2_string, '%d-%m-%Y')
				fecha2 = fecha2_string[6:10] +'-'+ fecha2_string[3:5] +'-'+ fecha2_string[0:2] # Formato YYYY-mm-dd

				if fecha1 > fecha2:
					update.message.reply_text(
						text="La primera fecha no puede ser posterior a la segunda fecha. Prueba de nuevo."
					)
				else:
					update.message.reply_text(
						text="⏳ Generando gráfica..."
					)
					time.sleep(.8)

					db = pymysql.connect("localhost", "root", "password", "Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/peso/"+image_name_plot
					
					cur.execute("SELECT fecha,peso FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' and fecha<='"+fecha2+"' ORDER BY DATE(fecha) ASC;")
					user_date_weight = cur.fetchall()
					x_axis = []
					y_axis = []
					numbers = []
					for i in range(len(user_date_weight)):
						numbers.append(i)
						fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
						x_axis.append(fecha)

					for i in range(len(user_date_weight)):
						y_axis.append(user_date_weight[i][1])

					plt.clf()
					plt.plot(x_axis, y_axis, 'g--d')
					plt.xticks(rotation=25)
					plt.ylabel("Grasa (%)")
					plt.xlabel("Fecha")
					plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

					keyboard = [
						[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
					]

					reply_markup = InlineKeyboardMarkup(keyboard)
					plot = open(image_path_plot, 'rb')
					update.message.reply_photo(
						photo = plot,
						text="Aquí está tu evolución del porcentaje de grasa desde el día "+fecha1+" hasta el día "+fecha2+"."
					)
					time.sleep(.8)
					update.message.reply_text(
						text="Puedes continuar generando más gráficas con /rango",
					)
					time.sleep(.8)
					update.message.reply_text(
						text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa",
						reply_markup=reply_markup
					)
		else:
			update.message.reply_text(
				text="No has introducido dos fechas. Recuerda usar el formato dd-mm-yyyy."
			)

def evolucion_musculo(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando gráfica..."
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/musculo/"+image_name_plot

	cur.execute("SELECT fecha,musculo FROM Peso WHERE id_usuario='"+username+"' ORDER BY DATE(fecha) ASC;")
	user_date_weight = cur.fetchall()
	x_axis = []
	y_axis = []
	numbers = []
	for i in range(len(user_date_weight)):
		numbers.append(i)
		fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
		x_axis.append(fecha)

	for i in range(len(user_date_weight)):
		y_axis.append(user_date_weight[i][1])

	plt.clf()
	plt.plot(x_axis, y_axis, 'g--d')
	plt.xticks(rotation=25)
	plt.ylabel("Músculo (%)")
	plt.xlabel("Fecha")
	plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

	keyboard = [
		[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	plot = open(image_path_plot, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = plot
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí está tu evolución de tu porcentaje de músculo desde que empezaste hasta hoy."
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución entre dos fechas, usa /rango <fecha_1> <fecha_2>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución desde una fecha hasta hoy, usa /rango <fecha>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el formato DD-MM-YYYY\n\nEjemplo: /rango 01-01-2019 31-12-2019"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = 'INICIO_PESO_EVOLUCION_MUSCULO'
	return INICIO_PESO_EVOLUCION_MUSCULO

def evolucion_musculo_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	if len(n_params) < 1 or len(n_params) > 2:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /rango 01-01-2019 01-12-2019\nEjemplo 2: /rango 01-01-2019"
		)
	elif len(n_params) == 1:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy"
				)
			else:
				update.message.reply_text(
					text="⏳ Generando gráfica..."
				)
				time.sleep(.8)

				fecha_date = datetime.strptime(fecha_string, '%d-%m-%Y')
				fecha1 = fecha_string[6:10] +'-'+ fecha_string[3:5] +'-'+ fecha_string[0:2] # Formato YYYY-mm-dd

				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/IMC/"+image_name_plot
				
				cur.execute("SELECT fecha,IMC FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' ORDER BY DATE(fecha) ASC;")
				user_date_weight = cur.fetchall()
				x_axis = []
				y_axis = []
				numbers = []
				for i in range(len(user_date_weight)):
					numbers.append(i)
					fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
					x_axis.append(fecha)

				for i in range(len(user_date_weight)):
					y_axis.append(user_date_weight[i][1])

				plt.clf()
				plt.plot(x_axis, y_axis, 'g--d')
				plt.xticks(rotation=25)
				plt.ylabel("IMC")
				plt.xlabel("Fecha")
				plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

				keyboard = [
					[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				plot = open(image_path_plot, 'rb')
				update.message.reply_photo(
					photo = plot,
					text="Aquí está tu evolución del IMC desde el día "+fecha1+" hasta hoy."
				)
				time.sleep(.8)
				update.message.reply_text(
					text="Puedes continuar generando más gráficas con /rango",
				)
				time.sleep(.8)
				update.message.reply_text(
					text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo",
					reply_markup=reply_markup
				)
		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy"
			)

	elif len(n_params) == 2:
		fecha1_string = context.args[0]
		fecha2_string = context.args[1]

		if is_valid_date(fecha1_string) and is_valid_date(fecha2_string):
			fecha1_len = len(fecha1_string)
			fecha2_len = len(fecha2_string)
			if fecha1_len != 10 and fecha2_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy para ambas fechas"
				)
			else:
				fecha1_date = datetime.strptime(fecha1_string, '%d-%m-%Y')
				fecha1 = fecha1_string[6:10] +'-'+ fecha1_string[3:5] +'-'+ fecha1_string[0:2] # Formato YYYY-mm-dd
				fecha2_date = datetime.strptime(fecha2_string, '%d-%m-%Y')
				fecha2 = fecha2_string[6:10] +'-'+ fecha2_string[3:5] +'-'+ fecha2_string[0:2] # Formato YYYY-mm-dd

				if fecha1 > fecha2:
					update.message.reply_text(
						text="La primera fecha no puede ser posterior a la segunda fecha. Prueba de nuevo."
					)
				else:
					update.message.reply_text(
						text="⏳ Generando gráfica..."
					)
					time.sleep(.8)

					db = pymysql.connect("localhost", "root", "password", "Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/IMC/"+image_name_plot
					
					cur.execute("SELECT fecha,IMC FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' and fecha<='"+fecha2+"' ORDER BY DATE(fecha) ASC;")
					user_date_weight = cur.fetchall()
					x_axis = []
					y_axis = []
					numbers = []
					for i in range(len(user_date_weight)):
						numbers.append(i)
						fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
						x_axis.append(fecha)

					for i in range(len(user_date_weight)):
						y_axis.append(user_date_weight[i][1])

					plt.clf()
					plt.plot(x_axis, y_axis, 'g--d')
					plt.xticks(rotation=25)
					plt.ylabel("IMC")
					plt.xlabel("Fecha")
					plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

					keyboard = [
						[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
					]

					reply_markup = InlineKeyboardMarkup(keyboard)
					plot = open(image_path_plot, 'rb')
					update.message.reply_photo(
						photo = plot,
						text="Aquí está tu evolución del IMC desde el día "+fecha1+" hasta el día "+fecha2+"."
					)
					time.sleep(.8)
					update.message.reply_text(
						text="Puedes continuar generando más gráficas con /rango",
					)
					time.sleep(.8)
					update.message.reply_text(
						text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo",
						reply_markup=reply_markup
					)
		else:
			update.message.reply_text(
				text="No has introducido dos fechas. Recuerda usar el formato dd-mm-yyyy."
			)

def evolucion_imc(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando gráfica..."
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/IMC/"+image_name_plot

	cur.execute("SELECT fecha,IMC FROM Peso WHERE id_usuario='"+username+"' ORDER BY DATE(fecha) ASC;")
	user_date_weight = cur.fetchall()
	x_axis = []
	y_axis = []
	numbers = []
	for i in range(len(user_date_weight)):
		numbers.append(i)
		fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
		x_axis.append(fecha)

	for i in range(len(user_date_weight)):
		y_axis.append(user_date_weight[i][1])

	plt.clf()
	plt.plot(x_axis, y_axis, 'g--d')
	plt.xticks(rotation=25)
	plt.ylabel("IMC")
	plt.xlabel("Fecha")
	plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

	keyboard = [
		[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	plot = open(image_path_plot, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = plot
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí está tu evolución de tu IMC desde que empezaste hasta hoy."
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución entre dos fechas, usa /rango <fecha_1> <fecha_2>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver tu evolución desde una fecha hasta hoy, usa /rango <fecha>"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el formato DD-MM-YYYY\n\nEjemplo: /rango 01-01-2019 31-12-2019"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de IMC",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = 'INICIO_PESO_EVOLUCION_IMC'
	return INICIO_PESO_EVOLUCION_IMC

def evolucion_imc_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	if len(n_params) < 1 or len(n_params) > 2:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /rango 01-01-2019 01-12-2019\nEjemplo 2: /rango 01-01-2019"
		)
	elif len(n_params) == 1:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy"
				)
			else:
				update.message.reply_text(
					text="⏳ Generando gráfica..."
				)
				time.sleep(.8)

				fecha_date = datetime.strptime(fecha_string, '%d-%m-%Y')
				fecha1 = fecha_string[6:10] +'-'+ fecha_string[3:5] +'-'+ fecha_string[0:2] # Formato YYYY-mm-dd

				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/musculo/"+image_name_plot
				
				cur.execute("SELECT fecha,musculo FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' ORDER BY DATE(fecha) ASC;")
				user_date_weight = cur.fetchall()
				x_axis = []
				y_axis = []
				numbers = []
				for i in range(len(user_date_weight)):
					numbers.append(i)
					fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
					x_axis.append(fecha)

				for i in range(len(user_date_weight)):
					y_axis.append(user_date_weight[i][1])

				plt.clf()
				plt.plot(x_axis, y_axis, 'g--d')
				plt.xticks(rotation=25)
				plt.ylabel("IMC")
				plt.xlabel("Fecha")
				plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

				keyboard = [
					[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
				]

				reply_markup = InlineKeyboardMarkup(keyboard)
				plot = open(image_path_plot, 'rb')
				update.message.reply_photo(
					photo = plot,
					text="Aquí está tu evolución del IMC desde el día "+fecha1+" hasta hoy."
				)
				time.sleep(.8)
				update.message.reply_text(
					text="Puedes continuar generando más gráficas con /rango",
				)
				time.sleep(.8)
				update.message.reply_text(
					text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de IMC",
					reply_markup=reply_markup
				)
		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy"
			)

	elif len(n_params) == 2:
		fecha1_string = context.args[0]
		fecha2_string = context.args[1]

		if is_valid_date(fecha1_string) and is_valid_date(fecha2_string):
			fecha1_len = len(fecha1_string)
			fecha2_len = len(fecha2_string)
			if fecha1_len != 10 and fecha2_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy para ambas fechas"
				)
			else:
				fecha1_date = datetime.strptime(fecha1_string, '%d-%m-%Y')
				fecha1 = fecha1_string[6:10] +'-'+ fecha1_string[3:5] +'-'+ fecha1_string[0:2] # Formato YYYY-mm-dd
				fecha2_date = datetime.strptime(fecha2_string, '%d-%m-%Y')
				fecha2 = fecha2_string[6:10] +'-'+ fecha2_string[3:5] +'-'+ fecha2_string[0:2] # Formato YYYY-mm-dd

				if fecha1 > fecha2:
					update.message.reply_text(
						text="La primera fecha no puede ser posterior a la segunda fecha. Prueba de nuevo."
					)
				else:
					update.message.reply_text(
						text="⏳ Generando gráfica..."
					)
					time.sleep(.8)

					db = pymysql.connect("localhost", "root", "password", "Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/jumacasni/Documentos/ImagymBot/evolucion/musculo/"+image_name_plot
					
					cur.execute("SELECT fecha,musculo FROM Peso WHERE id_usuario='"+username+"' and fecha>='"+fecha1+"' and fecha<='"+fecha2+"' ORDER BY DATE(fecha) ASC;")
					user_date_weight = cur.fetchall()
					x_axis = []
					y_axis = []
					numbers = []
					for i in range(len(user_date_weight)):
						numbers.append(i)
						fecha = user_date_weight[i][0].strftime("%d-%m-%Y")
						x_axis.append(fecha)

					for i in range(len(user_date_weight)):
						y_axis.append(user_date_weight[i][1])

					plt.clf()
					plt.plot(x_axis, y_axis, 'g--d')
					plt.xticks(rotation=25)
					plt.ylabel("IMC")
					plt.xlabel("Fecha")
					plt.savefig(image_path_plot,bbox_inches='tight',dpi=100)

					keyboard = [
						[InlineKeyboardButton("Volver a Evolución 🔙", callback_data='back_inicio_peso_evolucion')]
					]

					reply_markup = InlineKeyboardMarkup(keyboard)
					plot = open(image_path_plot, 'rb')
					update.message.reply_photo(
						photo = plot,
						text="Aquí está tu evolución del IMC desde el día "+fecha1+" hasta el día "+fecha2+"."
					)
					time.sleep(.8)
					update.message.reply_text(
						text="Puedes continuar generando más gráficas con /rango"
					)
					time.sleep(.8)
					update.message.reply_text(
						text="👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo",
						reply_markup=reply_markup
					)
		else:
			update.message.reply_text(
				text="No has introducido dos fechas. Recuerda usar el formato dd-mm-yyyy."
			)

def show_inicio_peso_valoracion(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando informe de tu IMC... "
	)
	time.sleep(.8)
	# IMC más reciente
	username_user = query.from_user.username
	cur = db.cursor()
	cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL)")
	resultado = cur.fetchall()
	imc = resultado[0][0]

	image_path = "/home/jumacasni/Documentos/ImagymBot/imagenes/IMC.jpg"

	keyboard = [
		[InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if imc < 18.5:
		text = "Tu IMC es "+str(imc)+"\nTienes una delgadez muy severa. Quizá deberías acudir a un médico o nutricionista."
	elif imc >= 18.5 and imc < 25:
		text = "Tu IMC es "+str(imc)+"\n¡Estás en el peso perfecto! Sigue así."
	elif imc >= 25 and imc < 30:
		text = "Tu IMC es "+str(imc)+"\nTienes un peso un poco por encima de lo normal. Conmigo puedes trabajar para llegar al peso perfecto. ¡Ánimo!"
	elif imc >= 30 and imc < 35:
		text = "Tu IMC es "+str(imc)+"\nTienes una obesidad moderada. Haciendo ejercicio y con una dieta saludable podemos hacer grandes cosas y mejorar ese peso. ¡Ánimo!"
	elif imc >= 35 and imc < 40:
		text = "Tu IMC es "+str(imc)+"\nTienes obesidad severa. Puedo ayudarte a mejorar tu IMC, aunque no estaría mal que consultaras tu estado de salud a un médico o nutricionista."
	else:
		text = "Tu IMC es "+str(imc)+"\nTienes obesidad mórbida. Deberías acudir a un médico o nutricionista."

	photo_imc = open(image_path, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = photo_imc,
		text = "Esta imagen muestra una tabla con los valores del IMC."
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text=text,
		reply_markup=reply_markup
	)

	current_state = "INICIO_PESO_VALORACION"
	return INICIO_PESO_VALORACION

############# MI OBJETIVO DE ACTIVIDADES CARDIO #############
def show_inicio_cardio(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Actividades cardio... "
	)

	# Comprobar si hoy ha hecho cardio
	username_user = query.from_user.username

	keyboard = [[InlineKeyboardButton("Registrar actividad cardio 🏃", callback_data='inicio_cardio_registrar')]]

	cur = db.cursor()
	cur.execute("SELECT DISTINCT id_actividad_cardio FROM Registra_cardio WHERE id_usuario='"+username_user+"';")
	hay_cardio = cur.fetchall()

	cur.execute("SELECT DISTINCT id_actividad_cardio FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND DATE(fecha)=CURDATE();")
	resultado = cur.fetchall()

	if hay_cardio:
		keyboard.append([InlineKeyboardButton("Ver mis registros en cardio 📋", callback_data='inicio_cardio_ver')])

	if not resultado:
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="📌 Hoy no has realizado cardio aún. Cuando hagas cardio, ¡regístralo!"
		)

	else:
		time.sleep(.8)

		if len(resultado) == 1:
			text="📌 Hoy has registrado una actividad cardio:\n"

		else:
			text="📌 Hoy has registrado las siguientes actividades cardio:\n"

		for i in range(len(resultado)):
			cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(resultado[i][0])+";")
			res = cur.fetchall()
			nombre = res[0][0]
			text=text+"\n✔"+nombre

		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text
		)

	cur.execute("SELECT id_actividad_cardio,objetivo,fecha_inicio,fecha_fin FROM Objetivo_personal_cardio WHERE id_usuario='"+username_user+"' AND fecha_fin>=CURDATE() AND estado='P';")
	resultado = cur.fetchall()
	# Si no tiene un objetivo personal de cardio
	if not resultado:
		keyboard.append([InlineKeyboardButton("Establecer objetivo 🏁", callback_data='inicio_cardio_establecer')])
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="📌 No tienes aún ningún objetivo personal de actividad cardio.\n\nLos objetivos personales de cardio duran un mes y puedes proponerte un número mínimo de minutos, kilómetros o calorías para cumplir."
		)

	else:
		keyboard.append([InlineKeyboardButton("Eliminar objetivo 🏁", callback_data='inicio_cardio_eliminar')])
		id_actividad_cardio = resultado[0][0]
		objetivo = resultado[0][1]
		objetivo_numero = objetivo.split(' ',2)[0]
		objetivo_tipo = objetivo.split(' ',2)[1]
		fecha_inicio = resultado[0][2]
		fecha_fin = resultado[0][3]

		cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
		res = cur.fetchall()
		nombre = res[0][0]

		text="📌 Tienes un objetivo personal de cardio en <b>"+nombre.lower()+"</b>:\n"

		if objetivo_tipo == "distancia":
			tipo = "kilómetros"
			text=text+"\nObjetivo: "+objetivo_numero.rstrip('0').rstrip('. ')+" "+tipo
		elif objetivo_tipo == "calorias":
			tipo = "calorías"
			text=text+"\nObjetivo: "+objetivo_numero+" "+tipo
		else:
			objetivo_tipo = "tiempo"
			tipo = "minutos"
			text=text+"\nObjetivo: "+objetivo_numero+" "+tipo


		if fecha_inicio == date.today():
			fecha_inicio = "hoy"
		else:
			fecha_inicio = fecha_inicio.strftime("%d-%b-%Y")

		text=text+"\nFecha inicio: "+str(fecha_inicio)
		text=text+"\nFecha fin: "+fecha_fin.strftime("%d-%b-%Y")
		text=text+"\n\n"

		cur.execute("SELECT SUM("+objetivo_tipo+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+username_user+"' AND fecha>='"+str(resultado[0][2])+"' AND fecha<='"+str(resultado[0][3])+"';")
		resultado = cur.fetchall()

		if resultado[0][0] is None:
			text=text+"Aún no has acumulado "+tipo+". ¡Registra cardio en <b>"+nombre.lower()+"</b> para comenzar tu marcador!"
		else:
			diferencia = round(float(objetivo_numero) - float(resultado[0][0]), 2)
			if diferencia > 0:
				text=text+"Llevas ya <b>"+str(resultado[0][0]).rstrip('0').rstrip('. ')+" "+tipo+"</b>."
				text=text+"\nTe quedan: "+str(diferencia).rstrip('0').rstrip('. ')+" "+tipo
				porcentaje = round(float(resultado[0][0]) / float(objetivo_numero), 2) * 100
				text=text+"\n¡Ya llevas un "+str(round(porcentaje,1))+"%!"

				if porcentaje >= 50 and porcentaje < 80:
					text=text+" TE QUEDA MENOS DE LA MITAD!! 😄"
				elif porcentaje >= 80 and porcentaje < 90:
					text=text+" YA CASI LO CONSIGUES!! 😄"
				elif porcentaje >= 90:
					text=text+" YA ESTÁS CASI EN LA CIMA!! 😄"
			else:
				keyboard.pop()
				keyboard.append([InlineKeyboardButton("Establecer objetivo 🏁", callback_data='inicio_cardio_establecer')])
				text="¡HAS ALCANZADO TU OBJETIVO DE <b>"+objetivo_numero+" "+tipo+"</b>!!!!! 🥳🥳🥳🥳"
				bot.send_message(
					chat_id = query.message.chat_id,
					text=text,
					parse_mode='HTML'
				)
				text="¡ENHORABUENA! Sigue así. Puedes comenzar un nuevo objetivo cuando quieras 😄😄😄"
				cur.execute("UPDATE Objetivo_personal_cardio SET estado='C' WHERE id_usuario='"+username_user+"' AND fecha_fin>=CURDATE() AND estado='P';")
				db.commit()

		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			parse_mode='HTML'
		)

	cur.close()
	db.close()

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	time.sleep(.8)
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Actividades cardio",
		reply_markup = reply_markup
	)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

def show_inicio_cardio_registrar(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Actividades cardio > Registrar cardio... "
	)

	username_user = query.from_user.username

	cur = db.cursor()

	# Eliminar registro de cardio si está nulo
	cur.execute("SELECT * FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND tiempo IS NULL AND distancia IS NULL AND nivel IS NULL AND calorias IS NULL;")
	resultado = cur.fetchall()

	if resultado:
		cur.execute("DELETE FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND tiempo IS NULL AND distancia IS NULL AND nivel IS NULL AND calorias IS NULL;")
		db.commit()

	cur.execute("SELECT id_gym FROM Usuarios WHERE id_usuario='"+username_user+"'")
	resultado = cur.fetchall()
	id_gym = resultado[0][0]

	cur.execute("SELECT nombre,id_actividad_cardio FROM Actividad_cardio WHERE id_actividad_cardio IN (SELECT id_actividad_cardio FROM Cardio_en_gimnasio WHERE id_gym="+str(id_gym)+");")
	resultado = cur.fetchall()
	
	keyboard = []

	if resultado:
		for i in range(len(resultado)):
			text_callback_data = "inicio_cardio_registrar_actividad_"+str(resultado[i][1])
			keyboard.append([InlineKeyboardButton(resultado[i][0], callback_data=text_callback_data)])

			callback_query = CallbackQueryHandler(show_inicio_cardio_registrar_actividad, pattern=text_callback_data)

			if callback_query in conv_handler.states[INICIO_CARDIO_REGISTRAR]:
				pass
			else:
				conv_handler.states[INICIO_CARDIO_REGISTRAR].append(callback_query)

	keyboard.append([InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	cur.close()
	db.close()

	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Qué actividad quieres registrar?"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Actividades cardio > Registrar cardio",
		reply_markup = reply_markup
	)

	current_state = "INICIO_CARDIO_REGISTRAR"
	return INICIO_CARDIO_REGISTRAR

def show_inicio_cardio_registrar_actividad(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	data = update.callback_query.data
	id_actividad_cardio = data.split('_', 4)[4]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Vas a registrar la actividad cardio: "+nombre.lower() 
	)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el comando /cardio <minutos> <kilometros> <nivel_inclinación> <calorias>"
	)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Pon 0 cuando no quieras poner alguna medida"
	)

	cur.execute("SELECT NOW();")
	resultado = cur.fetchall()
	fecha = resultado[0][0]

	cur.execute("INSERT INTO Registra_cardio(id_actividad_cardio,id_usuario,fecha) VALUES (%s, %s, %s)",(id_actividad_cardio,username_user,fecha))
	db.commit()

	cur.close()
	db.close()

	keyboard = [
		[InlineKeyboardButton("Registrar otra actividad cardio 🔙", callback_data='back_inicio_cardio_registrar')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Por ejemplo, si quieres registrar que has estado 30 minutos, has recorrido 4.3 kilometros y has consumido 100 calorías:\n\n/cardio 30 4.3 0 100",
		reply_markup = reply_markup
	)

	curret_state = "INICIO_CARDIO_REGISTRAR_ACTIVIDAD"
	return INICIO_CARDIO_REGISTRAR_ACTIVIDAD

def registrar_cardio(update, context):
	global current_state 

	n_params = context.args

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	keyboard = [
		[InlineKeyboardButton("Registrar otra actividad cardio 🔙", callback_data='back_inicio_cardio_registrar')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 4:
		update.message.reply_text(
			text="Has introducido mal el comando.\nEjemplo: /cardio 10 3 1 0",
			reply_markup = reply_markup
		)
	else:
		minutos = context.args[0]
		kilometros = context.args[1]
		nivel = context.args[2]
		calorias = context.args[3]
		username = update.message.from_user.username

		if is_int(minutos) and is_float(kilometros) and is_int(nivel) and is_int(calorias):
			minutos = int(minutos)
			kilometros = float(kilometros)
			nivel = int(nivel)
			calorias = int(calorias)

			if minutos < 0:
				update.message.reply_text(
					text="No puedes introducir minutos negativos. Prueba el comando /cardio de nuevo.",
					reply_markup = reply_markup
				)

				return

			elif kilometros < 0:
				update.message.reply_text(
					text="No puedes introducir kilómetros negativos. Prueba el comando /cardio de nuevo.",
					reply_markup = reply_markup
				)

				return

			elif nivel < 0:
				update.message.reply_text(
					text="No puedes introducir un nivel negativo. Prueba el comando /cardio de nuevo.",
					reply_markup = reply_markup
				)

				return

			elif calorias < 0:
				update.message.reply_text(
					text="No puedes introducir calorías negativas. Prueba el comando /cardio de nuevo.",
					reply_markup = reply_markup
				)

				return

			# Todos los parámetros positivos
			else:

				# Actividad cardio más reciente
				cur.execute("SELECT id_actividad_cardio,id_usuario,fecha FROM Registra_cardio WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(c2.fecha) FROM Registra_cardio c2 WHERE id_usuario='"+username+"')")
				resultado = cur.fetchall()

				id_actividad_cardio = resultado[0][0]
				fecha = resultado[0][2]

				cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
				resultado = cur.fetchall()
				nombre = resultado[0][0]

				text="Vas a registrar lo siguiente:\n"
				text=text+"\nActividad cardio: "+nombre
				if minutos != 0:
					text=text+"\nMinutos: "+str(minutos)
					cur.execute("UPDATE Registra_cardio SET tiempo="+str(minutos)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\nMinutos: sin datos"
				if kilometros != 0:
					text=text+"\nDistancia: "+str(kilometros).rstrip('0').rstrip('. ')+"km"
					cur.execute("UPDATE Registra_cardio SET distancia="+str(kilometros)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\nDistancia: sin datos"
				if nivel != 0:
					text=text+"\nNivel: "+str(nivel)
					cur.execute("UPDATE Registra_cardio SET nivel="+str(nivel)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\nNivel/Inclinación: sin datos"
				if calorias != 0:
					text=text+"\nCalorías: "+str(calorias)
					cur.execute("UPDATE Registra_cardio SET calorias="+str(calorias)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\nCalorías: sin datos"

				resultado = cur.fetchall()

				keyboard = [
					[InlineKeyboardButton("Si ✔", callback_data='registrar_cardio_si')],
					[InlineKeyboardButton("No ❌", callback_data='registrar_cardio_no')]
				]
				update.message.reply_text(
					text=text
				)

				# Si tiene un objetivo
				cur.execute("SELECT id_actividad_cardio,objetivo,fecha_fin FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND fecha_fin>=CURDATE() AND estado='P';")
				resultado = cur.fetchall()

				if resultado:
					id_actividad_cardio_objetivo = resultado[0][0]
					if id_actividad_cardio_objetivo == id_actividad_cardio:
						objetivo = resultado[0][1]
						objetivo_numero = objetivo.split(' ',2)[0]
						objetivo_tipo = objetivo.split(' ',2)[1]

						text="Añadirás <b>"
						if objetivo_tipo == "distancia":
							if kilometros != 0:
								text=text+str(kilometros).rstrip('0').rstrip('. ')+" kilómetros</b>"
								text=text+" a tu objetivo en <b>"+nombre+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						elif objetivo_tipo == "calorias":
							if calorias != 0:
								text=text+str(calorias)+" calorías</b>"
								text=text+" a tu objetivo en <b>"+nombre+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						else:
							if minutos != 0:
								text=text+str(minutos)+" minutos</b>"
								text=text+" a tu objetivo en <b>"+nombre+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)


				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="¿Confirmas este registro?",
					reply_markup = reply_markup
				)

				current_state = "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR"
				return INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR

		elif not is_int(minutos):
			update.message.reply_text(
				text="Minutos incorrectos. Prueba el comando /cardio de nuevo.",
				reply_markup = reply_markup
			)

		elif not is_float(kilometros):
			update.message.reply_text(
				text="Kilómetros incorrectos. Prueba el comando /cardio de nuevo.",
				reply_markup = reply_markup
			)

		elif not is_int(nivel):
			update.message.reply_text(
				text="Nivel o inclinación incorrecta. Prueba el comando /cardio de nuevo.",
				reply_markup = reply_markup
			)

		elif not is_int(calorias):
			update.message.reply_text(
				text="Calorías incorrectas. Prueba el comando /cardio de nuevo.",
				reply_markup = reply_markup
			)

def show_inicio_cardio_ver(update,context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Todas las actividades cardio del último día que hizo cardio
	cur.execute("SELECT id_actividad_cardio,TIME(fecha),DATE(fecha),tiempo,distancia,nivel,calorias FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND DATE(fecha)=(SELECT MAX(DATE(fecha)) FROM Registra_cardio WHERE id_usuario='"+username_user+"');")
	resultado = cur.fetchall()

	fecha = resultado[0][2]

	if fecha == date.today():
		text="Actividades cardio registradas hoy:\n"
	else:
		text="La última vez que realizaste cardio fue el día "+str(fecha)+" y fueron las siguientes:\n"

	for i in range(len(resultado)):
		cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(resultado[i][0])+";")
		res = cur.fetchall()
		nombre = res[0][0]

		fecha = resultado[i][2].strftime("%d-%b-%Y")
		text=text+"\n📌<b>"+fecha+" "
		text=text+str(resultado[i][1])+" "
		text=text+nombre+":</b> "
		if resultado[i][3] is not None:
			text=text+str(resultado[i][3])+" minutos; "
		if resultado[i][4] is not None:
			text=text+str(resultado[i][4]).rstrip('0').rstrip('. ')+" kilómetros; "
		if resultado[i][5] is not None:
			text=text+"nivel/inclinación: "+str(resultado[i][5])+"; "
		if resultado[i][6] is not None:
			text=text+str(resultado[i][6])+" calorías; "
		text=text+"\n"

	keyboard = [[InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')],
	[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]]

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Si quieres ver el cardio que hiciste en otra fecha, usa /rango dd-mm-yyyy\n\nPor ejemplo: /rango 01-01-2020",
		reply_markup=reply_markup
	)

	current_state = "INICIO_CARDIO_VER"
	return INICIO_CARDIO_VER

def registrar_cardio_si(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has registrado la actividad cardio con éxito ✔",
	)

	time.sleep(.8)
	show_inicio_cardio_registrar(update, context)

	current_state = "INICIO_CARDIO_REGISTRAR"
	return INICIO_CARDIO_REGISTRAR

def registrar_cardio_no(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("SELECT id_actividad_cardio,fecha FROM Registra_cardio WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(c2.fecha) FROM Registra_cardio c2 WHERE id_usuario='"+username+"');")
	resultado = cur.fetchall()
	id_actividad_cardio=resultado[0][0]
	fecha=resultado[0][1]
	cur.execute("DELETE FROM Registra_cardio WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"' AND id_actividad_cardio="+str(id_actividad_cardio)+"")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="No has registrado la actividad cardio ❌",
	)

	time.sleep(.8)
	show_inicio_cardio_registrar(update, context)

	current_state = "INICIO_CARDIO_REGISTRAR"
	return INICIO_CARDIO_REGISTRAR

def ver_cardio_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	keyboard = [[InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')]]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /rango 01-01-2019 01-12-2019\nEjemplo 2: /rango 01-01-2019",
			reply_markup=reply_markup
		)
	else:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy. Prueba el comando /rango de nuevo.",
					reply_markup=reply_markup
				)
			else:
				time.sleep(.8)
				fecha_date = datetime.strptime(fecha_string, '%d-%m-%Y')
				fecha1 = fecha_string[6:10] +'-'+ fecha_string[3:5] +'-'+ fecha_string[0:2] # Formato YYYY-mm-dd

				if fecha_date.date() > date.today():
					update.message.reply_text(
						text="No puedes introducir una fecha mayor que la de hoy. Prueba de nuevo",
						reply_markup=reply_markup
					)

					return

				db = pymysql.connect("localhost", "root", "password", "Imagym")
				db.begin()
				cur = db.cursor()

				# Todas las actividades cardio del día
				cur.execute("SELECT id_actividad_cardio,TIME(fecha),DATE(fecha),tiempo,distancia,nivel,calorias FROM Registra_cardio WHERE id_usuario='"+username+"' AND DATE(fecha)='"+fecha1+"';")
				resultado = cur.fetchall()

				if resultado:
					text="Actividades cardio registradas el día "+fecha1+":\n"

					for i in range(len(resultado)):
						cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(resultado[i][0])+";")
						res = cur.fetchall()
						nombre = res[0][0]

						fecha = resultado[i][2].strftime("%d-%b-%Y")
						text=text+"\n📌<b>"+fecha+" "
						text=text+str(resultado[i][1])+" "
						text=text+nombre+":</b> "
						if resultado[i][3] is not None:
							text=text+str(resultado[i][3])+" minutos; "
						if resultado[i][4] is not None:
							text=text+str(resultado[i][4]).rstrip('0').rstrip('. ')+" kilómetros; "
						if resultado[i][5] is not None:
							text=text+"nivel/inclinación: "+str(resultado[i][5])+"; "
						if resultado[i][6] is not None:
							text=text+str(resultado[i][6])+" calorías; "
						text=text+"\n"

				else:
					text="El día "+fecha1+" no registraste ninguna actividad cardio."

				update.message.reply_text(
					text=text,
					parse_mode='HTML'
				)

				time.sleep(1)
				update.message.reply_text(
					text="Puedes seguir consultando más días",
					reply_markup=reply_markup
				)

		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy.",
				reply_markup=reply_markup
			)

def show_inicio_cardio_establecer(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Actividades cardio > Establecer objetivo... "
	)

	username_user = query.from_user.username

	cur = db.cursor()

	# Eliminar objetivo personal de cardio si está nulo
	cur.execute("SELECT * FROM Objetivo_personal_cardio WHERE id_usuario='"+username_user+"' AND objetivo IS NULL;")
	resultado = cur.fetchall()

	if resultado:
		cur.execute("DELETE FROM Objetivo_personal_cardio WHERE id_usuario='"+username_user+"' AND objetivo IS NULL;")
		db.commit()

	cur.execute("SELECT id_gym FROM Usuarios WHERE id_usuario='"+username_user+"'")
	resultado = cur.fetchall()
	id_gym = resultado[0][0]

	cur.execute("SELECT nombre,id_actividad_cardio FROM Actividad_cardio WHERE id_actividad_cardio IN (SELECT id_actividad_cardio FROM Cardio_en_gimnasio WHERE id_gym="+str(id_gym)+");")
	resultado = cur.fetchall()
	
	keyboard = []

	if resultado:
		for i in range(len(resultado)):
			text_callback_data = "inicio_cardio_establecer_actividad_"+str(resultado[i][1])
			keyboard.append([InlineKeyboardButton(resultado[i][0], callback_data=text_callback_data)])

			callback_query = CallbackQueryHandler(show_inicio_cardio_establecer_actividad, pattern=text_callback_data)

			if callback_query in conv_handler.states[INICIO_CARDIO_ESTABLECER]:
				pass
			else:
				conv_handler.states[INICIO_CARDIO_ESTABLECER].append(callback_query)

	keyboard.append([InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	cur.close()
	db.close()

	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿De qué actividad cardio quieres establecer un objetivo?"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Actividades cardio > Establecer objetivo",
		reply_markup = reply_markup
	)

	current_state = "INICIO_CARDIO_ESTABLECER"
	return INICIO_CARDIO_ESTABLECER

def show_inicio_cardio_establecer_actividad(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	data = update.callback_query.data
	id_actividad_cardio = data.split('_', 4)[4]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_actividad_cardio,nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][1]
	id_actividad_cardio = resultado[0][0]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Vas a establecer un objetivo personal de cardio en "+nombre.lower() 
	)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el comando /minutos <minutos> si quieres establecer un mínimo de minutos para hacer durante 1 mes."
	)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el comando /distancia <kilometros> si quieres establecer un mínimo de kilómetros para hacer durante 1 mes."
	)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Usa el comando /calorias <calorias> si quieres establecer un mínimo de calorías para hacer durante 1 mes."
	)

	cur.execute("SELECT CURDATE() + INTERVAL 1 MONTH;")
	resultado = cur.fetchall()
	next_month = resultado[0][0]
	cur.execute("SELECT CURDATE();")
	resultado = cur.fetchall()
	date_today = resultado[0][0]
	cur.execute("INSERT INTO Objetivo_personal_cardio (estado,fecha_inicio,fecha_fin,date_add,id_usuario,id_actividad_cardio) VALUES (%s, %s, %s, %s, %s, %s)",('P',date_today,next_month,date_today,username_user,id_actividad_cardio))
	db.commit()

	cur.close()
	db.close()

	keyboard = [
		[InlineKeyboardButton("Establecer objetivo de otra actividad cardio 🔙", callback_data='back_inicio_cardio_establecer')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.5)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Por ejemplo, si quieres registrar un objetivo de hacer 300 minutos en "+nombre.lower()+" este mes, usa /minutos 300",
		reply_markup = reply_markup
	)

	curret_state = "INICIO_CARDIO_ESTABLECER_ACTIVIDAD"
	return INICIO_CARDIO_ESTABLECER_ACTIVIDAD

def establecer_cardio_minutos(update, context):
	global current_state 

	n_params = context.args

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	keyboard = [
		[InlineKeyboardButton("Establecer objetivo otra actividad cardio 🔙", callback_data='back_inicio_cardio_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\nEjemplo: /minutos 300",
			reply_markup = reply_markup
		)
	else:
		minutos = context.args[0]
		username = update.message.from_user.username

		if is_int(minutos):
			minutos = int(minutos)

			if minutos < 0:
				update.message.reply_text(
					text="No puedes introducir minutos negativos. Prueba el comando /minutos de nuevo.",
					reply_markup = reply_markup
				)
				return

			elif minutos == 0:
				update.message.reply_text(
					text="No puedes establecer un objetivo de 0 minutos. Prueba el comando /minutos de nuevo.",
					reply_markup = reply_markup
				)
				return

			else:
				cur.execute("SELECT id_actividad_cardio,fecha_inicio,fecha_fin FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				resultado = cur.fetchall()

				id_actividad_cardio = resultado[0][0]
				fecha_inicio = resultado[0][1]
				fecha_fin = resultado[0][2]

				cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
				resultado = cur.fetchall()
				nombre = resultado[0][0]

				text="Vas a establecer el siguiente objetivo:\n"
				text=text+"\nActividad cardio: "+nombre
				text=text+"\nMinutos: "+str(minutos)
				objetivo = str(minutos)+" minutos"
				cur.execute("UPDATE Objetivo_personal_cardio SET objetivo='"+objetivo+"' WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				db.commit()
				text=text+"\nFecha inicio: hoy"
				text=text+"\nFecha fin: "+str(fecha_fin)

				resultado = cur.fetchall()

				keyboard = [
					[InlineKeyboardButton("Si ✔", callback_data='establecer_cardio_si')],
					[InlineKeyboardButton("No ❌", callback_data='establecer_cardio_no')]
				]
				update.message.reply_text(
					text=text
				)
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="¿Confirmas este objetivo personal de cardio?",
					reply_markup = reply_markup
				)

				current_state = "INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR"
				return INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR

		elif not is_int(minutos):
			update.message.reply_text(
				text="Minutos incorrectos. Prueba el comando /minutos de nuevo.",
				reply_markup = reply_markup
			)

def establecer_cardio_distancia(update, context):
	global current_state 

	n_params = context.args

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	keyboard = [
		[InlineKeyboardButton("Establecer objetivo otra actividad cardio 🔙", callback_data='back_inicio_cardio_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\nEjemplo: /distancia 300",
			reply_markup = reply_markup
		)
	else:
		distancia = context.args[0]
		username = update.message.from_user.username

		if is_float(distancia):
			distancia = round(float(distancia),2)

			if distancia < 0:
				update.message.reply_text(
					text="No puedes introducir una distancia negativa. Prueba el comando /distancia de nuevo.",
					reply_markup = reply_markup
				)
				return

			elif distancia == 0:
				update.message.reply_text(
					text="No puedes establecer un objetivo de 0 distancia. Prueba el comando /distancia de nuevo.",
					reply_markup = reply_markup
				)
				return
			else:
				cur.execute("SELECT id_actividad_cardio,fecha_inicio,fecha_fin FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				resultado = cur.fetchall()

				id_actividad_cardio = resultado[0][0]
				fecha_inicio = resultado[0][1]
				fecha_fin = resultado[0][2]

				cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
				resultado = cur.fetchall()
				nombre = resultado[0][0]

				text="Vas a establecer el siguiente objetivo:\n"
				text=text+"\nActividad cardio: "+nombre
				text=text+"\nDistancia: "+str(distancia)+"km"
				objetivo = str(distancia)+" distancia"
				cur.execute("UPDATE Objetivo_personal_cardio SET objetivo='"+objetivo+"' WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				db.commit()
				text=text+"\nFecha inicio: hoy"
				text=text+"\nFecha fin: "+str(fecha_fin)

				resultado = cur.fetchall()

				keyboard = [
					[InlineKeyboardButton("Si ✔", callback_data='establecer_cardio_si')],
					[InlineKeyboardButton("No ❌", callback_data='establecer_cardio_no')]
				]
				update.message.reply_text(
					text=text
				)
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="¿Confirmas este objetivo personal de cardio?",
					reply_markup = reply_markup
				)

				current_state = "INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR"
				return INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR

		elif not is_float(distancia):
			update.message.reply_text(
				text="Distancia incorrecta. Prueba el comando /distancia de nuevo.",
				reply_markup = reply_markup
			)

def establecer_cardio_calorias(update, context):
	global current_state 

	n_params = context.args

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	keyboard = [
		[InlineKeyboardButton("Establecer objetivo otra actividad cardio 🔙", callback_data='back_inicio_cardio_establecer')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\nEjemplo: /calorias 300",
			reply_markup = reply_markup
		)
	else:
		calorias = context.args[0]
		username = update.message.from_user.username

		if is_int(calorias):
			calorias = int(calorias)

			if calorias < 0:
				update.message.reply_text(
					text="No puedes introducir calorías negativas. Prueba el comando /calorias de nuevo.",
					reply_markup = reply_markup
				)
				return

			elif calorias == 0:
				update.message.reply_text(
					text="No puedes establecer un objetivo de 0 calorías. Prueba el comando /calorias de nuevo.",
					reply_markup = reply_markup
				)
				return

			# Todos los parámetros positivos
			else:

				# Actividad cardio más reciente
				cur.execute("SELECT id_actividad_cardio,fecha_inicio,fecha_fin FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				resultado = cur.fetchall()

				id_actividad_cardio = resultado[0][0]
				fecha_inicio = resultado[0][1]
				fecha_fin = resultado[0][2]

				cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
				resultado = cur.fetchall()
				nombre = resultado[0][0]

				text="Vas a establecer el siguiente objetivo:\n"
				text=text+"\nActividad cardio: "+nombre
				text=text+"\nCalorías: "+str(calorias)
				objetivo = str(calorias)+" calorias"
				cur.execute("UPDATE Objetivo_personal_cardio SET objetivo='"+objetivo+"' WHERE id_usuario='"+username+"' AND objetivo IS NULL;")
				db.commit()
				text=text+"\nFecha inicio: hoy"
				text=text+"\nFecha fin: "+str(fecha_fin)

				resultado = cur.fetchall()

				keyboard = [
					[InlineKeyboardButton("Si ✔", callback_data='establecer_cardio_si')],
					[InlineKeyboardButton("No ❌", callback_data='establecer_cardio_no')]
				]
				update.message.reply_text(
					text=text
				)
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="¿Confirmas este objetivo personal de cardio?",
					reply_markup = reply_markup
				)

				current_state = "INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR"
				return INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR

		elif not is_int(calorias):
			update.message.reply_text(
				text="Calorías incorrectos. Prueba el comando /calorias de nuevo.",
				reply_markup = reply_markup
			)

def establecer_cardio_si(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has registrado tu objetivo personal de cardio con éxito ✔",
	)

	time.sleep(.8)
	show_inicio_cardio(update, context)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

def establecer_cardio_no(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("SELECT id_objetivo_personal FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND fecha_inicio=(SELECT MAX(c2.fecha_inicio) FROM Objetivo_personal_cardio c2 WHERE id_usuario='"+username+"' AND estado='P')")
	resultado = cur.fetchall()

	if resultado:
		id_objetivo_personal = resultado[0][0]
		cur.execute("DELETE FROM Objetivo_personal_cardio WHERE id_objetivo_personal="+str(id_objetivo_personal)+";")
		db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="No has establecido el objetivo de actividad cardio ❌",
	)

	time.sleep(.8)
	show_inicio_cardio(update, context)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

def show_inicio_cardio_eliminar(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='objetivo_cardio_eliminar_si')],
		[InlineKeyboardButton("No ❌", callback_data='objetivo_cardio_eliminar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Deseas eliminar tu objetivo personal de cardio actual?",
		reply_markup = reply_markup
	)

	current_state = "INICIO_CARDIO_ELIMINAR"
	return INICIO_CARDIO_ELIMINAR

def objetivo_cardio_eliminar_si(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("SELECT id_objetivo_personal FROM Objetivo_personal_cardio WHERE id_usuario='"+username+"' AND fecha_inicio=(SELECT MAX(c2.fecha_inicio) FROM Objetivo_personal_cardio c2 WHERE id_usuario='"+username+"' AND estado='P')")
	resultado = cur.fetchall()
	
	if resultado:
		id_objetivo_personal = resultado[0][0]
		cur.execute("DELETE FROM Objetivo_personal_cardio WHERE id_objetivo_personal="+str(id_objetivo_personal)+";")
		db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has eliminado tu objetivo personal de cardio. Puedes proponerte otro siempre que quieras.",
	)

	time.sleep(.8)
	show_inicio_cardio(update, context)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

def objetivo_cardio_eliminar_no(update, context):
	global current_state 

	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="De acuerdo, no eliminaré tu objetivo personal de cardio actual.",
	)

	time.sleep(.8)
	show_inicio_cardio(update, context)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

############# RETOS #############
def show_inicio_retos(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos... "
	)
	time.sleep(.8)

	cur = db.cursor()
	# Retos futuros
	cur.execute("SELECT id_reto FROM Retos where fecha_inicio > CURDATE();")
	retos_futuros = cur.fetchall();
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_usuario = cur.fetchall();
	# Retos que aún no han empezado pero el usuario está apuntado
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='A';")
	reto_usuario_futuro = cur.fetchall();
	# Si tiene retos en su historial
	cur.execute("SELECT * FROM Realiza_reto WHERE id_usuario='"+username_user+"' AND estado != 'A' AND estado != 'R';")
	tiene_retos = cur.fetchall();

	keyboard = []

	if reto_usuario:
		id_reto = reto_usuario[0][0]
		# Reto actual del usuario
		cur.execute("SELECT fecha_inicio FROM Retos WHERE id_reto="+str(id_reto)+";")
		fecha = cur.fetchall();
		fecha_inicio = fecha[0][0]

		cur.execute("SELECT CURDATE();")
		resultado = cur.fetchall()
		date_today = resultado[0][0]

		dia_reto = date_today - fecha_inicio
		dia_reto = dia_reto.days+1

		cur.execute("SELECT * FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+"")
		resultado = cur.fetchall()

		# Si no ha guardado el registro de hoy
		if not resultado:
			keyboard.append([InlineKeyboardButton("Anotar progreso 📝", callback_data='inicio_retos_anotar')])

		keyboard.append([InlineKeyboardButton("Calendario de mi reto 📆", callback_data='inicio_retos_calendario')])

	if retos_futuros:
		keyboard.append([InlineKeyboardButton("Ver retos disponibles 🔛", callback_data='inicio_retos_ver')])

	if reto_usuario:
		keyboard.append([InlineKeyboardButton("Descalificarme del reto ❌", callback_data='inicio_retos_descalificar')])

	if reto_usuario_futuro:
		keyboard.append([InlineKeyboardButton("Eliminar mi inscripción de retos ❌", callback_data='inicio_retos_eliminar')])

	if tiene_retos:
		keyboard.append([InlineKeyboardButton("Ver mi historial de retos 📖", callback_data='inicio_retos_historial')])

	if not retos_futuros and not reto_usuario and not tiene_retos:
		text="¡Lo siento! Esta sección aún está vacía. ¡Tu gimnasio pondrá nuevos retos muy pronto!"

	if reto_usuario:
		# Reto que ya ha empezado y el usuario está apuntado
		cur.execute("SELECT Retos.id_reto,Retos.fecha_inicio,Retos.fecha_fin,Retos.id_ejercicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
		reto_actual = cur.fetchall();
		id_reto = reto_actual[0][0]
		fecha_inicio = reto_actual[0][1]
		fecha_fin = reto_actual[0][2]
		id_ejercicio = reto_actual[0][3]

		cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
		ejercicio = cur.fetchall();
		ejercicio = ejercicio[0][0]

		if fecha_inicio == date.today():
			text="¡Hoy empieza tu <b>reto de "+ejercicio.lower()+"</b>!"
			dia_reto = 1
		else:
			dia_reto = date.today()-fecha_inicio
			dia_reto = dia_reto.days+1
			text="¡Sigues en el <b>reto de "+ejercicio.lower()+"</b>"

		text=text+"\n\nDía del reto: <b>"+str(dia_reto)+"</b>"

		cur.execute("SELECT repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+";")
		resultado = cur.fetchall();
		repeticiones = resultado[0][0]
		# Buscar si el usuario ha anotado ya el progreso
		cur.execute("SELECT * FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+"")
		resultado = cur.fetchall()

		if resultado:
			text=text+"\n\n¡Hoy ya has anotado tu progreso! Has hecho <b>"+repeticiones+" "+ejercicio.lower()+"</b>"
		else:
			if repeticiones is None:
				text=text+"\n\n¡Hoy toca descansar!"

			else:
				text=text+"\n\nHoy debes hacer <b>"+repeticiones+" "+ejercicio.lower()+"</b>"

		cur.execute("SELECT COUNT(*) FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND estado='R';")
		resultado = cur.fetchall();
		n_personas = resultado[0][0]

		if n_personas == 1:
			text=text+"\n\n👥 ¡Sólo quedas tú en el reto! ¡Aguanta y consigue la victoria!"

		else:
			text=text+"\n\n👥 Quedan "+str(n_personas)+" personas en el reto"

		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			parse_mode='HTML'
		)

	if reto_usuario_futuro:
		# De todos los retos a los que está apuntado el usuario, coger el que va a ser el próximo
		cur.execute("SELECT Retos.id_ejercicio,Retos.fecha_inicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Retos.fecha_inicio=(SELECT MIN(r1.fecha_inicio) FROM Retos r1 INNER JOIN Realiza_reto r2 WHERE r2.id_usuario='"+username_user+"' and r2.estado='A');")
		proximo_reto = cur.fetchall();
		if proximo_reto:
			ejercicio_proximo_reto = proximo_reto[0][0]
			fecha_inicio_proximo_reto = proximo_reto[0][1]
			fecha_inicio_proximo_reto = fecha_inicio_proximo_reto.strftime('%d-%B-%Y')

			cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(ejercicio_proximo_reto)+";")
			ejercicio = cur.fetchall();
			ejercicio = ejercicio[0][0]

			text="📌 Tu próximo reto: reto de "+ejercicio.lower()
			text=text+"\n\nFecha de inicio: "+fecha_inicio_proximo_reto

			bot.send_message(
				chat_id = query.message.chat_id,
				text=text
		)

	if not reto_usuario and not reto_usuario_futuro:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="📌 Actualmente no estás apuntado a ningún reto"
		)

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS"
	return INICIO_RETOS

def show_inicio_retos_ver(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos > Retos disponibles... "
	)
	time.sleep(.8)

	cur = db.cursor()
	cur.execute("SELECT id_reto FROM Retos where fecha_inicio > CURDATE();")
	resultado = cur.fetchall();

	list_keyboards = []
	callback_query_list = []

	for id_reto in resultado:
		cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
		resultado = cur.fetchall()
		id_ejercicio = resultado[0][0]
		nivel_ejercicio = resultado[0][1]
		start_day = resultado[0][2]

		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		ejercicio_name = cur.fetchall()
		ejercicio_name = ejercicio_name[0][0]

		name_button = "Reto de "+ejercicio_name.lower()+" | Nivel "+str(nivel_ejercicio)+" | "+start_day.strftime('%B').upper()
		button = InlineKeyboardButton(name_button, callback_data="inicio_retos_ver_"+str(id_reto[0]))
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_retos_ver = CallbackQueryHandler(ver_reto, pattern="inicio_retos_ver_"+str(id_reto[0]))
		callback_query_retos_ver_apuntarse = CallbackQueryHandler(ver_reto_apuntarse, pattern="inicio_retos_ver_apuntarse_"+str(id_reto[0]))
		
		if not callback_query_retos_ver in conv_handler.states[INICIO_RETOS_VER]:
			conv_handler.states[INICIO_RETOS_VER].append(callback_query_retos_ver)

		if not callback_query_retos_ver_apuntarse in conv_handler.states[INICIO_RETOS_VER_RETO]:
			conv_handler.states[INICIO_RETOS_VER_RETO].append(callback_query_retos_ver_apuntarse)

		table_reto_path = "/home/jumacasni/Documentos/ImagymBot/retos/"+str(id_reto[0])+".png"
		if not path.exists(table_reto_path):
			createTable(id_reto[0], name_button)

	list_keyboards.append([InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos > Ver retos disponibles",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_VER"
	return INICIO_RETOS_VER

def ver_reto(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',4)
	id_reto = id_reto[3]
	table_reto_path = "/home/jumacasni/Documentos/ImagymBot/retos/"+id_reto+".png"

	pic = open(table_reto_path, 'rb')
	
	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando información del reto... "
	)
	time.sleep(1.2)
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = pic
	)
	cur = db.cursor()

	# Si el reto que selecciona está ya apuntado
	cur.execute("SELECT * FROM Realiza_reto INNER JOIN Retos ON Realiza_reto.id_reto = Retos.id_reto and Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.id_reto="+id_reto+" and Retos.fecha_inicio > CURDATE()")
	esta_apuntado = cur.fetchall()

	# Fecha de inicio del reto
	cur.execute("SELECT fecha_inicio FROM Retos where id_reto="+id_reto+";")
	resultado = cur.fetchall();
	fecha_inicio = resultado[0][0]
	fecha_inicio = fecha_inicio.strftime('%d-%B-%Y')

	# Si el usuario no está apuntado a este reto
	if not esta_apuntado:
		cur.execute("SELECT COUNT(*) FROM Realiza_reto where id_reto="+id_reto+";")
		resultado = cur.fetchall();
		num_usuarios_apuntados = resultado[0][0]

		if num_usuarios_apuntados == 1:
			text = "Hay "+str(num_usuarios_apuntados)+" usuario apuntado a este reto. ¡Anímate!"
		else:
			text = "Hay "+str(num_usuarios_apuntados)+" usuarios apuntados a este reto. ¡Anímate!"

		if num_usuarios_apuntados == 0:
			text = "¡Aún no hay nadie apuntado a este reto! Sé la primera persona en apuntarse y corre la voz para competir con tus rivales 💪💪💪"

		keyboard = [
			[InlineKeyboardButton("Apuntarse al reto ✔", callback_data="inicio_retos_ver_apuntarse_"+id_reto)],
			[InlineKeyboardButton("Volver a Retos disponibles 🔙", callback_data="back_inicio_retos_ver")],
			[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)
		
		bot.send_message(
			chat_id = query.message.chat_id,
			text = "Aquí tienes el calendario de este reto.\n\nFecha de inicio: "+fecha_inicio
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="👣 Inicio > Retos > Ver retos > Apuntarse a reto",
			reply_markup = reply_markup
		)

	else:
		text="¡Ya tienes inscripción en este reto!\n\nFecha de inicio: "+fecha_inicio
		keyboard = [
			[InlineKeyboardButton("Volver a Retos disponibles 🔙", callback_data="back_inicio_retos_ver")],
			[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)

		bot.send_message(
			chat_id = query.message.chat_id,
			text = text
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="👣 Inicio > Retos > Ver retos > Apuntarse a reto",
			reply_markup = reply_markup
		)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_VER_RETO"
	return INICIO_RETOS_VER_RETO

def ver_reto_apuntarse(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',5)
	id_reto = id_reto[4]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si el usuario está apuntado a un reto que coincide en la fecha del reto actual
	cur.execute("SELECT fecha_inicio, fecha_fin FROM Retos WHERE id_reto="+str(id_reto))
	resultado = cur.fetchall()
	start_day_reto = resultado[0][0]
	end_day_reto = resultado[0][1]
	start_day_reto = start_day_reto.strftime("%Y-%m-%d")
	end_day_reto = end_day_reto.strftime("%Y-%m-%d")

	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto ON Retos.id_reto=Realiza_reto.id_reto and Retos.fecha_inicio <= '"+start_day_reto+"' and Retos.fecha_fin >= '"+start_day_reto+"' and Realiza_reto.id_usuario='"+username_user+"' and (Realiza_reto.estado='A' or Realiza_reto.estado='R')")
	resultado_before = cur.fetchall()
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto ON Retos.id_reto=Realiza_reto.id_reto and Retos.fecha_inicio <= '"+end_day_reto+"' and Retos.fecha_fin >= '"+end_day_reto+"' and Realiza_reto.id_usuario='"+username_user+"' and (Realiza_reto.estado='A' or Realiza_reto.estado='R')")
	resultado_after = cur.fetchall()

	keyboard = [
		[InlineKeyboardButton("Volver a Retos disponibles 🔙", callback_data="back_inicio_retos_ver")],
		[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if not resultado_before and not resultado_after:
		cur.execute("INSERT INTO Realiza_reto(id_reto, id_usuario, estado) VALUES (%s, %s, 'A')",(id_reto,username_user)) 
		db.commit()
		bot.send_message(
			chat_id = query.message.chat_id,
			text="⏳ Registrando tu inscripción al reto..."
		)
		time.sleep(1.5)

		text="¡Te has apuntado al reto! Te deseo mucha suerte. Te avisaré cuando empiece el reto."

		cur = db.cursor()
		cur.execute("SELECT fecha_inicio FROM Retos WHERE id_reto="+id_reto)
		resultado = cur.fetchall()
		start_day_object = resultado[0][0]

		ESP = tz.gettz('Europe/Madrid')
		dt = datetime(start_day_object.year,start_day_object.month,start_day_object.day,8,0,0, tzinfo=ESP)

		name_alarm=username_user+"_"+str(id_reto)
		context.job_queue.run_once(primer_dia_reto, dt, context=(query.message.chat_id, update, id_reto), name=name_alarm)

		bot.send_message(
			chat_id = query.message.chat_id,
			text = text
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text = '👣 Inicio > Retos > Ver retos disponibles > Apuntarse a reto',
			reply_markup = reply_markup
		)
	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text = 'No puedes apuntarte al reto porque sus fechas coinciden con otro reto al que ya estás apuntado.',
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text = '👣 Inicio > Retos > Ver retos disponibles > Apuntarse a reto',
			reply_markup = reply_markup
		)

	cur.close()
	db.close()

def primer_dia_reto(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_reto = job.context[2]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Ejercicio
	cur.execute("SELECT id_ejercicio FROM Retos WHERE id_reto="+str(id_reto)+";")
	resultado = cur.fetchall()
	id_ejercicio = resultado[0][0]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	# Actualizar estado del reto
	cur.execute("UPDATE Realiza_reto SET estado='R' WHERE id_reto="+str(id_reto)+" AND id_usuario='"+username_user+"'")
	db.commit()

	# Ponemos la alarma para que a las 00:00 del día siguiente compruebe si hay que descalificar al usuario del reto o no
	cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL 1 DAY);");
	resultado = cur.fetchall()
	datetime_alarm = resultado[0][0]

	ESP = tz.gettz('Europe/Madrid')
	dt = datetime(datetime_alarm.year,datetime_alarm.month,datetime_alarm.day,0,0,0, tzinfo=ESP)

	name_alarm="descalificar_"+username_user+"_"+str(id_reto)
	context.job_queue.run_once(descalificar_reto, dt, context=(query.message.chat_id, job.context[1], id_reto), name=name_alarm)

	bot.send_message(
		job.context[0],
		text="🌄 ¡BUENOS DÍAS! 🌄\n\nHoy comienza tu <b>reto de "+nombre.lower()+"</b>",
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Ir a Inicio > Retos 👣", callback_data='back_inicio_retos')],
		[InlineKeyboardButton("Ir a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		job.context[0],
		text="Puedes anotar tu progreso en 👣 <b>Inicio > Retos</b> en cualquier momento del día",
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	for i in conv_handler.states:
		show_inicio_retos = CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos')
		show_inicio = CallbackQueryHandler(show_inicio, pattern='back_inicio')
		if not show_inicio in conv_handler.states[i]:
			conv_handler.states[i].append(show_inicio)
		if not show_inicio_retos in conv_handler.states[i]:
			conv_handler.states[i].append(show_inicio_retos)

	cur.close()
	db.close()

def recordar_reto(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_reto = job.context[2]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Ejercicio
	cur.execute("SELECT id_ejercicio FROM Retos WHERE id_reto="+str(id_reto)+";")
	resultado = cur.fetchall()
	id_ejercicio = resultado[0][0]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	# Actualizar estado del reto
	cur.execute("UPDATE Realiza_reto SET estado='R' WHERE id_reto="+str(id_reto)+" AND id_usuario='"+username_user+"'")
	db.commit()

	# Ponemos la alarma para que a las 00:00 del día siguiente compruebe si hay que descalificar al usuario del reto o no
	cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL 1 DAY);");
	resultado = cur.fetchall()
	datetime_alarm = resultado[0][0]

	ESP = tz.gettz('Europe/Madrid')
	dt = datetime(datetime_alarm.year,datetime_alarm.month,datetime_alarm.day,0,0,0, tzinfo=ESP)

	name_alarm="descalificar_"+username_user+"_"+str(id_reto)
	context.job_queue.run_once(descalificar_reto, dt, context=(query.message.chat_id, job.context[1], id_reto), name=name_alarm)

	bot.send_message(
		job.context[0],
		text="🌄 ¡BUENOS DÍAS! 🌄\n\nTe recuerdo sigues participando en el <b>reto de "+nombre.lower()+"</b>",
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Ir a Inicio > Retos 👣", callback_data='back_inicio_retos')],
		[InlineKeyboardButton("Ir a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		job.context[0],
		text="Puedes anotar tu progreso en 👣 <b>Inicio > Retos</b> en cualquier momento del día",
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	cur.close()
	db.close()

def descalificar_reto(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_reto = job.context[2]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	# Ejercicio
	cur.execute("SELECT id_ejercicio FROM Retos WHERE id_reto="+str(id_reto)+";")
	resultado = cur.fetchall()
	id_ejercicio = resultado[0][0]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	# Actualizar estado del reto
	cur.execute("UPDATE Realiza_reto SET estado='D' WHERE id_reto="+str(id_reto)+" AND id_usuario='"+username_user+"'")
	db.commit()

	bot.send_message(
		job.context[0],
		text="❌ Lo siento ❌\n\nHas sido descalificado del <b>reto de "+nombre.lower()+"</b>",
		parse_mode='HTML'
	)
	bot.send_message(
		job.context[0],
		text="¡Suerte en el próximo reto!",
		parse_mode='HTML'
	)
	keyboard = [
		[InlineKeyboardButton("Ir a Inicio > Retos 👣", callback_data='back_inicio_retos')],
		[InlineKeyboardButton("Ir a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		job.context[0],
		text="Puedes ver tu historial de retos en 👣 <b>Inicio > Retos</b>",
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	cur.close()
	db.close()

def show_inicio_retos_eliminar(update, context):
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos > Eliminar inscripción de retos... "
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_reto FROM Realiza_reto where id_usuario='"+username_user+"' AND estado='A';")
	resultado = cur.fetchall();

	list_keyboards = []

	for id_reto in resultado:
		cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
		resultado = cur.fetchall()
		id_ejercicio = resultado[0][0]
		nivel_ejercicio = resultado[0][1]
		start_day = resultado[0][2]

		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		ejercicio_name = cur.fetchall()
		ejercicio_name = ejercicio_name[0][0]

		name_button = "Reto de "+ejercicio_name.lower()+" | Nivel "+str(nivel_ejercicio)+" | "+start_day.strftime('%B').upper()
		button = InlineKeyboardButton(name_button, callback_data="inicio_retos_eliminar_"+str(id_reto[0]))

		callback_query_retos_eliminar = CallbackQueryHandler(eliminar_reto_confirmar, pattern="inicio_retos_eliminar_"+str(id_reto[0]))
		callback_query_retos_eliminar_confirmar = CallbackQueryHandler(eliminar_reto_confirmar_si, pattern="inicio_retos_eliminar_confirmar_"+str(id_reto[0]))
		
		if not callback_query_retos_eliminar in conv_handler.states[INICIO_RETOS_ELIMINAR]:
			conv_handler.states[INICIO_RETOS_ELIMINAR].append(callback_query_retos_eliminar)

		if not callback_query_retos_eliminar_confirmar in conv_handler.states[INICIO_RETOS_ELIMINAR_CONFIRMAR]:
			conv_handler.states[INICIO_RETOS_ELIMINAR_CONFIRMAR].append(callback_query_retos_eliminar_confirmar)

		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)

	list_keyboards.append([InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos > Eliminar inscripción de retos",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_ELIMINAR"
	return INICIO_RETOS_ELIMINAR

def eliminar_reto_confirmar(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',4)
	id_reto = id_reto[3]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='inicio_retos_eliminar_confirmar_'+str(id_reto))],
		[InlineKeyboardButton("No ❌", callback_data='eliminar_reto_confirmar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
	resultado = cur.fetchall()
	id_ejercicio = resultado[0][0]
	nivel_ejercicio = resultado[0][1]
	start_day = resultado[0][2]

	cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
	ejercicio_name = cur.fetchall()
	ejercicio_name = ejercicio_name[0][0]

	text = "reto de "+ejercicio_name.lower()+", nivel "+str(nivel_ejercicio)+" de "+start_day.strftime('%B')

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Deseas eliminar el <b>"+text+"</b>?",
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_ELIMINAR_CONFIRMAR"
	return INICIO_RETOS_ELIMINAR_CONFIRMAR

def eliminar_reto_confirmar_si(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',5)
	id_reto = id_reto[4]

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("DELETE FROM Realiza_reto WHERE id_usuario='"+username_user+"' AND id_reto="+str(id_reto)+";") 
	db.commit()

	# Retos que aún no han empezado pero el usuario está apuntado
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='A';")
	reto_usuario_futuro = cur.fetchall();

	cur.close()
	db.close()
	
	if not reto_usuario_futuro:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="He eliminado tu inscripción de ese reto con éxito ✔"
		)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="¡Ya no estás apuntado a más retos! Te voy a reedirigir al apartado de Retos"
		)
		time.sleep(1.5)
		show_inicio_retos(update, context)

		current_state = "INICIO_RETOS"
		return "INICIO_RETOS"

	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="He eliminado tu inscripción de ese reto con éxito ✔"
		)
		time.sleep(.8)

		show_inicio_retos_eliminar(update, context)

		current_state = "INICIO_RETOS_ELIMINAR"
		return INICIO_RETOS_ELIMINAR

def eliminar_reto_confirmar_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡Puedes relajarte, no he eliminado tu inscripción!"
	)

	show_inicio_retos_eliminar(update, context)

	current_state= "INICIO_RETOS_ELIMINAR"
	return INICIO_RETOS_ELIMINAR

def show_inicio_retos_anotar(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos > Anotar progreso... "
	)
	time.sleep(.8)

	cur = db.cursor()
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto,Retos.fecha_inicio,Retos.id_ejercicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_usuario = cur.fetchall();
	id_reto = reto_usuario[0][0]
	fecha_inicio = reto_usuario[0][1]
	id_ejercicio = reto_usuario[0][2]

	cur.execute("SELECT CURDATE();")
	resultado = cur.fetchall()
	date_today = resultado[0][0]

	dia_reto = date_today - fecha_inicio
	dia_reto = dia_reto.days+1

	cur.execute("SELECT repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+";")
	resultado = cur.fetchall();
	repeticiones = resultado[0][0]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	ejercicio = cur.fetchall();
	ejercicio = ejercicio[0][0]

	text="¿Has hecho ya <b>"+repeticiones+" "+ejercicio.lower()+"?</b>"

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='inicio_retos_anotar_si')],
		[InlineKeyboardButton("No ❌", callback_data='inicio_retos_anotar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_ANOTAR_CONFIRMAR"
	return INICIO_RETOS_ANOTAR_CONFIRMAR

def inicio_retos_anotar_si(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Anotando tu progreso..."
	)
	time.sleep(.8)

	cur = db.cursor()
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto,Retos.fecha_inicio,Retos.fecha_fin FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_usuario = cur.fetchall();
	id_reto = reto_usuario[0][0]
	fecha_inicio = reto_usuario[0][1]
	fecha_fin = reto_usuario[0][2]

	cur.execute("SELECT CURDATE();")
	resultado = cur.fetchall()
	date_today = resultado[0][0]

	dia_reto = date_today - fecha_inicio
	dia_reto = dia_reto.days+1

	cur.execute("UPDATE Realiza_reto SET dia="+str(dia_reto)+" WHERE id_reto="+str(id_reto)+" and id_usuario='"+username_user+"';")
	db.commit()


	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡He anotado tu progreso con éxito ✔! ¡Ánimo!"
	)
	time.sleep(1)

	# Seleccionar el próximo día del reto
	cur.execute("SELECT dia,repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia=(SELECT MIN(dia) FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia>"+str(dia_reto)+" AND repeticiones != NULL);")
	resultado = cur.fetchall()

	# Si no hay próximo día de reto o la fecha fin es hoy
	if not resultado or fecha_fin == date.today():
		cur.execute("UPDATE Realiza_reto SET estado='C' WHERE id_reto="+str(id_reto)+" and id_usuario='"+username_user+"';")
		db.commit()

		bot.send_message(
			chat_id = query.message.chat_id,
			text="¡HAS COMPLETADO EL RETO! 🥳🥳🥳🥳🥳🥳🥳\n\n🏆 ¡ENHORABUENA! 🏆"
		)
		time.sleep(1)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Has conseguido una insignia que se mostrará en tu perfil de la página web, ¡sigue así!\n\nNos vemos en más retos 🤗"
		)
	else:
		dia_siguiente = resultado[0][0]
		diferencia_dias = int(dia_siguiente)-dia_reto

		if diferencia_dias == 1:
			text = "Tu reto continua mañana. ¡Te lo recordaré! ⏰⏰⏰"
			cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL 1 DAY);");
			resultado = cur.fetchall()
			fecha_recordatorio = fecha_recordatorio[0][0]
		else:
			cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL "+str(diferencia_dias)+" DAY);");
			resultado = cur.fetchall()
			fecha_recordatorio = resultado[0][0]
			fecha = fecha_recordatorio.strftime('%d-%B-%Y')
			text = "Tu reto continua el día "+fecha+". No te preocupes, yo te lo recordaré ⏰⏰⏰"

		ESP = tz.gettz('Europe/Madrid')
		dt = datetime(fecha_recordatorio.year,fecha_recordatorio.month,fecha_recordatorio.day,8,0,0, tzinfo=ESP)

		name_alarm=username_user+"_"+str(id_reto)
		context.job_queue.run_once(recordar_reto, dt, context=(query.message.chat_id, update, id_reto), name=name_alarm)

		alarma_descalificar = "descalificar_"+username_user+"_"+str(id_reto)
		for job in context.job_queue.get_jobs_by_name(alarma_descalificar):
			job.schedule_removal()

		bot.send_message(
			chat_id = query.message.chat_id,
			text=text
		)

	time.sleep(1.5)

	show_inicio_retos(update, context)

	current_state="INICIO_RETOS"
	return INICIO_RETOS

def inicio_retos_anotar_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡De acuerdo! Podrás anotarlo durante todo el día."
	)
	time.sleep(1.5)

	show_inicio_retos(update, context)

	current_state="INICIO_RETOS"
	return INICIO_RETOS

def show_inicio_retos_calendario(update, context):
	global current_state

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando calendario..."
	)
	time.sleep(.8)

	cur = db.cursor()
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto,Retos.fecha_inicio,Retos.nivel,Retos.id_ejercicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_actual = cur.fetchall();
	id_reto = reto_actual[0][0]
	fecha_inicio = reto_actual[0][1]
	nivel = reto_actual[0][2]
	id_ejercicio = reto_actual[0][3]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	ejercicio = cur.fetchall();
	ejercicio = ejercicio[0][0]

	dia_reto = date.today()-fecha_inicio
	dia_reto = dia_reto.days+1

	text="Reto de "+ejercicio.lower()+", nivel "+str(nivel)+", "+fecha_inicio.strftime("%B")

	nombre_imagen = str(id_reto)+"_"+username_user+"_"+str(dia_reto)
	path_imagen = "/home/jumacasni/Documentos/ImagymBot/retos/"+nombre_imagen+".png"

	cur.close()
	db.close()

	if not path.exists(path_imagen):
		createTableColors(id_reto,text,dia_reto,username_user,"")

	pic = open(path_imagen, 'rb')
	
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = pic
	)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text = "Aquí tienes una imagen del calendario de tu reto junto con tu progreso."
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos > Calendario de mi reto",
		reply_markup=reply_markup
	)

	current_state = "INICIO_RETOS_CALENDARIO"
	return INICIO_RETOS_CALENDARIO

def show_inicio_retos_descalificar(update, context):
	global current_state

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos > Descalificarme del reto..."
	)
	time.sleep(.8)

	cur = db.cursor()
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto,Retos.fecha_inicio,Retos.fecha_fin,Retos.id_ejercicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_actual = cur.fetchall();
	id_reto = reto_actual[0][0]
	fecha_inicio = reto_actual[0][1]
	fecha_fin = reto_actual[0][2]
	id_ejercicio = reto_actual[0][3]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	ejercicio = cur.fetchall();
	ejercicio = ejercicio[0][0]

	text="¿De verdad quieres descalificarte del <b>reto de "+ejercicio.lower()+" de "+fecha_inicio.strftime('%B')+"</b>? Una vez hecho esto, no podrás volver atrás."

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='inicio_retos_descalificar_si')],
		[InlineKeyboardButton("No ❌", callback_data='inicio_retos_descalificar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	current_state = "INICIO_RETOS_DESCALIFICAR_CONFIRMAR"
	return INICIO_RETOS_DESCALIFICAR_CONFIRMAR

def inicio_retos_descalificar_si(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Descalificando del reto..."
	)
	time.sleep(.8)

	cur = db.cursor()
	# Reto que ya ha empezado y el usuario está apuntado
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='R';")
	reto_usuario = cur.fetchall();
	id_reto = reto_usuario[0][0]

	cur.execute("UPDATE Realiza_reto SET estado='D' WHERE id_reto="+str(id_reto)+" AND id_usuario='"+username_user+"';")
	db.commit()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has sido descalificado del reto... ¡Espero verte en más retos!\n\nSuerte en la próxima 💪"
	)
	time.sleep(1)

	show_inicio_retos(update, context)

	current_state="INICIO_RETOS"
	return INICIO_RETOS

def inicio_retos_descalificar_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡Qué susto! No te has descalificado del reto.\n\n¡Mucho ánimo!"
	)
	time.sleep(1.5)

	show_inicio_retos(update, context)

	current_state="INICIO_RETOS"
	return INICIO_RETOS

def show_inicio_retos_historial(update, context):
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Cargando Inicio > Retos > Historial de retos... "
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_reto FROM Realiza_reto where id_usuario='"+username_user+"' AND estado='D' or estado='C';")
	resultado = cur.fetchall();

	list_keyboards = []

	for id_reto in resultado:
		cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
		resultado = cur.fetchall()
		id_ejercicio = resultado[0][0]
		nivel_ejercicio = resultado[0][1]
		start_day = resultado[0][2]

		cur.execute("SELECT estado FROM Realiza_reto WHERE id_reto="+str(id_reto[0])+" AND id_usuario='"+username_user+"' AND estado='D' or estado='C';")
		resultado = cur.fetchall();
		if resultado[0][0] == 'C':
			insignia = "🏆"
		else:
			insignia = "❌"

		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		ejercicio_name = cur.fetchall()
		ejercicio_name = ejercicio_name[0][0]

		name_button = "Reto de "+ejercicio_name.lower()+" | Nivel "+str(nivel_ejercicio)+" | "+start_day.strftime('%B-%Y').upper()+" | "+insignia
		button = InlineKeyboardButton(name_button, callback_data="inicio_retos_historial_"+str(id_reto[0]))

		callback_query_retos_historial = CallbackQueryHandler(historial_reto, pattern="inicio_retos_historial_"+str(id_reto[0]))
		
		if not callback_query_retos_historial in conv_handler.states[INICIO_RETOS_HISTORIAL]:
			conv_handler.states[INICIO_RETOS_HISTORIAL].append(callback_query_retos_historial)

		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)

	list_keyboards.append([InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí te muestro una lista de todos los retos a los que te has apuntado:\n\n🏆 Reto superado\n❌ Reto no superado"
	)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos > Historial",
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS_HISTORIAL"
	return INICIO_RETOS_HISTORIAL

def historial_reto(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',4)
	id_reto = id_reto[3]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando información de reto... "
	)
	time.sleep(.8)

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT dia,estado FROM Realiza_reto where id_usuario='"+username_user+"' AND id_reto="+str(id_reto)+";")
	resultado = cur.fetchall();
	dia = resultado[0][0]
	estado = resultado[0][1]

	cur.execute("SELECT id_ejercicio,nivel,fecha_inicio,fecha_fin FROM Retos WHERE id_reto="+str(id_reto)+";")
	resultado = cur.fetchall()
	id_ejercicio = resultado[0][0]
	nivel = resultado[0][1]
	fecha_inicio = resultado[0][2]
	fecha_fin = resultado[0][3]

	cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(id_ejercicio)+";")
	ejercicio = cur.fetchall();
	ejercicio = ejercicio[0][0]

	text="Reto de "+ejercicio.lower()+", nivel "+str(nivel)+", "+fecha_inicio.strftime("%B")

	nombre_imagen = str(id_reto)+"_"+username_user+"_historial"
	path_imagen = "/home/jumacasni/Documentos/ImagymBot/retos/"+nombre_imagen+".png"

	if not path.exists(path_imagen):
		createTableColors(id_reto,text,dia,username_user,nombre_imagen)

	pic = open(path_imagen, 'rb')
	bot.send_photo(
		chat_id = query.message.chat_id,
		photo = pic
	)
	time.sleep(1)

	cur.execute("SELECT COUNT(*) FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND estado='C';")
	resultado = cur.fetchall()
	n_personas_c = resultado[0][0]

	cur.execute("SELECT COUNT(*) FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND estado='R';")
	resultado = cur.fetchall()
	n_personas_r = resultado[0][0]

	cur.close()
	db.close()

	if estado == 'C':
		if n_personas_c == 1:
			bot.send_message(
				chat_id = query.message.chat_id,
				text = "¡Solo tú conseguiste completar este reto! ¡ENHORABUENA! 💪💪💪"
			)
		else:
			bot.send_message(
				chat_id = query.message.chat_id,
				text = "¡"+str(n_personas_c)+" usuarios conseguísteis completar este reto! ¡ENHORABUENA! 💪💪💪"
			)
	else:
		if n_personas_c == 0:
			if fecha_fin >= date.today() and n_personas_r != 0:
				bot.send_message(
					chat_id = query.message.chat_id,
					text = "Este reto aún no ha acabado. Aún participan "+str(n_personas_r)+" usuarios."
				)
			else:
				bot.send_message(
					chat_id = query.message.chat_id,
					text = "Nadie consiguió completar este reto... 😥"
				)
				bot.send_message(
					chat_id = query.message.chat_id,
					text = "Las casillas en verde son los días que superaste 💪"
				)
		else:
			bot.send_message(
				chat_id = query.message.chat_id,
				text = +str(n_personas_c)+" usuarios consiguieron completar este reto 🎉"
			)

	keyboard = [
		[InlineKeyboardButton("Volver a Historial de retos 🔙", callback_data='back_inicio_retos_historial')],
		[InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')],
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="👣 Inicio > Retos > Historial de retos > Reto seleccionado",
		reply_markup=reply_markup
	)

	current_state = "INICIO_RETOS_HISTORIAL_CLASIFICACION"
	return INICIO_RETOS_HISTORIAL_CLASIFICACION

def createTable(id_reto, name):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT dia,repeticiones FROM Calendario where id_reto="+str(id_reto)+";")
	resultado = cur.fetchall();
	cur.close()
	db.close()

	mitad_1 = round(len(resultado)/3)
	mitad_2 = round(2*len(resultado)/3)
	fin = len(resultado)

	# Primera mitad
	plt.title(name, y=1.05)
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []

	for i in range(mitad_1):
		day = 'Día ' + str(resultado[i][0])
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center left')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Segunda mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []

	for i in range(mitad_1, mitad_2):
		day = 'Día ' + str(resultado[i][0])
		repeticiones = str(resultado[i][1])
		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Tercera mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []

	for i in range(mitad_2, fin):
		day = 'Día ' + str(resultado[i][0])
		repeticiones = str(resultado[i][1])
		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center right')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	table_path = "/home/jumacasni/Documentos/ImagymBot/retos/"+str(id_reto)+".png"
	plt.savefig(table_path)

def createTableColors(id_reto, name, day_limit, id_usuario, name_graph):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT dia,repeticiones FROM Calendario where id_reto="+str(id_reto)+";")
	resultado = cur.fetchall();

	mitad_1 = round(len(resultado)/3)
	mitad_2 = round(2*len(resultado)/3)
	fin = len(resultado)

	cur.execute("SELECT fecha_inicio FROM Retos WHERE id_reto="+str(id_reto))
	fecha_inicio = cur.fetchall()
	fecha_inicio = fecha_inicio[0][0]

	# Primera mitad
	plt.title(name, y=1.05)
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []
	cell_colours = []

	for i in range(mitad_1):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0])
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('g')
			cell_colours.append(cell_color)
		else:
			cell_color = []
			cell_color.append('w')
			cell_colours.append(cell_color)

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center left')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Segunda mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []
	cell_colours = []

	for i in range(mitad_1, mitad_2):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0])
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('g')
			cell_colours.append(cell_color)
		else:
			cell_color = []
			cell_color.append('w')
			cell_colours.append(cell_color)

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Tercera mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	row_labels = []
	table_vals = []
	cell_colours = []

	for i in range(mitad_2, fin):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0])
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('g')
			cell_colours.append(cell_color)
		else:
			cell_color = []
			cell_color.append('w')
			cell_colours.append(cell_color)

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center right')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	if name_graph == "":
		name_graph = str(id_reto)+"_"+id_usuario+"_"+str(day_limit)

	table_path = "/home/jumacasni/Documentos/ImagymBot/retos/"+name_graph+".png"
	plt.savefig(table_path)

	cur.close()
	db.close()



def inicio_ficha(update, context):
	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	update.message.reply_text(
		text="⏳ Cargando Inicio > Mi ficha personal... "
	)

	# Obtener datos
	username_user = update.message.from_user.username

	cur = db.cursor()
	cur.execute("SELECT altura, fecha_nacimiento, genero, email FROM Usuarios where id_usuario='"+username_user+"';")
	resultado = cur.fetchall()

	altura = resultado[0][0]
	fecha_nacimiento = resultado[0][1]
	genero = resultado[0][2]
	email = resultado[0][3]

	if altura is None or not altura:
		altura = "✏"
	else:
		altura = str(altura) + " cm"

	if fecha_nacimiento is None or not fecha_nacimiento:
		fecha_nacimiento = "✏"
	else:
		fecha_nacimiento = fecha_nacimiento.strftime("%d-%b-%Y")

	if genero is None or not genero:
		genero = "✏"
	else:
		if genero == "m":
			genero = "👩"
		elif genero == "v":
			genero = "👨"
		elif genero == "o":
			genero = "otro"

	if email is None or not email:
		email = "✏"

	# Peso más reciente
	cur.execute("SELECT peso FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND peso IS NOT NULL)")
	resultado = cur.fetchall()

	if not resultado:
		peso = " ✏"
	else:
		if resultado[0][0] is None or not resultado[0][0]:
			peso = " ✏"
		else:
			peso = resultado[0][0]

	cur.close()
	db.close()

	time.sleep(.8)
	keyboard = [
		[InlineKeyboardButton("Peso: "+str(peso).rstrip('0').rstrip('. ')+"kg", callback_data='inicio_ficha_peso')],
		[InlineKeyboardButton("Altura: "+altura, callback_data='inicio_ficha_altura')],
		[InlineKeyboardButton("Fecha nacimiento: "+fecha_nacimiento, callback_data='inicio_ficha_nacimiento')],
		[InlineKeyboardButton("Género: "+genero, callback_data='inicio_ficha_genero')],
		[InlineKeyboardButton("Correo electrónico: "+email, callback_data='inicio_ficha_email')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]

	update.message.reply_text(
		text="Pulsa un botón para cambiar la información"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
		text="👣 Inicio > Mi ficha personal",
		reply_markup = reply_markup
	)

def inicio_peso(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	update.message.reply_text(
		text="⏳ Cargando Inicio > Mi objetivo de peso... "
	)

	# Peso más reciente
	username_user = update.message.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso,grasa,musculo,fecha,hora,imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
	resultado = cur.fetchall()

	time.sleep(.8)

	if not resultado:
		keyboard = [
			[InlineKeyboardButton("Anotar datos 📝", callback_data='inicio_peso_anotar')]
		]
		update.message.reply_text(			
			text="📌 Aún no tienes registrado ningún peso.\n\nPodrás establecer un objetivo de peso cuando anotes tu peso por primera vez."
		)

	else:
			peso = resultado[0][0]
			grasa = resultado[0][1]
			musculo = resultado[0][2]
			imc = resultado[0][5]
			fecha = resultado[0][3]

			if fecha == date.today():
				fecha = "hoy"
			else:
				fecha = fecha.strftime("%d-%b-%Y")

			text="📌 Última vez que anotaste datos: "+fecha
			if peso is not None:
				text=text+"\n\nPeso: "+str(peso).rstrip('0').rstrip('. ')+"kg"
			else:
				text=text+"\n\nPeso: sin datos"

			if grasa is not None:
				text=text+"\nGrasa: "+str(grasa).rstrip('0').rstrip('. ')+"%"
			else:
				text=text+"\nGrasa: sin datos"

			if musculo is not None:
				text=text+"\nMúsculo: "+str(musculo).rstrip('0').rstrip('. ')+"%"
			else:
				text=text+"\nMúsculo: sin datos"

			if imc is not None:
				text=text+"\nIMC: "+str(imc).rstrip('0').rstrip('. ')

			time.sleep(.8)
			update.message.reply_text(				
				text=text
			)

			cur.execute("SELECT tipo,objetivo,fecha_fin,fecha_inicio FROM Objetivo_peso WHERE id_usuario='"+username_user+"' AND fecha_fin>CURDATE();")
			resultado = cur.fetchall()

			keyboard = [
				[InlineKeyboardButton("Anotar datos 📝", callback_data='inicio_peso_anotar')]
			]

			if not resultado:
				keyboard.append([InlineKeyboardButton("Establecer objetivo 🏁", callback_data='inicio_peso_establecer')])
				keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])
				time.sleep(.8)
				update.message.reply_text(					
					text="📌 Actualmente no tienes ningún objetivo establecido."
				)
			else:
				tipo = resultado[0][0]
				peso_objetivo = resultado[0][1]
				fecha_fin = resultado[0][2]
				fecha_inicio = resultado[0][3]

				if tipo == "peso":
					medida = "kg"
				else:
					medida = "%"

				cur.execute("SELECT "+tipo+" FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND "+tipo+" IS NOT NULL);")
				resultado = cur.fetchall()
				peso = resultado[0][0]
				diferencia_peso = peso_objetivo - peso


				fecha_fin = fecha_fin.strftime("%d-%b-%Y")
				if fecha_inicio == date.today():
					fecha_inicio = "hoy"
				else:
					fecha_inicio = fecha_inicio.strftime("%d-%b-%Y")

				text="📌 Actualmente tienes un <b>objetivo de "+tipo+"</b>.\n\nÚltimo registro de "+tipo+": "+str(peso).rstrip('0').rstrip('. ')+medida+"\nTu objetivo: "+str(peso_objetivo).rstrip('0').rstrip('. ')+medida
				text=text+"\nTe queda: "+str(diferencia_peso).rstrip('0').rstrip('. ')+medida
				text=text+"\nFecha inicio: "+fecha_inicio+"\nFecha fin: "+fecha_fin

				keyboard.append([InlineKeyboardButton("Eliminar objetivo 🏁", callback_data='inicio_peso_eliminar')])
				keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])

				time.sleep(.8)
				update.message.reply_text(					
					text=text,
					parse_mode='HTML'
				)

	cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL")
	resultado = cur.fetchall()

	if resultado:
		keyboard.append([InlineKeyboardButton("Valoración del IMC 🗨", callback_data='inicio_peso_valoracion')])
		keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	else:
		keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	cur.close()
	db.close()

	time.sleep(.8)
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(		
		text="👣 Inicio > Mi objetivo de peso",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def inicio_peso_anotar(update, context):
	global current_state 

	db = pymysql.connect("localhost", "root", "password", "Imagym")
	db.begin()

	update.message.reply_text(
		text="⏳ Cargando Inicio > Mi objetivo de peso > Anotar datos... "
	)

	username_user = update.message.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso,grasa,musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
	resultado = cur.fetchall()

	time.sleep(.8)

	if not resultado:
		text="No has registrado ningún dato aún."
		update.message.reply_text(
			text=text
		)
		keyboard = [
			[InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')],
			[InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')],
			[InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
		]
	else:
		# Comprobar si ya hay datos registrados de hoy
		cur.execute("SELECT peso,grasa,musculo FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=CURDATE();")
		resultado = cur.fetchall()

		# Si no hay nada registrado hoy
		if not resultado:
			text="Hoy no has registrado nada aún."
			update.message.reply_text(
				text=text
			)
			keyboard = [
				[InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')],
				[InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')],
				[InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')],
				[InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')],
				[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
			]
		# Si ya hay algo registrado hoy
		else:
			keyboard = []
			text="Hoy ya has registrado lo siguiente:\n"

			if resultado[0][0] is not None:
				peso = resultado[0][0]
				text=text+"\nPeso: "+str(peso).rstrip('0').rstrip('. ')+"kg"
				keyboard.append([InlineKeyboardButton("Modificar peso", callback_data='inicio_peso_anotar_peso')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')])


			if resultado[0][1] is not None:
				grasa = resultado[0][1]
				text=text+"\nGrasa: "+str(grasa).rstrip('0').rstrip('. ')+"%"
				keyboard.append([InlineKeyboardButton("Modificar grasa", callback_data='inicio_peso_anotar_grasa')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')])

			if resultado[0][2] is not None:
				musculo = resultado[0][2]
				text=text+"\nMúsculo: "+str(musculo).rstrip('0').rstrip('. ')+"%"
				keyboard.append([InlineKeyboardButton("Modificar músculo", callback_data='inicio_peso_anotar_musculo')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar músculo ✏", callback_data='inicio_peso_anotar_musculo')])

			keyboard.append([InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')])
			keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

			update.message.reply_text(
				text=text
			)

	time.sleep(.8)
	update.message.reply_text(
		text="¿Qué quieres anotar?"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(.8)
	update.message.reply_text(
		text="👣 Inicio > Mi objetivo de peso > Anotar datos",
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR"
	return INICIO_PESO_ANOTAR


# def delete_messages(update, context):
# 	bot = context.bot
# 	query = update.callback_query
# 	for id_msg in messages:
# 		try:
# 			bot.delete_message(update.message.chat_id, id_msg)
# 		except:
# 			None
# 	for id_msg in messages:
# 		try:
# 			bot.delete_message(query.message.chat_id, id_msg)
# 		except:
# 			None
# 	messages.clear()

def error(update, context):
	"""Log Errors caused by Updates."""

	try:
		update.message.reply_text(
			text="¡Lo siento! No te he entendido. Puedes reiniciarme usando /start"
		)
	except:
		None

	try:
		query = update.callback_query
		bot = context.bot
		bot.send_message(
			chat_id=query.message.chat_id,
			text="¡Lo siento! Algo ha salido mal. Puedes reiniciarme usando /start"
		)
	except:
		None
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	global conv_handler

	updater = Updater('872358293:AAFUSbMbHl5SrInTVXlq67lbJRJnTp4WCJQ', use_context=True)

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message_start)],
		states={
			WELCOME: [CommandHandler('start', start),
					CommandHandler('mensaje', mandar_mensaje),
					MessageHandler(Filters.all, any_message)],

			WELCOME_PRESS_START: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, any_message),
								CallbackQueryHandler(show_inicio, pattern='start_menu')],

			INICIO: [CommandHandler('start', start),
					CommandHandler('mensaje', mandar_mensaje),
					MessageHandler(Filters.all, any_message),
					CallbackQueryHandler(show_inicio_peso, pattern='inicio_peso'),
					CallbackQueryHandler(show_inicio_cardio, pattern='inicio_cardio'),
					CallbackQueryHandler(show_inicio_retos, pattern='inicio_retos'),
					# CallbackQueryHandler(show_inicio_ejercicio, pattern='inicio_ejercicio'),
					# CallbackQueryHandler(show_inicio_rutinas, pattern='inicio_rutinas'),
					CallbackQueryHandler(show_inicio_ficha, pattern='inicio_ficha'),
					CallbackQueryHandler(show_inicio, pattern='show_inicio'),
					# CallbackQueryHandler(show_inicio_soporte, pattern='inicio_soporte'),
					],

			INICIO_FICHA: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(anotar_peso, pattern='inicio_ficha_peso'),
						CallbackQueryHandler(modify_altura, pattern='inicio_ficha_altura'),
						CallbackQueryHandler(modify_nacimiento, pattern='inicio_ficha_nacimiento'),
						CallbackQueryHandler(modify_genero, pattern='inicio_ficha_genero'),
						CallbackQueryHandler(modify_email, pattern='inicio_ficha_email'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_FICHA_PESO: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, check_anotar_peso),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_ALTURA: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, check_altura),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_NACIMIENTO: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_nacimiento),
									CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
									],

			INICIO_FICHA_GENERO: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, any_message),
								CallbackQueryHandler(check_genero_hombre, pattern='select_genero_hombre'),
								CallbackQueryHandler(check_genero_mujer, pattern='select_genero_mujer'),
								CallbackQueryHandler(check_genero_otro, pattern='select_genero_otro'),
								CallbackQueryHandler(check_genero_sin, pattern='select_genero_sin'),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_EMAIL: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, check_email),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_PESO: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_peso_anotar, pattern='inicio_peso_anotar'),
						CallbackQueryHandler(show_inicio_peso_establecer, pattern='inicio_peso_establecer'),
						CallbackQueryHandler(show_inicio_peso_eliminar, pattern='inicio_peso_eliminar'),
						CallbackQueryHandler(show_inicio_peso_evolucion, pattern='inicio_peso_evolucion'),
						CallbackQueryHandler(show_inicio_peso_valoracion, pattern='inicio_peso_valoracion'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ANOTAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(anotar_peso, pattern='inicio_peso_anotar_peso'),
						CallbackQueryHandler(anotar_grasa, pattern='inicio_peso_anotar_grasa'),
						CallbackQueryHandler(anotar_musculo, pattern='inicio_peso_anotar_musculo'),
						CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ANOTAR_PESO: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_anotar_peso),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ANOTAR_PESO_ALTURA: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_altura),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_FICHA_PESO_ALTURA: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_altura),
									CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
									],

			INICIO_PESO_ANOTAR_GRASA: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_anotar_grasa),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ANOTAR_MUSCULO: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_anotar_musculo),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ESTABLECER: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(objetivo_peso, pattern='inicio_peso_establecer_peso'),
						CallbackQueryHandler(objetivo_grasa, pattern='inicio_peso_establecer_grasa'),
						CallbackQueryHandler(objetivo_musculo, pattern='inicio_peso_establecer_musculo'),
						CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ESTABLECER_PESO: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_objetivo_peso),
									CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_PESO_TIEMPO: [CommandHandler('start', start),
												CommandHandler('mensaje', mandar_mensaje),
												MessageHandler(Filters.all, any_message),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_1'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_2'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_3'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_4'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_GRASA: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									MessageHandler(Filters.all, check_objetivo_grasa),
									CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_GRASA_TIEMPO: [CommandHandler('start', start),
												CommandHandler('mensaje', mandar_mensaje),
												MessageHandler(Filters.all, any_message),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_1'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_2'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_3'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_4'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_MUSCULO: [CommandHandler('start', start),
											CommandHandler('mensaje', mandar_mensaje),
											MessageHandler(Filters.all, check_objetivo_musculo),
											CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_MUSCULO_TIEMPO: [CommandHandler('start', start),
												CommandHandler('mensaje', mandar_mensaje),
												MessageHandler(Filters.all, any_message),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_1'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_2'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_3'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_4'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR: [CommandHandler('start', start),
														CommandHandler('mensaje', mandar_mensaje),
														MessageHandler(Filters.all, any_message),
														CallbackQueryHandler(objetivo_peso_tiempo_si, pattern='objetivo_peso_tiempo_si'),
														CallbackQueryHandler(objetivo_peso_tiempo_no, pattern='objetivo_peso_tiempo_no')
														],

			INICIO_PESO_ELIMINAR: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, any_message),
								CallbackQueryHandler(objetivo_peso_eliminar_si, pattern='objetivo_peso_eliminar_si'),
								CallbackQueryHandler(objetivo_peso_eliminar_no, pattern='objetivo_peso_eliminar_no')
								],

			INICIO_PESO_EVOLUCION: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								MessageHandler(Filters.all, any_message),
								CallbackQueryHandler(evolucion_peso, pattern='inicio_peso_evolucion_peso'),
								CallbackQueryHandler(evolucion_grasa, pattern='inicio_peso_evolucion_grasa'),
								CallbackQueryHandler(evolucion_musculo, pattern='inicio_peso_evolucion_musculo'),
								CallbackQueryHandler(evolucion_imc, pattern='inicio_peso_evolucion_imc'),
								CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso')
								],

			INICIO_PESO_EVOLUCION_PESO: [CommandHandler('start', start),
										CommandHandler('mensaje', mandar_mensaje),
										MessageHandler(Filters.all, any_message),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_peso_rango)
										],

			INICIO_PESO_EVOLUCION_GRASA: [CommandHandler('start', start),
										CommandHandler('mensaje', mandar_mensaje),
										MessageHandler(Filters.all, any_message),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_grasa_rango)
										],

			INICIO_PESO_EVOLUCION_MUSCULO: [CommandHandler('start', start),
										CommandHandler('mensaje', mandar_mensaje),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_musculo_rango),
										MessageHandler(Filters.all, any_message)
										],

			INICIO_PESO_EVOLUCION_IMC: [CommandHandler('start', start),
										CommandHandler('mensaje', mandar_mensaje),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_imc_rango),
										MessageHandler(Filters.all, any_message)
										],

			INICIO_PESO_VALORACION: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
								CallbackQueryHandler(show_inicio, pattern='back_inicio'),
								MessageHandler(Filters.all, any_message)
								],

			INICIO_CARDIO: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_cardio_registrar, pattern='inicio_cardio_registrar'),
						CallbackQueryHandler(show_inicio_cardio_ver, pattern='inicio_cardio_ver'),
						CallbackQueryHandler(show_inicio_cardio_establecer, pattern='inicio_cardio_establecer'),
						CallbackQueryHandler(show_inicio_cardio_eliminar, pattern='inicio_cardio_eliminar'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_REGISTRAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_REGISTRAR_ACTIVIDAD: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									CommandHandler("cardio", registrar_cardio),
									CallbackQueryHandler(show_inicio_cardio_registrar, pattern='back_inicio_cardio_registrar'),
									MessageHandler(Filters.all, any_message),
									],

			INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR: [CommandHandler('start', start),
														CommandHandler('mensaje', mandar_mensaje),
														CallbackQueryHandler(registrar_cardio_si, pattern='registrar_cardio_si'),
														CallbackQueryHandler(registrar_cardio_no, pattern='registrar_cardio_no'),
														MessageHandler(Filters.all, any_message),
														],

			INICIO_CARDIO_VER: [CommandHandler('start', start),
							CommandHandler('mensaje', mandar_mensaje),
							CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
							CallbackQueryHandler(show_inicio, pattern='back_inicio'),
							CommandHandler("rango", ver_cardio_rango),
							MessageHandler(Filters.all, any_message),
							],

			INICIO_CARDIO_ESTABLECER: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_ESTABLECER_ACTIVIDAD: [CommandHandler('start', start),
									CommandHandler('mensaje', mandar_mensaje),
									CommandHandler('minutos', establecer_cardio_minutos),
									CommandHandler('distancia', establecer_cardio_distancia),
									CommandHandler('calorias', establecer_cardio_calorias),
									CallbackQueryHandler(show_inicio_cardio_establecer, pattern='back_inicio_cardio_establecer'),
									MessageHandler(Filters.all, any_message),
									],

			INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR: [CommandHandler('start', start),
														CommandHandler('mensaje', mandar_mensaje),
														CallbackQueryHandler(establecer_cardio_si, pattern='establecer_cardio_si'),
														CallbackQueryHandler(establecer_cardio_no, pattern='establecer_cardio_no'),
														MessageHandler(Filters.all, any_message),
														],

			INICIO_CARDIO_ELIMINAR: [CommandHandler('start', start),
								CommandHandler('mensaje', mandar_mensaje),
								CallbackQueryHandler(objetivo_cardio_eliminar_si, pattern='objetivo_cardio_eliminar_si'),
								CallbackQueryHandler(objetivo_cardio_eliminar_no, pattern='objetivo_cardio_eliminar_no'),
								MessageHandler(Filters.all, any_message),
								],

			INICIO_RETOS: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos_ver, pattern='inicio_retos_ver'),
						CallbackQueryHandler(show_inicio_retos_eliminar, pattern='inicio_retos_eliminar'),
						CallbackQueryHandler(show_inicio_retos_anotar, pattern='inicio_retos_anotar'),
						CallbackQueryHandler(show_inicio_retos_calendario, pattern='inicio_retos_calendario'),
						CallbackQueryHandler(show_inicio_retos_descalificar, pattern='inicio_retos_descalificar'),
						CallbackQueryHandler(show_inicio_retos_historial, pattern='inicio_retos_historial'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_VER: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_VER_RETO: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos_ver, pattern='back_inicio_retos_ver'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ELIMINAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ELIMINAR_CONFIRMAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(eliminar_reto_confirmar_no, pattern='eliminar_reto_confirmar_no'),
						CallbackQueryHandler(show_inicio_retos_eliminar, pattern='back_inicio_retos_eliminar'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ANOTAR_CONFIRMAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(inicio_retos_anotar_si, pattern='inicio_retos_anotar_si'),
						CallbackQueryHandler(inicio_retos_anotar_no, pattern='inicio_retos_anotar_no'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_CALENDARIO: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_DESCALIFICAR_CONFIRMAR: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(inicio_retos_descalificar_si, pattern='inicio_retos_descalificar_si'),
						CallbackQueryHandler(inicio_retos_descalificar_no, pattern='inicio_retos_descalificar_no'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_HISTORIAL: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_HISTORIAL_CLASIFICACION: [CommandHandler('start', start),
						CommandHandler('mensaje', mandar_mensaje),
						MessageHandler(Filters.all, any_message),
						CallbackQueryHandler(show_inicio_retos_historial, pattern='back_inicio_retos_historial'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],


			# MENU: [MessageHandler(Filters.all, any_message_menu),
			# 		CallbackQueryHandler(show_menu_retos, pattern='show_menu_retos'),
			# 		MessageHandler(Filters.all, any_message),
			# 		CallbackQueryHandler(show_menu, pattern='go_back_menu')],

			# RETOS: [MessageHandler(Filters.all, any_message_menu),
			# 		CallbackQueryHandler(register_progress, pattern='register_progress'),
			# 		CallbackQueryHandler(user_realiza, pattern='user_realiza'),
			# 		CallbackQueryHandler(show_retos, pattern='show_retos'),
			# 		CallbackQueryHandler(show_menu_retos, pattern='show_menu_retos'),
			# 		CallbackQueryHandler(show_calendar_reto, pattern='show_calendar_reto'),
			# 		CallbackQueryHandler(show_menu_current_reto, pattern='current_reto'),
			# 		CallbackQueryHandler(delete_enroll_current_reto, pattern='delete_enroll_current_reto'),
			# 		CallbackQueryHandler(show_menu, pattern='go_back_menu')],

			# DELETE_CURRENT_RETO: [MessageHandler(Filters.regex('^(Si|No)$'), confirm_delete_current_reto),
			# 					CallbackQueryHandler(show_menu_current_reto, pattern='current_reto'),
			# 					CallbackQueryHandler(show_menu_retos, pattern='show_menu_retos'),
			# 					MessageHandler(Filters.all, any_message)],
			# WAITING_USERNAME: [CommandHandler("username", enter_username_login),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(register_window, pattern='register'),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# WAITING_PASSWORD: [CommandHandler("password", enter_password_login),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_USERNAME: [CommandHandler("reg_user", register_username),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_PASSWORD: [CommandHandler("reg_password", register_password),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_AGE: [CommandHandler("cumple", register_age),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_WEIGHT: [CommandHandler("peso", register_weight),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_HEIGHT: [CommandHandler("altura", register_height),
			# 					MessageHandler(Filters.all, any_message),
			# 					CallbackQueryHandler(goback_start, pattern='go_back')],

			# REGISTER_GENDER: [CallbackQueryHandler(register_gender, pattern='masculino'),
			# 					CallbackQueryHandler(register_gender, pattern='femenino'),
			# 					CallbackQueryHandler(goback_start, pattern='go_back'),
			# 					MessageHandler(Filters.all, any_message)],

			# CHOOSE: [CallbackQueryHandler(show_menu, pattern='go_menu'),
			# 			CallbackQueryHandler(goback_start, pattern='go_back'),
			# 			MessageHandler(Filters.all, any_message)],

			# MENU: [CallbackQueryHandler(goback_start, pattern='go_back'),
			# 		CallbackQueryHandler(add_weight, pattern='add_weight'),
			# 		CallbackQueryHandler(set_goal, pattern='set_goal'),
			# 		CallbackQueryHandler(show_IMC, pattern='show_IMC'),
			# 		CallbackQueryHandler(graph_weight, pattern='graph_weight'),
			# 		CallbackQueryHandler(show_perfil, pattern='go_perfil'),
			# 		CallbackQueryHandler(show_menu, pattern='go_menu'),
			# 		MessageHandler(Filters.all, any_message)],

			# MODIFY_WEIGHT: [CallbackQueryHandler(modify_weight, pattern='modify_weight'),
			# 				CallbackQueryHandler(show_menu, pattern='go_menu'),
			# 				MessageHandler(Filters.all, any_message)],

			# CONFIRM_MODIFY_WEIGHT: [CommandHandler("nuevo_peso", confirm_modify_weight),
			# 						MessageHandler(Filters.all, any_message),
			# 						CallbackQueryHandler(show_menu, pattern='go_menu')],

			# ADD_NEW_WEIGHT: [CommandHandler("nuevo_peso", add_new_weight),
			# 						MessageHandler(Filters.all, any_message),
			# 						CallbackQueryHandler(show_menu, pattern='go_menu')],

			# GRAPH_WEIGHT: [CommandHandler("rango", graph_weight_range),
			# 				MessageHandler(Filters.all, any_message),
			# 				CallbackQueryHandler(graph_weight, pattern='graph_weight'),
			# 				CallbackQueryHandler(show_menu, pattern='go_menu')],

			# PERFIL: [CallbackQueryHandler(delete_profile, pattern='delete_profile'),
			# 		CallbackQueryHandler(modify_height, pattern='modify_height'),
			# 		CallbackQueryHandler(show_menu, pattern='go_menu'),
			# 		MessageHandler(Filters.all, any_message)],

			# CONFIRM_DELETE_PROFILE: [CommandHandler("eliminar_perfil", confirm_delete_profile),
			# 						CallbackQueryHandler(show_perfil, pattern='go_perfil'),
			# 						CallbackQueryHandler(goback_start, pattern='go_back'),
			# 						MessageHandler(Filters.all, any_message)],

			# CONFIRM_MODIFY_HEIGHT: [CommandHandler("nueva_altura", confirm_modify_height),
			# 						MessageHandler(Filters.all, any_message),
			# 						CallbackQueryHandler(show_perfil, pattern='go_perfil')],

			# SET_GOAL: [CommandHandler("objetivo", set_goal_deadline),
			# 			MessageHandler(Filters.all, any_message),
			# 			CallbackQueryHandler(show_menu, pattern='go_menu')],

			# SET_GOAL_DEADLINE: [CallbackQueryHandler(show_goal, pattern='1 semana'),
			# 					CallbackQueryHandler(show_goal, pattern='2 semanas'),
			# 					CallbackQueryHandler(show_goal, pattern='3 semanas'),
			# 					CallbackQueryHandler(show_goal, pattern='1 mes'),
			# 					CallbackQueryHandler(show_goal, pattern='2 meses'),
			# 					CallbackQueryHandler(show_goal, pattern='3 meses'),
			# 					CallbackQueryHandler(show_goal, pattern='6 meses'),
			# 					CallbackQueryHandler(show_goal, pattern='1 año'),
			# 					CallbackQueryHandler(confirm_goal, pattern='confirm_goal'),
			# 					CallbackQueryHandler(set_goal, pattern='set_goal'),
			# 					CallbackQueryHandler(show_menu, pattern='go_menu')],

			# MODIFY_GOAL: [CommandHandler("objetivo", set_goal_deadline),
			# 			CallbackQueryHandler(modify_goal, pattern='modify_goal'),
			# 			CallbackQueryHandler(ask_delete_goal, pattern='delete_goal'),
			# 			MessageHandler(Filters.all, any_message),
			# 			CallbackQueryHandler(show_menu, pattern='go_menu')],

			# CONFIRM_DELETE_GOAL: [CallbackQueryHandler(delete_goal, pattern='delete_goal'),
			# 						CallbackQueryHandler(set_goal, pattern='keep_goal'),
			# 						CallbackQueryHandler(show_menu, pattern='go_menu'),
			# 						MessageHandler(Filters.all, any_message)],
		},
		fallbacks=[CommandHandler('start',start)]
	)
	updater.dispatcher.add_handler(conv_handler)
	updater.dispatcher.add_error_handler(error)

	# Start the Bot
	updater.start_polling()#allowed_updates=[])

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


def randomPassword(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False


def is_float(s):
	try: 
		float(s)
		return True
	except ValueError:
		return False


def is_valid_date(date):
	try:
		datetime.strptime(date, '%d-%m-%Y')
		return True
	except ValueError:
		return False


def calculate_age(birthday):
	today = date.today() 
	age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day)) 
  
	return age


if __name__ == '__main__':
    main()