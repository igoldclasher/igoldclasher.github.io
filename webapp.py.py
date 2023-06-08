import sqlite3 as sqlite
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from datetime import timedelta, datetime, timezone
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, \
	KeyboardButton, ContentType
from aiogram.utils.exceptions import Throttled



data = {'таблица':'def', 'строка':'def', 'ячейка':'def'}
TOKEN = '6059382160:AAEN6sMngi3g_4QOKHHGnX4HZ1tyfwi0KnE'
bd = 'base.db'
bot = Bot(token=TOKEN, parse_mode='html')
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
db = sqlite.connect(bd)
cur = db.cursor()


class info(StatesGroup):
	text = State()

class photo(StatesGroup):
	parametr = State()

class newtable(StatesGroup):
	nazvanie = State()
	

@dp.message_handler(state=info.text, content_types=types.ContentTypes.TEXT)
async def text(message: types.Message, state: FSMContext):
	сообщение=message.message_id-1
	await bot.delete_message(message.from_user.id, сообщение)
	await message.delete()
	await state.finish()
	cur.execute(f"SELECT * FROM '{data['таблица']}'")
	columns = [description[0] for description in cur.description]
	имястолбца = columns[int(data['ячейка'])]
	имястолбца=str(имястолбца)
	with db:
		cur.execute(f"UPDATE {data['таблица']} SET {имястолбца}=? WHERE id=?", (message.text, data['строка']))
	await редактор(data['таблица'], data['строка'], message)


	
@dp.message_handler(state=photo.parametr, content_types=types.ContentTypes.PHOTO)
async def parametr(message: types.Message, state: FSMContext):
	сообщение=message.message_id-1
	await bot.delete_message(message.from_user.id, сообщение)
	await message.delete()
	await state.finish()
	with db:
		cur.execute(f"UPDATE {data['таблица']} SET фото=? WHERE id=?", (message.photo[0].file_id, data['строка']))
	await редактор(data['таблица'], data['строка'], message)
	

