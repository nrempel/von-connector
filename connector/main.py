#! /usr/bin/python3

from von_agent.service_wrapper_project.wrapper_api.agent.nodepool import NodePool

import asyncio


async def main():
    pool = NodePool('test', '.indy/pool_transactions_sandbox_genesis')
    await pool.open()

    # trust_anchor = 

    await pool.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
