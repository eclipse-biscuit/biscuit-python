"""
Type stubs for lib.rs
"""

from __future__ import annotations
from datetime import timedelta
from typing import Callable, Optional, Mapping, Any, List, Union, TypeAlias, final

__all__ = [
    "PublicKey",
    "PrivateKey",
    "Biscuit",
    "BiscuitBuilder",
    "BlockBuilder",
    "Authorizer",
    "AuthorizerBuilder",
    "AuthorizerLimits",
    "Fact",
    "Rule",
    "Check",
    "Policy",
    "UnverifiedBiscuit",
    "Algorithm",
    "ThirdPartyRequest",
    "ThirdPartyBlock",
    "DataLogError",
    "AuthorizationError",
    "BiscuitBuildError",
    "BiscuitBlockError",
    "BiscuitValidationError",
    "BiscuitSerializationError",
    "Parameters",
    "ScopeParameters",
    "PublicKeyProvider",
    "ExternFunc",
    "Term",
]

class DataLogError(Exception):
    pass

class AuthorizationError(Exception):
    pass

class BiscuitBuildError(Exception):
    pass

class BiscuitValidationError(Exception):
    pass

class BiscuitSerializationError(Exception):
    pass

class BiscuitBlockError(Exception):
    pass

# Also defined at runtime, in add_type_aliases (src/lib.rs). Keep both in sync.

#: A datalog term, as a python value: `int`, `str`, `bytes`, `bool`, `datetime` (with a timezone),
#: a `set` of those, a `list` of terms, or a `dict` with `str` or `int` keys and term values
Term: TypeAlias = Any
#: Values for the parameters (`{name}`) in a datalog snippet, indexed by parameter name
Parameters: TypeAlias = Optional[Mapping[str, Term]]
#: Public keys for the public key parameters (`trusting {name}`) in a datalog snippet, indexed by parameter name
ScopeParameters: TypeAlias = Optional[Mapping[str, PublicKey]]
#: A function selecting the root public key used to verify a token. It is called
#: with the token's root key id (or `None` if it does not have one)
PublicKeyProvider: TypeAlias = Callable[[Optional[int]], PublicKey]
#: An external function, called by the datalog `.extern::name()` operations. It is called
#: with one argument for unary operations and two for binary operations, and returns a term
ExternFunc: TypeAlias = Union[Callable[[Term], Term], Callable[[Term, Term], Term]]

@final
class Algorithm:
    Ed25519: Algorithm
    Secp256r1: Algorithm

