import hashlib
import json
from typing import Any


def crypto_hash(*args: Any) -> str:
    """Return a deterministic SHA-256 hash of the given arguments.

    Arguments are serialized to JSON with sorted keys and ordered lexicographically
    to guarantee consistent hashing regardless of input order or dictionary key placement.

    :param args: Arbitrary data objects to hash.
    :return: Hexadecimal SHA-256 hash string.
    """
    sorted_stringified_args = sorted(json.dumps(arg, sort_keys=True) for arg in args)
    payload = "".join(sorted_stringified_args).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")


if __name__ == "__main__":
    main()