import re #importa regex
Exp = ['python','Python',"javascript",".js","react.js",".py","db"]; #Expressoes a serem comparadas
for i in range(len(Exp)): #laco pra correr por tudo
	pythonregex = re.compile('.js|.py|python|javascript',re.I); #compilando a regex e ignorando o caso (maiusculas e minusculas)
	if pythonregex.search(Exp[i]):#se ele achar, tanto no meio, quanto no fim...
		print("Achou");#printa que achou
	else:#senao...
		print("não achou");#printa que nao...