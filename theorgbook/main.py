#!/usr/bin/python3

import asyncio
import calendar
import time
import json

from sanic import Sanic
from sanic.response import json as sanic_json
from von_agent.nodepool import NodePool
from von_agent.demo_agents import OrgBookAgent

app = Sanic(__name__)


async def boot():
    global pool
    global orgbook

    pool = NodePool(
        # Hack to use different pool names. Agent lib doesn't support
        # reopening existing pool config
        'theorgbook' + str(calendar.timegm(time.gmtime())),
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()
    orgbook = OrgBookAgent(
        pool,
        'The-Org-Book-Agent-0000000000000',
        'the-org-book-agent-wallet',
        None,
        '127.0.0.1',
        9702,
        'api/v0')
    await orgbook.open()
    await orgbook.create_master_secret('secret')


@app.route("/")
async def test(request):
    return sanic_json({"hello": "world"})


@app.route("/get-claim-request", methods=['POST'])
async def get_claim_request(request):
    did = request.json['did']
    seqNo = request.json['seqNo']
    claim_def_json = request.json['claim_def']

    await orgbook.store_claim_offer(did, seqNo)
    claim_req_json = await orgbook.store_claim_req(did, claim_def_json)

    return sanic_json(claim_req_json)


@app.route("/store-claim", methods=['POST'])
async def store_claim(request):
    await orgbook.store_claim(json.dumps(request.json))

    return sanic_json({'success': True})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)
