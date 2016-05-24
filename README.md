# CryptPass

#### Criptografia Simples de Senhas

### Descrição:

###### Este é um simples programa de criptografia escrito em Python.
###### O programa, ao ser executado, cria uma pasta 'CryptPass' no mesmo diretório que o programa está sendo executado, nesta pasta será armazenada as senhas criptografadas.
###### Ao fazer uma das operações, o programa irá criar (caso não exista) um arquivo de chave privada (Private.key) no mesmo diretório que o programa está sendo executado, esta chave é única e necessária para encriptar e decriptar corretamente suas senhas.
###### O arquivo de senha será criado na pasta 'CryptPass', possuindo uma timestamp (hora e data que foi criado) e com extensão '.key'. É neste arquivo que será armazenado a Master Key e a Seed gerada pelo programa, isto é, sua senha criptografada

###### É possível também utilizar uma chave privada definida pelo usuário.
###### Ao criar uma nova chave, é recomendável fazer um backup da chave anterior e os arquivos de senha encriptados por ela, ou senão será impossível decriptar suas senhas corretamente!

### Método:

###### O método é bem simples, o programa converte a senha para hexadecimal e gera uma Seed aleatória pelo sistema, esta Seed também é convertida em hexadecimal e é combinada com a senha e a Private Key para gerar uma Master Key.
###### A decriptação da senha é o processo inverso, retirando a Seed e a Private Key da Master Key para obter a senha em hexadecimal, convertendo novamente para um formato legível.
###### Por ser um método simples, o programa é melhor recomendado para ofuscação ou aprendizagem.

#### [Confira aqui o changelog do programa para maiores informações sobre diferentes versões.](https://raw.github.com/Wolfterro/CryptPass/master/CHANGELOG.txt)<br />

### Requisitos:
 - Python 2.x

### Download:

###### Para baixar o programa, basta inserir estes comandos no terminal, um de cada vez:

    git clone https://github.com/Wolfterro/CryptPass.git
    cd CryptPass
    chmod +x CryptPass.py
    ./CryptPass.py
