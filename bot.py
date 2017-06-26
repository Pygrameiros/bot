import telepot, time, logging, sys
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now()

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)

updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

def welcome(msg):
	chat_id = telepot.glance(msg)
	try:
		text = msg['text']
	except:
		text = ''

	if(text.startswith('/welcome')):
		first_name = msg['from']['first_name']
		user_id = msg['from']['id']
		admins = bot.getChatAdministrators(msg['chat']['id'])
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			text = text.replace("/welcome ", "")
			with open('welcome.txt', 'w') as welcome:
				welcome.write(text)
			bot.sendMessage(msg['chat']['id'], "As mensagens de boas-vindas foram alteradas com sucesso!")

		else:
			bot.sendMessage(msg['chat']['id'], "Comando restrito aos administradores.")

	if ('new_chat_member' in msg):
		user_first_name = msg['new_chat_member']['first_name']
		user_last_name = msg['new_chat_member']['last_name']
		get_bot_name = bot.getMe()
		bot_name = get_bot_name['first_name']
		if(user_first_name == bot_name):
			bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
		else:
			with open('welcome.txt', 'r') as welcome:
				welcome = welcome.read()
				welcome = welcome.replace("$name", user_first_name)
				welcome = welcome.replace('$surname', user_last_name)
				#welcome = welcome.replace('$username', username)
				bot.sendMessage(msg['chat']['id'], welcome)

def goodbye(msg):
    if('left_chat_member' in msg):
        user_first_name = str(msg['left_chat_member']['first_name'])
        bot.sendMessage(msg['chat']['id'], "Tchau, {}".format(user_first_name))
        bot.sendVideo(msg['chat']['id'], "https://media.giphy.com/media/l3V0gpbjA6fD7ym9W/giphy.mp4")

def rules(msg):
	try:
		text = msg['text']
	except:
		text = ''

	if(text.startswith('/defregras')):
		user_id = msg['from']['id']
		admins = bot.getChatAdministrators(msg['chat']['id'])
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			text = text.replace("/defregras ", "")
			with open('regras.txt', 'w') as rules:
				rules.write(text)
			bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")
		else:
			bot.sendMessage(msg['chat']['id'], "Comando restrito aos administradores.")

	if(text.startswith('/regras')):
		with open('regras.txt', 'r') as rules:
			bot.sendMessage(msg['chat']['id'], rules.read())
			rules = rules.read()
			bot.sendMessage(msg['chat']['id'], rules)


def log(msg):
	day = str(now.day)
	month = str(now.month)
	year = str(now.year)
	hour = str(now.hour)
	minute = str(now.minute)
	second = str(now.second)
	user, userid, comando = msg['from']['username'], msg['from']['id'], msg['text']

	content_type, chat_type, chat_id = telepot.glance(msg)
	try:
		text = msg['text']
	except:
		text = ''

	if(text.startswith('/start')):
		logging.basicConfig(filename='users_register.log', filemode='w', level=logging.INFO)
		logging.info("log [{}/{}/{}][{}:{}:{}]".format(day,month,year,hour,minute,second))

		logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(user,userid, comando))

		print("@{} Iniciou o Bot - Dados salvos!".format(user))

	elif(text.startswith('/') and text != '/start'):
		logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
		logging.info("log [{}/{}/{}][{}:{}:{}]" .format(day,month,year,hour,minute,second))

		logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(user,userid,comando))

		print("@{} Usou o Bot - Dados salvos!".format(user))


def commands(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	try:
		text = msg['text']
	except:
		text = ''

	if(chat_type == 'private'):
		if(text.startswith('/start')):
			bot.sendMessage(chat_id, ("Olá, eu sou o PygrameirosBot!"
									"\nFui criado pela galera do Pygrameiros para te ajudar"
									" a administrar teu grupo!"))
			log(msg)
	else:
		if(text.startswith('/start')):
			bot.sendMessage(chat_id, ("Oi! Por favor, inicie uma conversa privada."
									" Bots funcionam apenas desta forma."))
			log(msg)

	if(text.startswith('/info')):
		if chat_type == 'private':
			bot.sendMessage(chat_id, ("ID INFO \n\n NOME: " + str(msg['from']['username']) + "\n ID: " + str(msg['from']['id']) + "."))
		else:
			bot.sendMessage(chat_id, ("ID INFO \n NOME: " + str(msg['from']['username']) + "\n ID: " + str(msg['from']['id']) +" \nNOME DO GRUPO: " + msg['chat']['title'] + "\n ID GROUP: {}".format(chat_id)))

	if(text.startswith('/link')):
		bot.sendMessage(chat_id, '[Pygrameiros](https://t.me/joinchat/AAAAAEOnjcIiD2WH_TD8Vg)',
						parse_mode='Markdown')
		log(msg)

	if(text.startswith('/ajuda')):
		arrow = u'\U000027A1'#u'\U00027A1'
		bot.sendMessage(chat_id, ('''
Olá, sou o PygrameirosBot!
Segue minha lista de comandos:
/info -> informações do grupo
/link -> link do grupo
/regras -> regras do grupo
/leave -> sair do grupo
							'''))

		log(msg)
	if(text.startswith('/leave')):
		chat_id = msg['chat']['id']
		user_id = msg['from']['id']
		bot.sendMessage(chat_id, "Tem certeza que deseja sair do grupo?\nEnvie 'sim' ou 'não'.")
		if(text == 'sim'):
			bot.kickChatMember(chat_id, user_id)

	###  ADMINS COMMANDS  ###
	if(text.startswith('/ban') or text.startswith('/kick')):
		user_id = msg['from']['id']
		user = msg['reply_to_message']['from']['first_name']
		reply_id = msg['reply_to_message']['from']['id']
		admins = bot.getChatAdministrators(chat_id)
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			if reply_id not in adm_list:
				bot.sendMessage(chat_id, "*{}* foi retirado do grupo.", parse_mode="Markdown".format(user))
				bot.kickChatMember(chat_id, reply_id)
			else:
				bot.sendMessage(chat_id, '*{}* é um dos administradores. Não posso remover administradores.', parse_mode="Markdown".format(user))
		else:
			bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')


def handle(msg):
	try:
		text = msg['text']
	except:
		text = ''

	log(msg)
	commands(msg)
	welcome(msg)
	goodbye(msg)
	rules(msg)

MessageLoop(bot, handle).run_as_thread()
while 1:
	time.sleep(10)
