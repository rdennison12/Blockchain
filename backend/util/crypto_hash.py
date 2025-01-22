import hashlib
import json


def stringify(data):
    return json.dumps(data)


def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguments.
    :param *args: the arguments to hash
    :return:
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one',  [3])}")
    print(f"crypto_hash(1, [2], 'three'): {crypto_hash(1, [2], 'three')}")
    print(f"crypto_hash(foo): {crypto_hash('foo')}")


if __name__ == '__main__':
    main()
