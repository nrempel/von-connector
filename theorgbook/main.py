#!/usr/bin/python3

import asyncio

from sanic import Sanic
from sanic.response import json
from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, SRIAgent, OrgBookAgent, BCRegistrarAgent

app = Sanic(__name__)

pool = None


async def boot():
    pool = NodePool(
        'test', '.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()




@app.route("/get-claim-request")
def get_claim_request():
    return "Hello World!"


@app.route("/store-claim")
def store_claim():
    return "Hello World!"


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)
