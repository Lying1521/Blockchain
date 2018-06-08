import hashlib


def proof_of_work(last_proof):

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


def valid_proof(last_proof, proof):
    guess = str(last_proof)+str(proof).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"