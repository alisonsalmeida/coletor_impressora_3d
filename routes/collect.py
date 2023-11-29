from sanic import Request, Blueprint, response
from datetime import datetime

import hashlib


collect_route = Blueprint('collect_route', '/collect')


# inicia a colecta na impressora
@collect_route.post('/start')
async def start(request: Request) -> response.HTTPResponse:
    seed = datetime.utcnow().isoformat().encode()

    if request.app.config['COLLECT_ID'] is None:
        collect_id = hashlib.md5(seed).hexdigest()
        request.app.config['COLLECT_ID'] = collect_id

        data_collect = {
            'collect_id': collect_id,
            'created_at': datetime.utcnow()
        }

        storage_engine = request.app.config['MONGO_INTERFACE']
        await storage_engine.create_collect(data_collect)

        return response.json({'collect_id': collect_id}, status=201)

    return response.empty(status=401)


# para a coleta na impressora
@collect_route.post('/stop')
async def stop(request: Request) -> response.HTTPResponse:
    if request.app.config['COLLECT_ID'] is not None:
        request.app.config['COLLECT_ID'] = None

        return response.empty(status=204)

    return response.empty(status=401)
