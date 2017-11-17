#! /usr/bin/python3

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, \
    OrgBookAgent, BCRegistrarAgent

import asyncio
import json


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
    obag = OrgBookAgent(
        pool,
        'The-Org-Book-Agent-0000000000000',
        'the-org-book-agent-wallet',
        None,
        '127.0.0.1',
        9702,
        'api/v0')

    await tag.open()
    await bcrag.open()
    await obag.open()

    # Register agent on the network
    print('\n\nRegister agents\n\n')
    for ag in (tag, bcrag):

        print('\n\nGet Nym: ' + str(ag) + '\n\n')
        if not json.loads(await tag.get_nym(ag.did)):
            # pass
            print('\n\nSend Nym: ' + str(ag) + '\n\n')
            await tag.send_nym(ag.did, ag.verkey)
            print('\n\nGet Endpoint: ' + str(ag) + '\n\n')
        if not json.loads(await tag.get_endpoint(ag.did)):
            # pass
            print('\n\nSend Endpoint: ' + str(ag) + '\n\n')
            await ag.send_endpoint()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
