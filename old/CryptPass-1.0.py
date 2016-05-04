#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#--------------------------------------------
# Criado por: Wolfterro
# Versão: 1.0 - Python 2.x
# Data: 01/05/2016
#--------------------------------------------
# Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>
#-----------------------------------------------------------------------
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

from __future__ import print_function
import random
import string
import binascii
import getpass
import time
import os
import sys

# Versão do Programa
#===================
version = "1.0"

# Verificando Existência da pasta "CryptPass"
#============================================
def check_cryptpass_folder():
	check_folder = os.path.exists("CryptPass")

	if check_folder == False:
		try:
			print("Criando diretório 'CryptPass'...")
			os.makedirs("CryptPass")
			os.chdir("CryptPass")
		except OSError:
			print("!!! Erro ao criar o diretório! Saindo...")
			sys.exit(1)
	else:
		os.chdir("CryptPass")

# Gerando Timestamp Para o Arquivo
#=================================
def get_timestamp_for_file():
	tempo_atual = time.strftime("%H-%M-%S_-_%d-%m-%Y")
	return tempo_atual

# Gerando Seed Aleatória
#=======================
def get_random_seed():
	return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

# Método de String para Binário
#==============================
def string_to_binary(string):
	result_bin = bin(int(binascii.hexlify(string), 16))
	return result_bin

# Método Principal: Encriptando Senha
#====================================
def main_encrypt_password():
	# Resgatando Senha
	#=================
	print("")
	get_password = getpass.getpass("Insira sua senha: ")
	get_password_bin = string_to_binary(get_password)

	# Gerando Seed
	#=============
	generated_seed = get_random_seed()
	generated_seed_bin = string_to_binary(generated_seed)

	# Gerando Master Key
	#===================
	master_key_bin = bin(int(generated_seed_bin, 2) + int(get_password_bin, 2))

	# Enviando Informações Para o Usuário
	#====================================
	print ("\nMaster Key: %s\n" % (master_key_bin))
	print ("Seed: %s\n" % (generated_seed_bin))

	# Salvando em Arquivo
	#====================
	file_generated = "CryptPass_-_" + get_timestamp_for_file() + ".txt"
	file = open(file_generated, "w")
	file.write("Master Key: " + master_key_bin + "\n" + "Seed: " + generated_seed_bin + "\n")
	file.close()

	print("Arquivo criado em: %s" % (os.path.realpath(file_generated)))

# Método Principal: Decriptando Senha
#====================================
def main_decrypt_password():
	escolher_arquivo = raw_input("\nEscolha um arquivo através do número listado: ")
	escolher_arquivo = int(escolher_arquivo)

	try:
		file = open(list_files_cryptpass_folder[escolher_arquivo - 1], "r")
		linhas = file.readlines()

		get_master_key_from_file = str(linhas[0])
		get_seed_from_file = str(linhas[1])

		print ("\n%s" % (get_master_key_from_file))
		print ("%s" % (get_seed_from_file))

		get_master_key_from_file = get_master_key_from_file.replace("Master Key: ", "")
		get_seed_from_file = get_seed_from_file.replace("Seed: ", "")

		master_key_decrypted = bin(int(get_master_key_from_file, 2) - int(get_seed_from_file, 2))
		master_key_decrypted_int = int(master_key_decrypted, 2)
		password_plain_text = binascii.unhexlify("%x" % master_key_decrypted_int)

		print ("Master Key Decriptada: %s" % (master_key_decrypted))
		print ("\nSenha: %s" % (password_plain_text))

		file.close()

	except IndexError:
		print("\nErro! Arquivo escolhido não consta na lista!")
		escolher_arquivo_novamente = raw_input("Deseja escolher outro arquivo? [s/N]: ")
		escolher_arquivo_novamente = escolher_arquivo_novamente.upper()

		if escolher_arquivo_novamente == "S":
			main_decrypt_password()
		else:
			print("Saindo...")

# Listando Arquivos de Senha
#===========================
def file_listing():
	global list_files_cryptpass_folder
	list_files_cryptpass_folder = os.listdir("../CryptPass")
	tamanho_lista = len(list_files_cryptpass_folder)

	listando = "\nListando arquivos de senha existentes (" + str(tamanho_lista) + "):\n"
	tamanho_listando = len(listando) - 2
	print (listando + ("=" * tamanho_listando))

	quantidade_itens = 0

	for listar_arquivos in list_files_cryptpass_folder:
		quantidade_itens += 1
		listar_arquivos = listar_arquivos.replace("_-_", " *** ").replace(".txt", "")
		print (str(quantidade_itens) + " - " + listar_arquivos)

	if tamanho_lista > 0:
		decriptar_escolha = raw_input("\nDeseja decriptar um dos arquivos de senha? [s/N]: ")
		decriptar_escolha = decriptar_escolha.upper()

	if decriptar_escolha == "S":
		main_decrypt_password()
	else:
		print ("Saindo...")

def main():
	# Inicializando Verificação de Pasta
	#===================================
	check_cryptpass_folder()

	# Menu Principal do Programa
	#===========================
	print("===============================================")
	print("CryptPass: Criptografia Simples de Senhas (%s)" % (version))
	print("===============================================\n")

	print("Escolha uma das opções abaixo:")
	print(" (1) - Encriptar Senha e Criar Arquivo")
	print(" (2) - Decriptar Arquivo e Mostar Senha\n")

	escolha_principal = raw_input("Selecione uma das opções (qualquer outra tecla para sair): ")

	if escolha_principal == "1":
		main_encrypt_password()
	elif escolha_principal == "2":
		file_listing()
	else:
		print("Saindo...")

# Inicializando Programa
#=======================
main()
