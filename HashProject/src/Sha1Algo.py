import os.path
import struct
import io
import pprint
import operator


class Sha1Algo(object):

    def __init__(self):
        # Initial h variables
        self.h_values = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

    def hash_text(self, input_text):
        # Convert text to bytes (utf8).
        utf8_codes = self._convert_text_to_utf8_codes(input_text)
        text_bytes = bytearray(utf8_codes)
        # Hash the bytes.
        return self._hash_bytes(text_bytes)

    def _convert_text_to_utf8_codes(self, input_text):
        utf8_input = unicode(input_text, 'utf-8').encode('utf-8')
        return [ord(c) for c in utf8_input]

    def _hash_bytes(self, byte_array):
        # Prepare and chunk message.
        prepared_msg = self._prepare_msg(byte_array)
        chunks = self._chunk_msg(prepared_msg)
        h_values = self.h_values
        # Process all chunks
        for i, chunk in enumerate(chunks):
            print('======CHUNK %d======') % i
            h_values = self._process_chunk(chunk, h_values)
        quit()
        # Convert last h values to hexadecimal numbers.
        hex_values = [hex(x)[2:-1].zfill(8) for x in h_values]
        # Join the numbers together
        final_hash = ''.join(hex_values)
        # result
        print('>>>DIGEST<<<\n' + final_hash)
        return final_hash

    def _prepare_msg(self, msg):
        """Prepares message (bytes) for dividing into chunks."""
        # Save original message length (in bytes).
        msg_byte_length = len(msg)
        # Append bit 1 to the end.
        msg.append(0b10000000)
        # Append zeros until len(stream) mod 512 = 448 (in bits).
        # But stream is in bytes (1B = 8b): len(stream) mod 64 = 56
        remainder = len(msg) % 64
        if remainder <= 56:
            add_zero_bytes = 56 - remainder
        else:
            add_zero_bytes = 128 - remainder
        msg += struct.pack(b'>b', 0) * add_zero_bytes
        # Append original stream length as 64 bit (8 B) value.
        msg += struct.pack(b'>q', msg_byte_length * 8)
        # result
        return msg

    def _chunk_msg(self, msg):
        """Split message (bytes) into chunks of size 512 b (64 B)."""
        size = 64
        chunks = []
        for i in range(0, len(msg), size):
            chunks.append(msg[i:i+size])
        return chunks
        # Above can be also written as: [msg[i:i+size] for i in range(0, len(msg), size)]

    def _process_chunk(self, chunk, h_values):
        # Split chunk into 16 32-bit words ... 16 x 4 bytes integers
        size = 4
        w = [0] * 80
        # I will just use 4 bytes as an integer.
        for i in range(16):
            w[i] = struct.unpack(b'>I', chunk[i*4:i*4 + 4])[0]
        # Extend 16 words into 80 words.
        for i in range(16, 80):
            w[i] = self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)



    def _bytes_to_bin_string(self, byte_array):
        new_vals = [bin(x)[2:].zfill(8) for x in byte_array]
        return ''.join([str(x) for x in new_vals])

    def _left_rotate(self, n, b):
        """Left rotate a 32-bit integer n by b bits."""
        return ((n << b) | (n >> (32 - b))) & 0xffffffff
