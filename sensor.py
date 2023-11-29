import struct

from mqtt_client import CollectorMQTTClient

import random
import asyncio


async def main():
    collector_mqtt = CollectorMQTTClient('lse.dev.br', 'lse', ' lse')
    await collector_mqtt.main()

    while True:
        data = list()

        for i in range(0, 902):
            d = random.uniform(0.5, 0.8) if i < 900 else random.uniform(25.5, 28.5)
            data.append(d)

        fmt = '<'
        fmt += 'f' * 902
        payload = struct.pack(fmt, *data)

        collector_mqtt.client.publish('testando_sensor_3d', payload)
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
