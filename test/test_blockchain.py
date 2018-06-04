import requests
import encryption as encrypt
import json
import nacl.encoding

psw_bob = "This is Bob's psw"
psw_alice = "This is Alice's psw"

Bob_private_key2,Bob_public_key2 = encrypt.create_key(psw_bob)
Alice_private_key2,Alice_public_key2 = encrypt.create_key(psw_alice)


receiver_key = encrypt.encode_key(Alice_public_key2)
sender_key = encrypt.encode_key(Bob_public_key2)
msg = "Hi Alice, I love you"
msg_256 = encrypt.sha_256(msg)

signature = encrypt.sign(nacl.encoding.HexEncoder.encode(msg_256),Bob_private_key2)

transcation= {
    "sender": "d4ee26eee15148ee92c6cd394edd974e",
    "receiver": "someone-other-address",
    "msg": nacl.encoding.HexEncoder.encode(msg_256),
    "signature": signature,
    "receiver_public_key": receiver_key,
    "sender_public_key": sender_key,
    "id": "123174123"
 }

headers = {"Content-Type": "application/json"}
res = requests.post("http://127.0.0.1:5000/transactions/new", data=json.dumps(transcation),headers=headers)
print(res.json()['message'])

