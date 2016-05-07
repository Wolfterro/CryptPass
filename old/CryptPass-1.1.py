#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#--------------------------------------------
# Criado por: Wolfterro
# Versão: 1.1 - Python 2.x
# Data: 04/05/2016
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
import ConfigParser
import getpass
import time
import os
import sys

# Versão do Programa
#===================
version = "1.1"

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

# Verificando Private Key
#========================
def check_private_key():
    config_check = ConfigParser.ConfigParser()
    config_check.read("../Private.key")

    try:
        private_key = config_check.get("Private Key", "Key")
        return private_key
    except ConfigParser.Error:
        print ("Private Key não existe! Criando...")
        new_private_key = get_random_seed()
        new_private_key_hex = string_to_hex(new_private_key)

        file = open("../Private.key", "w")
        file.write("[Private Key]" + "\n" + "Key: " + new_private_key_hex)
        file.close()
        return new_private_key_hex

# Gerando Timestamp Para o Arquivo
#=================================
def get_timestamp_for_file():
	tempo_atual = time.strftime("%H-%M-%S_-_%d-%m-%Y")
	return tempo_atual

# Gerando Seed Aleatória
#=======================
def get_random_seed():
	return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

# Método de String para Hexadecimal
#==================================
def string_to_hex(string):
    result_hex = hex(int(binascii.hexlify(string), 16))
    return result_hex.replace("0x", "").replace("L", "").upper()

# Método de Hexadecimal para String
#==================================
def hex_to_string(hex_dump):
    hex_dump_int = int(hex_dump, 16)
    hex_dump_string = binascii.unhexlify("%x" % hex_dump_int)
    return hex_dump_string

# Método Principal: Encriptando Senha
#====================================
def main_encrypt_password():
	# Resgatando Private Key
	#=======================
	get_private_key = check_private_key()

	# Resgatando Senha
	#=================
	print("")
	get_password = getpass.getpass("Insira sua senha: ")
	get_password_hex = string_to_hex(get_password)

	# Gerando Seed
	#=============
	get_seed = get_random_seed()
	get_seed_hex = string_to_hex(get_seed)

	# Gerando Master Key
	#===================
	master_key_hex = hex(int(get_private_key, 16) * (int(get_password_hex, 16) + int(get_seed_hex, 16))).replace("0x", "").replace("L", "").upper()

	# Enviando Informações Para o Usuário
	#====================================
	print ("\nMaster Key: %s\n" % (master_key_hex))
	print ("Seed: %s\n" % (get_seed_hex))

	# Salvando em Arquivo
	#====================
	file_generated = "CryptPass_-_" + get_timestamp_for_file() + ".txt"
	file = open(file_generated, "w")
	file.write("Master Key: " + master_key_hex + "\n" + "Seed: " + get_seed_hex + "\n")
	file.close()

	print("Arquivo criado em: %s" % (os.path.realpath(file_generated)))

# Método Principal: Decriptando Senha
#====================================
def main_decrypt_password():
	# Resgatando Private Key
	#=======================
	get_private_key = check_private_key()

	# Resgatando Arquivo
	#===================
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

		master_key_decrypted = hex((int(get_master_key_from_file, 16) / int(get_private_key, 16)) - int(get_seed_from_file, 16)).replace("0x", "").replace("L", "").upper()
		password_string = hex_to_string(master_key_decrypted)

		print ("Master Key Decriptada: %s" % (master_key_decrypted))
		print ("\nSenha: %s" % (password_string))

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
