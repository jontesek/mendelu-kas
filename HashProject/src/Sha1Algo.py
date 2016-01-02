import struct
import os.path


class Sha1Algo(object):

    def __init__(self):
        # Initial H variables
        self.h_values = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

    def hash_text(self, input_text):
        """Public method for hashing given text."""
        # Convert text to bytes (utf8).
        utf8_codes = self._convert_text_to_utf8_codes(input_text)
        text_bytes = bytearray(utf8_codes)
        # Hash the bytes.
        return self._hash_bytes(text_bytes)

    def hash_file(self, file_path):
        """Public method for hashing given file."""
        try:
            # Read file to array of bytes.
            file_obj = open(os.path.abspath(file_path), 'rb')
            file_bytes = bytearray(file_obj.read())
            file_obj.close()
            # Hash the bytes.
            return self._hash_bytes(file_bytes)
        except IOError:
            print('The file ' + file_path + ' was not found.')

    def _hash_bytes(self, byte_array):
        """Main private method for hashing (both strings and files)."""
        # Prepare and chunk message.
        prepared_msg = self._prepare_msg(byte_array)
        chunks = self._chunk_msg(prepared_msg)
        h_values = self.h_values
        # Process all chunks
        for i, chunk in enumerate(chunks):
            #print('======CHUNK %d======') % i
            h_values = self._process_chunk(chunk, h_values)
        # Produce digest from final h values.
        final_hash = self._produce_hex_digest(h_values)
        # result
        print('>>>DIGEST<<<\n' + final_hash)
        return final_hash

    def _prepare_msg(self, msg):
        """Prepares message (bytes) before dividing into chunks."""
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
        """Process a chunk of data and return new H values."""
        # Split chunk into 16 32-bit words ... 16 x 4 bytes integers
        words = [0] * 80
        for i in range(16):
            words[i] = struct.unpack(b'>I', chunk[i*4:i*4 + 4])[0]
        # Extend 16 words into 80 words.
        for i in range(16, 80):
            words[i] = self._left_rotate(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1)
        # Initialize variables
        a = h_values[0]
        b = h_values[1]
        c = h_values[2]
        d = h_values[3]
        e = h_values[4]
        # Process all words
        for i, word in enumerate(words):
            if 0 <= i <= 19:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            # Update letters
            a, b, c, d, e = ((self._left_rotate(a, 5) + f + e + k + word) & 0xffffffff, a, self._left_rotate(b, 30), c, d)

        # Calculate new H values (truncate the ones longer than 32 bits)
        updated_h_values = [
            (h_values[0] + a) & 0xffffffff,
            (h_values[1] + b) & 0xffffffff,
            (h_values[2] + c) & 0xffffffff,
            (h_values[3] + d) & 0xffffffff,
            (h_values[4] + e) & 0xffffffff,
        ]

        return updated_h_values


    def _left_rotate(self, n, b):
        """Left rotate a 32-bit integer n by b bits."""
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    def _produce_hex_digest(self, h_values):
        """Produce the final digest (hash value) as a string from HEX numbers."""
        hex_values = [hex(x)[2:-1].zfill(8) for x in h_values]
        return ''.join(hex_values)

    def _convert_text_to_utf8_codes(self, input_text):
        """Convert given text to a list of utf8 codes of its characters."""
        utf8_input = unicode(input_text, 'utf-8').encode('utf-8')
        return [ord(c) for c in utf8_input]

    def _bytes_to_bin_string(self, byte_array):
        """Helper method for debugging."""
        new_vals = [bin(x)[2:].zfill(8) for x in byte_array]
        return ''.join([str(x) for x in new_vals])
