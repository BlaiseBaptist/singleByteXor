from itertools import cycle
from typing import Dict, Any


def singleByteXor(text: bytearray, b: int) -> bytearray:
    out = bytearray()

    for i in text:
        out.append(i ^ b)

    return out


def vigenere(text: bytearray, key: bytearray) -> bytearray:
    out = bytearray()

    for i, j in zip(text, cycle(key)):
        out.append(i ^ j)

    return out


def write_ctext_file(ptext: str, fname: str) -> None:
    cbytes = ptext
    with open(fname, 'wb') as f:
        f.write(cbytes)


def read_ctext_file(fname: str) -> bytearray:
    with open(fname, 'rb') as f:
        cbytes = bytearray(f.read())
        return cbytes


def byte_counts(data: bytearray) -> Dict[int, int]:
    out = {b: 0 for b in data}  # Initialize a count of zero for each byte that appears in the data.
    for b in data:
        out[b] += 1  # Count how many times each byte appears.
    return out


def byte_ranks(data: bytearray) -> bytearray:
    counts = sorted(byte_counts(data).items(),  # Convert dictionary to a list of tuples
                    key=lambda item: item[1],  # Sort on the second item in the tuple (the count)
                    reverse=True  # Reverse order (more common bytes first)
                    )
    return bytearray([k[0] for k in counts])  # Throw away the counts, return bytes as a bytearray


def english_score(test: bytearray, english: bytearray, penalty=1000) -> int:
    return sum([english.index(b) if b in english  # The score of a byte is its position in the english ranks
                else penalty  # If a character does not appear in english then assign a high score
                for b in test]) / len(test)  # Add up the scores from each individual byte in test


def gen_english_ranks(infile='pg2701.txt') -> bytearray:
    with open(infile, 'rb') as f:
        data = f.read()
    return byte_ranks(data)


def break_single_byte(cbytes: bytearray, eng_ranks: bytearray) -> int:
    best_score = 10 ** 10
    best_key = 0
    for key in range(255):
        score = english_score(singleByteXor(cbytes, key), eng_ranks)
        if score < best_score:
            best_score = score
            best_key = key
    return best_key


def break_fixed_len_vigenere(cbytes: bytearray, key_len: int, eng_ranks: bytearray) -> bytearray:
    return bytearray([break_single_byte(cbytes[sep::key_len], eng_ranks) for sep in range(key_len)])


def break_vigenere(cbytes: bytearray, eng_ranks: bytearray, check_keys: int = 1) -> bytearray:
    return (lambda x: x[min(x)])(dict([(lambda key: (english_score(vigenere(cbytes, key), eng_ranks), key))(
        break_fixed_len_vigenere(cbytes, key_len, eng_ranks)) for key_len in n_mins(
        {x: hamming_len(cbytes[0:x], cbytes[x:2 * x]) / x for x in range(2, round(len(cbytes) / 2))},
        check_keys).keys()]))


def hamming_len(t1: bytearray, t2: bytearray) -> int:
    return sum(bin(a ^ b).count("1") for a, b in zip(t1, t2))


def n_mins(values: dict, n: int) -> dict:
    mins = {}
    for x in values.items():
        mins[x[0]] = x[1]
        if len(mins) > n:
            del mins[dict_max(mins)]
    return mins


def dict_max(values: dict):
    max_key = next(iter(values))
    for key in values.keys():
        if values[key] > values[max_key]:
            max_key = key
    return max_key


def decode(cbytes):
    eng_ranks = gen_english_ranks()
    keys = break_vigenere(cbytes, eng_ranks)
    print(vigenere(cbytes, keys).decode())
    print(keys.decode())


def encode():
    key = "fun.exe".encode('utf8')
    header = "get rid if this text or use the name of the file as the key to read".encode('utf8')
    text = """\nmade a text with some bad bytes at the start
hope it worked to fool your algorithm
I guess it didnt work if your reading this :(
you should see if it fools someone else by sending it to them
if do does you can say your better which is really funny\n""".encode('utf8')
    ctext = header + "\n".encode("utf8") + vigenere(text, key)
    return ctext


def main():
    #cbytes: bytearray = encode()
    #write_ctext_file(cbytes, "fun.exe")
    #decode(cbytes)
    #print(vigenere(cbytes,"fun".encode('utf8')).decode())
    cbytes= read_ctext_file("the.bin")
    decode(cbytes)


main()
