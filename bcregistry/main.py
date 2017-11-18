#! /usr/bin/python3

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, SRIAgent, OrgBookAgent, BCRegistrarAgent
from von_agent.util import encode

import requests

import asyncio
import json
import os


def claim_value_pair(plain):
    return [str(plain), encode(plain)]


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

CLAIMS = [
    {
        'id': claim_value_pair('1'),
        'busId': claim_value_pair('11121398'),
        'orgTypeId': claim_value_pair('2'),
        'jurisdictionId': claim_value_pair('1'),
        'LegalName': claim_value_pair('The Original House of Pies'),
        'effectiveDate': claim_value_pair('2010-10-10'),
        'endDate': claim_value_pair(None),
        'sriRegDate': claim_value_pair(None)
    },
    {
        'id': claim_value_pair('2'),
        'busId': claim_value_pair('11133333'),
        'orgTypeId': claim_value_pair('1'),
        'jurisdictionId': claim_value_pair('1'),
        'LegalName': claim_value_pair('Planet Cake'),
        'effectiveDate': claim_value_pair('2011-10-01'),
        'endDate': claim_value_pair(None),
        'sriRegDate': claim_value_pair(None)
    },
    {
        'id': claim_value_pair('3'),
        'busId': claim_value_pair('11144444'),
        'orgTypeId': claim_value_pair('2'),
        'jurisdictionId': claim_value_pair('1'),
        'LegalName': claim_value_pair('Tart City'),
        'effectiveDate': claim_value_pair('2012-12-01'),
        'endDate': claim_value_pair(None),
        'sriRegDate': claim_value_pair(None)
    }
]


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

    claim_req_json = r.json()

    for c in CLAIMS:
        (_, claim_json) = await bcrag.create_claim(claim_req_json, c)
        r = requests.post(
            base_url + '/store-claim',
            json=json.loads(claim_json)
        )

        print(r.text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
