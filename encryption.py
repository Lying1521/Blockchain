import nacl.signing
import nacl.utils
import nacl.encoding
from nacl.public import SealedBox
import hashlib as hash


def create_key(pwd):

    hashcode = sha_256(pwd)
    private_key = nacl.signing.SigningKey(hashcode)
    public_key = private_key.verify_key
    return private_key,public_key


def sha_256(msg):
    return hash.sha256(msg).digest()


def sign(msg,sender_private_key):
    signature = sender_private_key.sign(msg, encoder =nacl.encoding.HexEncoder)
    return signature


def verify(signature,sender_public_key):
    try:
        raw_msg=sender_public_key.verify(signature,encoder=nacl.encoding.HexEncoder)
        return "signature is good",raw_msg
    except nacl.exceptions.BadSignatureError:
        return "signature is bad!", None


def send_secret_msg(receiver_public_key,msg):
    key = receiver_public_key.to_curve25519_public_key()
    sealed_box = SealedBox(key)
    return sealed_box.encrypt(msg)


def read_secret_msg(receiver_private_key,msg):
    try:
        key = receiver_private_key.to_curve25519_private_key()
        unseal_box = SealedBox(key)
        return unseal_box.decrypt(msg)
    except nacl.exceptions.CryptoError:
        return "wrong secret key"


def encode_key(secret_key):
    return secret_key.encode(encoder=nacl.encoding.HexEncoder)


def decode_public_key(raw_key):
    try:
        public_key = nacl.signing.VerifyKey(raw_key, encoder=nacl.encoding.HexEncoder)
        return public_key
    except nacl.exceptions.ValueError:
        return "wrong secret key"


def decode_private_key(raw_key):
    try:
        private_key = nacl.signing.SigningKey(raw_key, encoder=nacl.encoding.HexEncoder)
        return private_key
    except nacl.exceptions.ValueError:
        return "wrong secret key"


def check_block(block,block_chain):
    result = None
    required = ['index', 'transactions', 'last_proof', 'message', 'previous_hash', 'proof','timestamp']
    if not all(k in block for k in required):
        result = 'Missing values'

    if not pow.valid_proof(int(block['last_proof']), int(block['proof'])):
        result = 'Wrong proof'

    if len(block_chain.chain)>block['index']:
        result = 'update chain'

    if len(block_chain.chain) == block['index']:
        result = 'hold chain'

    return result


def check_transcations(transcations,current_transcation):
    result = None
    required = ['sender', 'receiver', 'msg', 'receiver_public_key', 'sender_public_key', 'id', 'signature']
    if not all(k in transcations for k in required):
        result = 'Missing values'
    for k in current_transcation:
        if k['id'] == transcations['id']:
            result = 'transcations has exist'
    sender_public_key = decode_public_key(transcations['sender_public_key'])
    res,msg = verify(transcations['signature'],sender_public_key)
    if not msg:
        result = res
    elif not msg == transcations['msg']:
        result = 'wrong message'
    return result