@dp.message_handler(Text(equals='Отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	
	
@dp.message_handler(state=newtable.nazvanie, content_types=types.ContentTypes.TEXT)
async def nazvanie(message: types.Message, state: FSMContext):
	сообщение=message.message_id-1
	await bot.delete_message(message.from_user.id, сообщение)
	await message.delete()
	with db:
		cur.execute(
			f"""CREATE TABLE IF NOT EXISTS `{message.text}`(id INTEGER PRIMARY KEY AUTOINCREMENT, количество TEXT, фото TEXT, название TEXT, описание TEXT, цена TEXT);""")
		await state.finish()
		await главная(message)
		with db:
					cur.execute(f"INSERT INTO `{message.text}` (`количество`, `фото`, `название`, `описание`, `цена`) VALUES (?,?,?,?,?)", ("0", "0", "0", "0", "0",))
	
	
@dp.callback_query_handler(text="главное")
async def главное(call: CallbackQuery):
	await call.message.delete()
	await главная(call)	
	
@dp.callback_query_handler(text="new")
async def new(call: CallbackQuery):
	await call.message.delete()
	await newtable.nazvanie.set()
	text='Введи название создаваемой таблицы, опционально "Отмена"'
	await bot.send_message(call.from_user.id, text)
	
	
	
@dp.callback_query_handler(text="del")
async def dels(call: CallbackQuery):
	await call.message.delete()
	markup =InlineKeyboardMarkup(row_width=4)
	tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('клиенты', 'sqlite_sequence');").fetchall()
	if int(len(tables))==0:
			reply = f"БД пуста"
			markup.insert(InlineKeyboardButton("Новая", callback_data="new"))
			await bot.send_message(call.from_user.id, reply, reply_markup=markup)
	else:
		  	for table in tables:
		  		markup.insert(InlineKeyboardButton(f"{table[0]}", callback_data=f"ddeell{table[0]}"))
		  	await bot.send_message(call.from_user.id, "Выбери таблицу для удаления", reply_markup=markup)
	

@dp.callback_query_handler()
async def call(call: CallbackQuery):
		await call.message.delete()
		if "newtovar" in call.data:
			msg = call.data[8:]
			with db:
				cur.execute(f"INSERT INTO `{msg}` (`количество`, `фото`, `название`, `описание`, `цена`) VALUES (?,?,?,?,?)", ("0", "0", "0", "0", "0",))
			base=cur.execute(f'SELECT * FROM {msg}" ORDER BY id DESC LIMIT 1').fetchone()
			await редактор(msg, base[0], call)
		
		
		if "ddeell" in call.data:
			msg = call.data[6:]
			msg=str(msg)
			with db:
				cur.execute(f"""DROP TABLE '{msg}'""")
			await главная(call)
		
		if "rt" in call.data:
			msg = call.data[2:]
			msg = msg.split("|")
			таблица = msg[0]
			строка = msg[1]
			ячейка = msg[2]
			if int(ячейка)==2:
				data['таблица'] = таблица
				data['строка'] = строка
				data['ячейка'] = ячейка
				await редфото(call)
			else:
				data['таблица'] = таблица
				data['строка'] = строка
				data['ячейка'] = ячейка
				await рединф(call)
			
		if "table" in call.data:
			msg = call.data[5:]
			base = cur.execute(f"SELECT * FROM `{msg}`").fetchall()
			if int(len(base))==1:
				await редактор(msg, 1, call)
			else:
					with db:
						cur.execute(f"INSERT INTO `{msg}` (`количество`, `фото`, `название`, `описание`, `цена`) VALUES (?,?,?,?,?)", ("0", "0", "0", "0", "0",))
					base= cur.execute(f"SELECT * FROM '{msg}' WHERE id = {len(base)}").fetchone()
					print(base)
					await редактор(msg, base[0], call)
			 		
			 	
		
async def рединф(call):
	print(data)
	await bot.send_message(call.from_user.id, "Укажи новое значение.") 	
	await info.text.set()		 		
			 		
			 		
async def редфото(call):
	print(data)
	await bot.send_message(call.from_user.id, "Пришли фото товара.") 	
	await photo.parametr.set()	
	

async def редактор(table, id, message):
	товар = cur.execute(f"SELECT * FROM '{table}' WHERE id = {id}").fetchone()
	markup =InlineKeyboardMarkup(row_width=2)
	markup.insert(InlineKeyboardButton(f"Количество", callback_data=f"rt{table}|{товар[0]}|1"))
	markup.insert(InlineKeyboardButton(f"Фото", callback_data=f"rt{table}|{товар[0]}|2"))
	markup.insert(InlineKeyboardButton(f"Название", callback_data=f"rt{table}|{товар[0]}|3"))
	markup.insert(InlineKeyboardButton(f"Описание", callback_data=f"rt{table}|{товар[0]}|4"))
	markup.insert(InlineKeyboardButton(f"Цена", callback_data=f"rt{table}|{товар[0]}|5"))
	markup.add(InlineKeyboardButton("Новый", callback_data=f"newtovar{table}"))
	markup.insert(InlineKeyboardButton(f"Назад", callback_data=f"главное"))
	await bot.send_message(message.from_user.id, f"Выбери параметр для редактирования:\nКоличество - {товар[1]}\nФото - {товар[2]}\nНазвание - {товар[3]}\nОписание - {товар[4]}\nЦена - {товар[5]}", reply_markup=markup)
	

@dp.message_handler(commands=['start'])
async def command_start(message):
	#await message.delete()
	await регистрация(message)
	#await логсообщение(message.from_user.id, f"Зарегистрирован {message.from_user.first_name}")
	await главная(message)


async def регистрация(message):
	with db:
		cur.execute(
			f"""CREATE TABLE IF NOT EXISTS `клиенты`(id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, user_id TEXT, message_id TEXT, телефон TEXT);""")
	if not cur.execute(f"SELECT * FROM клиенты WHERE user_id = {message.from_user.id}").fetchone():
		with db:
			cur.execute(f"INSERT INTO клиенты (`user_name`, `user_id`, `телефон`) VALUES(?,?,?)",
						(message.from_user.first_name, message.from_user.id, 0))


async def главная(message):
		markup =InlineKeyboardMarkup(row_width=4)
		tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('клиенты', 'sqlite_sequence');").fetchall()
		if int(len(tables))==0:
			reply = f"БД пуста"
			markup.insert(InlineKeyboardButton("Новая", callback_data="new"))
			await bot.send_message(message.from_user.id, reply, reply_markup=markup)
		else:
		  for table in tables:
		  	markup.insert(InlineKeyboardButton(f"{table[0]}", callback_data=f"table{table[0]}"))
		  reply = f"Выбери таблицу"
		  markup.add(InlineKeyboardButton("Новая", callback_data="new"))
		  markup.insert(InlineKeyboardButton("Удалить", callback_data="del"))
		  await bot.send_message(message.from_user.id, reply, reply_markup=markup)
		


@dp.message_handler(content_types=['contact'])
async def get_contact(message: types.Message):
	await message.delete()
	клиент = cur.execute(f"SELECT * FROM клиенты WHERE user_id = {message.from_user.id}").fetchone()
	await bot.delete_message(message.from_user.id, клиент[3])
	with db:
		cur.execute("UPDATE клиенты SET телефон=? WHERE user_id=?",
					(message.contact.phone_number, message.from_user.id))
	sms = await bot.send_message(message.from_user.id, "Номер телефона зарегистрирован!\nТеперь Вам доступны покупки.")
	await asyncio.sleep(5)
	await bot.delete_message(message.from_user.id, sms['message_id'])


@dp.message_handler()
async def message_handler(message):
	await bot.send_message(1848273742, f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}:</a>\n{message.text}')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
