from socketio import AsyncNamespace


class CollectNamespace(AsyncNamespace):
    def on_connect(self, sid: str, environ: dict):
        print(f'conectado: {sid}, {environ}')

    def on_disconnect(self, sid: str):
        pass

    async def start_monitor(self, sid: str, data: dict):
        pass

    async def stop_monitor(self, sid: str, data: dict):
        pass
