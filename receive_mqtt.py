import paho.mqtt.client as mqtt
from datetime import datetime
import struct

class MQTT_Receiver():

    def __init__(self):
        self.broker = "broker.hivemq.com"
        self.topic_pub = "TCC_MAYUMI/SENSORS/P"
        self.topic_sub = "TCC_MAYUMI/SENSORS/S"

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        self.client.connect(self.broker)

    def on_connect(self, client, userdata, flags, rc):
        print("[STATUS] Conectado ao Broker. Resultado da conexao: " + str(rc) + " " + datetime.now().strftime('%d/%m/%Y %H:%M:%S:%f'))
        client.subscribe(self.topic_pub)
        client.subscribe(self.topic_sub)


    def on_message(self, client, userdata, msg):
        # print(len(msg.payload), msg.payload)

        temperature = 0
        humidity = 0

        format = '<'
        format += 'f'*902
        temp_buf = struct.unpack(format, msg.payload)


        acelerometros = {}
        nomes_acelerometros = ["acelerometro1", "acelerometro2", "acelerometro3"]
        nomes_eixos = ["x", "y", "z"]
        i = 0
        for nome_acelerometro in nomes_acelerometros:
            acelerometros[nome_acelerometro] = {}
            for nome_eixo in nomes_eixos:
                acelerometros[nome_acelerometro][nome_eixo] = temp_buf[i*100:i*100 + 99]
                i += 1

        temperature = temp_buf[900]
        humidity = temp_buf[901]
        print('accell1', acelerometros['acelerometro1']['x'][0], acelerometros['acelerometro1']['y'][0], acelerometros['acelerometro1']['z'][0], "m/s²")

        print('accell2', acelerometros['acelerometro2']['x'][0], acelerometros['acelerometro2']['y'][0], acelerometros['acelerometro2']['z'][0], "m/s²")

        print('accell3', acelerometros['acelerometro3']['x'][0], acelerometros['acelerometro3']['y'][0], acelerometros['acelerometro3']['z'][0], "m/s²")
        print(f"temperatura {temperature}ªC, umidade {humidity}%" )
        print()

    def main_loop(self):

        while True:
            self.client.loop()


MQTT_Receiver().main_loop()