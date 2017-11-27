#! /usr/bin/python3

import asyncio
import json

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, BCRegistrarAgent
from von_agent.agents import BaseAgent

from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)
app.static('/', './html')


VORG_SCHEMA = {
    'name': 'supplier-registration',
    'version': '1.1',
    'attr_names': [
        'id',
        'busId',
        'orgTypeId',
        'jurisdictionId',
        'LegalName',
        'effectiveDate',
        'endDate',
        'sriRegDate'
    ]
}


async def boot():
    global pool
    global trust_anchor
    global claim_def_json

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

    bcreg_agent = BCRegistrarAgent(
        pool,
        'BC-Registrar-Agent-0000000000000',
        'bc-registrar-agent-wallet',
        None,
        '127.0.0.1',
        9703,
        'api/v0')

    await bcreg_agent.open()

    # Check if schema exists on ledger
    print('\n\nCheck if schema exists\n\n')
    schema_json = await trust_anchor.get_schema(
        trust_anchor.did, VORG_SCHEMA['name'], VORG_SCHEMA['version'])

    # If not, send the schema to the ledger
    print('\n\nsend the schema to the ledger\n\n')
    if not json.loads(schema_json):
        schema_json = await trust_anchor.send_schema(json.dumps(VORG_SCHEMA))

    schema = json.loads(schema_json)

    get_schema_result = await trust_anchor.get_schema(
        trust_anchor.did, VORG_SCHEMA['name'], VORG_SCHEMA['version'])

    print('-==--=-=---=')
    print(get_schema_result)
    print('-==--=-=---=')

    # Send claim definition
    print('\n\nSend claim definition\n\n')
    claim_def_json = await bcreg_agent.send_claim_def(get_schema_result)
    claim_def_json = await bcreg_agent.get_claim_def(
        schema['seqNo'], bcreg_agent.did)

    # Close pool
    print('\n\nclose pool\n\n')
    await pool.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)
