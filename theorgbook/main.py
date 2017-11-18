#!/usr/bin/python3

import asyncio
import calendar
import time

from sanic import Sanic
from sanic.response import json
from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, SRIAgent, OrgBookAgent, BCRegistrarAgent

app = Sanic(__name__)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/get-claim-request", methods=['POST'])
async def get_claim_request(request):

    pool = NodePool(
        # Hack to use different pool names. Agent lib doesn't support
        # reopening existing pool config
        'theorgbook' + str(calendar.timegm(time.gmtime())),
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()

    obag = OrgBookAgent(
        pool,
        'The-Org-Book-Agent-0000000000000',
        'the-org-book-agent-wallet',
        None,
        '127.0.0.1',
        9702,
        'api/v0')
    await obag.open()
    await obag.create_master_secret('secret')

    did = request.json['did']
    seqNo = request.json['seqNo']
    claim_def_json = request.json['claim_def']

    print(obag)

    await obag.store_claim_offer(did, seqNo)
    claim_req_json = await obag.store_claim_req(did, claim_def_json)

    return json(claim_req_json)


@app.route("/store-claim")
async def store_claim(request):
    return json({"hello": "world"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
