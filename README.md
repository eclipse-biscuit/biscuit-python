# Python bindings for biscuit

This library provides python bindings to the [eclipse biscuit_auth](https://docs.rs/biscuit-auth/latest/biscuit_auth/) rust library.

As it is a pre-1.0 version, you can expect some API changes. However, most of the use cases are covered:

- building a token
- appending a (first-party or third-party) block to a token
- parsing a token
- authorizing a token
- querying an authorizer

## Documentation

Documentation is available at <https://python.biscuitsec.org>.

## Installation

`biscuit-python` is published on PyPI: [biscuit-python](https://pypi.org/project/biscuit-python/):

```
pip install biscuit-python
```

## Building/Testing

Set up a virtualenv and install the dev dependencies. Plenty of ways to do that... Here's one of them:

```
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements-dev.txt
```

With that, you should be able to run `maturin develop` to build and install the extension. You can then `import biscuit_auth` in a Python shell to play around, or run `pytest` to run the Python tests.

## License

Licensed under Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE) or http://www.apache.org/licenses/LICENSE-2.0)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be licensed as above, without any additional terms or
conditions.
