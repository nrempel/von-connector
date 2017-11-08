# VON Connector

Verifiable Organization Network Connector

## Requirements

To run this project locally, you must have a local instance of the VON Network running.

## Running the VON Connector

Start the Indy nodes:

```bash
./manage start_nodes
```

Once that completes, start the VON Connector in a separate terminal window:

```bash
./manage start_von_connector
```

It will first take a minute to bootstrap the environment and once that completes you should see something like this:

```
Opening pool...



 INFO|command_executor              |                src/commands/mod.rs:71  | Worker thread started
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:54  | Create command received
_indy_loop_callback: Function returned None
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:62  | Open command received
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node3 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 {"ppSeqNo":null,"txnSeqNo":4,"op":"LEDGER_STATUS","ledgerId":0,"viewNo":null,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg"}
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node2 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node4 po
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "{\"op\":\"LEDGER_STATUS\",\"txnSeqNo\":4,\"merkleRoot\":\"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg\",\"ledgerId\":0,\"ppSeqNo\":null,\"viewNo\":null}"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node2 {"ppSeqNo":null,"viewNo":null,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg","ledgerId":0,"txnSeqNo":4,"op":"LEDGER_STATUS"}
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node3 {"ppSeqNo":null,"ledgerId":0,"merkleRoot":"EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg","viewNo":null,"op":"LEDGER_STATUS","txnSeqNo":4}
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|indy::commands::pool          |               src/commands/pool.rs:66  | OpenAck handle 1, result Ok(2)
_indy_loop_callback: Function returned 2



Finished opening pool






Closing pool...



 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:81  | Close command received
 INFO|pooltest                      |           src/services/pool/mod.rs:792 | Drop started
 INFO|pooltest                      |           src/services/pool/mod.rs:800 | Drop wait worker
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 INFO|indy::services::pool          |           src/services/pool/mod.rs:863 | Sending "pi"
 WARN|indy::services::pool          |           src/services/pool/mod.rs:146 | unhandled msg LedgerStatus(LedgerStatus { txnSeqNo: 4, merkleRoot: "EzzssMLPWnemT3HVM8c5iWtgjNB5DD3ZwXJfhFJWugeg", ledgerId: 0, ppSeqNo: None, viewNo: None })
 INFO|indy::services::pool          |           src/services/pool/mod.rs:857 | RemoteNode::recv_msg Node1 po
 WARN|indy::services::pool          |           src/services/pool/mod.rs:146 | unhandled msg Pong
 INFO|pooltest                      |           src/services/pool/mod.rs:803 | Drop finished
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:85  | CloseAck command received
_indy_loop_callback: Function returned None
 INFO|indy::commands                |                src/commands/mod.rs:107 | PoolCommand command received
 INFO|pool_command_executor         |               src/commands/pool.rs:58  | Delete command received
_indy_loop_callback: Function returned None



Finished closing pool
```

The VON Agent has connected to the network!

## Magic

For now we bootstrap our local network of nodes using some magic functions provided by the Indy team. I'll try to demystify some things here.

The following genesis transaction file is generated by running

```
{"dest":"V4SGRU86Z58d6TV7PBUe6f","role":"0","type":"1","verkey":"~CoRER63DVYnWZtK8uAzNbx"}
{"dest":"Th7MpTaRZVRYnPiabds81Y","identifier":"V4SGRU86Z58d6TV7PBUe6f","role":"2","type":"1","verkey":"~7TYfekw4GUagBnBVCqPjiC"}
{"dest":"EbP4aYNeTHL6q385GuVpRV","identifier":"V4SGRU86Z58d6TV7PBUe6f","role":"2","type":"1","verkey":"~RHGNtfvkgPEUQzQNtNxLNu"}
{"dest":"4cU41vWW82ArfxJxHkzXPG","identifier":"V4SGRU86Z58d6TV7PBUe6f","role":"2","type":"1","verkey":"~EMoPA6HrpiExVihsVfxD3H"}
{"dest":"TWwCRQRZ2ZHMJFn9TzLp7W","identifier":"V4SGRU86Z58d6TV7PBUe6f","role":"2","type":"1","verkey":"~UhP7K35SAXbix1kCQV4Upx"}
{"dest":"7JhapNNMLnwkbiC2ZmPZSE","identifier":"V4SGRU86Z58d6TV7PBUe6f","type":"1","verkey":"~LgpYPrzkB6awcHMTPZ9TVn"}
```