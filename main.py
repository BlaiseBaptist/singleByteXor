from itertools import cycle
from typing import Dict


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


def write_ctext_file(ptext: str, key: bytearray, fname: str) -> None:
    pbytes = bytearray(ptext, 'utf-8')
    cbytes = singleByteXor(pbytes, key)
    with open(fname, 'wb') as f:
        f.write(cbytes)


def read_ctext_file(key: bytearray, fname: str) -> bytearray:
    with open(fname, 'rb') as f:
        cbytes = bytearray(f.read())
        ptext = vigenere(cbytes, key)
        return ptext


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
                for b in test])  # Add up the scores from each individual byte in test


def gen_english_ranks(infile='pg2701.txt') -> bytearray:
    with open('pg2701.txt', 'rb') as f:
        data = f.read()
    return byte_ranks(data)


def break_single_byte(cbytes: bytearray, eng_ranks: bytearray) -> (int, bytearray):
    best_value = 10000000
    best_key = int
    best_out = bytearray
    for x in range(255):
        ptext = singleByteXor(cbytes, x)
        score = english_score(ptext, eng_ranks)
        if score < best_value:
            best_key = x
            best_value = score
            best_out = ptext
    return best_key, best_out


def encrypt():
    text = """Cryptography 2/5:
        - Finish implementing break_single_byte
        - Use your code to encrypt some text (must be long enough, a few sentances)
        - Include the plaintext and ciphertext in your repo
        - Send ciphertext to a classmate, have them try to break it
        - SEND THIS FILE TO 2 MORE PEOPLE"""
    write_ctext_file(text, 3,"scheme.bin")


def main():
    encrypt()
    cbytes = read_ctext_file([0b00000000], 'awesome_pt.bin')
    eng_ranks = gen_english_ranks()
    key, message = break_single_byte(cbytes, eng_ranks)
    print(message.decode('utf-8'), "\n\nkey:", key)


if __name__ == '__main__':
    main()
