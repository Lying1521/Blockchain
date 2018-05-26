from blockchain import Blockchain
import pow

bc = Blockchain()

block = bc.new_block(1,123124124124)
print(bc.hash(block))

print(pow.proof_of_work(100))
