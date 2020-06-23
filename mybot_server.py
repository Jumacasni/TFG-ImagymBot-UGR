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
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

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
INICIO_PESO_EVOLUCION_PESO, INICIO_FICHA_VALORACION, INICIO_PESO_EVOLUCION_GRASA, INICIO_PESO_EVOLUCION_MUSCULO,\
INICIO_PESO_EVOLUCION_IMC, INICIO_CARDIO, INICIO_CARDIO_REGISTRAR, INICIO_CARDIO_REGISTRAR_ACTIVIDAD,\
INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR, INICIO_CARDIO_VER, INICIO_CARDIO_ESTABLECER, INICIO_CARDIO_ESTABLECER_ACTIVIDAD,\
INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR, INICIO_CARDIO_ELIMINAR, INICIO_FICHA_PESO, INICIO_RETOS,\
INICIO_PESO_ANOTAR_PESO_ALTURA, INICIO_FICHA_PESO_ALTURA, INICIO_RETOS_VER, INICIO_RETOS_VER_RETO,\
INICIO_RETOS_ELIMINAR, INICIO_RETOS_ELIMINAR_CONFIRMAR, INICIO_RETOS_ANOTAR_CONFIRMAR, INICIO_RETOS_CALENDARIO,\
INICIO_RETOS_DESCALIFICAR, INICIO_RETOS_DESCALIFICAR_CONFIRMAR, INICIO_RETOS_HISTORIAL, INICIO_RETOS_HISTORIAL_CLASIFICACION,\
INICIO_RUTINAS, INICIO_EJERCICIO, INICIO_SOPORTE, INICIO_EJERCICIO_REGISTRAR, INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD,\
INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR, INICIO_EJERCICIO_RANKING, INICIO_EJERCICIO_DESCALIFICAR_CONFIRMAR,\
INICIO_EJERCICIO_ELIMINAR_CONFIRMAR, INICIO_EJERCICIO_HISTORIAL, INICIO_EJERCICIO_HISTORIAL_CLASIFICACION,\
INICIO_RUTINAS_VER, INICIO_RUTINAS_VER_RUTINA, INICIO_RUTINAS_ANOTAR, INICIO_RUTINAS_ANOTAR_RUTINA, INICIO_RUTINAS_CONSULTAR,\
INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO, INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO = range(69)

db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")

global current_state, conv_handler, updater

############# INICIO #############
def start(update, context):
	global current_state

	name_user = update.message.from_user.first_name
	username_user = update.message.from_user.username

	if username_user is None:
		update.message.reply_text(
			text="¡Bienvenido/a a Imagym! Parece que no tienes un usuario/alias de Telegram. Ve a ajustes, ponte un nombre de usuario y podremos empezar!!"
		)
	else:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT id_usuario FROM Usuarios where id_usuario='"+username_user+"';")
		resultado = cur.fetchall()
		cur.close()
		db.close()

		if not resultado:
			update.message.reply_text(
				text="¡Bienvenido/a a Imagym! Soy un divulgador de gimnasios y mi objetivo es fortalecer la comunidad de un gimnasio. Introduce la contraseña de tu gimnasio para hablar conmigo 😃")

			# Le decimos al bot que estamos en el estado WELCOME
			current_state = 'WELCOME'
			return WELCOME

		else:
			update.message.reply_text(
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="<b>⏳ Cargando inicio...</b>",
		parse_mode='HTML'
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
		text="<b>👣 Inicio</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO"
	return INICIO

def usuario_pulsa_boton_anterior(update, context):
	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>🚫 No puedes pulsar un botón de un menú anterior 🚫</b>",
		parse_mode='HTML'
	)

def usuario_usa_comando_anterior(update, context):
	update.message.reply_text(
		text="<b>🚫 No puedes usar ese comando en este momento 🚫</b>",
		parse_mode='HTML'
	)

############# MI FICHA PERSONAL #############
def show_inicio_ficha(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Obtener datos
	query = update.callback_query
	username_user = query.from_user.username
	bot = context.bot

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Mi ficha personal...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	# IMC más reciente
	cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL)")
	imc = cur.fetchall()
	text="Pulsa un botón para cambiar la información"

	if imc:
		imc = imc[0][0]
		text=text+"\n\n<b>👉Tu IMC actual:</b> "+str(imc)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

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
			peso = str(resultado[0][0])+"kg 👉 "
			fecha = resultado[0][1]
			if fecha == date.today():
				fecha = "Registrado hoy"
			else:
				fecha = "Registrado el día "+fecha.strftime("%d-%B-%Y")

	cur.close()
	db.close()

	keyboard = [
		[InlineKeyboardButton("Peso: "+peso+fecha, callback_data='inicio_ficha_peso')],
		[InlineKeyboardButton("Altura: "+altura, callback_data='inicio_ficha_altura')],
		[InlineKeyboardButton("Fecha nacimiento: "+fecha_nacimiento, callback_data='inicio_ficha_nacimiento')],
		[InlineKeyboardButton("Género: "+genero, callback_data='inicio_ficha_genero')],
		[InlineKeyboardButton("Correo electrónico: "+email, callback_data='inicio_ficha_email')]
	]

	if imc:
		keyboard.append([InlineKeyboardButton("Valoración del IMC 🗨", callback_data='inicio_ficha_valoracion')])

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Mi ficha personal</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_FICHA"
	return INICIO_FICHA

def modify_altura(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
						text="¡Genial! Puedes comprobar tu IMC desde <b>👣 Inicio > Mi ficha personal</b>",
						parse_mode='HTML'
					)

					inicio_peso_anotar(update, context)

					current_state = "INICIO_PESO_ANOTAR"
					return INICIO_PESO_ANOTAR

				elif current_state == "INICIO_FICHA_PESO_ALTURA":
					update.message.reply_text(
						text="¡Genial! Puedes comprobar tu IMC desde <b>👣 Inicio > Mi ficha personal</b>",
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

def show_inicio_ficha_valoracion(update, context):
	global current_state
	query = update.callback_query
	bot = context.bot

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	image_path = "/home/castinievas/ImagymBot/imagenes/IMC.jpg"

	keyboard = [
		[InlineKeyboardButton("Volver a Mi ficha personal 🔙", callback_data='back_inicio_ficha')],
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

	current_state = "INICIO_FICHA_VALORACION"
	return INICIO_FICHA_VALORACION

############# MI OBJETIVO DE PESO #############
def show_inicio_peso(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username
	cur = db.cursor()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	# Peso más reciente
	cur.execute("SELECT peso,grasa,musculo,fecha,hora FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
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
		fecha = resultado[0][3]

		if fecha == date.today():
			fecha = "HOY"
		else:
			fecha = fecha.strftime("%d-%B-%Y").upper()

		text="📌 <b>ÚLTIMA VEZ QUE ANOTASTE DATOS: "+fecha+"</b>"
		if peso is not None:
			text=text+"\n\n<b>👉 Peso:</b> "+str(peso)+"kg"
		else:
			text=text+"\n\n<b>👉 Peso:</b> sin datos"

		if grasa is not None:
			text=text+"\n<b>👉 Grasa:</b> "+str(grasa)+"%"
		else:
			text=text+"\n<b>👉 Grasa:</b> sin datos"

		if musculo is not None:
			text=text+"\n<b>👉 Músculo:</b> "+str(musculo)+"%"
		else:
			text=text+"\n<b>👉 Músculo:</b> sin datos"

		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			parse_mode='HTML'
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

			text="📌 ACTUALMENTE TIENES UN <b>OBJETIVO DE "+tipo.upper()+"</b>.\n\n👉 <b>Último registro de "+tipo+":</b> "+str(peso)+medida+"\n<b>👉 Tu objetivo:</b> "+str(peso_objetivo)+medida
			text=text+"\n👉 <b>Te queda:</b> "+str(diferencia_peso)+medida
			text=text+"\n👉 <b>Fecha inicio:</b> "+fecha_inicio+"\n👉 <b>Fecha fin:</b> "+fecha_fin

			keyboard.append([InlineKeyboardButton("Eliminar objetivo 🏁", callback_data='inicio_peso_eliminar')])
			keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])

			time.sleep(.8)
			bot.send_message(
				chat_id = query.message.chat_id,
				text=text,
				parse_mode='HTML'
			)
		keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

		cur.close()
		db.close()

		time.sleep(.8)
		reply_markup = InlineKeyboardMarkup(keyboard)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="<b>👣 Inicio > Mi objetivo de peso</b>",
			parse_mode='HTML',
			reply_markup = reply_markup
		)

		current_state = "INICIO_PESO"
		return INICIO_PESO

def show_inicio_peso_anotar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso > Anotar datos...</b>",
		parse_mode='HTML'
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
				text=text+"\nPeso: "+str(peso)+"kg"
				keyboard.append([InlineKeyboardButton("Modificar peso", callback_data='inicio_peso_anotar_peso')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')])


			if resultado[0][1] is not None:
				grasa = resultado[0][1]
				text=text+"\nGrasa: "+str(grasa)+"%"
				keyboard.append([InlineKeyboardButton("Modificar grasa", callback_data='inicio_peso_anotar_grasa')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')])

			if resultado[0][2] is not None:
				musculo = resultado[0][2]
				text=text+"\nMúsculo: "+str(musculo)+"%"
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
		text="<b>👣 Inicio > Mi objetivo de peso > Anotar datos</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR"
	return INICIO_PESO_ANOTAR

def anotar_peso(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
			text="Vas a modificar tu peso de hoy: "+str(hay_peso[0][0])+"kg\n\n¿Cuál es tu peso de hoy (en kg)?"
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
						text="¡Es momento de registrar tu altura! Con tu altura podré calcular tu IMC y podré valorarlo desde el menú 👣 <b>Inicio > Mi ficha personal</b>",
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
						text="¿Quieres registrar tu altura? Con tu altura podré calcular tu IMC y podré valorarlo desde el menú 👣 <b>Inicio > Mi ficha personal</b>",
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nPesas <b>"+str(diferencia_peso)+"kg más</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2))+" kg el día "+fecha,
								parse_mode = 'HTML'
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nPesas <b>"+str(diferencia_peso)+"kg menos</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2))+" kg el día "+fecha,
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nPesas <b>"+str(diferencia_peso)+"kg menos</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2))+" kg el día "+fecha,
								parse_mode = 'HTML'
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nPesas <b>"+str(diferencia_peso)+"kg más</b> que la última vez.\n\nÚltima vez: "+str(round(peso_ultimo,2))+" kg el día "+fecha,
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso)+"% más que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso)+"% menos que la última vez"
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso)+"% menos que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso)+"% más que la última vez"
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso)+"% más que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso)+"% menos que la última vez"
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
								text="Has avanzado en tu objetivo. ¡GENIAL!\n\nTienes un "+str(diferencia_peso)+"% menos que la última vez"
							)
						else:
							time.sleep(.8)
							update.message.reply_text(
								text="No has avanzado en tu objetivo. ¡NO TE RINDAS!\n\nTienes un "+str(diferencia_peso)+"% más que la última vez"
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso > Establecer objetivo...</b>",
		parse_mode='HTML'
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

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Selecciona un tipo de objetivo"
	)

	cur.close()
	db.close()
	# Si no hay nada registrado
	keyboard = []
	if hay_peso:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de peso", callback_data='inicio_peso_establecer_peso')])
	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Para establecer un objetivo de peso, debes anotar por primera vez tu peso"
		)
	if hay_grasa:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de grasa", callback_data='inicio_peso_establecer_grasa')])
	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Para establecer un objetivo de grasa, debes anotar por primera vez tu grasa"
		)

	if hay_musculo:
		keyboard.append([InlineKeyboardButton("Establecer objetivo de músculo", callback_data='inicio_peso_establecer_musculo')])
	else:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="Para establecer un objetivo de grasa, debes anotar por primera vez la grasa"
		)

	if not hay_peso or not hay_grasa or not hay_musculo:
		keyboard.append([InlineKeyboardButton("Ir a Anotar datos ✏", callback_data='inicio_peso_anotar')])

	keyboard.append([InlineKeyboardButton("Volver a Peso 🔙", callback_data='back_inicio_peso')])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	

	time.sleep(.8)
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Mi objetivo de peso > Establecer objetivo</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ESTABLECER"
	return INICIO_PESO_ESTABLECER

def objetivo_peso(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="Tu último peso registrado es: "+str(peso)+"kg"
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
						text="Tu objetivo es de "+str(diferencia_peso)+"kg más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso))+"kg menos que actualmente."
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	text = "RESUMEN DEL OBJETIVO:\n\n<b>Peso objetivo:</b>  "+str(peso)+"kg\n<b>Diferencia de peso:</b>  "+diferencia+"kg\n<b>Fecha fin:</b> "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="Tu último porcentaje de grasa registrado es: "+str(peso)+"%"
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
						text="Tu objetivo es de "+str(diferencia_peso)+"% más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso))+"% menos que actualmente."
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	text = "RESUMEN DEL OBJETIVO:\n\n<b>Porcentaje de grasa objetivo:</b>  "+str(peso)+"%\n<b>Diferencia de porcentaje:</b>  "+diferencia+"%\n<b>Fecha fin:</b>  "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="Tu último porcentaje de músculo registrado es: "+str(peso)+"%"
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
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
						text="Tu objetivo es de "+str(diferencia_peso)+"% más que actualmente."
					)
				else:
					time.sleep(.8)
					update.message.reply_text(
						text="Tu objetivo es de "+str(abs(diferencia_peso))+"% menos que actualmente."
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	text = "RESUMEN DEL OBJETIVO:\n\n<b>Porcentaje de músculo objetivo:</b> "+str(peso)+"%\n<b>Diferencia de porcentaje:</b> "+diferencia+"%\n<b>Fecha fin:</b> "+fecha
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso > Evolución...</b>",
		parse_mode='HTML'
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
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Mi objetivo de peso > Evolución</b>",
		parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/castinievas/ImagymBot/evolucion/peso/"+image_name_plot

	# image_name_bar = current_user+"_"+current_date[0][0]+"_"+current_time[0][0]+"_bar.png"
	# image_path_bar = "/home/castinievas/ingenieria_informatica/curso1920/TFG/graphs/"+image_name_bar

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
		text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso</b>",
		parse_mode='HTML',
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/castinievas/ImagymBot/evolucion/peso/"+image_name_plot

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
					text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso</b>",
					parse_mode='HTML',
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

					db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/castinievas/ImagymBot/evolucion/peso/"+image_name_plot

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
						text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de peso</b>",
						parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/castinievas/ImagymBot/evolucion/grasa/"+image_name_plot

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
		text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa</b>",
		parse_mode='HTML',
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/castinievas/ImagymBot/evolucion/grasa/"+image_name_plot

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
					text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa</b>",
					parse_mode='HTML',
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

					db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/castinievas/ImagymBot/evolucion/peso/"+image_name_plot

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
						text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de grasa</b>",
						parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/castinievas/ImagymBot/evolucion/musculo/"+image_name_plot

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
		text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo</b>",
		parse_mode='HTML',
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/castinievas/ImagymBot/evolucion/IMC/"+image_name_plot

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
					text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo</b>",
					parse_mode='HTML',
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

					db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/castinievas/ImagymBot/evolucion/IMC/"+image_name_plot

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
						text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo</b>",
						parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
	cur = db.cursor()
	cur.execute("SELECT CURDATE();")
	current_date = cur.fetchall()
	cur.execute("SELECT CURTIME();")
	current_time = cur.fetchall()

	image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
	image_path_plot = "/home/castinievas/ImagymBot/evolucion/IMC/"+image_name_plot

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
		text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de IMC</b>",
		parse_mode='HTML',
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
				cur = db.cursor()
				cur.execute("SELECT CURDATE();")
				current_date = cur.fetchall()
				cur.execute("SELECT CURTIME();")
				current_time = cur.fetchall()

				image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
				image_path_plot = "/home/castinievas/ImagymBot/evolucion/musculo/"+image_name_plot

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
					text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de IMC</b>",
					parse_mode='HTML',
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

					db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
					db.begin()
					# El nombre de la imagen será del formato: username_currentdate_currenttime_[plot/bar].png
					cur = db.cursor()
					cur.execute("SELECT CURDATE();")
					current_date = cur.fetchall()
					cur.execute("SELECT CURTIME();")
					current_time = cur.fetchall()

					image_name_plot = username+"_"+str(current_date[0][0])+"_"+str(current_time[0][0])+"_plot.png"
					image_path_plot = "/home/castinievas/ImagymBot/evolucion/musculo/"+image_name_plot

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
						text="<b>👣 Inicio > Mi objetivo de peso > Evolución > Evolución de músculo</b>",
						parse_mode='HTML',
						reply_markup=reply_markup
					)
		else:
			update.message.reply_text(
				text="No has introducido dos fechas. Recuerda usar el formato dd-mm-yyyy."
			)

