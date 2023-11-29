from sanic import Sanic, Request, response
from mqtt_client import CollectorMQTTClient
from database import StorageInterface
from routes import routes
from datetime import datetime
from socketio import AsyncServer
from collect import CollectNamespace
from serializer import Json

import struct
import asyncio


app = Sanic('Server_3D')
app.blueprint(routes)
app.static('/static', './static')


sio = AsyncServer(async_mode='sanic', cors_allowed_origins=[], json=Json)
sio.attach(app)
sio.register_namespace(CollectNamespace('/collect'))

app.config['MONGO_INTERFACE'] = StorageInterface()
app.config['MQTT_INTERFACE'] = CollectorMQTTClient('lse.dev.br', 'lse', 'lse')
app.config['COLLECT_ID'] = None
app.config['SIO'] = sio


async def process_queue_data(server: Sanic):
    collector_mqtt_client: CollectorMQTTClient = server.config['MQTT_INTERFACE']
    storage_interface: StorageInterface = app.config['MONGO_INTERFACE']

    while True:
        data = await collector_mqtt_client.queue_data.get()
        collect_id = server.config['COLLECT_ID']
        socket: AsyncServer = server.config['SIO']

        fmt = '<'
        fmt += 'f' * 902
        temp_buf = struct.unpack(fmt, data)

        acelerometros = {}
        nomes_acelerometros = ["acelerometro1", "acelerometro2", "acelerometro3"]
        nomes_eixos = ["x", "y", "z"]
        i = 0

        for nome_acelerometro in nomes_acelerometros:
            acelerometros[nome_acelerometro] = {}
            for nome_eixo in nomes_eixos:
                acelerometros[nome_acelerometro][nome_eixo] = temp_buf[i * 100:i * 100 + 99]
                i += 1

        temperature = temp_buf[900]
        humidity = temp_buf[901]
        data_to_save = {
            'timestamp': datetime.utcnow(),
            'data': acelerometros,
            'collect_id': collect_id,
            'temperature': temperature,
            'humidity': humidity
        }

        await socket.emit('DATA_AVAILABLE', data_to_save, namespace='/collect')

        if collect_id is not None:
            print('accell1', acelerometros['acelerometro1']['x'][0], acelerometros['acelerometro1']['y'][0],
                  acelerometros['acelerometro1']['z'][0], "m/s²")

            print('accell2', acelerometros['acelerometro2']['x'][0], acelerometros['acelerometro2']['y'][0],
                  acelerometros['acelerometro2']['z'][0], "m/s²")

            print('accell3', acelerometros['acelerometro3']['x'][0], acelerometros['acelerometro3']['y'][0],
                  acelerometros['acelerometro3']['z'][0], "m/s²")

            print(f"temperatura {temperature}ªC, umidade {humidity}%")

            await storage_interface.insert_data(data_to_save)


@app.listener('before_server_start')
async def start_task_mqtt(server: Sanic, loop: asyncio.AbstractEventLoop):
    collector_mqtt_client = server.config['MQTT_INTERFACE']
    collector_mqtt_client.add_topic('testando_sensor_3d')

    await collector_mqtt_client.main()


@app.listener('before_server_start')
async def init_database(server: Sanic, loop: asyncio.AbstractEventLoop):
    _storage_interface: StorageInterface = server.config['MONGO_INTERFACE']
    await _storage_interface.init()


@app.listener('after_server_start')
async def init_task_insert_data(server: Sanic, loop: asyncio.AbstractEventLoop):
    loop.create_task(process_queue_data(server))


@app.get('/')
async def index(request: Request):
    with open('app.html') as fs:
        return response.html(fs.read())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True, access_log=True, auto_reload=True)
