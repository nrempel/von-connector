#! /usr/bin/python3

import asyncio
import json


from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent
from von_agent.agents import BaseAgent

from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)
app.static('/', './html')


async def boot():
    global pool
    global trust_anchor

    pool = NodePool(
        'nodepool',
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()

    trust_anchor = TrustAnchorAgent(
        pool,
        '000000000000000000000000Trustee1',
        'trustee_wallet',
        None,
        '127.0.0.1',
        9700,
        'api/v0')
    await trust_anchor.open()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)
