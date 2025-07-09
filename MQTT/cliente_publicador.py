import time
from paho.mqtt.client import Client  # Não estamos usando CallbackAPIVersion

#pip install paho-mqtt==2.0.0
#pip install --upgrade paho-mqtt

# Configurações do broker
broker = "192.168.137.197"
porta = 1884
usuario = "admin"
senha = "DEEUFPE"

# Criação do cliente MQTT
cliente = Client()

# Define login e senha
cliente.username_pw_set(usuario, senha)

# Conecta ao broker
print(f"Conectando ao broker {broker}:{porta} com usuário '{usuario}'...")
cliente.connect(broker, porta)
cliente.loop_start()

# Publica mensagem
topico = "casa/led"
mensagem = "on"
print(f"Publicando no tópico '{topico}': {mensagem}")
cliente.publish(topico, mensagem)

# Aguarda para garantir envio
time.sleep(3)

# Finaliza conexão
cliente.loop_stop()
cliente.disconnect()
print("Publicador desconectado.")