############# MI OBJETIVO DE ACTIVIDADES CARDIO #############
def show_inicio_cardio(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Actividades cardio...</b>",
		parse_mode='HTML'
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
			text=text+"\n<b>Objetivo:</b> "+objetivo_numero+" "+tipo
		elif objetivo_tipo == "calorias":
			tipo = "calorías"
			text=text+"\n<b>Objetivo:</b> "+objetivo_numero+" "+tipo
		else:
			objetivo_tipo = "tiempo"
			tipo = "minutos"
			text=text+"\n<b>Objetivo:</b> "+objetivo_numero+" "+tipo


		if fecha_inicio == date.today():
			fecha_inicio = "hoy"
		else:
			fecha_inicio = fecha_inicio.strftime("%d-%b-%Y")

		text=text+"\n<b>Fecha inicio:</b> "+str(fecha_inicio)
		text=text+"\n<b>Fecha fin:</b> "+fecha_fin.strftime("%d-%b-%Y")
		text=text+"\n\n"

		cur.execute("SELECT SUM("+objetivo_tipo+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+username_user+"' AND fecha>='"+str(resultado[0][2])+"' AND fecha<='"+str(resultado[0][3])+"';")
		resultado = cur.fetchall()

		if resultado[0][0] is None:
			text=text+"Aún no has acumulado "+tipo+". ¡Registra cardio en <b>"+nombre.lower()+"</b> para comenzar tu marcador!"
		else:
			diferencia = round(float(objetivo_numero) - float(resultado[0][0]), 0)
			if diferencia > 0:
				text=text+"Llevas ya <b>"+str(resultado[0][0])+" "+tipo+"</b>."
				text=text+"\nTe quedan: "+str(diferencia)+" "+tipo
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
		text="<b>👣 Inicio > Actividades cardio</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_CARDIO"
	return INICIO_CARDIO

def show_inicio_cardio_registrar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	print(current_state)
	if current_state == "INICIO_EJERCICIO" or current_state == "INICIO_EJERCICIO_REGISTRAR" or current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD":
		bot.send_message(
			chat_id = query.message.chat_id,
			text="<b>⏳ Cargando Inicio > Ejercicio del mes > Registrar cardio...</b>",
			parse_mode='HTML'
		)
	elif current_state == "INICIO_CARDIO" or current_state == "INICIO_CARDIO_REGISTRAR" or current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD":
		bot.send_message(
			chat_id = query.message.chat_id,
			text="<b>⏳ Cargando Inicio > Actividades cardio > Registrar cardio...</b>",
			parse_mode='HTML'
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

			if callback_query in conv_handler.states[INICIO_EJERCICIO_REGISTRAR]:
				pass
			else:
				conv_handler.states[INICIO_EJERCICIO_REGISTRAR].append(callback_query)

	if current_state == "INICIO_EJERCICIO" or current_state == "INICIO_EJERCICIO_REGISTRAR" or current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD":
		keyboard.append([InlineKeyboardButton("Volver a Ejercicio del mes 🔙", callback_data='back_inicio_ejercicio')])
		
	elif current_state == "INICIO_CARDIO" or current_state == "INICIO_CARDIO_REGISTRAR" or current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD":
		keyboard.append([InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')])

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	cur.close()
	db.close()

	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="¿Qué actividad quieres registrar?"
	)

	if current_state == "INICIO_EJERCICIO" or current_state == "INICIO_EJERCICIO_REGISTRAR" or current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD":
		reply_markup = InlineKeyboardMarkup(keyboard)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="<b>👣 Inicio > Ejercicio del mes > Registrar cardio</b>",
			parse_mode='HTML',
			reply_markup = reply_markup
		)

		current_state = "INICIO_EJERCICIO_REGISTRAR"
		return INICIO_EJERCICIO_REGISTRAR

	elif current_state == "INICIO_CARDIO" or current_state == "INICIO_CARDIO_REGISTRAR" or current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD":
		reply_markup = InlineKeyboardMarkup(keyboard)
		time.sleep(.8)
		bot.send_message(
			chat_id = query.message.chat_id,
			text="<b>👣 Inicio > Actividades cardio > Registrar cardio</b>",
			parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	if current_state == "INICIO_CARDIO_REGISTRAR":
		current_state = "INICIO_CARDIO_REGISTRAR_ACTIVIDAD"
		return INICIO_CARDIO_REGISTRAR_ACTIVIDAD

	elif current_state == "INICIO_EJERCICIO_REGISTRAR":
		current_state = "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD"
		return INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD

def registrar_cardio(update, context):
	global current_state

	n_params = context.args

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
				text=text+"\n<b>Actividad cardio:</b> "+nombre
				if minutos != 0:
					text=text+"\n<b>Minutos:</b> "+str(minutos)
					cur.execute("UPDATE Registra_cardio SET tiempo="+str(minutos)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\n<b>Minutos: sin datos</b>"
				if kilometros != 0:
					text=text+"\n<b>Distancia:</b> "+str(kilometros)+"km"
					cur.execute("UPDATE Registra_cardio SET distancia="+str(kilometros)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\n<b>Distancia: sin datos</b>"
				if nivel != 0:
					text=text+"\n<b>Nivel:</b> "+str(nivel)
					cur.execute("UPDATE Registra_cardio SET nivel="+str(nivel)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\n<b>Nivel/Inclinación:</b> sin datos"
				if calorias != 0:
					text=text+"\n<b>Calorías:</b> "+str(calorias)
					cur.execute("UPDATE Registra_cardio SET calorias="+str(calorias)+" WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"'")
					db.commit()
				else:
					text=text+"\n<b>Calorías:</b> sin datos"

				resultado = cur.fetchall()

				keyboard = [
					[InlineKeyboardButton("Si ✔", callback_data='registrar_cardio_si')],
					[InlineKeyboardButton("No ❌", callback_data='registrar_cardio_no')]
				]
				update.message.reply_text(
					text=text,
					parse_mode='HTML'
				)

				# Si tiene un objetivo personal
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
								text=text+str(kilometros)+" kilómetros</b>"
								text=text+" a tu objetivo en <b>"+nombre.lower()+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						elif objetivo_tipo == "calorias":
							if calorias != 0:
								text=text+str(calorias)+" calorías</b>"
								text=text+" a tu objetivo en <b>"+nombre.lower()+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						else:
							if minutos != 0:
								text=text+str(minutos)+" minutos</b>"
								text=text+" a tu objetivo en <b>"+nombre.lower()+"</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)

				# Si tiene un ejercicio del mes
				cur.execute("SELECT id_objetivo_mensual FROM Se_apunta WHERE id_usuario='"+username+"' AND estado='R';")
				resultado = cur.fetchall()
				if resultado:
					id_objetivo_mensual = resultado[0][0]
					cur.execute("SELECT id_actividad_cardio,objetivo FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
					resultado = cur.fetchall()
					id_actividad_cardio_objetivo_mensual = resultado[0][0]
					objetivo = resultado[0][1]
					if id_actividad_cardio_objetivo_mensual == id_actividad_cardio:
						objetivo_numero = objetivo.split(' ',2)[0]
						objetivo_tipo = objetivo.split(' ',2)[1]

						text="\n\nAñadirás <b>"
						if objetivo_tipo == "distancia":
							if kilometros != 0:
								text=text+str(kilometros)+" kilómetros</b>"
								text=text+" al <b>ejercicio del mes</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						elif objetivo_tipo == "calorias":
							if calorias != 0:
								text=text+str(calorias)+" calorías</b>"
								text=text+" al <b>ejercicio del mes</b>"
								time.sleep(.8)
								update.message.reply_text(
									text=text,
									parse_mode='HTML'
								)
						else:
							if minutos != 0:
								text=text+str(minutos)+" minutos</b>"
								text=text+" al <b>ejercicio del mes</b>"
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

						if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD":
							current_state = "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO"
							return INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO

						elif current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD":
							current_state = "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO"
							return INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO


				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="¿Confirmas este registro?",
					reply_markup = reply_markup
				)

				if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD":
					current_state = "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR"
					return INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR

				elif current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD":
					current_state = "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR"
					return INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR

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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Todas las actividades cardio del último día que hizo cardio
	cur.execute("SELECT id_actividad_cardio,TIME(fecha),DATE(fecha),tiempo,distancia,nivel,calorias FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND DATE(fecha)=(SELECT MAX(DATE(fecha)) FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND (aprobada!='N' OR aprobada IS NULL));")
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
			text=text+str(resultado[i][4])+" kilómetros; "
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
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has registrado la actividad cardio con éxito ✔",
	)
	if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO" or current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO":
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		# Seleccionar actividad del ejercicio del mes
		cur.execute("SELECT Ejercicio_del_mes.id_actividad_cardio FROM Ejercicio_del_mes INNER JOIN Se_apunta WHERE Ejercicio_del_mes.id_objetivo_mensual=Se_apunta.id_objetivo_mensual AND Se_apunta.id_usuario='"+username_user+"' AND Se_apunta.estado='R';")
		resultado = cur.fetchall()
		if resultado:
			id_actividad_cardio = resultado[0][0]
			cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
			resultado = cur.fetchall()
			nombre = resultado[0][0]

			bot.send_message(
				chat_id = query.message.chat_id,
				text="Envíame una foto de <b>"+nombre+"</b> en la que se pueda ver y confirmar tu registro de cardio. Tu marcador del ejercicio del mes se actualizará cuando se apruebe.",
				parse_mode='HTML'
			)

			return

	time.sleep(1)

	if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR":
		current_state = "INICIO_CARDIO_REGISTRAR"
		show_inicio_cardio_registrar(update, context)

		return INICIO_CARDIO_REGISTRAR

	elif current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR":
		current_state = "INICIO_EJERCICIO"
		show_inicio_ejercicio(update, context)

		return INICIO_EJERCICIO

def registrar_cardio_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username = query.from_user.username

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR" or current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO":
		current_state = "INICIO_CARDIO_REGISTRAR"
		show_inicio_cardio_registrar(update, context)

		return INICIO_CARDIO_REGISTRAR

	elif current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR" or current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO":
		current_state = "INICIO_EJERCICIO"
		show_inicio_ejercicio(update, context)

		return INICIO_EJERCICIO

def ver_cardio_rango(update, context):
	global current_state
	username = update.message.from_user.username

	n_params = context.args

	keyboard = [[InlineKeyboardButton("Volver a Actividad cardio 🔙", callback_data='back_inicio_cardio')]]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo 1: /consultar 01-01-2019 01-12-2019\nEjemplo 2: /consultar 01-01-2019",
			reply_markup=reply_markup
		)
	else:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy. Prueba el comando /consultar de nuevo.",
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
							text=text+str(resultado[i][4])+" kilómetros; "
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Actividades cardio > Establecer objetivo...</b>",
		parse_mode='HTML'
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
		text="<b>👣 Inicio > Actividades cardio > Establecer objetivo</b>",
		parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	current_state = "INICIO_CARDIO_ESTABLECER_ACTIVIDAD"
	return INICIO_CARDIO_ESTABLECER_ACTIVIDAD

def establecer_cardio_minutos(update, context):
	global current_state

	n_params = context.args

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

def check_photo(update, context):
	username = update.message.from_user.username
	array_photos = update.message.photo
	# Se coge la foto con mayor calidad
	file = context.bot.getFile(array_photos[-1].file_id)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Seleccionar la actividad cardio más reciente
	cur.execute("SELECT id_actividad_cardio,fecha FROM Registra_cardio WHERE id_usuario='"+username+"' AND fecha=(SELECT MAX(c2.fecha) FROM Registra_cardio c2 WHERE id_usuario='"+username+"');")
	resultado = cur.fetchall()
	id_actividad_cardio=resultado[0][0]
	fecha=resultado[0][1]
	# Descargar imagen
	name_image = str(id_actividad_cardio)+"_"+fecha.strftime('%d-%m-%Y-%H:%M:%S')+"_"+username

	ruta = "/home/castinievas/ImagymBot/comprobar_cardio/"+name_image
	file.download(ruta)
	cur.execute("UPDATE Registra_cardio SET ruta='"+ruta+"', aprobada='N' WHERE id_usuario='"+username+"' AND fecha='"+str(fecha)+"' AND id_actividad_cardio="+str(id_actividad_cardio)+";")
	db.commit()

	cur.close()
	db.close()

	if current_state == "INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO":
		keyboard = [
			[InlineKeyboardButton("Volver a Mi objetivo de actividades cardio 🔙", callback_data='inicio_cardio')],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
		]
	elif current_state == "INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO":
		keyboard = [
			[InlineKeyboardButton("Volver a Ejercicio del mes 🔙", callback_data='inicio_ejercicio')],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
		text="He enviado tu foto con éxito ✔\n\nSe actualizará tu marcador cuando un moderador externo la apruebe.",
		reply_markup = reply_markup
	)

	time.sleep(1)

############# RETOS #############
def show_inicio_retos(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Retos...</b>",
		parse_mode='HTML'
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

		keyboard.append([InlineKeyboardButton("Calendario del reto actual 📆", callback_data='inicio_retos_calendario')])

	if retos_futuros:
		keyboard.append([InlineKeyboardButton("Ver próximos retos 🔛", callback_data='inicio_retos_ver')])

	if reto_usuario:
		keyboard.append([InlineKeyboardButton("Descalificarme del reto actual ❌", callback_data='inicio_retos_descalificar')])

	if reto_usuario_futuro:
		keyboard.append([InlineKeyboardButton("Eliminar mi inscripción de próximos retos ❌", callback_data='inicio_retos_eliminar')])

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
			text="⭐ <b>¡HOY EMPIEZA TU RETO DE "+ejercicio.upper()+"!</b>!"
			dia_reto = 1
		else:
			dia_reto = date.today()-fecha_inicio
			dia_reto = dia_reto.days+1
			text="<b>⭐¡SIGUES EN EL RETO DE "+ejercicio.upper()+"!</b>"

		text=text+"\n\n👉 <b>Día del reto: </b>"+str(dia_reto)

		cur.execute("SELECT repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+";")
		resultado = cur.fetchall();
		repeticiones = resultado[0][0]
		# Buscar si el usuario ha anotado ya el progreso
		cur.execute("SELECT * FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND dia="+str(dia_reto)+"")
		resultado = cur.fetchall()

		if resultado:
			text=text+"\n\n✅ ¡Hoy ya has anotado tu progreso! Has hecho <b>"+repeticiones+" "+ejercicio.lower()+"</b>"+"\n<b>Ejercicio:</b> /"+str(id_ejercicio)
			# Seleccionar el próximo día del reto
			cur.execute("SELECT dia,repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia=(SELECT MIN(dia) FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia>"+str(dia_reto)+" AND repeticiones is NOT NULL);")
			resultado = cur.fetchall()
			dia_siguiente = resultado[0][0]
			repeticiones = resultado[0][1]
			diferencia_dias = int(dia_siguiente)-int(dia_reto)

			if diferencia_dias == 1:
				text = text+"\n\n👉 <b>Próximo día del reto:</b> mañana, "+repeticiones+" "+ejercicio.lower()
				cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL 1 DAY);");
				resultado = cur.fetchall()
				fecha_recordatorio = resultado[0][0]
			else:
				cur.execute("SELECT DATE_ADD(CURDATE(), INTERVAL "+str(diferencia_dias)+" DAY);");
				resultado = cur.fetchall()
				fecha_recordatorio = resultado[0][0]
				fecha = fecha_recordatorio.strftime('%d-%B-%Y')
				text = text+"\n\n👉 <b>Próximo día del reto:</b> "+fecha+", "+repeticiones+" "+ejercicio.lower()
		else:
			if repeticiones is None:
				text=text+"\n\n✅ ¡Hoy toca descansar!"

			else:
				text=text+"\n<b>👉 Hoy debes hacer </b>"+repeticiones+" "+ejercicio.lower()+"\n<b>👉 Ejercicio:</b> /"+str(id_ejercicio)


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
		cur.execute("SELECT Retos.id_ejercicio,Retos.fecha_inicio FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Retos.fecha_inicio=(SELECT MIN(r1.fecha_inicio) FROM Retos r1 INNER JOIN Realiza_reto r2 WHERE r1.id_reto=r2.id_reto AND r1.fecha_inicio>CURDATE() AND r2.id_usuario='"+username_user+"' AND r2.estado='A');")
		proximo_reto = cur.fetchall();
		if proximo_reto:
			ejercicio_proximo_reto = proximo_reto[0][0]
			fecha_inicio_proximo_reto = proximo_reto[0][1]
			fecha_inicio_proximo_reto = fecha_inicio_proximo_reto.strftime('%d-%B-%Y')

			cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+str(ejercicio_proximo_reto)+";")
			ejercicio = cur.fetchall();
			ejercicio = ejercicio[0][0]

			text="📌 <b>TU PRÓXIMO RETO: RETO DE "+ejercicio.upper()+"</b>"
			text=text+"\n\n<b>Fecha de inicio:</b> "+fecha_inicio_proximo_reto

			bot.send_message(
				chat_id = query.message.chat_id,
				text=text,
				parse_mode='HTML'
			)

	if not reto_usuario and not reto_usuario_futuro and tiene_retos:
		bot.send_message(
			chat_id = query.message.chat_id,
			text="📌 Actualmente no estás apuntado a ningún reto"
		)

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Retos</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	cur.close()
	db.close()

	current_state = "INICIO_RETOS"
	return INICIO_RETOS

def show_inicio_retos_ver(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Retos > Ver próximos retos...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Los retos que muestran un check ✔ indican que ya te has inscrito en ellos."
	)
	time.sleep(.8)

	cur = db.cursor()
	cur.execute("SELECT id_reto FROM Retos where fecha_inicio > CURDATE();")
	resultado = cur.fetchall();

	cur.close()
	db.close()

	list_keyboards = []
	callback_query_list = []

	for id_reto in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()

		cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
		resultado = cur.fetchall()
		id_ejercicio = resultado[0][0]
		nivel_ejercicio = resultado[0][1]
		start_day = resultado[0][2]

		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		ejercicio_name = cur.fetchall()
		ejercicio_name = ejercicio_name[0][0]

		cur.execute("SELECT * FROM Realiza_reto where id_reto="+str(id_reto[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()

		cur.close()
		db.close()

		name_button = "Reto de "+ejercicio_name.lower()+" | Nivel "+str(nivel_ejercicio)+" | "+start_day.strftime('%B').upper()
		if esta_apuntado:
			name_button=name_button+" ✔"
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

		table_reto_path = "/home/castinievas/ImagymBot/retos/"+str(id_reto[0])+".png"
		if not path.exists(table_reto_path):
			createTable(id_reto[0], name_button)

	list_keyboards.append([InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Retos > Ver próximos retos</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RETOS_VER"
	return INICIO_RETOS_VER

def ver_reto(update, context):
	global current_state
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_reto_callback = query.data
	id_reto = id_reto_callback.split('_',4)
	id_reto = id_reto[3]
	table_reto_path = "/home/castinievas/ImagymBot/retos/"+id_reto+".png"

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

	cur.execute("SELECT id_ejercicio FROM Retos WHERE id_reto="+id_reto+";")
	id_ejercicio = cur.fetchall()
	id_ejercicio = id_ejercicio[0][0]

	# Fecha de inicio del reto
	cur.execute("SELECT fecha_inicio,fecha_fin FROM Retos where id_reto="+id_reto+";")
	resultado = cur.fetchall();
	fecha_inicio = resultado[0][0]
	fecha_inicio = fecha_inicio.strftime('%d-%B-%Y')
	fecha_fin = resultado[0][1]
	fecha_fin = fecha_fin.strftime('%d-%B-%Y')

	# Si el usuario no está apuntado a este reto
	cur.execute("SELECT COUNT(*) FROM Realiza_reto where id_reto="+id_reto+";")
	resultado = cur.fetchall();
	num_usuarios_apuntados = resultado[0][0]
	if not esta_apuntado:
		text="Aquí tienes el calendario de este reto.\n\n<b>Fecha de inicio:</b> "+fecha_inicio+"\n<b>Fecha fin:</b> "+fecha_fin+"\n<b>Ejercicio que hay que hacer:</b> /"+str(id_ejercicio)
		if num_usuarios_apuntados == 1:
			text = text+"\n\nHay "+str(num_usuarios_apuntados)+" usuario apuntado a este reto. ¡Anímate!"
		elif num_usuarios_apuntados > 1:
			text = text+"\n\nHay "+str(num_usuarios_apuntados)+" usuarios apuntados a este reto. ¡Anímate!"
		elif num_usuarios_apuntados == 0:
			text = text+"\n\n¡Aún no hay nadie apuntado a este reto! Sé la primera persona en apuntarse y corre la voz para competir con tus rivales 💪💪💪"

		keyboard = [
			[InlineKeyboardButton("Apuntarse al reto ✅", callback_data="inicio_retos_ver_apuntarse_"+id_reto)],
			[InlineKeyboardButton("Volver a Ver próximos retos 🔙", callback_data="back_inicio_retos_ver")],
			[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)

		text=text+"\n\nCompleta todos los días de este reto y gana una insignia que podrás lucir en la página web 🎖\n\n"
		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			reply_markup=reply_markup,
			parse_mode='HTML'
		)

	else:
		text="<b>ESTÁS APUNTADO A ESTE RETO</b>\n\n<b>Fecha de inicio:</b> "+fecha_inicio+"\n<b>Fecha fin:</b> "+fecha_fin+"\n<b>Ejercicio que hay que hacer:</b> /"+str(id_ejercicio)
		keyboard = [
			[InlineKeyboardButton("Desapuntarse al reto ❌", callback_data="inicio_retos_ver_apuntarse_"+id_reto)],
			[InlineKeyboardButton("Volver a Ver próximos retos 🔙", callback_data="back_inicio_retos_ver")],
			[InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")],
			[InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)

		if num_usuarios_apuntados == 1:
			text = text+"\n\n¡No hay nadie más en este reto! ¡Corre la voz y anima a otra gente!"
		else:
			text = text+"\n\nHay "+str(num_usuarios_apuntados)+" usuarios apuntados a este reto. ¡Ya mismo empieza la competición!"

		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Comprobar si el usuario está apuntado a un reto que coincide en la fecha del reto actual
	cur.execute("SELECT fecha_inicio,fecha_fin,id_ejercicio FROM Retos WHERE id_reto="+str(id_reto))
	resultado = cur.fetchall()
	start_day_reto = resultado[0][0]
	end_day_reto = resultado[0][1]
	id_ejercicio = resultado[0][2]
	fecha_inicio = start_day_reto.strftime('%d-%B-%Y')
	fecha_fin = end_day_reto.strftime('%d-%B-%Y')
	start_day_reto = start_day_reto.strftime("%Y-%m-%d")
	end_day_reto = end_day_reto.strftime("%Y-%m-%d")

	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto ON Retos.id_reto=Realiza_reto.id_reto and Retos.fecha_inicio <= '"+start_day_reto+"' and Retos.fecha_fin >= '"+start_day_reto+"' and Realiza_reto.id_usuario='"+username_user+"' and (Realiza_reto.estado='A' or Realiza_reto.estado='R')")
	resultado_before = cur.fetchall()
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto ON Retos.id_reto=Realiza_reto.id_reto and Retos.fecha_inicio <= '"+end_day_reto+"' and Retos.fecha_fin >= '"+end_day_reto+"' and Realiza_reto.id_usuario='"+username_user+"' and (Realiza_reto.estado='A' or Realiza_reto.estado='R')")
	resultado_after = cur.fetchall()

	keyboard=[]
	
	# Si está apuntado al reto
	cur.execute("SELECT * FROM Realiza_reto INNER JOIN Retos ON Realiza_reto.id_reto = Retos.id_reto and Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.id_reto="+id_reto+" and Retos.fecha_inicio > CURDATE()")
	esta_apuntado = cur.fetchall()
	if esta_apuntado:
		cur.execute("DELETE FROM Realiza_reto WHERE id_reto="+str(id_reto)+" AND id_usuario='"+username_user+"';")
		db.commit()

		# Quitar alarmas
		alarma_primer_dia = username_user+"_"+str(id_reto)
		alarma_descalificar = "descalificar_"+username_user+"_"+str(id_reto)
		for job in context.job_queue.get_jobs_by_name(alarma_primer_dia):
			job.schedule_removal()
		for job in context.job_queue.get_jobs_by_name(alarma_descalificar):
			job.schedule_removal()

		cur.execute("SELECT COUNT(*) FROM Realiza_reto where id_reto="+str(id_reto)+";")
		resultado = cur.fetchall();
		num_usuarios_apuntados = resultado[0][0]
		text="<b>NO ESTÁS APUNTADO A ESTE RETO</b>"
		text=text+"\n\nAquí tienes el calendario de este reto.\n\n<b>Fecha de inicio:</b> "+fecha_inicio+"\n<b>Fecha fin:</b> "+fecha_fin+"\n<b>Ejercicio que hay que hacer:</b> /"+str(id_ejercicio)
		if num_usuarios_apuntados == 1:
			text = text+"\n\nHay "+str(num_usuarios_apuntados)+" usuario apuntado a este reto. ¡Anímate!"
		else:
			text = text+"\n\nHay "+str(num_usuarios_apuntados)+" usuarios apuntados a este reto. ¡Anímate!"

		if num_usuarios_apuntados == 0:
			text = text+"\n\n¡Aún no hay nadie apuntado a este reto! Sé la primera persona en apuntarse y corre la voz para competir con tus rivales 💪💪💪"

		text=text+"\n\nCompleta este reto y gana una insignia que podrás lucir en la página web 🎖"
		keyboard.append([InlineKeyboardButton("Apuntarse al reto ✅", callback_data="inicio_retos_ver_apuntarse_"+str(id_reto))])

	else:
		if not resultado_before and not resultado_after:
			cur.execute("INSERT INTO Realiza_reto(id_reto, id_usuario, estado) VALUES (%s, %s, 'A')",(id_reto,username_user))
			db.commit()

			text="<b>ESTÁS APUNTADO AL RETO</b>"
			text=text+"\n\nTe deseo mucha suerte."+"\n\n<b>Ejercicio que hay que hacer:</b> /"+str(id_ejercicio)

			cur = db.cursor()
			cur.execute("SELECT fecha_inicio FROM Retos WHERE id_reto="+id_reto)
			resultado = cur.fetchall()
			start_day_object = resultado[0][0]

			ESP = tz.gettz('Europe/Madrid')
			dt = datetime(start_day_object.year,start_day_object.month,start_day_object.day,8,0,0, tzinfo=ESP)

			name_alarm=username_user+"_"+str(id_reto)
			context.job_queue.run_once(primer_dia_reto, dt, context=(query.message.chat_id, update, id_reto), name=name_alarm)

			text=text+"\n\nEl día que empice el reto te enviaré un recordatorio para que no se te olvide 🛎🛎🛎"
			keyboard.append([InlineKeyboardButton("Desapuntarse del reto ❌", callback_data="inicio_retos_ver_apuntarse_"+str(id_reto))])

		else:
			text="No puedes apuntarte al reto porque sus fechas coinciden con otro reto al que ya estás apuntado"

	cur.close()
	db.close()

	keyboard.append([InlineKeyboardButton("Volver a Ver próximos retos 🔙", callback_data="back_inicio_retos_ver")])
	keyboard.append([InlineKeyboardButton("Volver a Retos 🔙", callback_data="back_inicio_retos")])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.edit_message_text(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text = text,
		parse_mode='HTML',
		reply_markup=reply_markup
	)

def primer_dia_reto(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_reto = job.context[2]

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		[InlineKeyboardButton("Ir a Inicio > Retos 🔙", callback_data='back_inicio_retos')],
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
		callback_show_inicio_retos = CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos')
		callback_start_retos = CallbackQueryHandler(show_inicio_retos, pattern='inicio_retos')
		callback_show_inicio = CallbackQueryHandler(show_inicio, pattern='back_inicio')
		if not callback_show_inicio in conv_handler.states[i]:
			conv_handler.states[i].append(callback_show_inicio)
		if not callback_show_inicio_retos in conv_handler.states[i] and not callback_start_retos in conv_handler.states[i]:
			conv_handler.states[i].append(callback_show_inicio_retos)
	cur.close()
	db.close()

def recordar_reto(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_reto = job.context[2]

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="<b>⏳ Cargando Inicio > Retos > Eliminar inscripción de retos...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí se muestran todos los retos a los que te has inscrito."
	)
	time.sleep(.8)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
		text="<b>👣 Inicio > Retos > Eliminar inscripción de retos</b>",
		parse_mode='HTML',
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("DELETE FROM Realiza_reto WHERE id_usuario='"+username_user+"' AND id_reto="+str(id_reto)+";")
	db.commit()

	# Retos que aún no han empezado pero el usuario está apuntado
	cur.execute("SELECT Retos.id_reto FROM Retos INNER JOIN Realiza_reto WHERE Realiza_reto.id_reto=Retos.id_reto AND Realiza_reto.id_usuario='"+username_user+"' and Realiza_reto.estado='A';")
	reto_usuario_futuro = cur.fetchall();

	alarma_primer_dia = username_user+"_"+str(id_reto)
	alarma_descalificar = "descalificar_"+username_user+"_"+str(id_reto)
	for job in context.job_queue.get_jobs_by_name(alarma_primer_dia):
		job.schedule_removal()
	for job in context.job_queue.get_jobs_by_name(alarma_descalificar):
		job.schedule_removal()

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
		return INICIO_RETOS

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
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Retos > Anotar progreso...</b>",
		parse_mode='HTML'
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
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
	cur.execute("SELECT dia,repeticiones FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia=(SELECT MIN(dia) FROM Calendario WHERE id_reto="+str(id_reto)+" AND dia>"+str(dia_reto)+" AND repeticiones is NOT NULL);")
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
			fecha_recordatorio = resultado[0][0]
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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	cur.execute("SELECT dia FROM Realiza_reto WHERE id_usuario='"+username_user+"' AND id_reto="+str(id_reto)+";")
	dia = cur.fetchall()
	if dia[0][0] is None:
		dia_reto = 0
	else:
		dia_reto = dia[0][0]

	text="Reto de "+ejercicio.lower()+", nivel "+str(nivel)+", "+fecha_inicio.strftime("%B")

	nombre_imagen = str(id_reto)+"_"+username_user+"_"+str(dia_reto)
	path_imagen = "/home/castinievas/ImagymBot/retos/"+nombre_imagen+".png"

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
		text="<b>👣 Inicio > Retos > Calendario de mi reto</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RETOS_CALENDARIO"
	return INICIO_RETOS_CALENDARIO

def show_inicio_retos_descalificar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Retos > Descalificarme del reto...</b>",
		parse_mode='HTML'
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
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	alarma_primer_dia = username_user+"_"+str(id_reto)
	alarma_descalificar = "descalificar_"+username_user+"_"+str(id_reto)
	for job in context.job_queue.get_jobs_by_name(alarma_primer_dia):
		job.schedule_removal()
	for job in context.job_queue.get_jobs_by_name(alarma_descalificar):
		job.schedule_removal()

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
		text="<b>⏳ Cargando Inicio > Retos > Ver mi historial de retos...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_reto FROM Realiza_reto WHERE id_usuario='"+username_user+"' AND (estado='D' or estado='C');")
	cur.close()
	db.close()
	resultado = cur.fetchall();
	print(resultado)
	list_keyboards = []

	for id_reto in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT id_ejercicio,nivel,fecha_inicio FROM Retos where id_reto="+str(id_reto[0])+";")
		resultado = cur.fetchall()
		id_ejercicio = resultado[0][0]
		nivel_ejercicio = resultado[0][1]
		start_day = resultado[0][2]

		cur.execute("SELECT estado FROM Realiza_reto WHERE id_reto="+str(id_reto[0])+" AND id_usuario='"+username_user+"';")
		resultado = cur.fetchall();
		if resultado[0][0] == 'C':
			insignia = "🏆"
		else:
			insignia = "❌"

		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		ejercicio_name = cur.fetchall()
		ejercicio_name = ejercicio_name[0][0]

		cur.close()
		db.close()

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
		text="<b>👣 Inicio > Retos > Ver mi historial de retos</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

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

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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

	text="Reto de "+ejercicio.lower()+", nivel "+str(nivel)+", "+fecha_inicio.strftime("%B-%Y").upper()

	nombre_imagen = str(id_reto)+"_"+username_user+"_historial"
	path_imagen = "/home/castinievas/ImagymBot/retos/"+nombre_imagen+".png"

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
					text = "Las casillas en azul claro son los días que superaste 💪"
				)
		else:
			bot.send_message(
				chat_id = query.message.chat_id,
				text = "Las casillas en azul claro son los días que superaste 💪"
			)
			bot.send_message(
				chat_id = query.message.chat_id,
				text = str(n_personas_c)+" usuarios consiguieron completar este reto 🎉"
			)

	keyboard = [
		[InlineKeyboardButton("Volver a Ver mi historial de retos 🔙", callback_data='back_inicio_retos_historial')],
		[InlineKeyboardButton("Volver a Retos 🔙", callback_data='back_inicio_retos')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')],
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Retos > Historial de retos > Reto seleccionado</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RETOS_HISTORIAL_CLASIFICACION"
	return INICIO_RETOS_HISTORIAL_CLASIFICACION

def createTable(id_reto, name):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
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
	plt.clf()
	plt.title(name, y=1.05)
	plt.axis('off')
	col_labels = ['Repeticiones']
	col_colours = ['#f1c232']
	row_labels = []
	table_vals = []
	cell_colours = []
	row_colours = []

	for i in range(mitad_1):
		day = 'Día ' + str(resultado[i][0])
		repeticiones = str(resultado[i][1])

		row_colours.append('#f1c232')
		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowColours=row_colours,
	                      colColours=col_colours,
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
		row_colours.append('#f1c232')
		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowColours=row_colours,
	                      colColours=col_colours,
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
		row_colours.append('#f1c232')
		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_labels.append(day)
		cell = []
		cell.append(repeticiones)
		table_vals.append(cell)

	# Draw table
	the_table = plt.table(cellText=table_vals,
	                      colWidths=[0.1],
	                      rowColours=row_colours,
	                      colColours=col_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center right')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	table_path = "/home/castinievas/ImagymBot/retos/"+str(id_reto)+".png"
	plt.savefig(table_path)

def createTableColors(id_reto, name, day_limit, id_usuario, name_graph):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT dia,repeticiones FROM Calendario where id_reto="+str(id_reto)+";")
	resultado = cur.fetchall();
	print(resultado)
	mitad_1 = round(len(resultado)/3)
	mitad_2 = round(2*len(resultado)/3)
	fin = len(resultado)

	cur.execute("SELECT fecha_inicio FROM Retos WHERE id_reto="+str(id_reto))
	fecha_inicio = cur.fetchall()
	fecha_inicio = fecha_inicio[0][0]

	# Primera mitad
	plt.clf()
	plt.title(name, y=1.05)
	plt.axis('off')
	col_labels = ['Repeticiones']
	col_colours = ['#f1c232']
	row_labels = []
	table_vals = []
	cell_colours = []
	row_colours = []

	for i in range(mitad_1):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0]-1)
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_colours.append('#f1c232')
		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('#cfe2f3')
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
	                      rowColours=row_colours,
	                      colColours=col_colours,
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center left')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Segunda mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	col_colours = ['#f1c232']
	row_labels = []
	table_vals = []
	cell_colours = []
	row_colours = []

	for i in range(mitad_1, mitad_2):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0]-1)
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_colours.append('#f1c232')
		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('#cfe2f3')
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
	                      rowColours=row_colours,
	                      colColours=col_colours,
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	# Tercera mitad
	plt.axis('off')
	col_labels = ['Repeticiones']
	col_colours = ['#f1c232']
	row_labels = []
	table_vals = []
	cell_colours = []
	row_colours = []

	for i in range(mitad_2, fin):
		date = datetime.combine(fecha_inicio, datetime.min.time()) + timedelta(days=resultado[i][0]-1)
		date = datetime.strftime(date, '%d-%m')

		day = 'Día '+date
		repeticiones = str(resultado[i][1])

		if resultado[i][1] == 0 or not resultado[i][1]:
			repeticiones = 'Descanso'

		row_colours.append('#f1c232')
		if resultado[i][0] <= day_limit:
			cell_color = []
			cell_color.append('#cfe2f3')
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
	                      rowColours=row_colours,
	                      colColours=col_colours,
	                      cellColours=cell_colours,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center right')
	plt.subplots_adjust(bottom=0.05)
	the_table.scale(2, 2)

	if name_graph == "":
		name_graph = str(id_reto)+"_"+id_usuario+"_"+str(day_limit)

	table_path = "/home/castinievas/ImagymBot/retos/"+name_graph+".png"
	plt.savefig(table_path)

	cur.close()
	db.close()

############# EJERCICIO DEL MES #############
def show_inicio_ejercicio(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Ejercicio del mes...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	actualizar_marcador()

	keyboard = []

	cur = db.cursor()

	cur.execute("SELECT id_objetivo_mensual,puntuacion FROM Se_apunta WHERE estado='R' AND id_usuario='"+username_user+"';")
	resultado = cur.fetchall();
	# Hay algún ejercicio del mes actualmente
	if resultado:
		keyboard.append([InlineKeyboardButton("Registrar cardio 🏃", callback_data='inicio_cardio_registrar')])
		keyboard.append([InlineKeyboardButton("Ranking actual del ejercicio de este mes 🥇", callback_data='inicio_ejercicio_ranking')])
		keyboard.append([InlineKeyboardButton("Me rindo en el ejercicio de este mes ❌", callback_data='inicio_ejercicio_descalificar')])
		
		id_objetivo_mensual = resultado[0][0]
		puntuacion = resultado[0][1]

		cur.execute("SELECT id_actividad_cardio,objetivo,fecha_inicio,fecha_fin FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
		resultado = cur.fetchall();
		id_actividad_cardio = resultado[0][0]
		objetivo = resultado[0][1]
		fecha_inicio = resultado[0][2]
		fecha_fin = resultado[0][3]

		cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
		resultado = cur.fetchall();
		nombre = resultado[0][0]

		text="<b>⭐ RESUMEN DE LO QUE LLEVAS EN EL EJERCICIO DE ESTE MES ⭐</b>"
		text=text+"\n\n<b>👉 Actividad cardio:</b> "+nombre.lower()
		tipo_objetivo = objetivo.split(' ', 1)[1]
		if tipo_objetivo == "distancia":
			tipo_objetivo = "kilómetros"
			medida="distancia"
		elif tipo_objetivo == "calorias":
			tipo_objetivo = "calorías"
			medida="calorias"
		else:
			tipo_objetivo = "minutos"
			medida="tiempo"

		text=text+"\n<b>👉Objetivo:</b> "+objetivo.split(' ', 1)[0]+" "+tipo_objetivo
		cur.execute("SELECT SUM("+medida+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+username_user+"' AND DATE(fecha)>='"+str(fecha_inicio)+"' AND DATE(fecha)<='"+str(fecha_fin)+"' AND aprobada='S';")
		resultado = cur.fetchall()
		contador = resultado[0][0]
		if contador is None:
			contador = 0
		text=text+"\n<b>👉 Llevas:</b> "+str(contador)+" "+tipo_objetivo
		text=text+"\n<b>👉 Puntuación:</b> "+str(round(puntuacion,1))+" puntos"
		text=text+"\n\nUna vez alcanzado el objetivo, los puntos que acumules de más se multiplicarán de acuerdo a tu IMC:\n"
		text=text+"\n✖1.1 si tu IMC es <b>menor que 18.5</b> ó <b>mayor que 25.0</b>"
		text=text+"\n✖1.25 si tu IMC está <b>entre 18.5 y 20.0</b> ó <b>entre 22.5 y 25.0</b>"
		text=text+"\n✖1.35 si tu IMC está <b>entre 20.0 y 22.5</b>"

		bot.send_message(
			chat_id = query.message.chat_id,
			text=text,
			parse_mode='HTML'
		)
		time.sleep(1)

	# Ejercicios futuros
	cur.execute("SELECT id_objetivo_mensual,fecha_inicio,id_actividad_cardio,objetivo,fecha_fin FROM Ejercicio_del_mes WHERE fecha_inicio=(SELECT MIN(fecha_inicio) FROM Ejercicio_del_mes WHERE fecha_inicio > CURDATE());;")
	ejercicio_futuro = cur.fetchall();
	if ejercicio_futuro:
		id_ejercicio_futuro = ejercicio_futuro[0][0]
		fecha_inicio = ejercicio_futuro[0][1]
		id_actividad_cardio = ejercicio_futuro[0][2]
		objetivo = ejercicio_futuro[0][3]
		fecha_fin = ejercicio_futuro[0][4]

		mes = fecha_inicio.strftime("%B")

		cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
		resultado = cur.fetchall();
		nombre = resultado[0][0]

		text="<b>PRÓXIMO EJERCICIO DEL MES DE "+str(mes).upper()+"</b>"
		text=text+"\n\n<b>👉 Actividad cardio:</b> "+nombre.lower()
		tipo_objetivo = objetivo.split(' ', 1)[1]
		if tipo_objetivo == "distancia":
			tipo_objetivo = "kilómetros"
		elif tipo_objetivo == "calorias":
			tipo_objetivo = "calorías"
		else:
			tipo_objetivo = "minutos"

		text=text+"\n<b>👉 Objetivo:</b> "+objetivo.split(' ', 1)[0]+" "+tipo_objetivo


		cur.execute("SELECT COUNT(*) FROM Se_apunta WHERE id_objetivo_mensual="+str(id_ejercicio_futuro)+";")
		resultado = cur.fetchall();
		n_personas = resultado[0][0]

		cur.execute("SELECT estado FROM Se_apunta WHERE id_objetivo_mensual="+str(id_ejercicio_futuro)+" AND id_usuario='"+username_user+"';")
		resultado = cur.fetchall();

		if not resultado:
			keyboard.append([InlineKeyboardButton("Apuntarse al ejercicio del mes de "+str(mes).lower()+" ✔", callback_data='inicio_ejercicio_apuntarse')])
			text=text+"\n\n¡Aún no te has apuntado al <b>ejercicio del mes de "+str(mes).upper()+"</b>!"

			if n_personas > 0:
				text=text+"\nYa hay "+str(n_personas)+" personas dispuestas a entrar en el ranking de este ejercicio. ¡Anímate!"
			else:
				text=text+"\n¡Eres la primera persona en llegar! ¡Apúntate al ejercicio del mes y entra en el ranking!"

			bot.send_message(
				chat_id = query.message.chat_id,
				text="📌 "+text,
				parse_mode='HTML'
			)	
			time.sleep(1)
		else:
			estado = resultado[0][0]
			if estado == 'A':
				keyboard.append([InlineKeyboardButton("Quitarse del ejercicio del mes de "+str(mes).lower()+" ❌", callback_data='inicio_ejercicio_eliminar')])
				text=text+"\n\nYa te has apuntado al ejercicio del mes de "+str(mes).lower()+" ⬆\n"
				if n_personas > 1:
					text=text+"Ya hay <b>"+str(n_personas)+" personas apuntadas</b>"
				else:
					text=text+"¡Has sido la primera persona en apuntarse!"

				bot.send_message(
					chat_id = query.message.chat_id,
					text="📌 "+text,
					parse_mode='HTML'
				)	
				time.sleep(1)	

	cur.execute("SELECT id_objetivo_mensual,puntuacion FROM Se_apunta WHERE estado = 'C' AND id_usuario='"+username_user+"';")
	resultado = cur.fetchall();
	if resultado:
		keyboard.append([InlineKeyboardButton("Ver mi historial de ejercicios del mes 📖", callback_data='inicio_ejercicio_historial')])

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Ejercicio del mes</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	cur.close()
	db.close()

	current_state = "INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def actualizar_marcador():
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	# Comprobar si está apuntado a un objetivo de cardio mensual
	cur.execute("SELECT id_objetivo_mensual,id_usuario FROM Se_apunta WHERE estado='R';")
	usuarios = cur.fetchall()
	cur.close()
	db.close()
	for i in range(len(usuarios)):
		id_objetivo_mensual=usuarios[i][0]
		username_user=usuarios[i][1]
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		# Seleccionar la actividad de cardio más reciente
		cur.execute("SELECT id_actividad_cardio FROM Registra_cardio WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(fecha) FROM Registra_cardio WHERE id_usuario='"+username_user+"');")
		hay_actividad_cardio_reciente = cur.fetchall()
		if hay_actividad_cardio_reciente:
			id_actividad_cardio_reciente = hay_actividad_cardio_reciente[0][0]
			# Comprobar si el usuario tiene registrado cardio de esa actividad cardio
			cur.execute("SELECT id_actividad_cardio,fecha_inicio,fecha_fin,objetivo FROM Ejercicio_del_mes WHERE id_actividad_cardio="+str(id_actividad_cardio_reciente)+";")
			tiene_cardio = cur.fetchall()
			if tiene_cardio:
				id_actividad_cardio = tiene_cardio[0][0]
				fecha_inicio = tiene_cardio[0][1]
				fecha_fin = tiene_cardio[0][2]
				objetivo = tiene_cardio[0][3]
				if id_actividad_cardio == id_actividad_cardio_reciente:
					tipo_objetivo = objetivo.split(' ', 1)[1]
					if tipo_objetivo == "distancia":
						medida="distancia"
					elif tipo_objetivo == "calorias":
						medida="calorias"
					else:
						medida="tiempo"

					cur.execute("SELECT SUM("+medida+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+username_user+"' AND DATE(fecha)>='"+str(fecha_inicio)+"' AND DATE(fecha)<='"+str(fecha_fin)+"' AND aprobada='S';")
					resultado = cur.fetchall()
					contador = resultado[0][0]
					if contador is None:
						contador = 0

					objetivo_numero = round(float(objetivo.split(' ', 1)[0]), 2)
					contador = round(float(contador),2)
					puntuacion = contador

					if contador > objetivo_numero:
						contador_restantes = contador-objetivo_numero
						cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL)")
						resultado = cur.fetchall()
						# Si el usuario tiene IMC, se le suman puntos
						if resultado:
							imc = round(float(resultado[0][0]),1)
							if imc < 18.5:
								puntuacion = contador+contador_restantes*1.1
							elif imc >= 18.5 and imc < 20.0:
								puntuacion = contador+contador_restantes*1.25
							elif imc >= 20.0 and imc < 22.5:
								puntuacion = contador+contador_restantes*1.35
							elif imc >= 22.5 and imc < 25.0:
								puntuacion = contador+contador_restantes*1.25
							else:
								puntuacion = contador+contador_restantes*1.1

					cur.execute("UPDATE Se_apunta SET puntuacion="+str(puntuacion)+" WHERE id_usuario='"+username_user+"' AND id_objetivo_mensual="+str(id_objetivo_mensual)+";")
					db.commit()
		
		cur.close()
		db.close()

def show_inicio_ejercicio_apuntarse(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Coger el proximo ejercicio del mes
	cur.execute("SELECT id_objetivo_mensual,fecha_inicio FROM Ejercicio_del_mes WHERE fecha_inicio=(SELECT MIN(fecha_inicio) FROM Ejercicio_del_mes WHERE fecha_inicio > CURDATE());;")
	resultado = cur.fetchall();
	id_ejercicio_futuro = resultado[0][0]
	fecha_inicio = resultado[0][1]

	cur.execute("INSERT INTO Se_apunta(id_objetivo_mensual, id_usuario, estado, puntuacion) VALUES (%s, %s, 'A', 0)",(id_ejercicio_futuro,username_user))
	db.commit()

	bot.send_message(
		chat_id = query.message.chat_id,
		text = "¡Te has apuntado al ejercicio del mes con éxito ✔"
	)
	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text = "¡No te preocupes! El día que comience te lo recordaré 🛎🛎🛎"
	)
	time.sleep(.8)

	ESP = tz.gettz('Europe/Madrid')
	dt = datetime(fecha_inicio.year,fecha_inicio.month,fecha_inicio.day,8,30,0, tzinfo=ESP)
	name_alarm="ejercicio_"+username_user+"_"+str(id_ejercicio_futuro)
	context.job_queue.run_once(primer_dia_ejercicio, dt, context=(query.message.chat_id, update, id_ejercicio_futuro), name=name_alarm)

	cur.close()
	db.close()

	show_inicio_ejercicio(update, context)

	current_state = "INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def primer_dia_ejercicio(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_objetivo_mensual = job.context[2]

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Actividad cardio
	cur.execute("SELECT id_actividad_cardio,objetivo,fecha_fin FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	resultado = cur.fetchall()
	id_actividad_cardio = resultado[0][0]
	objetivo = resultado[0][1]
	fecha_fin = resultado[0][2]

	# Poner alarma para cuando termine el ejercicio del mes
	ESP = tz.gettz('Europe/Madrid')
	dt = datetime(fecha_fin.year,fecha_fin.month,fecha_fin.day,23,59,59, tzinfo=ESP)

	name_alarm="termina_"+str(id_objetivo_mensual)
	if name_alarm not in context.job_queue.get_jobs_by_name(name_alarm):
		context.job_queue.run_once(termina_ejercicio, dt, context=(query.message.chat_id, job.context[1], id_objetivo_mensual), name=name_alarm)


	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	# Actualizar estado del ejercicio
	cur.execute("UPDATE Se_apunta SET estado='R' AND puntuacion=0 WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+" AND id_usuario='"+username_user+"'")
	db.commit()

	bot.send_message(
		job.context[0],
		text="🌄 ¡BUENOS DÍAS! 🌄\n\nHoy comienza el <b>ejercicio del mes de "+date.today().strftime('%B')+"</b>",
		parse_mode='HTML'
	)

	tipo_objetivo = objetivo.split(' ', 1)[1]
	if tipo_objetivo == "distancia":
		tipo_objetivo = "kilómetros"
	elif tipo_objetivo == "calorias":
		tipo_objetivo = "calorías"
	else:
		tipo_objetivo = "minutos"

	text="\n\nTe recuerdo que el ojetivo es hacer <b>"+objetivo.split(' ', 1)[0]+" "+tipo_objetivo+" en "+nombre.lower()+"</b> a lo largo de todo el mes."
	bot.send_message(
		job.context[0],
		text=text,
		parse_mode='HTML'
	)

	text="Recibirás 1 punto por cada "+tipo_objetivo[:-1]+" que registres en esta actividad de cardio."
	keyboard = [
		[InlineKeyboardButton("Ir a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		job.context[0],
		text=text,
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	for i in conv_handler.states:
		callback_show_inicio = CallbackQueryHandler(show_inicio, pattern='back_inicio')
		if not callback_show_inicio in conv_handler.states[i]:
			conv_handler.states[i].append(callback_show_inicio)

	cur.close()
	db.close()

def termina_ejercicio(context):
	global current_state, conv_handler
	job = context.job
	bot = context.bot
	query = job.context[1].callback_query
	username_user = query.from_user.username
	id_objetivo_mensual = job.context[2]

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	# Actividad cardio
	cur.execute("SELECT id_actividad_cardio,objetivo FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	resultado = cur.fetchall()
	id_actividad_cardio = resultado[0][0]
	objetivo = resultado[0][1]

	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	# Actualizar estado del ejercicio
	cur.execute("UPDATE Se_apunta SET estado='C' WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	db.commit()

	bot.send_message(
		job.context[0],
		text="🏁 EJERCICIO DEL MES TERMINADO 🏁\n\nHa terminado el <b>ejercicio del mes de "+date.today().strftime('%B')+"</b>\n\nPuedes ver la clasificación final en 👣 Inicio > Ejercicio del mes",
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Ir a Inicio > Ejercicio del mes 👣", callback_data='back_inicio_ejercicio')]
		[InlineKeyboardButton("Ir a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		job.context[0],
		text=text,
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	for i in conv_handler.states:
		callback_show_inicio_ejercicio = CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio')
		if not callback_show_inicio_ejercicio in conv_handler.states[i]:
			conv_handler.states[i].append(callback_show_inicio_ejercicio)

	cur.close()
	db.close()

def show_inicio_ejercicio_ranking(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Ejercicio del mes > Ranking actual del ejercicio del mes...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	cur.execute("SELECT id_usuario,puntuacion FROM Se_apunta WHERE estado='R' ORDER BY puntuacion DESC LIMIT 10")
	resultado = cur.fetchall();

	text="🏆 Top 10 del ejercicio del mes 🏆:\n"
	aparece_usuario = False
	for i in range(len(resultado)):
		usuario = resultado[i][0]
		puntuacion = round(float(resultado[i][1]),1)
		text=text+"\n"
		if i == 0:
			text=text+"🥇 "
		elif i == 1:
			text=text+"🥈 "
		elif i == 2:
			text = text+"🥉 "

		if usuario == username_user:
			aparece_usuario = True
			text=text+"<b>"+usuario+" - "+str(puntuacion)+" puntos</b>"
		else:
			text=text+usuario+" - "+str(puntuacion)+" puntos"

	if not aparece_usuario:
		cur.execute("SELECT puntuacion FROM Se_apunta WHERE estado='R' AND id_usuario='"+username_user+"'")
		resultado = cur.fetchall();
		puntuacion_usuario = resultado[0][0]
		text=text+"\n\nTu puntuación: "+str(puntuacion_usuario)

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)
	time.sleep(.8)

	keyboard = [
		[InlineKeyboardButton("Volver a Ejercicio del mes 🔙", callback_data='back_inicio_ejercicio')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Ejercicio del mes > Ranking actual del ejercicio del mes</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_EJERCICIO_RANKING"
	return INICIO_EJERCICIO_RANKING

def show_inicio_ejercicio_descalificar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Ejercicio del mes > Descalificarme del ejercicio del mes...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	cur = db.cursor()

	cur.execute("SELECT id_objetivo_mensual FROM Se_apunta WHERE estado='R' AND id_usuario='"+username_user+"';")
	resultado = cur.fetchall();
	id_objetivo_mensual = resultado[0][0]

	cur.execute("SELECT id_actividad_cardio FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	resultado = cur.fetchall();
	id_actividad_cardio = resultado[0][0]

	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall();
	nombre = resultado[0][0]

	cur.close()
	db.close()

	text="¿De verdad quieres descalificarte del <b>ejercicio de este mes</b>? Una vez hecho esto, no podrás volver atrás."

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='inicio_ejercicio_descalificar_si')],
		[InlineKeyboardButton("No ❌", callback_data='inicio_ejercicio_descalificar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	current_state = "INICIO_EJERCICIO_DESCALIFICAR_CONFIRMAR"
	return INICIO_EJERCICIO_DESCALIFICAR_CONFIRMAR

def inicio_ejercicio_descalificar_si(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Descalificando del ejercicio del mes..."
	)
	time.sleep(.8)

	cur = db.cursor()
	cur.execute("UPDATE Se_apunta SET estado='D' WHERE estado='R' AND id_usuario='"+username_user+"';")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Has sido descalificado del ejercicio del mes...\n\nSuerte en la próxima 💪"
	)
	time.sleep(1)

	show_inicio_ejercicio(update, context)

	current_state="INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def inicio_ejercicio_descalificar_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡Qué susto! No te has descalificado del ejercicio del mes.\n\n¡Mucho ánimo!"
	)
	time.sleep(1.5)

	show_inicio_ejercicio(update, context)

	current_state="INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def show_inicio_ejercicio_eliminar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Ejercicio del mes > Desapuntarme del ejercicio del mes...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	cur = db.cursor()

	cur.execute("SELECT id_objetivo_mensual FROM Se_apunta WHERE estado='A' AND id_usuario='"+username_user+"';")
	resultado = cur.fetchall();
	id_objetivo_mensual = resultado[0][0]

	cur.execute("SELECT id_actividad_cardio,fecha_inicio FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	resultado = cur.fetchall();
	id_actividad_cardio = resultado[0][0]
	fecha_inicio = resultado[0][1]

	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall();
	nombre = resultado[0][0]

	cur.close()
	db.close()

	text="¿De verdad quieres desapuntarte del <b>ejercicio del mes de "+fecha_inicio.strftime('%B')+"</b>? Podrás volver a apuntarte siempre que sea antes de su inicio."

	keyboard = [
		[InlineKeyboardButton("Si ✔", callback_data='inicio_ejercicio_eliminar_si')],
		[InlineKeyboardButton("No ❌", callback_data='inicio_ejercicio_eliminar_no')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	current_state = "INICIO_EJERCICIO_ELIMINAR_CONFIRMAR"
	return INICIO_EJERCICIO_ELIMINAR_CONFIRMAR

def inicio_ejercicio_eliminar_si(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Desapuntando del ejercicio del mes..."
	)
	time.sleep(.8)

	cur = db.cursor()
	cur.execute("SELECT id_objetivo_mensual FROM Se_apunta WHERE estado='A' AND id_usuario='"+username_user+"';")
	resultado = cur.fetchall()
	id_objetivo_mensual = resultado[0][0]

	cur.execute("DELETE FROM Se_apunta WHERE estado='A' AND id_usuario='"+username_user+"';")
	db.commit()

	cur.close()
	db.close()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Te has desapuntado del ejercicio del mes\n\n"
	)

	alarma_descalificar = "ejercicio_"+username_user+"_"+str(id_objetivo_mensual)
	for job in context.job_queue.get_jobs_by_name(alarma_descalificar):
		job.schedule_removal()

	time.sleep(1)

	show_inicio_ejercicio(update, context)

	current_state="INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def inicio_ejercicio_eliminar_no(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="¡Qué susto! No te has desapuntado.\n\n¡Mucho ánimo!"
	)
	time.sleep(1.5)

	show_inicio_ejercicio(update, context)

	current_state="INICIO_EJERCICIO"
	return INICIO_EJERCICIO

def show_inicio_ejercicio_historial(update, context):
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Ejercicio del mes > Mi historial de ejercicios del mes...</b>",
		parse_mode='HTML'
	)
	time.sleep(.8)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_objetivo_mensual FROM Se_apunta where id_usuario='"+username_user+"' AND estado='C';")
	cur.close()
	db.close()
	resultado = cur.fetchall();

	list_keyboards = []

	for id_objetivo_mensual in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT id_actividad_cardio,fecha_inicio FROM Ejercicio_del_mes where id_objetivo_mensual="+str(id_objetivo_mensual[0])+";")
		resultado = cur.fetchall()
		id_actividad_cardio = resultado[0][0]
		fecha_inicio = resultado[0][1]

		cur.execute("SELECT nombre FROM Actividad_cardio where id_actividad_cardio="+str(id_actividad_cardio)+";")
		resultado = cur.fetchall()
		nombre = resultado[0][0]

		cur.close()
		db.close()

		name_button = "Ejercicio del mes de "+fecha_inicio.strftime('%B')+" de "+fecha_inicio.strftime('%Y') 
		button = InlineKeyboardButton(name_button, callback_data="inicio_ejercicio_historial_"+str(id_objetivo_mensual[0]))

		callback_query_ejercicio_historial = CallbackQueryHandler(historial_ejercicio, pattern="inicio_ejercicio_historial_"+str(id_objetivo_mensual[0]))

		if not callback_query_ejercicio_historial in conv_handler.states[INICIO_EJERCICIO_HISTORIAL]:
			conv_handler.states[INICIO_EJERCICIO_HISTORIAL].append(callback_query_ejercicio_historial)

		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)

	list_keyboards.append([InlineKeyboardButton("Volver a Ejercicio del mes 🔙", callback_data='back_inicio_ejercicio')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Aquí te muestro una lista de todos los ejercicios del mes que has completado 🏆"
	)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Ejercicio del mes > Mi historial de ejercicios del mes</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_EJERCICIO_HISTORIAL"
	return INICIO_EJERCICIO_HISTORIAL

def historial_ejercicio(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_objetivo_mensual_callback = query.data
	id_objetivo_mensual = id_objetivo_mensual_callback.split('_',4)
	id_objetivo_mensual = id_objetivo_mensual[3]

	bot.send_message(
		chat_id = query.message.chat_id,
		text="⏳ Generando información del ejercicio del mes... "
	)
	time.sleep(.8)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_actividad_cardio,objetivo,fecha_inicio,fecha_fin FROM Ejercicio_del_mes WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+";")
	resultado = cur.fetchall();
	id_actividad_cardio = resultado[0][0]
	objetivo = resultado[0][1]
	fecha_inicio = resultado[0][2]
	fecha_fin = resultado[0][3]

	cur.execute("SELECT nombre FROM Actividad_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+";")
	resultado = cur.fetchall()
	nombre = resultado[0][0]

	text="<b>EJERCICIO DEL MES DE "+fecha_inicio.strftime('%B').upper()+" DE "+fecha_inicio.strftime('%Y')+"</b>"
	text=text+"\n\nActividad cardio: "+nombre.lower()
	tipo_objetivo = objetivo.split(' ', 1)[1]
	if tipo_objetivo == "distancia":
		tipo_objetivo = "kilómetros"
		medida = "distancia"
	elif tipo_objetivo == "calorias":
		tipo_objetivo = "calorías"
		medida = "calorias"
	else:
		tipo_objetivo = "minutos"
		medida = "tiempo"

	text=text+"\nObjetivo: "+objetivo.split(' ', 1)[0]+" "+tipo_objetivo

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	cur.execute("SELECT id_usuario,puntuacion FROM Se_apunta WHERE id_objetivo_mensual="+str(id_objetivo_mensual)+" ORDER BY puntuacion DESC LIMIT 10")
	resultado = cur.fetchall();

	text="🏆 Top 10 del ejercicio del mes 🏆:\n"
	aparece_usuario = False
	for i in range(len(resultado)):
		usuario = resultado[i][0]
		puntuacion = round(float(resultado[i][1]),1)
		cur.execute("SELECT SUM("+medida+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+usuario+"' AND DATE(fecha)>='"+str(fecha_inicio)+"' AND DATE(fecha)<='"+str(fecha_fin)+"' AND aprobada='S';")
		contador = cur.fetchall()
		contador = contador[0][0]
		if contador is None:
			contador = 0
		text=text+"\n"
		if i == 0:
			text=text+"🥇 "
		elif i == 1:
			text=text+"🥈 "
		elif i == 2:
			text = text+"🥉 "

		if usuario == username_user:
			aparece_usuario = True
			text=text+"<b>"+usuario+" - "+str(round(puntuacion,1))+" puntos - "+str(contador)+" "+tipo_objetivo+"</b>"
		else:
			text=text+usuario+" - "+str(round(puntuacion,1))+" puntos - "+str(contador)+" "+tipo_objetivo

	if not aparece_usuario:
		cur.execute("SELECT puntuacion FROM Se_apunta WHERE estado='R' AND id_usuario='"+username_user+"'")
		resultado = cur.fetchall();
		puntuacion_usuario = resultado[0][0]
		cur.execute("SELECT SUM("+medida+") FROM Registra_cardio WHERE id_actividad_cardio="+str(id_actividad_cardio)+" AND id_usuario='"+username_user+"' AND DATE(fecha)>='"+str(fecha_inicio)+"' AND DATE(fecha)<='"+str(fecha_fin)+"' AND aprobada='S';")
		contador = cur.fetchall()
		contador = contador[0][0]
		if contador is None:
			contador = 0
		text=text+"\n\nTu puntuación: "+str(round(puntuacion_usuario,1))+" - "+str(contador)+" "+tipo_objetivo 

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Mi historial de ejercicios del mes 🔙", callback_data='back_inicio_ejercicio_historial')],
		[InlineKeyboardButton("Volver a Ejercicio del mes 🔙", callback_data='back_inicio_ejercicio')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')],
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	time.sleep(1)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Ejercicio del mes > Mi historial de ejercicios del mes > Ejercicio del mes</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_EJERCICIO_HISTORIAL_CLASIFICACION"
	return INICIO_EJERCICIO_HISTORIAL_CLASIFICACION

############# RUTINAS #############
def show_inicio_rutinas(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Rutinas y entrenamiento...</b>",
		parse_mode='HTML'
	)
	time.sleep(1)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT DISTINCT id_rutina FROM Hace_rutina WHERE fecha=CURDATE() AND id_usuario='"+username_user+"' ORDER BY id_rutina;")
	rutinas = cur.fetchall()

	# Tiene rutinas anteriores
	cur.execute("SELECT DISTINCT id_rutina FROM Hace_rutina WHERE fecha<=CURDATE() AND id_usuario='"+username_user+"' ORDER BY id_rutina;")
	tiene_rutinas_anteriores = cur.fetchall()
	cur.close()
	db.close()

	if not rutinas:
		text="📌 Hoy no has anotado ningún ejercicio de las rutinas"

	else:
		text="<b>HOY DÍA "+date.today().strftime('%d-%B-%Y').upper()+" HAS HECHO:</b>"
	for id_rutina in rutinas:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
		resultado = cur.fetchall()
		id_trainer = resultado[0][0]

		cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
		nombre = cur.fetchall()
		nombre = nombre[0][0]

		dia_hoy = date.today().weekday()+1
		if dia_hoy == 1:
			dia_semana = "Lunes"
		elif dia_hoy == 2:
			dia_semana = "Martes"
		elif dia_hoy == 3:
			dia_semana = "Miércoles"
		elif dia_hoy == 4:
			dia_semana = "Jueves"
		elif dia_hoy == 5:
			dia_semana = "Viernes"
		elif dia_hoy == 6:
			dia_semana = "Sábado"
		elif dia_hoy == 7:
			dia_semana = "Domingo"

		text=text+"\n\n📌 <b>Ejercicios hechos de la rutina del "+dia_semana.lower()+" de "+nombre+"</b>"
		cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()
		if esta_apuntado:
			text=text+" ⭐"
		cur.execute("SELECT id_ejercicio FROM Hace_rutina WHERE fecha=CURDATE() AND id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina[0])+";")
		ejercicios = cur.fetchall()
		cur.close()
		db.close()
		for i in range(len(ejercicios)):
			id_ejercicio = ejercicios[i][0]
			
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
			db.begin()
			cur = db.cursor()
			cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
			nombre_ejercicio = cur.fetchall()
			nombre_ejercicio = nombre_ejercicio[0][0]

			cur.execute("SELECT repeticiones FROM Rutinas_ejercicios WHERE id_ejercicio="+str(id_ejercicio)+" AND id_rutina="+str(id_rutina[0])+" AND dia='"+str(dia_hoy)+"';")
			repeticiones = cur.fetchall()
			repeticiones = repeticiones[0][0]

			cur.close()
			db.close()

			text=text+"\n"+nombre_ejercicio+" - "+repeticiones+" 👉 tutorial: /"+str(id_ejercicio)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = []
	keyboard.append([InlineKeyboardButton("Ver rutinas de entrenamiento 🏋", callback_data='inicio_rutinas_ver')])
	keyboard.append([InlineKeyboardButton("Anotar rutina de hoy 📝", callback_data='inicio_rutinas_anotar')])
	if tiene_rutinas_anteriores:
		keyboard.append([InlineKeyboardButton("Consultar entrenamiento de otro día 📖", callback_data='inicio_rutinas_consultar')])

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Rutinas y entrenamiento</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RUTINAS"
	return INICIO_RUTINAS

def show_inicio_rutinas_ver(update, context):
	global current_state, conv_handler
	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username
	
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Rutinas y entrenamiento > Ver rutinas de entrenamiento...</b>",
		parse_mode='HTML'
	)
	time.sleep(1)

	cur = db.cursor()
	# Seleccionar las rutinas vigentes
	cur.execute("SELECT id_rutina FROM Ofrecen WHERE fecha_fin is NULL;")
	resultado = cur.fetchall();

	cur.close()
	db.close()

	list_keyboards = []
	callback_query_list = []

	for id_rutina in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()

		cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
		resultado = cur.fetchall()
		id_trainer = resultado[0][0]

		cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
		nombre = cur.fetchall()
		nombre = nombre[0][0]

		cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()

		cur.close()
		db.close()

		name_button = "Rutina de "+nombre
		if esta_apuntado:
			name_button=name_button+" ⭐"
		button = InlineKeyboardButton(name_button, callback_data="inicio_rutinas_ver_"+str(id_rutina[0]))
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_rutinas_ver = CallbackQueryHandler(ver_rutina, pattern="inicio_rutinas_ver_"+str(id_rutina[0]))
		callback_query_rutinas_ver_seguir = CallbackQueryHandler(ver_rutina_seguir, pattern="inicio_rutinas_ver_seguir_"+str(id_rutina[0]))

		if not callback_query_rutinas_ver in conv_handler.states[INICIO_RUTINAS_VER]:
			conv_handler.states[INICIO_RUTINAS_VER].append(callback_query_rutinas_ver)

		if not callback_query_rutinas_ver_seguir in conv_handler.states[INICIO_RUTINAS_VER_RUTINA]:
			conv_handler.states[INICIO_RUTINAS_VER_RUTINA].append(callback_query_rutinas_ver_seguir)

	list_keyboards.append([InlineKeyboardButton("Volver a Rutinas 🔙", callback_data='back_inicio_rutinas')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])
	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="Estas son las rutinas disponibles. Puedes ver una rutina y agregarla a favoritos ⭐\n\nAgregar una rutina a favoritos ⭐ significa que te aparecerá en primero en la sección de Inicio > Rutinas y entrenamiento > Anotar rutina de hoy"
	)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Rutinas y entrenamiento > Ver rutinas de entrenamiento</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RUTINAS_VER"
	return INICIO_RUTINAS_VER

def ver_rutina(update, context):
	global current_state
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_rutina_callback = query.data
	id_rutina = id_rutina_callback.split('_',4)
	id_rutina = id_rutina[3]

	cur = db.cursor()
	cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()
	id_trainer = resultado[0][0]

	cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
	nombre = cur.fetchall()
	nombre = nombre[0][0]

	text = "🏋️‍♂️ <b>RUTINA "+nombre.upper()+"</b> 🏋️‍♂️"

	cur.execute("SELECT DISTINCT dia FROM Rutinas_ejercicios where id_rutina="+str(id_rutina)+" ORDER BY dia;")
	resultado = cur.fetchall()

	cur.close()
	db.close()

	if resultado:
		for i in range(len(resultado)):
			text=text+"\n\n"
			if resultado[i][0] == '1':
				text=text+"<b>LUNES</b>"
			elif resultado[i][0] == '2':
				text=text+"<b>MARTES</b>"
			elif resultado[i][0] == '3':
				text=text+"<b>MIÉRCOLES</b>"
			elif resultado[i][0] == '4':
				text=text+"<b>JUEVES</b>"
			elif resultado[i][0] == '5':
				text=text+"<b>VIERNES</b>"
			elif resultado[i][0] == '6':
				text=text+"<b>SÁBADO</b>"
			else:
				text=text+"<b>DOMINGO</b>"

			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
			db.begin()
			cur = db.cursor()
			cur.execute("SELECT id_ejercicio,repeticiones FROM Rutinas_ejercicios where id_rutina="+str(id_rutina)+" AND dia='"+resultado[i][0]+"';")
			ejercicios_dia = cur.fetchall()
			cur.close()
			db.close()
			for i in range(len(ejercicios_dia)):
				id_ejercicio = ejercicios_dia[i][0]
				repeticiones = ejercicios_dia[i][1]
				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				cur = db.cursor()
				cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
				nombre_ejercicio = cur.fetchall()
				nombre_ejercicio = nombre_ejercicio[0][0]
				cur.close()
				db.close()

				text=text+"\n"+nombre_ejercicio+" - "+repeticiones+" 👉 tutorial: /"+str(id_ejercicio)

	keyboard = []
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("SELECT id_rutina FROM Sigue WHERE id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()

	if not resultado:
		keyboard.append([InlineKeyboardButton("Añadir a favoritos ⭐", callback_data="inicio_rutinas_ver_seguir_"+str(id_rutina))])

	else:
		text=text+"\n\n<b>Añadida a favoritos</b>⭐"
		keyboard.append([InlineKeyboardButton("Quitar de favoritos ❌", callback_data="inicio_rutinas_ver_seguir_"+str(id_rutina))])

	keyboard.append([InlineKeyboardButton("Volver a Ver rutinas de entrenamiento 🔙", callback_data="back_inicio_rutinas_ver")])
	keyboard.append([InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data="back_inicio_rutinas")])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")])

	reply_markup = InlineKeyboardMarkup(keyboard)

	time.sleep(.8)
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup = reply_markup,
		parse_mode='HTML'
	)

	current_state = "INICIO_RUTINAS_VER_RUTINA"
	return INICIO_RUTINAS_VER_RUTINA

def ver_rutina_seguir(update, context):	
	global current_state
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_rutina_callback = query.data
	id_rutina = id_rutina_callback.split('_',5)
	id_rutina = id_rutina[4]

	cur = db.cursor()
	cur.execute("SELECT id_rutina FROM Sigue WHERE id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()

	if not resultado:
		cur.execute("INSERT INTO Sigue(id_rutina,id_usuario) VALUES (%s, %s)",(id_rutina,username_user))
		db.commit()

	else:
		cur.execute("DELETE FROM Sigue WHERE id_rutina="+str(id_rutina)+" AND id_usuario='"+username_user+"';")
		db.commit()

	cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()
	id_trainer = resultado[0][0]

	cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
	nombre = cur.fetchall()
	nombre = nombre[0][0]

	text = "🏋️‍♂️ <b>RUTINA "+nombre.upper()+"</b> 🏋️‍♂️"

	cur.execute("SELECT DISTINCT dia FROM Rutinas_ejercicios where id_rutina="+str(id_rutina)+" ORDER BY dia;")
	resultado = cur.fetchall()

	cur.close()
	db.close()

	if resultado:
		for i in range(len(resultado)):
			text=text+"\n\n"
			if resultado[i][0] == '1':
				text=text+"<b>LUNES</b>"
			elif resultado[i][0] == '2':
				text=text+"<b>MARTES</b>"
			elif resultado[i][0] == '3':
				text=text+"<b>MIÉRCOLES</b>"
			elif resultado[i][0] == '4':
				text=text+"<b>JUEVES</b>"
			elif resultado[i][0] == '5':
				text=text+"<b>VIERNES</b>"
			elif resultado[i][0] == '6':
				text=text+"<b>SÁBADO</b>"
			else:
				text=text+"<b>DOMINGO</b>"

			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
			db.begin()
			cur = db.cursor()
			cur.execute("SELECT id_ejercicio,repeticiones FROM Rutinas_ejercicios where id_rutina="+str(id_rutina)+" AND dia='"+resultado[i][0]+"';")
			ejercicios_dia = cur.fetchall()
			cur.close()
			db.close()
			for i in range(len(ejercicios_dia)):
				id_ejercicio = ejercicios_dia[i][0]
				repeticiones = ejercicios_dia[i][1]
				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				cur = db.cursor()
				cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
				nombre_ejercicio = cur.fetchall()
				nombre_ejercicio = nombre_ejercicio[0][0]
				cur.close()
				db.close()

				text=text+"\n"+nombre_ejercicio+" - "+repeticiones+" 👉 tutorial: /"+str(id_ejercicio)

	keyboard = []
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	cur = db.cursor()
	cur.execute("SELECT id_rutina FROM Sigue WHERE id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()

	if not resultado:
		keyboard.append([InlineKeyboardButton("Añadir a favoritos ⭐", callback_data="inicio_rutinas_ver_seguir_"+str(id_rutina))])

	else:
		text=text+"\n\n<b>Añadida a favoritos</b>⭐"
		keyboard.append([InlineKeyboardButton("Quitar de favoritos ❌", callback_data="inicio_rutinas_ver_seguir_"+str(id_rutina))])

	keyboard.append([InlineKeyboardButton("Volver a Ver rutinas de entrenamiento 🔙", callback_data="back_inicio_rutinas_ver")])
	keyboard.append([InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data="back_inicio_rutinas")])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")])

	reply_markup = InlineKeyboardMarkup(keyboard)

	time.sleep(.8)
	bot.edit_message_text(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text=text,
		parse_mode='HTML',
		reply_markup = reply_markup
	)

def show_inicio_rutinas_anotar(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	keyboard = []

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Rutinas y entrenamiento > Anotar rutina...</b>",
		parse_mode='HTML'
	)
	time.sleep(1)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()

	dia_hoy = date.today().weekday()+1

	if dia_hoy == 1:
		dia_semana = "Lunes"
	elif dia_hoy == 2:
		dia_semana = "Martes"
	elif dia_hoy == 3:
		dia_semana = "Miércoles"
	elif dia_hoy == 4:
		dia_semana = "Jueves"
	elif dia_hoy == 5:
		dia_semana = "Viernes"
	elif dia_hoy == 6:
		dia_semana = "Sábado"
	elif dia_hoy == 7:
		dia_semana = "Domingo"

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Estas son todas las rutinas que se pueden anotar hoy <b>"+dia_semana.upper()+"</b>",
		parse_mode='HTML'
	)

	list_keyboards=[]
	# Primero se muestran las rutinas que tiene en favoritos
	cur.execute("SELECT DISTINCT Rutinas_ejercicios.id_rutina FROM Rutinas_ejercicios INNER JOIN Sigue WHERE Rutinas_ejercicios.id_rutina=Sigue.id_rutina AND Rutinas_ejercicios.dia='"+str(dia_hoy)+"' AND Sigue.id_usuario='"+username_user+"';")
	resultado = cur.fetchall()
	cur.close()
	db.close()

	for id_rutina in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()

		cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
		resultado = cur.fetchall()
		id_trainer = resultado[0][0]

		cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
		nombre = cur.fetchall()
		nombre = nombre[0][0]

		cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()

		cur.close()
		db.close()

		name_button = "Rutina del "+dia_semana.lower()+" de "+nombre+" ⭐"
		button = InlineKeyboardButton(name_button, callback_data="inicio_rutinas_anotar_"+str(id_rutina[0]))
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_rutinas_anotar = CallbackQueryHandler(show_inicio_rutinas_anotar_rutina, pattern="inicio_rutinas_anotar_"+str(id_rutina[0]))

		if not callback_query_rutinas_anotar in conv_handler.states[INICIO_RUTINAS_ANOTAR]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR].append(callback_query_rutinas_anotar)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	# Ahora las rutinas que no tiene en favoritos
	cur.execute("SELECT DISTINCT id_rutina FROM Rutinas_ejercicios WHERE Rutinas_ejercicios.dia='"+str(dia_hoy)+"' AND id_rutina NOT IN(SELECT DISTINCT Rutinas_ejercicios.id_rutina FROM Rutinas_ejercicios INNER JOIN Sigue WHERE Rutinas_ejercicios.id_rutina=Sigue.id_rutina AND Rutinas_ejercicios.dia='6' AND Sigue.id_usuario='"+username_user+"');")
	resultado = cur.fetchall()
	cur.close()
	db.close()
	for id_rutina in resultado:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()

		cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
		resultado = cur.fetchall()
		id_trainer = resultado[0][0]

		cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
		nombre = cur.fetchall()
		nombre = nombre[0][0]

		cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()

		cur.close()
		db.close()

		name_button = "Rutina del "+dia_semana.lower()+" de "+nombre
		button = InlineKeyboardButton(name_button, callback_data="inicio_rutinas_anotar_"+str(id_rutina[0]))
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_rutinas_anotar = CallbackQueryHandler(show_inicio_rutinas_anotar_rutina, pattern="inicio_rutinas_anotar_"+str(id_rutina[0]))

		if not callback_query_rutinas_anotar in conv_handler.states[INICIO_RUTINAS_ANOTAR]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR].append(callback_query_rutinas_anotar)

	list_keyboards.append([InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data="back_inicio_rutinas")])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data="back_inicio")])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Rutinas y entrenamiento > Anotar rutina</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RUTINAS_ANOTAR"
	return INICIO_RUTINAS_ANOTAR

def show_inicio_rutinas_anotar_rutina(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	id_rutina_callback = query.data
	id_rutina = id_rutina_callback.split('_',4)
	id_rutina = id_rutina[3]

	dia_hoy = date.today().weekday()+1

	if dia_hoy == 1:
		dia_semana = "Lunes"
	elif dia_hoy == 2:
		dia_semana = "Martes"
	elif dia_hoy == 3:
		dia_semana = "Miércoles"
	elif dia_hoy == 4:
		dia_semana = "Jueves"
	elif dia_hoy == 5:
		dia_semana = "Viernes"
	elif dia_hoy == 6:
		dia_semana = "Sábado"
	elif dia_hoy == 7:
		dia_semana = "Domingo"

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()
	id_trainer = resultado[0][0]

	cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
	nombre = cur.fetchall()
	nombre = nombre[0][0]

	text = "🏋️‍♂️ <b>RUTINA DEL "+dia_semana.upper()+" DE "+nombre.upper()+"</b> 🏋️‍♂️"

	cur.execute("SELECT id_ejercicio,repeticiones FROM Rutinas_ejercicios where id_rutina="+str(id_rutina)+" AND dia='"+str(dia_hoy)+"';")
	ejercicios_dia = cur.fetchall()
	cur.close()
	db.close()

	text=text+"\n\nPulsa un ejercicio para anotarlo o desapuntarlo de hoy.\n\nUn tick ✅ indica que ya has registrado el ejercicio hoy."

	list_keyboards=[]
	for i in range(len(ejercicios_dia)):
		id_ejercicio = ejercicios_dia[i][0]
		repeticiones = ejercicios_dia[i][1]
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		nombre_ejercicio = cur.fetchall()
		nombre_ejercicio = nombre_ejercicio[0][0]

		cur.execute("SELECT * FROM Hace_rutina WHERE fecha=CURDATE() AND id_rutina="+str(id_rutina)+" AND id_ejercicio="+str(id_ejercicio)+" AND dia='"+str(dia_hoy)+"' AND id_usuario='"+username_user+"';")
		ya_hecho = cur.fetchall()

		cur.close()
		db.close()

		name_button = nombre_ejercicio+" - "+repeticiones
		name_button = name_button+" 👉 tutorial: /"+str(id_ejercicio)
		if ya_hecho:
			name_button = name_button+" ✅"

		button = InlineKeyboardButton(name_button, callback_data="inicio_rutinas_anotar_"+str(id_rutina[0])+"_"+str(id_ejercicio)+"_"+str(dia_hoy))
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_rutinas_anotar_rutina = CallbackQueryHandler(anotar_ejercicio_rutina, pattern="inicio_rutinas_anotar_"+str(id_rutina[0])+"_"+str(id_ejercicio)+"_"+str(dia_hoy))

		if not callback_query_rutinas_anotar_rutina in conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA].append(callback_query_rutinas_anotar_rutina)

	time.sleep(.8)
	
	list_keyboards.append([InlineKeyboardButton("Volver a Anotar rutina de hoy 🔙", callback_data='back_inicio_rutinas_anotar')])
	list_keyboards.append([InlineKeyboardButton("Vover a Rutinas y entrenamiento 🔙", callback_data='back_inicio_rutinas')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

	current_state = "INICIO_RUTINAS_ANOTAR_RUTINA"
	return INICIO_RUTINAS_ANOTAR_RUTINA

def anotar_ejercicio_rutina(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	callback_data = query.data
	callback_data = callback_data.split('_',6)
	id_rutina = callback_data[3]
	id_ejercicio = callback_data[4]
	dia = callback_data[5]

	if dia == '1':
		dia_semana = "Lunes"
	elif dia == '2':
		dia_semana = "Martes"
	elif dia == '3':
		dia_semana = "Miércoles"
	elif dia == '4':
		dia_semana = "Jueves"
	elif dia == '5':
		dia_semana = "Viernes"
	elif dia == '6':
		dia_semana = "Sábado"
	elif dia == '7':
			dia_semana = "Domingo"

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT * FROM Hace_rutina WHERE fecha=CURDATE() AND id_rutina="+id_rutina+" AND id_ejercicio="+str(id_ejercicio)+" AND dia='"+dia+"' AND id_usuario='"+username_user+"';")
	ya_hecho = cur.fetchall()
	if ya_hecho:
		cur.execute("DELETE FROM Hace_rutina WHERE fecha=CURDATE() AND id_rutina="+id_rutina+" AND id_ejercicio="+str(id_ejercicio)+" AND dia='"+dia+"' AND id_usuario='"+username_user+"';")
		db.commit()
	else:
		cur.execute("INSERT INTO Hace_rutina(id_rutina,id_usuario,fecha,dia,id_ejercicio) VALUES(%s, %s, %s, %s, %s)",(id_rutina,username_user,date.today(),dia,id_ejercicio))
		db.commit()

	cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina)+";")
	resultado = cur.fetchall()
	id_trainer = resultado[0][0]

	cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
	nombre = cur.fetchall()
	nombre = nombre[0][0]

	text = "🏋️‍♂️ <b>RUTINA DEL "+dia_semana.upper()+" DE "+nombre.upper()+"</b> 🏋️‍♂️"

	cur.execute("SELECT id_ejercicio,repeticiones FROM Rutinas_ejercicios where id_rutina="+id_rutina+" AND dia='"+dia+"';")
	ejercicios_dia = cur.fetchall()
	cur.close()
	db.close()

	text=text+"\n\nPulsa un ejercicio para anotarlo o desapuntarlo de hoy.\n\nUn tick ✅ indica que ya has registrado el ejercicio hoy."

	list_keyboards=[]
	for i in range(len(ejercicios_dia)):
		id_ejercicio = ejercicios_dia[i][0]
		repeticiones = ejercicios_dia[i][1]
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
		nombre_ejercicio = cur.fetchall()
		nombre_ejercicio = nombre_ejercicio[0][0]

		name_button = nombre_ejercicio+" - "+repeticiones
		cur.execute("SELECT * FROM Hace_rutina WHERE fecha=CURDATE() AND id_rutina="+id_rutina+" AND id_ejercicio="+str(id_ejercicio)+" AND dia='"+dia+"' AND id_usuario='"+username_user+"';")
		ya_hecho = cur.fetchall()

		name_button = name_button+" 👉 tutorial: /"+str(id_ejercicio)
		if ya_hecho:
			name_button = name_button+" ✅"

		cur.close()
		db.close()

		button = InlineKeyboardButton(name_button, callback_data="inicio_rutinas_anotar_"+str(id_rutina[0])+"_"+str(id_ejercicio)+"_"+dia)
		keyboard = []
		keyboard.append(button)
		list_keyboards.append(keyboard)
		callback_query_rutinas_anotar_rutina = CallbackQueryHandler(anotar_ejercicio_rutina, pattern="inicio_rutinas_anotar_"+str(id_rutina[0])+"_"+str(id_ejercicio)+"_"+dia)

		if not callback_query_rutinas_anotar_rutina in conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA].append(callback_query_rutinas_anotar_rutina)

	time.sleep(.8)
	
	list_keyboards.append([InlineKeyboardButton("Volver a Anotar rutina de hoy 🔙", callback_data='back_inicio_rutinas_anotar')])
	list_keyboards.append([InlineKeyboardButton("Vover a Rutinas y entrenamiento 🔙", callback_data='back_inicio_rutinas')])
	list_keyboards.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(list_keyboards)
	bot.edit_message_text(
		chat_id = query.message.chat_id,
		message_id = query.message.message_id,
		text=text,
		reply_markup=reply_markup,
		parse_mode='HTML'
	)

def show_inicio_rutinas_consultar(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Rutinas y entrenamiento > Consultar entrenamiento de otro día...</b>",
		parse_mode='HTML'
	)
	time.sleep(1)

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	# Entrenamiento más reciente
	cur.execute("SELECT DISTINCT id_rutina,fecha FROM Hace_rutina WHERE fecha=(SELECT MAX(fecha) FROM Hace_rutina WHERE id_usuario='"+username_user+"' AND fecha <= CURDATE()) AND id_usuario='"+username_user+"' ORDER BY id_rutina;")
	rutinas = cur.fetchall()
	fecha = rutinas[0][1]

	cur.close()
	db.close()

	text="<b>ÚLTIMO ENTRENAMIENTO REGISTRADO:</b>\n\n"
	if fecha == date.today():
		text=text+"<b>HOY DÍA "+date.today().strftime('%d-%B-%Y').upper()+":</b>"
	else:
		text=text+"<b>EL DÍA "+fecha.strftime('%d-%B-%Y').upper()+":</b>"

	for id_rutina in rutinas:
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
		resultado = cur.fetchall()
		id_trainer = resultado[0][0]

		cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
		nombre = cur.fetchall()
		nombre = nombre[0][0]

		dia_hoy = fecha.weekday()+1
		if dia_hoy == 1:
			dia_semana = "Lunes"
		elif dia_hoy == 2:
			dia_semana = "Martes"
		elif dia_hoy == 3:
			dia_semana = "Miércoles"
		elif dia_hoy == 4:
			dia_semana = "Jueves"
		elif dia_hoy == 5:
			dia_semana = "Viernes"
		elif dia_hoy == 6:
			dia_semana = "Sábado"
		elif dia_hoy == 7:
			dia_semana = "Domingo"

		text=text+"\n\n📌 <b>Ejercicios hechos de la rutina del "+dia_semana.lower()+" de "+nombre+"</b>"
		cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
		esta_apuntado = cur.fetchall()
		if esta_apuntado:
			text=text+" ⭐"
		cur.execute("SELECT id_ejercicio FROM Hace_rutina WHERE fecha='"+str(fecha)+"' AND id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina[0])+";")
		ejercicios = cur.fetchall()
		cur.close()
		db.close()
		for i in range(len(ejercicios)):
			id_ejercicio = ejercicios[i][0]
			
			db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
			db.begin()
			cur = db.cursor()
			cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
			nombre_ejercicio = cur.fetchall()
			nombre_ejercicio = nombre_ejercicio[0][0]

			cur.execute("SELECT repeticiones FROM Rutinas_ejercicios WHERE id_ejercicio="+str(id_ejercicio)+" AND id_rutina="+str(id_rutina[0])+" AND dia='"+str(dia_hoy)+"';")
			repeticiones = cur.fetchall()
			repeticiones = repeticiones[0][0]

			cur.close()
			db.close()

			text=text+"\n"+nombre_ejercicio+" - "+repeticiones+" 👉 tutorial: /"+str(id_ejercicio)

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	bot.send_message(
		chat_id = query.message.chat_id,
		text="Puedes consultar el entrenamiento de otro día con el comando /consultar <dd-mm-yyyy>.\n\nEjemplo: /consultar 01-01-2020"
	)

	keyboard = []
	keyboard.append([InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data='back_inicio_rutinas')])
	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Rutinas y entrenamiento > Consultar entrenamiento de otro día</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_RUTINAS_CONSULTAR"
	return INICIO_RUTINAS_CONSULTAR

def rutinas_consultar_fecha(update, context):
	global current_state
	username_user = update.message.from_user.username

	n_params = context.args

	keyboard = [[InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data='back_inicio_rutinas')]]
	reply_markup = InlineKeyboardMarkup(keyboard)

	if len(n_params) != 1:
		update.message.reply_text(
			text="Has introducido mal el comando.\n\nEjemplo: /consultar 01-01-2019",
			reply_markup=reply_markup
		)
	else:
		fecha_string = context.args[0]

		if is_valid_date(fecha_string):
			fecha_len = len(fecha_string)

			if fecha_len != 10:
				update.message.reply_text(
					text="Utiliza el formato dd-mm-yyyy. Prueba el comando /consultar de nuevo.",
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

				db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
				db.begin()
				cur = db.cursor()

				# Entrenamiento de ese día
				cur.execute("SELECT DISTINCT id_rutina,fecha FROM Hace_rutina WHERE fecha='"+fecha1+"' AND id_usuario='"+username_user+"' ORDER BY id_rutina;")
				rutinas = cur.fetchall()

				cur.close()
				db.close()

				if rutinas:
					fecha = rutinas[0][1]
					text="<b>EL DÍA "+fecha.strftime('%d-%B-%Y').upper()+" HICISTE LO SIGUIENTE:</b>"
					for id_rutina in rutinas:
						db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
						db.begin()
						cur = db.cursor()
						cur.execute("SELECT id_trainer FROM Ofrecen where id_rutina="+str(id_rutina[0])+";")
						resultado = cur.fetchall()
						id_trainer = resultado[0][0]

						cur.execute("SELECT nombre FROM Trainers where id_trainer="+str(id_trainer)+";")
						nombre = cur.fetchall()
						nombre = nombre[0][0]

						dia_hoy = fecha.weekday()+1
						if dia_hoy == 1:
							dia_semana = "Lunes"
						elif dia_hoy == 2:
							dia_semana = "Martes"
						elif dia_hoy == 3:
							dia_semana = "Miércoles"
						elif dia_hoy == 4:
							dia_semana = "Jueves"
						elif dia_hoy == 5:
							dia_semana = "Viernes"
						elif dia_hoy == 6:
							dia_semana = "Sábado"
						elif dia_hoy == 7:
							dia_semana = "Domingo"

						text=text+"\n\n📌 <b>Ejercicios hechos de la rutina del "+dia_semana.lower()+" de "+nombre+"</b>"
						cur.execute("SELECT id_rutina FROM Sigue where id_rutina="+str(id_rutina[0])+" AND id_usuario='"+username_user+"';")
						esta_apuntado = cur.fetchall()
						if esta_apuntado:
							text=text+" ⭐"
						cur.execute("SELECT id_ejercicio FROM Hace_rutina WHERE fecha='"+str(fecha)+"' AND id_usuario='"+username_user+"' AND id_rutina="+str(id_rutina[0])+";")
						ejercicios = cur.fetchall()
						cur.close()
						db.close()
						for i in range(len(ejercicios)):
							id_ejercicio = ejercicios[i][0]
							
							db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
							db.begin()
							cur = db.cursor()
							cur.execute("SELECT nombre FROM Ejercicios where id_ejercicio="+str(id_ejercicio)+";")
							nombre_ejercicio = cur.fetchall()
							nombre_ejercicio = nombre_ejercicio[0][0]

							cur.execute("SELECT repeticiones FROM Rutinas_ejercicios WHERE id_ejercicio="+str(id_ejercicio)+" AND id_rutina="+str(id_rutina[0])+" AND dia='"+str(dia_hoy)+"';")
							repeticiones = cur.fetchall()
							repeticiones = repeticiones[0][0]

							cur.close()
							db.close()

							text=text+"\n"+nombre_ejercicio+" - "+repeticiones+" 👉 tutorial: /"+str(id_ejercicio)

				else:
					text="No hay ningún entrenamiento registrado el día "+fecha_date.strftime('%d-%B-%Y')

				update.message.reply_text(
					text=text,
					parse_mode='HTML'
				)

				update.message.reply_text(
					text="Puedes seguir consultando otras fechas",
					parse_mode='HTML'
				)

				keyboard = []
				keyboard.append([InlineKeyboardButton("Volver a Rutinas y entrenamiento 🔙", callback_data='back_inicio_rutinas')])
				keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(
					text="<b>👣 Inicio > Rutinas y entrenamiento > Consultar entrenamiento de otro día</b>",
					parse_mode='HTML',
					reply_markup=reply_markup
				)

		else:
			update.message.reply_text(
				text="No has introducido una fecha. Utiliza el formato dd-mm-yyyy.",
				reply_markup=reply_markup
			)

############# SOPORTE #############
def show_inicio_soporte(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>⏳ Cargando Inicio > Soporte...</b>",
		parse_mode='HTML'
	)
	time.sleep(1)

	keyboard = [
		[InlineKeyboardButton("Acerca de 📖", callback_data='inicio_soporte_acerca')],
		[InlineKeyboardButton("Qué es ImagymBot ❓", callback_data='inicio_soporte_que')],
		[InlineKeyboardButton("Política de protección de datos 📚", callback_data='inicio_soporte_politica')],
		[InlineKeyboardButton("Ayuda en Mi objetivo de peso 🆘", callback_data='inicio_soporte_peso')],
		[InlineKeyboardButton("Ayuda en Mi objetivo de actividades cardio 🆘", callback_data='inicio_soporte_cardio')],
		[InlineKeyboardButton("Ayuda en Retos 🆘", callback_data='inicio_soporte_retos')],
		[InlineKeyboardButton("Ayuda en Ejercicio del mes 🆘", callback_data='inicio_soporte_ejercicio')],
		[InlineKeyboardButton("Ayuda en Rutinas y entrenamiento 🆘", callback_data='inicio_soporte_rutinas')],
		[InlineKeyboardButton("Ayuda en Mi ficha personal 🆘", callback_data='inicio_soporte_ficha')],
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)

	current_state = "INICIO_SOPORTE"
	return INICIO_SOPORTE

def show_inicio_soporte_que(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>ImagymBot</b> es un divulgador de gimnasios. Cada gimnasio ofrece sus propios retos, ejercicios del mes y actividades cardio que quiera ofrecer a sus clientes. Los clientes podrán ver todo ese contenido desde <b>ImagymBot</b> y ser partícipe de una nueva experiencia como usuario de un gimnasio."

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Qué es ImagymBot</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_acerca(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>ImagymBot</b> forma parte del <b>Trabajo de Fin de Grado</b> de Juan Manuel Castillo Nievas en el <b>Grado en Ingeniería Informática</b> en la <b>Universidad de Granada</b>"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Acerca de</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_politica(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Para qué se utilizan tus datos personales?</b>\n\nTodos los datos personales son opcionales y puedes proporcionarlos o no. Proporcionando tus datos personales te ofrecemos una mejor experiencia en <b>ImagymBot</b>, así como más información precisa como el cálculo del IMC.\n\nProporcionando tu correo electrónico podrás estar al día de todas las ofertas y suscripciones de tu gimnasio, así como del nuevo contenido que ofrecen a <b>ImagymBot</b>"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_peso(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en MI OBJETIVO DE PESO?</b>\n\n👉 En esta sección podrás anotar diariamente tu peso, porcentaje de grasa y porcentaje de músculo.\n👉 También podrás establecer un objetivo de cada uno de ellos en el plazo que tú decidas.\n👉 Puedes ver tu evolución de cada medida en una gráfica que puedes filtrar por fechas."

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Mi objetivo de peso</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_cardio(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en MI OBJETIVO DE ACTIVIDADES CARDIO?</b>\n\n👉 En esta sección podrás anotar las actividades cardio que has hecho en el gimnasio. Podrás registrar una actividad cardio que esté disponible en tu gimnasio.\n👉 También puedes establecer un objetivo de una actividad cardio, que consiste en hacer un mínimo de minutos, kilómetros o calorías a lo largo de un mes. Este objetivo es personal y sólo tú podrás verlo.\n👉 Puedes comprobar todas las actividades cardio que hiciste en un día concreto."

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Mi objetivo de actividades cardio</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_retos(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en RETOS?</b>\n\nLos retos consisten en un ejercicio propuesto por tu gimnasio durante un mes. Cada día deberás hacer un número de repeticiones de ese ejercicio. Se pueden apuntar todos los usuarios del gimnasio que quieran. El objetivo es completar todos los días del reto.👉 Cada día deberás anotar que has hecho las repeticiones del reto\n👉 No anotar las repeticiones un día supone la descalificación del reto\n👉 Completar todo el reto supone la obtención de una insignia que todos podrán ver en el perfil de la web"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Retos</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_ejercicio(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en EJERCICIO DEL MES?</b>\n\nEl ejercicio del mes lo propone el gimnasio. Consiste en completar un objetivo de una actividad cardio específica a lo largo de un mes.\n👉 Un ejercicio del mes puede ser hacer mínimo de 500 minutos en elíptica, por ejemplo\n👉 Cada vez que registres cardio de esa actividad, se sumarán puntos a tu marcador. Para comprobar la veracidad de ello, deberás aportar una foto de la pantalla de la máquina en la que se muestre lo que has hecho.\n👉 Cuando se acabe el mes, se hará un ranking del TOP 10 con los usuarios con más puntos"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Ejercicio del mes</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_rutinas(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en RUTINAS Y ENTRENAMIENTO?</b>\n\n👉 Cada monitor o monitora del gimnasio ofrecerá su rutina a los usuarios.\n👉 Tendrás acceso a todas las rutinas, pudiendo añadir a favoritos las que más te gusten.\n👉 Puedes anotar la rutina de hoy. Al anotar la rutina de hoy se mostrarán todas las rutinas que tienen algún ejercicio para el día actual de la semana. Por ejemplo, si es martes, aparecerán todas las rutinas que tengan ejercicios los martes.\n👉 Puedes anotar diferentes ejercicios de diferentes rutinas\n👉 Podrás consultar los ejercicios y rutinas que hiciste en un día concreto"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Rutinas y entrenamiento</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def show_inicio_soporte_ficha(update, context):
	global current_state

	query = update.callback_query
	bot = context.bot
	username_user = query.from_user.username

	text="<b>¿Qué puedes hacer en MI FICHA PERSONAL?</b>\n\n👉 Aquí podrás añadir/modificar tus datos personales.\n👉 También podrás ver una valoración de tu IMC actual, siempre que hayas anotado un peso y tu altura"

	bot.send_message(
		chat_id = query.message.chat_id,
		text=text,
		parse_mode='HTML'
	)

	keyboard = [
		[InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(
		chat_id = query.message.chat_id,
		text="<b>👣 Inicio > Soporte > Ayuda en Mi ficha personal</b>",
		parse_mode='HTML',
		reply_markup=reply_markup
	)
	time.sleep(1)

def ver_ejercicio(update, context):
	id_ejercicio = update.message.text[1:]
	image_path = "/home/castinievas/ImagymBot/ejercicios/"+id_ejercicio+".jpeg"
	if path.exists(image_path):
		update.message.reply_text(
			text="<b>⏳ Cargando imagen...</b>",
			parse_mode='HTML'
		)
		db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
		db.begin()
		cur = db.cursor()
		cur.execute("SELECT nombre FROM Ejercicios WHERE id_ejercicio="+id_ejercicio+";")
		resultado = cur.fetchall()
		nombre = resultado[0][0]
		cur.close()
		db.close()
		update.message.reply_text(
			text="<b>👇 "+nombre+"</b>",
			parse_mode='HTML'
		)
		pic = open(image_path, 'rb')
		update.message.reply_photo(
			photo = pic
		)
	else:
		update.message.reply_text(
			text="Ese id de ejercicio no existe."
		)


def inicio_ficha(update, context):
	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	update.message.reply_text(
		text="<b>⏳ Cargando Inicio > Mi ficha personal...</b>",
		parse_mode='HTML'
	)

	# Obtener datos
	username_user = update.message.from_user.username

	# IMC más reciente
	cur = db.cursor()
	cur.execute("SELECT imc FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"' AND imc IS NOT NULL)")
	imc = cur.fetchall()
	text="Pulsa un botón para cambiar la información"

	if imc:
		imc = imc[0][0]
		text=text+"\n\n<b>👉Tu IMC actual:</b> "+str(imc)

	update.message.reply_text(
		text=text,
		parse_mode='HTML'
	)

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
			peso = str(resultado[0][0])+"kg 👉 "
			fecha = resultado[0][1]
			if fecha == date.today():
				fecha = "Registrado hoy"
			else:
				fecha = "Registrado el día "+fecha.strftime("%d-%B-%Y")

	cur.close()
	db.close()

	keyboard = [
		[InlineKeyboardButton("Peso: "+peso+fecha, callback_data='inicio_ficha_peso')],
		[InlineKeyboardButton("Altura: "+altura, callback_data='inicio_ficha_altura')],
		[InlineKeyboardButton("Fecha nacimiento: "+fecha_nacimiento, callback_data='inicio_ficha_nacimiento')],
		[InlineKeyboardButton("Género: "+genero, callback_data='inicio_ficha_genero')],
		[InlineKeyboardButton("Correo electrónico: "+email, callback_data='inicio_ficha_email')],
	]

	if imc:
		keyboard.append([InlineKeyboardButton("Valoración del IMC 🗨", callback_data='inicio_ficha_valoracion')])

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	update.message.reply_text(
		text="Pulsa un botón para cambiar la información"
	)

	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
		text="<b>👣 Inicio > Mi ficha personal</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

def inicio_peso(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	update.message.reply_text(
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso...</b>",
		parse_mode='HTML'
	)

	# Peso más reciente
	username_user = update.message.from_user.username
	cur = db.cursor()
	cur.execute("SELECT peso,grasa,musculo,fecha,hora FROM Peso WHERE id_usuario='"+username_user+"' AND fecha=(SELECT MAX(p2.fecha) FROM Peso p2 WHERE id_usuario='"+username_user+"')")
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
			fecha = resultado[0][3]

			if fecha == date.today():
				fecha = "hoy"
			else:
				fecha = fecha.strftime("%d-%b-%Y")

			text="📌 Última vez que anotaste datos: "+fecha
			if peso is not None:
				text=text+"\n\nPeso: "+str(peso)+"kg"
			else:
				text=text+"\n\nPeso: sin datos"

			if grasa is not None:
				text=text+"\nGrasa: "+str(grasa)+"%"
			else:
				text=text+"\nGrasa: sin datos"

			if musculo is not None:
				text=text+"\nMúsculo: "+str(musculo)+"%"
			else:
				text=text+"\nMúsculo: sin datos"

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

				text="📌 Actualmente tienes un <b>objetivo de "+tipo+"</b>.\n\nÚltimo registro de "+tipo+": "+str(peso)+medida+"\nTu objetivo: "+str(peso_objetivo)+medida
				text=text+"\nTe queda: "+str(diferencia_peso)+medida
				text=text+"\nFecha inicio: "+fecha_inicio+"\nFecha fin: "+fecha_fin

				keyboard.append([InlineKeyboardButton("Eliminar objetivo 🏁", callback_data='inicio_peso_eliminar')])
				keyboard.append([InlineKeyboardButton("Evolución 📉", callback_data='inicio_peso_evolucion')])

				time.sleep(.8)
				update.message.reply_text(
					text=text,
					parse_mode='HTML'
				)

	keyboard.append([InlineKeyboardButton("Volver a Inicio 👣", callback_data='back_inicio')])

	cur.close()
	db.close()

	time.sleep(.8)
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
		text="<b>👣 Inicio > Mi objetivo de peso</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO"
	return INICIO_PESO

def inicio_peso_anotar(update, context):
	global current_state

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()

	update.message.reply_text(
		text="<b>⏳ Cargando Inicio > Mi objetivo de peso > Anotar datos...</b>",
		parse_mode='HTML'
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
				text=text+"\nPeso: "+str(peso)+"kg"
				keyboard.append([InlineKeyboardButton("Modificar peso", callback_data='inicio_peso_anotar_peso')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar peso ✏", callback_data='inicio_peso_anotar_peso')])


			if resultado[0][1] is not None:
				grasa = resultado[0][1]
				text=text+"\nGrasa: "+str(grasa)+"%"
				keyboard.append([InlineKeyboardButton("Modificar grasa", callback_data='inicio_peso_anotar_grasa')])
			else:
				keyboard.append([InlineKeyboardButton("Anotar grasa ✏", callback_data='inicio_peso_anotar_grasa')])

			if resultado[0][2] is not None:
				musculo = resultado[0][2]
				text=text+"\nMúsculo: "+str(musculo)+"%"
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
		text="<b>👣 Inicio > Mi objetivo de peso > Anotar datos</b>",
		parse_mode='HTML',
		reply_markup = reply_markup
	)

	current_state = "INICIO_PESO_ANOTAR"
	return INICIO_PESO_ANOTAR

def actualizar_ejercicios():
	global conv_handler

	db = pymysql.connect("castinievas.mysql.eu.pythonanywhere-services.com", "castinievas", "password2020", "castinievas$Imagym")
	db.begin()
	cur = db.cursor()
	cur.execute("SELECT id_ejercicio FROM Ejercicios;")
	ejercicios = cur.fetchall()

	for ejercicio in ejercicios:
		handler_ejercicio = CommandHandler(str(ejercicio[0]), ver_ejercicio)
		handler_fallback = CommandHandler(str(ejercicio[0]), usuario_usa_comando_anterior)

		if not handler_fallback in conv_handler.fallbacks:
			conv_handler.fallbacks.append(handler_fallback)

		if not handler_ejercicio in conv_handler.states[INICIO_RUTINAS]:
			conv_handler.states[INICIO_RUTINAS].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RUTINAS_VER]:
			conv_handler.states[INICIO_RUTINAS_VER].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RUTINAS_VER_RUTINA]:
			conv_handler.states[INICIO_RUTINAS_VER_RUTINA].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RUTINAS_ANOTAR]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA]:
			conv_handler.states[INICIO_RUTINAS_ANOTAR_RUTINA].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RETOS_VER_RETO]:
			conv_handler.states[INICIO_RETOS_VER_RETO].append(handler_ejercicio)

		if not handler_ejercicio in conv_handler.states[INICIO_RETOS]:
			conv_handler.states[INICIO_RETOS].append(handler_ejercicio)

def error(update, context):
	"""Log Errors caused by Updates."""

	try:
		update.message.reply_text(
			text="¡Lo siento! No te he entendido. Puedes reiniciarme usando /start"
		)
	except:
		pass

	try:
		query = update.callback_query
		bot = context.bot
		bot.send_message(
			chat_id=query.message.chat_id,
			text="¡Lo siento! Algo ha salido mal. Puedes reiniciarme usando /start"
		)
	except:
		pass
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
	global conv_handler

	updater = Updater('984370362:AAHLDLk5DzZT7cx-z03NsecK_muV_h1NGMU', use_context=True)

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start',start),
						CommandHandler('ejercicios', actualizar_ejercicios),
						MessageHandler(Filters.text & (~Filters.command), any_message_start)],
		states={
			WELCOME: [
					MessageHandler(Filters.text & (~Filters.command), any_message)],

			WELCOME_PRESS_START: [
								MessageHandler(Filters.text & (~Filters.command), any_message),
								CallbackQueryHandler(show_inicio, pattern='start_menu')],

			INICIO: [
					MessageHandler(Filters.text & (~Filters.command), any_message),
					CallbackQueryHandler(show_inicio_peso, pattern='inicio_peso'),
					CallbackQueryHandler(show_inicio_cardio, pattern='inicio_cardio'),
					CallbackQueryHandler(show_inicio_retos, pattern='inicio_retos'),
					CallbackQueryHandler(show_inicio_ejercicio, pattern='inicio_ejercicio'),
					CallbackQueryHandler(show_inicio_rutinas, pattern='inicio_rutinas'),
					CallbackQueryHandler(show_inicio_ficha, pattern='inicio_ficha'),
					CallbackQueryHandler(show_inicio, pattern='show_inicio'),
					CallbackQueryHandler(show_inicio_soporte, pattern='inicio_soporte'),
					],

			INICIO_FICHA: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(anotar_peso, pattern='inicio_ficha_peso'),
						CallbackQueryHandler(modify_altura, pattern='inicio_ficha_altura'),
						CallbackQueryHandler(modify_nacimiento, pattern='inicio_ficha_nacimiento'),
						CallbackQueryHandler(modify_genero, pattern='inicio_ficha_genero'),
						CallbackQueryHandler(modify_email, pattern='inicio_ficha_email'),
						CallbackQueryHandler(show_inicio_ficha_valoracion, pattern='inicio_ficha_valoracion'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_FICHA_VALORACION: [
					CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha'),
					CallbackQueryHandler(show_inicio, pattern='back_inicio'),
					MessageHandler(Filters.text & (~Filters.command), any_message)
					],

			INICIO_FICHA_PESO: [
								MessageHandler(Filters.text & (~Filters.command), check_anotar_peso),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_ALTURA: [
								MessageHandler(Filters.text & (~Filters.command), check_altura),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_NACIMIENTO: [
									MessageHandler(Filters.text & (~Filters.command), check_nacimiento),
									CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
									],

			INICIO_FICHA_GENERO: [
								MessageHandler(Filters.text & (~Filters.command), any_message),
								CallbackQueryHandler(check_genero_hombre, pattern='select_genero_hombre'),
								CallbackQueryHandler(check_genero_mujer, pattern='select_genero_mujer'),
								CallbackQueryHandler(check_genero_otro, pattern='select_genero_otro'),
								CallbackQueryHandler(check_genero_sin, pattern='select_genero_sin'),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_FICHA_EMAIL: [
								MessageHandler(Filters.text & (~Filters.command), check_email),
								CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
								],

			INICIO_PESO: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_peso_anotar, pattern='inicio_peso_anotar'),
						CallbackQueryHandler(show_inicio_peso_establecer, pattern='inicio_peso_establecer'),
						CallbackQueryHandler(show_inicio_peso_eliminar, pattern='inicio_peso_eliminar'),
						CallbackQueryHandler(show_inicio_peso_evolucion, pattern='inicio_peso_evolucion'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ANOTAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(anotar_peso, pattern='inicio_peso_anotar_peso'),
						CallbackQueryHandler(anotar_grasa, pattern='inicio_peso_anotar_grasa'),
						CallbackQueryHandler(anotar_musculo, pattern='inicio_peso_anotar_musculo'),
						CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ANOTAR_PESO: [
									MessageHandler(Filters.text & (~Filters.command), check_anotar_peso),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ANOTAR_PESO_ALTURA: [
									MessageHandler(Filters.text & (~Filters.command), check_altura),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_FICHA_PESO_ALTURA: [
									MessageHandler(Filters.text & (~Filters.command), check_altura),
									CallbackQueryHandler(show_inicio_ficha, pattern='back_inicio_ficha')
									],

			INICIO_PESO_ANOTAR_GRASA: [
									MessageHandler(Filters.text & (~Filters.command), check_anotar_grasa),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ANOTAR_MUSCULO: [
									MessageHandler(Filters.text & (~Filters.command), check_anotar_musculo),
									CallbackQueryHandler(show_inicio_peso_anotar, pattern='back_inicio_peso_anotar')
									],

			INICIO_PESO_ESTABLECER: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(objetivo_peso, pattern='inicio_peso_establecer_peso'),
						CallbackQueryHandler(objetivo_grasa, pattern='inicio_peso_establecer_grasa'),
						CallbackQueryHandler(objetivo_musculo, pattern='inicio_peso_establecer_musculo'),
						CallbackQueryHandler(show_inicio_peso_anotar, pattern='inicio_peso_anotar'),
						CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_PESO_ESTABLECER_PESO: [
									MessageHandler(Filters.text & (~Filters.command), check_objetivo_peso),
									CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_PESO_TIEMPO: [
												MessageHandler(Filters.text & (~Filters.command), any_message),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_1'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_2'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_3'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_4'),
												CallbackQueryHandler(objetivo_peso_tiempo, pattern='objetivo_peso_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_GRASA: [
									MessageHandler(Filters.text & (~Filters.command), check_objetivo_grasa),
									CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_GRASA_TIEMPO: [
												MessageHandler(Filters.text & (~Filters.command), any_message),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_1'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_2'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_3'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_4'),
												CallbackQueryHandler(objetivo_grasa_tiempo, pattern='objetivo_grasa_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_MUSCULO: [
											MessageHandler(Filters.text & (~Filters.command), check_objetivo_musculo),
											CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
									],

			INICIO_PESO_ESTABLECER_MUSCULO_TIEMPO: [
												MessageHandler(Filters.text & (~Filters.command), any_message),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_1'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_2'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_3'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_4'),
												CallbackQueryHandler(objetivo_musculo_tiempo, pattern='objetivo_musculo_5'),
												CallbackQueryHandler(show_inicio_peso_establecer, pattern='back_inicio_peso_establecer')
												],

			INICIO_PESO_ESTABLECER_PESO_TIEMPO_CONFIRMAR: [
														MessageHandler(Filters.text & (~Filters.command), any_message),
														CallbackQueryHandler(objetivo_peso_tiempo_si, pattern='objetivo_peso_tiempo_si'),
														CallbackQueryHandler(objetivo_peso_tiempo_no, pattern='objetivo_peso_tiempo_no')
														],

			INICIO_PESO_ELIMINAR: [
								MessageHandler(Filters.text & (~Filters.command), any_message),
								CallbackQueryHandler(objetivo_peso_eliminar_si, pattern='objetivo_peso_eliminar_si'),
								CallbackQueryHandler(objetivo_peso_eliminar_no, pattern='objetivo_peso_eliminar_no')
								],

			INICIO_PESO_EVOLUCION: [
								MessageHandler(Filters.text & (~Filters.command), any_message),
								CallbackQueryHandler(evolucion_peso, pattern='inicio_peso_evolucion_peso'),
								CallbackQueryHandler(evolucion_grasa, pattern='inicio_peso_evolucion_grasa'),
								CallbackQueryHandler(evolucion_musculo, pattern='inicio_peso_evolucion_musculo'),
								CallbackQueryHandler(evolucion_imc, pattern='inicio_peso_evolucion_imc'),
								CallbackQueryHandler(show_inicio_peso, pattern='back_inicio_peso'),
								CallbackQueryHandler(show_inicio, pattern='back_inicio')
								],

			INICIO_PESO_EVOLUCION_PESO: [
										MessageHandler(Filters.text & (~Filters.command), any_message),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_peso_rango)
										],

			INICIO_PESO_EVOLUCION_GRASA: [
										MessageHandler(Filters.text & (~Filters.command), any_message),
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_grasa_rango)
										],

			INICIO_PESO_EVOLUCION_MUSCULO: [
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_musculo_rango),
										MessageHandler(Filters.text & (~Filters.command), any_message)
										],

			INICIO_PESO_EVOLUCION_IMC: [
										CallbackQueryHandler(show_inicio_peso_evolucion, pattern='back_inicio_peso_evolucion'),
										CommandHandler("rango", evolucion_imc_rango),
										MessageHandler(Filters.text & (~Filters.command), any_message)
										],

			INICIO_CARDIO: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_cardio_registrar, pattern='inicio_cardio_registrar'),
						CallbackQueryHandler(show_inicio_cardio_ver, pattern='inicio_cardio_ver'),
						CallbackQueryHandler(show_inicio_cardio_establecer, pattern='inicio_cardio_establecer'),
						CallbackQueryHandler(show_inicio_cardio_eliminar, pattern='inicio_cardio_eliminar'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_REGISTRAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_REGISTRAR_ACTIVIDAD: [
									CommandHandler("cardio", registrar_cardio),
									CallbackQueryHandler(show_inicio_cardio_registrar, pattern='back_inicio_cardio_registrar'),
									MessageHandler(Filters.text & (~Filters.command), any_message),
									],

			INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR: [
														CallbackQueryHandler(registrar_cardio_si, pattern='registrar_cardio_si'),
														CallbackQueryHandler(registrar_cardio_no, pattern='registrar_cardio_no'),
														MessageHandler(Filters.text & (~Filters.command), any_message),
														],

			INICIO_CARDIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO: [
														MessageHandler(Filters.photo, check_photo),
														CallbackQueryHandler(registrar_cardio_si, pattern='registrar_cardio_si'),
														CallbackQueryHandler(registrar_cardio_no, pattern='registrar_cardio_no'),
														CallbackQueryHandler(show_inicio_cardio, pattern='inicio_cardio'),
														CallbackQueryHandler(show_inicio, pattern='back_inicio'),
														MessageHandler(Filters.text & (~Filters.command), any_message),
														],


			INICIO_CARDIO_VER: [
							CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
							CallbackQueryHandler(show_inicio, pattern='back_inicio'),
							CommandHandler("consultar", ver_cardio_rango),
							MessageHandler(Filters.text & (~Filters.command), any_message),
							],

			INICIO_CARDIO_ESTABLECER: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_cardio, pattern='back_inicio_cardio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_CARDIO_ESTABLECER_ACTIVIDAD: [
									CommandHandler('minutos', establecer_cardio_minutos),
									CommandHandler('distancia', establecer_cardio_distancia),
									CommandHandler('calorias', establecer_cardio_calorias),
									CallbackQueryHandler(show_inicio_cardio_establecer, pattern='back_inicio_cardio_establecer'),
									MessageHandler(Filters.text & (~Filters.command), any_message),
									],

			INICIO_CARDIO_ESTABLECER_ACTIVIDAD_CONFIRMAR: [
														CallbackQueryHandler(establecer_cardio_si, pattern='establecer_cardio_si'),
														CallbackQueryHandler(establecer_cardio_no, pattern='establecer_cardio_no'),
														MessageHandler(Filters.text & (~Filters.command), any_message),
														],

			INICIO_CARDIO_ELIMINAR: [
								CallbackQueryHandler(objetivo_cardio_eliminar_si, pattern='objetivo_cardio_eliminar_si'),
								CallbackQueryHandler(objetivo_cardio_eliminar_no, pattern='objetivo_cardio_eliminar_no'),
								MessageHandler(Filters.text & (~Filters.command), any_message),
								],

			INICIO_RETOS: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos_ver, pattern='inicio_retos_ver'),
						CallbackQueryHandler(show_inicio_retos_eliminar, pattern='inicio_retos_eliminar'),
						CallbackQueryHandler(show_inicio_retos_anotar, pattern='inicio_retos_anotar'),
						CallbackQueryHandler(show_inicio_retos_calendario, pattern='inicio_retos_calendario'),
						CallbackQueryHandler(show_inicio_retos_descalificar, pattern='inicio_retos_descalificar'),
						CallbackQueryHandler(show_inicio_retos_historial, pattern='inicio_retos_historial'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_VER: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_VER_RETO: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos_ver, pattern='back_inicio_retos_ver'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ELIMINAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ELIMINAR_CONFIRMAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(eliminar_reto_confirmar_no, pattern='eliminar_reto_confirmar_no'),
						CallbackQueryHandler(show_inicio_retos_eliminar, pattern='back_inicio_retos_eliminar'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_ANOTAR_CONFIRMAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(inicio_retos_anotar_si, pattern='inicio_retos_anotar_si'),
						CallbackQueryHandler(inicio_retos_anotar_no, pattern='inicio_retos_anotar_no'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_CALENDARIO: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_DESCALIFICAR_CONFIRMAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(inicio_retos_descalificar_si, pattern='inicio_retos_descalificar_si'),
						CallbackQueryHandler(inicio_retos_descalificar_no, pattern='inicio_retos_descalificar_no'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_HISTORIAL: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RETOS_HISTORIAL_CLASIFICACION: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_retos_historial, pattern='back_inicio_retos_historial'),
						CallbackQueryHandler(show_inicio_retos, pattern='back_inicio_retos'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_cardio_registrar, pattern='inicio_cardio_registrar'),
						CallbackQueryHandler(show_inicio_ejercicio_apuntarse, pattern='inicio_ejercicio_apuntarse'),
						CallbackQueryHandler(show_inicio_ejercicio_ranking, pattern='inicio_ejercicio_ranking'),
						CallbackQueryHandler(show_inicio_ejercicio_descalificar, pattern='inicio_ejercicio_descalificar'),
						CallbackQueryHandler(show_inicio_ejercicio_eliminar, pattern='inicio_ejercicio_eliminar'),
						CallbackQueryHandler(show_inicio_ejercicio_historial, pattern='inicio_ejercicio_historial'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_REGISTRAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_RANKING: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD: [
									CommandHandler("cardio", registrar_cardio),
									CallbackQueryHandler(show_inicio_cardio_registrar, pattern='back_inicio_cardio_registrar'),
									MessageHandler(Filters.text & (~Filters.command), any_message),
									],

			INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR: [
														CallbackQueryHandler(registrar_cardio_si, pattern='registrar_cardio_si'),
														CallbackQueryHandler(registrar_cardio_no, pattern='registrar_cardio_no'),
														MessageHandler(Filters.text & (~Filters.command), any_message),
														],

			INICIO_EJERCICIO_REGISTRAR_ACTIVIDAD_CONFIRMAR_FOTO: [
														MessageHandler(Filters.photo, check_photo),
														CallbackQueryHandler(registrar_cardio_si, pattern='registrar_cardio_si'),
														CallbackQueryHandler(registrar_cardio_no, pattern='registrar_cardio_no'),
														CallbackQueryHandler(show_inicio_ejercicio, pattern='inicio_ejercicio'),
														CallbackQueryHandler(show_inicio, pattern='back_inicio'),
														MessageHandler(Filters.text & (~Filters.command), any_message),
														],

			INICIO_EJERCICIO_DESCALIFICAR_CONFIRMAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(inicio_ejercicio_descalificar_si, pattern='inicio_ejercicio_descalificar_si'),
						CallbackQueryHandler(inicio_ejercicio_descalificar_no, pattern='inicio_ejercicio_descalificar_no'),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_ELIMINAR_CONFIRMAR: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(inicio_ejercicio_eliminar_si, pattern='inicio_ejercicio_eliminar_si'),
						CallbackQueryHandler(inicio_ejercicio_eliminar_no, pattern='inicio_ejercicio_eliminar_no'),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_HISTORIAL: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_EJERCICIO_HISTORIAL_CLASIFICACION: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_ejercicio_historial, pattern='back_inicio_ejercicio_historial'),
						CallbackQueryHandler(show_inicio_ejercicio, pattern='back_inicio_ejercicio'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS: [
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas_ver, pattern='inicio_rutinas_ver'),
						CallbackQueryHandler(show_inicio_rutinas_anotar, pattern='inicio_rutinas_anotar'),
						CallbackQueryHandler(show_inicio_rutinas_consultar, pattern='inicio_rutinas_consultar'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS_VER: [
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas, pattern='back_inicio_rutinas'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS_ANOTAR: [
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas, pattern='back_inicio_rutinas'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS_CONSULTAR: [
						CommandHandler('consultar', rutinas_consultar_fecha),
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas, pattern='back_inicio_rutinas'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS_VER_RUTINA: [
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas_ver, pattern='back_inicio_rutinas_ver'),
						CallbackQueryHandler(show_inicio_rutinas, pattern='back_inicio_rutinas'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_RUTINAS_ANOTAR_RUTINA: [
						MessageHandler(Filters.command, ver_ejercicio),
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_rutinas_anotar, pattern='back_inicio_rutinas_anotar'),
						CallbackQueryHandler(show_inicio_rutinas, pattern='back_inicio_rutinas'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

			INICIO_SOPORTE: [
						MessageHandler(Filters.text & (~Filters.command), any_message),
						CallbackQueryHandler(show_inicio_soporte_que, pattern='inicio_soporte_que'),
						CallbackQueryHandler(show_inicio_soporte_acerca, pattern='inicio_soporte_acerca'),
						CallbackQueryHandler(show_inicio_soporte_peso, pattern='inicio_soporte_peso'),
						CallbackQueryHandler(show_inicio_soporte_cardio, pattern='inicio_soporte_cardio'),
						CallbackQueryHandler(show_inicio_soporte_retos, pattern='inicio_soporte_retos'),
						CallbackQueryHandler(show_inicio_soporte_ejercicio, pattern='inicio_soporte_ejercicio'),
						CallbackQueryHandler(show_inicio_soporte_rutinas, pattern='inicio_soporte_rutinas'),
						CallbackQueryHandler(show_inicio_soporte_ficha, pattern='inicio_soporte_ficha'),
						CallbackQueryHandler(show_inicio, pattern='back_inicio')
						],

		},
		fallbacks=[CommandHandler('start',start),
				CommandHandler('mensaje', mandar_mensaje),
				CommandHandler('ejercicios', actualizar_ejercicios),
				MessageHandler(Filters.photo, usuario_usa_comando_anterior),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='start_menu'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_rutinas'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='show_inicio'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_soporte'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha_altura'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha_nacimiento'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha_genero'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ficha_email'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_ficha'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='select_genero_hombre'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='select_genero_mujer'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='select_genero_otro'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='select_genero_sin'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_anotar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_establecer'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_eliminar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_evolucion'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_valoracion'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_anotar_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_anotar_grasa'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_anotar_musculo'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_peso_anotar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_establecer_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_establecer_grasa'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_establecer_musculo'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_peso_establecer'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_1'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_2'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_3'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_4'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_5'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_grasa_1'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_grasa_2'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_grasa_3'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_grasa_4'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_grasa_5'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_musculo_1'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_musculo_2'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_musculo_3'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_musculo_4'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_musculo_5'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_tiempo_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_tiempo_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_eliminar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_peso_eliminar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_evolucion_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_evolucion_grasa'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_evolucion_musculo'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_peso_evolucion_imc'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_peso_evolucion'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_peso'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio_registrar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio_ver'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio_establecer'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio_eliminar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_cardio_registrar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='registrar_cardio_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='registrar_cardio_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_cardio'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_cardio_establecer'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='establecer_cardio_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='establecer_cardio_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_cardio_eliminar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='objetivo_cardio_eliminar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_ver'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_eliminar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_anotar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_calendario'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_descalificar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_historial'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_retos_ver'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='eliminar_reto_confirmar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_retos_eliminar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_anotar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_anotar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_descalificar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_retos_descalificar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_retos_historial'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_retos'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_cardio_registrar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_apuntarse'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_ranking'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_descalificar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_eliminar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_historial'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_ejercicio'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_cardio_registrar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_descalificar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_descalificar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_eliminar_si'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_ejercicio_eliminar_no'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_ejercicio_historial'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_rutinas_ver'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_rutinas_anotar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_rutinas_consultar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_rutinas'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_rutinas_ver'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio_rutinas_anotar'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='inicio_soporte_acerca'),
				CallbackQueryHandler(usuario_pulsa_boton_anterior, pattern='back_inicio'),
				CommandHandler("rango", usuario_usa_comando_anterior),
				CommandHandler("rango", usuario_usa_comando_anterior),
				CommandHandler("rango", usuario_usa_comando_anterior),
				CommandHandler("rango", usuario_usa_comando_anterior),
				CommandHandler("cardio", usuario_usa_comando_anterior),
				CommandHandler("consultar", usuario_usa_comando_anterior),
				CommandHandler('minutos', usuario_usa_comando_anterior),
				CommandHandler('distancia', usuario_usa_comando_anterior),
				CommandHandler('calorias', usuario_usa_comando_anterior),
				CommandHandler("cardio", usuario_usa_comando_anterior),
				CommandHandler('consultar', usuario_usa_comando_anterior)
		]
	)
	updater.dispatcher.add_handler(conv_handler)
	updater.dispatcher.add_error_handler(error)

	# Start the Bot
	updater.start_polling()#allowed_updates=[])

	actualizar_ejercicios()

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