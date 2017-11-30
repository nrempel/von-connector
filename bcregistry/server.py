#! /usr/bin/python3

import asyncio
import csv
import os
import json
import logging
import time

import requests

from io import StringIO

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, BCRegistrarAgent
from von_agent.agents import BaseAgent
from von_agent.util import encode

from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)
db_settings = {'REQUEST_TIMEOUT': 3600}
app.config.update(db_settings)

app.static('/', './static/index.html')
app.static('/test_data.csv', './static/test_data.csv')


def claim_value_pair(plain):
    return [str(plain), encode(plain)]


VORG_SCHEMA = {
    'name': 'bc-corporate-registration',
    'version': '1.1',
    'attr_names': [
        'busId',
        'orgTypeId',
        'jurisdictionId',
        'LegalName',
        'effectiveDate',
        'endDate'
    ]
}


async def boot():
    global pool
    global trust_anchor
    global bcreg_agent
    global claim_def_json
    global schema

    pool = NodePool(
        'nodepool',
        '/home/indy/.genesis')
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


@app.route("/submit_claims", methods=['POST'])
async def submit_claims(request):
    resp_text = ""
    file = request.files.get('file')
    base_url = os.environ["TOB_URL"]

    resp_text += "Connect to TheOrgBook at %s...\n\n" % base_url

    resp_text += "Sending claim definition to TheOrgBook...\n\n"

    r = requests.post(
        base_url + '/bcovrin/generate-claim-request',
        json={
            'did': bcreg_agent.did,
            'seqNo': schema['seqNo'],
            'claim_def': claim_def_json
        }
    )
    claim_req_json = r.json()

    resp_text += "Received claim request from TheOrgBook: \n\n%s\n\n" % claim_req_json

    resp_text += "Parsing CSV...\n\n"

    rows = csv.DictReader(StringIO(file.body.decode('utf-8')))
    row_count = 0
    for row in rows:
        row_count += 1
        resp_text += "Handling row of CSV data:\n\n%s\n\n" % row

        claim = {
            "busId": claim_value_pair(row["CORP_NUM"]),
            "orgTypeId": claim_value_pair(row["CORP_NAME_TYP_CD"]),
            "jurisdictionId": claim_value_pair(row["PHYSICALCITY"]),
            "LegalName": claim_value_pair(row["CORP_NME"]),
            "effectiveDate": claim_value_pair("2010-10-01"),
            "endDate": claim_value_pair(None)
        }
        resp_text += "Generating claim for record and claim request...\n\n\n"
        (_, claim_json) = await bcreg_agent.create_claim(json.dumps(claim_req_json), claim)
        resp_text += "Successfully generated claim json:\n\n%s\n\n" % claim_json
        resp_text += "Sending claim json to TheOrgBook...\n\n"
        r = requests.post(
            base_url + '/bcovrin/store-claim',
            json=json.loads(claim_json)
        )
        time.sleep(1)


    resp_text += "Successfully sent %d claims to TheOrgBook." % row_count
    return text(resp_text)


@app.route("/submit_claim", methods=['POST'])
async def submit_claim(request):
    busId = request.form["busId"][0]
    orgTypeId = request.form["orgTypeId"][0]
    jurisdictionId = request.form["jurisdictionId"][0]
    LegalName = request.form["LegalName"][0]

    if not busId or not orgTypeId or not jurisdictionId or not LegalName:
        return text("bad request, missing form fields", status=400)

    base_url = os.environ["TOB_URL"]
    r = requests.post(
        base_url + '/bcovrin/generate-claim-request',
        json={
            'did': bcreg_agent.did,
            'seqNo': schema['seqNo'],
            'claim_def': claim_def_json
        }
    )
    claim_req_json = r.json()

    claim = {
        "busId": claim_value_pair(busId),
        "orgTypeId": claim_value_pair(orgTypeId),
        "jurisdictionId": claim_value_pair(jurisdictionId),
        "LegalName": claim_value_pair(LegalName),
        "effectiveDate": claim_value_pair("2010-10-01"),
        "endDate": claim_value_pair(None)
    }

    (_, claim_json) = await bcreg_agent.create_claim(json.dumps(claim_req_json), claim)
    r = requests.post(
        base_url + '/bcovrin/store-claim',
        json=json.loads(claim_json)
    )

    resp_text = "Successfully generated payload and sent to TheOrgBook:\n\n%s"\
        % claim_json

    return text(resp_text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=7000, debug=True)
