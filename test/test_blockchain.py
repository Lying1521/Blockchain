import requests
import encryption as encrypt
import json
import nacl.encoding
from hog import Hog_descriptor
import cv2

psw_bob = "This is Bob's psw"
psw_alice = "This is Alice's psw"

Bob_private_key2,Bob_public_key2 = encrypt.create_key(psw_bob)
Alice_private_key2,Alice_public_key2 = encrypt.create_key(psw_alice)


receiver_key = encrypt.encode_key(Alice_public_key2)
sender_key = encrypt.encode_key(Bob_public_key2)

img = cv2.imread('/Users/liyu/Desktop/blockchain/Blockchain/ADE_train_00000158.jpg', cv2.IMREAD_GRAYSCALE)
hog = Hog_descriptor(img, cell_size=8, bin_size=8)
vector, image = hog.extract()
msg = vector.__str__()
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

