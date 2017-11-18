#! /usr/bin/python3

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, SRIAgent, OrgBookAgent, BCRegistrarAgent

import requests

import asyncio
import json
import os


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


async def main():

    # Open pool
    print('\n\nOpen pool\n\n')

    pool = NodePool(
        'test',
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()

    # Instantiate agents
    print('\n\nInstantiate agents\n\n')
    tag = TrustAnchorAgent(
        pool,
        '000000000000000000000000Trustee1',
        'trustee_wallet',
        None,
        '127.0.0.1',
        9700,
        'api/v0')
    bcrag = BCRegistrarAgent(
        pool,
        'BC-Registrar-Agent-0000000000000',
        'bc-registrar-agent-wallet',
        None,
        '127.0.0.1',
        9703,
        'api/v0')

    await tag.open()
    await bcrag.open()

    # Check if schema exists on ledger
    print('\n\nCheck if schema exists\n\n')
    schema_json = await tag.get_schema(
        tag.did, VORG_SCHEMA['name'], VORG_SCHEMA['version'])

    # If not, send the schema to the ledger
    print('\n\nsend the schema to the ledger\n\n')
    if not json.loads(schema_json):
        schema_json = await tag.send_schema(json.dumps(VORG_SCHEMA))

    schema = json.loads(schema_json)

    get_schema_result = await tag.get_schema(
        tag.did, VORG_SCHEMA['name'], VORG_SCHEMA['version'])

    get_schema_result = json.loads(get_schema_result)
    get_schema_result['data']['attr_names'] = get_schema_result['data'].pop('keys')
    get_schema_result = json.dumps(get_schema_result)

    print('-==--=-=---=')
    print(get_schema_result)
    print('-==--=-=---=')

    # Send claim definition
    print('\n\nSend claim definition\n\n')
    claim_def_json = await bcrag.send_claim_def(get_schema_result)
    claim_def_json = await bcrag.get_claim_def(schema['seqNo'], bcrag.did) 

    # Close pool
    print('\n\nclose pool\n\n')
    await pool.close()

    print('-==--=-=---=')
    print('claim_def_json:')
    print(claim_def_json)
    print('-==--=-=---=')

    base_url = os.environ["TOB_URL"]
    r = requests.post(
        base_url + '/get-claim-request',
        json={
            'did': bcrag.did,
            'seqNo': schema['seqNo'],
            'claim_def': claim_def_json
        }
    )

    print(r.text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
