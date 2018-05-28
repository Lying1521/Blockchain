import encryption as encrypt
from nacl import encoding


psw_bob = "This is Bob's psw"
psw_alice = "This is Alice's psw"

Bob_private_key2,Bob_public_key2 = encrypt.create_key(psw_bob)
Alice_private_key2,Alice_public_key2 = encrypt.create_key(psw_alice)

raw_private_key = encrypt.encode_key(Bob_private_key2)
raw_public_key = encrypt.encode_key(Alice_public_key2)

secert_key = encrypt.decode_private_key(raw_private_key)

public_key = encrypt.decode_public_key(raw_public_key)


msg = encrypt.sha_256("Hi Alice, I love you")

print(raw_public_key)

msg_sign = encrypt.sign(msg, secert_key)
s=encoding.RawEncoder.encode(msg_sign)
print (s)

res,s = encrypt.verify(str(111),public_key)

print(res)

msg_send = "bob to alice"
secert_msg=encrypt.send_secret_msg(Alice_public_key2, msg_send)
plain_text=encrypt.read_secret_msg(Alice_private_key2, secert_msg)
print(plain_text)