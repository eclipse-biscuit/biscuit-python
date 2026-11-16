import unittest
import pytest
from biscuit_auth import Biscuit, KeyPair, BlockBuilder, BiscuitBuilder, ThirdPartyBlock, AuthorizerBuilder, Rule, \
    Authorizer


class SetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # generate auth keypair
        keypair = KeyPair()
        cls.private_auth_key = keypair.private_key
        cls.public_auth_key = keypair.public_key

        # some test data
        cls.arms = [ '1', '2', '3', '4', '5']
        cls.legs = [ '1', '2', '3', '4', '5']
        cls.heads = [ '1', '2', '3', '4', '5']

        # test state by exploiting mutable default bug :)
        cls.state = {}
        cls.block_keys = []

    def test_00_create_authority(self):
        biscuit = BiscuitBuilder("""
            arms({arms});
            legs({legs});
            heads({heads});
        """, {
            'arms' : self.arms,
            'legs' : self.legs,
            'heads' : self.heads,
        })
        self.state['block_count'] = 5
        self.state['biscuit'] = biscuit.build(self.private_auth_key)
        self.assertIsInstance(self.state['biscuit'] , Biscuit)

    def test_01_add_blocks(self):
        for block_id in range(1,self.state['block_count']):
            biscuit = self.state['biscuit']
            block_keypair = KeyPair()
            self.block_keys.append(block_keypair)

            request = biscuit.third_party_request()

            block_contents = BlockBuilder("""
                limb_id({limb_id});
                                
                check if arms($arms), limb_id($limb_id), $arms.contains($limb_id);
                check if legs($legs), limb_id($limb_id), $legs.contains($limb_id);
                check if heads($heads), limb_id($limb_id), $heads.contains($limb_id);
                """, {
                    'limb_id' : str(block_id),
                })
            self.assertIsInstance(block_contents, BlockBuilder)

            block = request.create_block(block_keypair.private_key, block_contents)
            self.assertIsInstance(block, ThirdPartyBlock)

            self.state['biscuit']  = biscuit.append_third_party(block_keypair.public_key, block)
            self.assertIsInstance(self.state['biscuit'] , Biscuit)

        print(f"\n\nBiscuit Created : {self.state['biscuit'] }")

    def test_02_create_authorizer(self):
        source = ""
        biscuit = self.state['biscuit']
        print()
        print("Blockcount: ", self.state['block_count'])
        print("Block_keys: ", self.block_keys)

        for block_id in range(1,self.state['block_count']):
            pubkey = self.block_keys[block_id - 1].public_key
            source += f'allow if limb_id("{block_id}") trusting {pubkey};'

        authorizer_builder = AuthorizerBuilder(source, parameters={'limb_id':2})
        self.assertIsInstance(authorizer_builder, AuthorizerBuilder)
        authorizer = authorizer_builder.build(biscuit)
        print(f"Authorizer Created : {authorizer}")
        result = authorizer.authorize()
        self.assertGreaterEqual(result, 0)
        self.state['authorizer'] = authorizer