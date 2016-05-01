# CryptPass

#### Criptografia Simples de Senhas

### Descrição:

###### Este é um simples programa de criptografia escrito em Python.
###### O programa, ao ser executado, cria uma pasta 'CryptPass' no mesmo diretório que o programa está sendo executado, nesta pasta será armazenada as senhas criptografadas.
###### O arquivo é criado em formato de puro texto e com extensão '.txt', possuindo a Master Key e a Seed gerada pelo programa.

### Método:

###### O método é muito simples, o programa converte a senha para binário e gera uma Seed aleatória pelo sistema, esta Seed também é convertida em binário e é combinada com a senha para gerar uma Master Key.
###### A decriptação da senha é o processo inverso, retirando a Seed da Master Key para obter a senha em binário, convertendo novamente para um formato legível.
###### Por ser um método simples demais, o programa não é recomendado para armazenar senhas importantes ou ser utilizado em situações críticas, apenas para aprendizado ou ofuscação.

### Requisitos:
 - Python 2.x

### Download:

###### Para baixar o programa, basta inserir estes comandos no terminal, um de cada vez:

    wget -O CryptPass 'https://raw.github.com/Wolfterro/CryptPass/master/CryptPass.py'
    chmod +x CryptPass
    ./CryptPass