@final
class BiscuitBuilder:
    # Create a builder from a datalog snippet and optional parameter values
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def __new__(
        cls,
        source: Optional[str] = None,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> BiscuitBuilder: ...

    # Build a biscuit token, using the provided private key to sign the authority block
    #
    # :param root: a keypair that will be used to sign the authority block
    # :type root: PrivateKey
    # :return: a biscuit token
    # :rtype: Biscuit
    def build(self, root: PrivateKey) -> Biscuit: ...

    # Add code to the builder, using the provided parameters.
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def add_code(
        self,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> None: ...

    # Add a single fact to the builder. A single fact can be built with
    # the `Fact` class and its constructor
    #
    # :param fact: a datalog fact
    # :type fact: Fact
    def add_fact(self, fact: Fact) -> None: ...

    # Add a single rule to the builder. A single rule can be built with
    # the `Rule` class and its constructor
    #
    # :param rule: a datalog rule
    # :type rule: Rule
    def add_rule(self, rule: Rule) -> None: ...

    # Add a single check to the builder. A single check can be built with
    # the `Check` class and its constructor
    #
    # :param check: a datalog check
    # :type check: Check
    def add_check(self, check: Check) -> None: ...

    # Merge a `BlockBuilder` in this `BiscuitBuilder`. The `BlockBuilder` parameter will not be modified
    #
    # :param builder: a datalog BlockBuilder
    # :type builder: BlockBuilder
    def merge(self, builder: BlockBuilder) -> None: ...

    # Set the root key identifier for this `BiscuitBuilder`
    #
    # :param root_key_id: the root key identifier
    # :type root_key_id: int
    def set_root_key_id(self, root_key_id: int) -> None: ...

@final
class Biscuit:
    # Creates a BiscuitBuilder
    #
    # :return: an empty BiscuitBuilder
    # :rtype: BiscuitBuilder
    @staticmethod
    def builder() -> BiscuitBuilder: ...

    # Deserializes a token from raw data
    #
    # This will check the signature using the provided root key (or function)
    #
    # :param data: raw biscuit bytes
    # :type data: bytes
    # :param root: either a public key or a function taking an integer (or `None`) and returning an public key
    # :type root: function,PublicKey
    # :return: the parsed and verified biscuit
    # :rtype: Biscuit
    @classmethod
    def from_bytes(
        cls, data: bytes, root: PublicKey | PublicKeyProvider
    ) -> Biscuit: ...

    # Deserializes a token from URL safe base 64 data
    #
    # This will check the signature using the provided root key (or function)
    #
    # :param data: a (url-safe) base64-encoded string
    # :type data: str
    # :param root: either a public key or a function taking an integer (or `None`) and returning an public key
    # :type root: function,PublicKey
    # :return: the parsed and verified biscuit
    # :rtype: Biscuit
    @classmethod
    def from_base64(cls, data: str, root: PublicKey | PublicKeyProvider) -> Biscuit: ...

    # Serializes to raw bytes
    #
    # :return: the serialized biscuit
    # :rtype: bytes
    def to_bytes(self) -> bytes: ...

    # Serializes to URL safe base 64 data
    #
    # :return: the serialized biscuit
    # :rtype: str
    def to_base64(self) -> str: ...

    # Returns the number of blocks in the token
    #
    # :return: the number of blocks
    # :rtype: int
    def block_count(self) -> int: ...

    # Prints a block's content as Datalog code
    #
    # :param index: the block index
    # :type index: int
    # :return: the code for the corresponding block
    # :rtype: str
    def block_source(self, index: int) -> str: ...

    # Create a new `Biscuit` by appending an attenuation block
    #
    # :param block: a builder for the new block
    # :type block: BlockBuilder
    # :return: the attenuated biscuit
    # :rtype: Biscuit
    def append(self, block: BlockBuilder) -> Biscuit: ...

    # Create a new `Biscuit` by appending a third-party attenuation block
    #
    # :param external_key: the public key of the third-party that signed the block.
    # :type external_key: PublicKey
    # :param block: the third party block to append
    # :type block: ThirdPartyBlock
    # :return: the attenuated biscuit
    # :rtype: Biscuit
    def append_third_party(
        self,
        external_key: PublicKey,
        block: ThirdPartyBlock,
    ) -> Biscuit: ...

    # Create a third-party request for generating third-party blocks.
    #
    # :return: the third-party request
    # :rtype: ThirdPartyRequest
    def third_party_request(self) -> ThirdPartyRequest: ...

    # The revocation ids of the token, encoded as hexadecimal strings
    @property
    def revocation_ids(self) -> List[str]: ...

    # Get the external key of a block if it exists
    #
    # :param index: the block index
    # :type index: int
    # :return: the public key if it exists
    # :rtype: PublicKey | None
    def block_external_key(self, index: int) -> Optional[PublicKey]: ...

# Runtime limits of the authorizer
@final
class AuthorizerLimits:
    max_facts: int
    max_iterations: int
    max_time: timedelta
    max_steps: int

@final
class AuthorizerBuilder:
    # Create a new authorizer from a datalog snippet and optional parameter values
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def __new__(
        cls,
        source: Optional[str] = None,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> AuthorizerBuilder: ...

    # Add code to the builder, using the provided parameters.
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def add_code(
        self,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> None: ...

    # Add a single fact to the authorizer. A single fact can be built with
    # the `Fact` class and its constructor
    #
    # :param fact: a datalog fact
    # :type fact: Fact
    def add_fact(self, fact: Fact) -> None: ...

    # Add a single rule to the authorizer. A single rule can be built with
    # the `Rule` class and its constructor
    #
    # :param rule: a datalog rule
    # :type rule: Rule
    def add_rule(self, rule: Rule) -> None: ...

    # Add a single check to the authorizer. A single check can be built with
    # the `Check` class and its constructor
    #
    # :param check: a datalog check
    # :type check: Check
    def add_check(self, check: Check) -> None: ...

    # Add a single policy to the authorizer. A single policy can be built with
    # the `Policy` class and its constructor
    #
    # :param policy: a datalog policy
    # :type policy: Policy
    def add_policy(self, policy: Policy) -> None: ...

    # Returns the runtime limits of the authorizer
    def limits(self) -> AuthorizerLimits: ...

    # Sets the runtime limits of the authorizer
    #
    # Those limits cover all the executions under the `authorize`, `query` and `query_all` methods
    def set_limits(self, limits: AuthorizerLimits) -> None: ...

    # adds a fact `time($current_time)` with the current time
    def set_time(self) -> None: ...

    # Merge another `AuthorizerBuilder` in this `AuthorizerBuilder`. The `AuthorizerBuilder` argument will not be modified
    #
    # :param builder: an AuthorizerBuilder
    # :type builder: AuthorizerBuilder
    def merge(self, builder: AuthorizerBuilder) -> None: ...

    # Merge a `BlockBuilder` in this `Authorizer`. The `BlockBuilder` will not be modified
    #
    # :param builder: a BlockBuilder
    # :type builder: BlockBuilder
    def merge_block(self, builder: BlockBuilder) -> None: ...

    # Register an external function, called by the datalog `.extern::name()` operations
    def register_extern_func(self, name: str, func: ExternFunc) -> None: ...

    # Register several external functions
    def register_extern_funcs(self, funcs: Mapping[str, ExternFunc]) -> None: ...

    # Replace all the registered external functions
    def set_extern_funcs(self, funcs: Mapping[str, ExternFunc]) -> None: ...

    # Take a snapshot of the authorizer builder and return it, base64-encoded
    #
    # :return: a snapshot as a base64-encoded string
    # :rtype: str
    def base64_snapshot(self) -> str: ...

    # Take a snapshot of the authorizer builder and return it, as raw bytes
    #
    # :return: a snapshot as raw bytes
    # :rtype: bytes
    def raw_snapshot(self) -> bytes: ...

    # Build an authorizer builder from a base64-encoded snapshot
    #
    # :param input: base64-encoded snapshot
    # :type input: str
    # :return: the authorizer builder
    # :rtype: AuthorizerBuilder
    @classmethod
    def from_base64_snapshot(cls, input: str) -> AuthorizerBuilder: ...

    # Build an authorizer builder from a snapshot's raw bytes
    #
    # :param input: raw snapshot bytes
    # :type input: bytes
    # :return: the authorizer builder
    # :rtype: AuthorizerBuilder
    @classmethod
    def from_raw_snapshot(cls, input: bytes) -> AuthorizerBuilder: ...

    # Build the `AuthorizerBuilder` with the provided `Biscuit`
    #
    # :param token: the token to authorize
    # :type token: Biscuit
    # :return: the authorizer
    # :rtype: Authorizer
    def build(self, token: Biscuit) -> Authorizer: ...

    # Build the `AuthorizerBuilder` without a token
    #
    # :return: the authorizer
    # :rtype: Authorizer
    def build_unauthenticated(self) -> Authorizer: ...

@final
class Authorizer:
    # Runs the authorization checks and policies
    #
    # Returns the index of the matching allow policy, or an error containing the matching deny
    # policy or a list of the failing checks
    #
    # :return: the index of the matched allow rule
    # :rtype: int
    def authorize(self) -> int: ...

    # Query the authorizer by returning all the `Fact`s generated by the provided `Rule`. The generated facts won't be
    # added to the authorizer world.
    #
    # This function can be called before `authorize`, but in that case will only return facts that are directly defined,
    # not the facts generated by rules.
    #
    # :param rule: a rule that will be ran against the authorizer contents
    # :type rule: Rule
    # :return: a list of generated facts
    # :rtype: list
    def query(self, rule: Rule) -> List[Fact]: ...

    # Take a snapshot of the authorizer and return it, base64-encoded
    #
    # :return: a snapshot as a base64-encoded string
    # :rtype: str
    def base64_snapshot(self) -> str: ...

    # Take a snapshot of the authorizer and return it, as raw bytes
    #
    # :return: a snapshot as raw bytes
    # :rtype: bytes
    def raw_snapshot(self) -> bytes: ...

    # Build an authorizer from a base64-encoded snapshot
    #
    # :param input: base64-encoded snapshot
    # :type input: str
    # :return: the authorizer
    # :rtype: Authorizer
    @classmethod
    def from_base64_snapshot(cls, input: str) -> Authorizer: ...

    # Build an authorizer from a snapshot's raw bytes
    #
    # :param input: raw snapshot bytes
    # :type input: bytes
    # :return: the authorizer
    # :rtype: Authorizer
    @classmethod
    def from_raw_snapshot(cls, input: bytes) -> Authorizer: ...

# Builder class allowing to create a block meant to be appended to an existing token
@final
class BlockBuilder:
    # Create a builder from a datalog snippet and optional parameter values
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def __new__(
        cls,
        source: Optional[str] = None,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> BlockBuilder: ...

    # Add a single fact to the builder. A single fact can be built with
    # the `Fact` class and its constructor
    #
    # :param fact: a datalog fact
    # :type fact: Fact
    def add_fact(self, fact: Fact) -> None: ...

    # Add a single rule to the builder. A single rule can be built with
    # the `Rule` class and its constructor
    #
    # :param rule: a datalog rule
    # :type rule: Rule
    def add_rule(self, rule: Rule) -> None: ...

    # Add a single check to the builder. A single check can be built with
    # the `Check` class and its constructor
    #
    # :param check: a datalog check
    # :type check: Check
    def add_check(self, check: Check) -> None: ...

    # Merge a `BlockBuilder` in this `BlockBuilder`. The `BlockBuilder` will not be modified
    #
    # :param builder: a datalog BlockBuilder
    # :type builder: BlockBuilder
    def merge(self, builder: BlockBuilder) -> None: ...

    # Add code to the builder, using the provided parameters.
    #
    # :param source: a datalog snippet
    # :type source: str, optional
    # :param parameters: values for the parameters in the datalog snippet
    # :type parameters: dict, optional
    # :param scope_parameters: public keys for the public key parameters in the datalog snippet
    # :type scope_parameters: dict, optional
    def add_code(
        self,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> None: ...

# public key
@final
class PublicKey:
    # Serializes a public key to raw bytes
    #
    # :return: the public key bytes
    # :rtype: bytes
    def to_bytes(self) -> bytes: ...

    # Serializes a public key to DER format
    #
    # :return: the public key DER bytes
    # :rtype: bytes
    def to_der(self) -> bytes: ...

    # Serializes a public key to PEM format
    #
    # :return: the public key PEM string
    # :rtype: str
    def to_pem(self) -> str: ...

    # Deserializes a public key from raw bytes
    #
    # :param data: the raw bytes
    # :type data: bytes
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_bytes(cls, data: bytes, alg: Algorithm) -> PublicKey: ...

    # Deserializes a public key from DER bytes
    #
    # :param der: the DER bytes
    # :type der: bytes
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_der(cls, der: bytes) -> PublicKey: ...

    # Deserializes a public key from a PEM string
    #
    # :param pem: the PEM string
    # :type pem: str
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_pem(cls, pem: str) -> PublicKey: ...

    # Deserializes a public key from a hexadecimal string
    #
    # :param data: the hex-encoded string
    # :type data: str
    # :return: the public key
    # :rtype: PublicKey
    def __new__(cls, data: str) -> PublicKey: ...
    # Serializes a public key to raw bytes
    #
    # :return: the public key bytes
    # :rtype: list
    def to_bytes(self) -> bytes: ...

    # Deserializes a public key from raw bytes
    #
    # :param data: the raw bytes
    # :type data: bytes
    # :param alg: the key algorithm
    # :type alg: Algorithm
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_bytes(cls, data: bytes, alg: Algorithm) -> PublicKey: ...

    # Deserializes a public key from a hexadecimal string
    #
    # :param data: the hex-encoded string
    # :type data: str
    # :return: the public key
    # :rtype: PublicKey
    def __new__(cls, data: str) -> PublicKey: ...

    # Deserializes a public key from a DER buffer
    #
    # :param der: the DER buffer
    # :type der: bytes
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_der(cls, der: bytes) -> PublicKey: ...

    # Deserializes a public key from a PEM string
    #
    # :param pem: the PEM string
    # :type pem: str
    # :return: the public key
    # :rtype: PublicKey
    @classmethod
    def from_pem(cls, pem: str) -> PublicKey: ...

# private key
@final
class PrivateKey:
    # Serializes a private key to raw bytes
    #
    # :return: the private key bytes
    # :rtype: bytes
    def to_bytes(self) -> bytes: ...

    # Deserializes a private key from raw bytes
    #
    # :param data: the raw bytes
    # :type data: bytes
    # :param alg: the key algorithm
    # :type alg: Algorithm
    # :return: the private key
    # :rtype: PrivateKey
    @classmethod
    def from_bytes(cls, data: bytes, alg: Algorithm) -> PrivateKey: ...

    # Deserializes a private key from a hexadecimal string
    #
    # :param data: the hex-encoded string
    # :type data: str
    # :return: the private key
    # :rtype: PrivateKey
    def __new__(cls, data: str) -> PrivateKey: ...

    # Deserializes a private key from a DER buffer
    #
    # :param der: the DER buffer
    # :type der: bytes
    # :return: the private key
    # :rtype: PrivateKey
    @classmethod
    def from_der(cls, der: bytes) -> PrivateKey: ...

    # Deserializes a private key from a PEM string
    #
    # :param pem: the PEM string
    # :type pem: str
    # :return: the private key
    # :rtype: PrivateKey
    @classmethod
    def from_pem(cls, pem: str) -> PrivateKey: ...

    # Generate a random ed25519 private key
    @classmethod
    def random(cls) -> PrivateKey: ...

    # The public key part
    @property
    def public_key(self) -> PublicKey: ...

# A single datalog Fact
#
# :param source: a datalog fact (without the ending semicolon)
# :type source: str
# :param parameters: values for the parameters in the datalog fact
# :type parameters: dict, optional
@final
class Fact:
    # Build a datalog fact from the provided source and optional parameter values
    def __new__(cls, source: str, parameters: Parameters = None) -> Fact: ...

    # The fact name
    @property
    def name(self) -> str: ...

    # The fact terms
    @property
    def terms(self) -> List[Any]: ...

# A single datalog rule
#
# :param source: a datalog rule (without the ending semicolon)
# :type source: str
# :param parameters: values for the parameters in the datalog rule
# :type parameters: dict, optional
# :param scope_parameters: public keys for the public key parameters in the datalog rule
# :type scope_parameters: dict, optional
@final
class Rule:
    # Build a rule from the source and optional parameter values
    def __new__(
        cls,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> Rule: ...

# A single datalog check
#
# :param source: a datalog check (without the ending semicolon)
# :type source: str
# :param parameters: values for the parameters in the datalog check
# :type parameters: dict, optional
# :param scope_parameters: public keys for the public key parameters in the datalog check
# :type scope_parameters: dict, optional
@final
class Check:
    # Build a check from the source and optional parameter values
    def __new__(
        cls,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> Check: ...

# A single datalog policy
#
# :param source: a datalog policy (without the ending semicolon)
# :type source: str
# :param parameters: values for the parameters in the datalog policy
# :type parameters: dict, optional
# :param scope_parameters: public keys for the public key parameters in the datalog policy
# :type scope_parameters: dict, optional
@final
class Policy:
    # Build a check from the source and optional parameter values
    def __new__(
        cls,
        source: str,
        parameters: Parameters = None,
        scope_parameters: ScopeParameters = None,
    ) -> Policy: ...

# Representation of a biscuit token that has been parsed but not cryptographically verified
@final
class UnverifiedBiscuit:
    # Deserializes a token from URL safe base 64 data
    #
    # The signature will NOT be checked
    #
    # :param data: a (url-safe) base64-encoded string
    # :type data: str
    # :return: the parsed, unverified biscuit
    # :rtype: UnverifiedBiscuit
    @classmethod
    def from_base64(cls, data: str) -> UnverifiedBiscuit: ...

    # Returns the root key identifier for this `UnverifiedBiscuit` (or `None` if there is none)
    #
    # :return: the root key identifier
    # :rtype: int
    def root_key_id(self) -> Optional[int]: ...

    # Returns the number of blocks in the token
    #
    # :return: the number of blocks
    # :rtype: int
    def block_count(self) -> int: ...

    # Prints a block's content as Datalog code
    #
    # :param index: the block index
    # :type index: int
    # :return: the code for the corresponding block
    # :rtype: str
    def block_source(self, index: int) -> str: ...

    # Create a new `UnverifiedBiscuit` by appending an attenuation block
    #
    # :param block: a builder for the new block
    # :type block: BlockBuilder
    # :return: the attenuated biscuit
    # :rtype: Biscuit
    def append(self, block: BlockBuilder) -> UnverifiedBiscuit: ...

    # The revocation ids of the token, encoded as hexadecimal strings
    @property
    def revocation_ids(self) -> List[str]: ...

    # Verifies the token signature using the provided root key (or function)
    #
    # :param root: either a public key or a function taking an integer (or `None`) and returning an public key
    # :type root: function,PublicKey
    # :return: the verified biscuit
    # :rtype: Biscuit
    def verify(self, root: PublicKey | PublicKeyProvider) -> Biscuit: ...

# Third party block request
@final
class ThirdPartyRequest:
    # Create a third-party block
    #
    # :param private_key: the third-party's private key used to sign the block
    # :type external_key: PrivateKey
    # :param block: the block builder to be signed
    # :type block: BlockBuilder
    # :return: a signed block that can be appended to a Biscuit
    # :rtype: ThirdPartyBlock
    #
    # :note: this method consumes the `ThirdPartyRequest` object.
    def create_block(
        self,
        private_key: PrivateKey,
        block: BlockBuilder
    ) -> ThirdPartyBlock: ...

# Third party block contents
@final
class ThirdPartyBlock:
    pass
