import encryption as encrypt


psw_bob = "This is Bob's psw"
psw_alice = "This is Alice's psw"

Bob_private_key2,Bob_public_key2 = encrypt.create_key(psw_bob)
Alice_private_key2,Alice_public_key2 = encrypt.create_key(psw_alice)

raw_private_key = encrypt.encode_key(Bob_private_key2)
raw_public_key = encrypt.encode_key(Bob_public_key2)

str1 = 'a123456789012345678901234567890d'
print(len(str1))
print(encrypt.decode_private_key(str1))
secert_key = encrypt.decode_private_key(raw_private_key)

public_key = encrypt.decode_public_key(raw_public_key)


msg = encrypt.sha_256("Hi Alice, I love you")

msg_sign = encrypt.sign(msg, secert_key)

res,s = encrypt.verify(msg_sign,public_key)
print(s,'utf-8')
print(msg,'utf-8')

print(res)

msg_send = "bob to alice"
secert_msg=encrypt.send_secret_msg(Alice_public_key2, msg_send)
plain_text=encrypt.read_secret_msg(Alice_private_key2, secert_msg)
print(plain_text)