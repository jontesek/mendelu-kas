

class Sha1Algo(object):

    INIT_BUFFERS = {
        'h0': '01100111010001010010001100000001',  # 0x67452301
        'h1': '11101111110011011010101110001001',  # 0xEFCDAB89
        'h2': '10011000101110101101110011111110',  # 0x98BADCFE
        'h3': '00010000001100100101010001110110',  # 0x10325476
        'h4': '11000011110100101110000111110000',  # 0xC3D2E1F0
    }

    def __init__(self):
        self.h_values = {
            'h0': '01100111010001010010001100000001',  # 0x67452301
            'h1': '11101111110011011010101110001001',  # 0xEFCDAB89
            'h2': '10011000101110101101110011111110',  # 0x98BADCFE
            'h3': '00010000001100100101010001110110',  # 0x10325476
            'h4': '11000011110100101110000111110000',  # 0xC3D2E1F0
        }

    def hash_text(self, input_text):
        # Convert text to binary string
        ascii_codes = self._convert_text_to_ascii_codes(input_text)
        binary_numbers = self._convert_ascii_to_binary(ascii_codes)
        bin_together = ''.join(binary_numbers)
        # Prepare and chunk message
        chunks = self._pad_and_chunk_message(bin_together)
        # Process all chunks
        for chunk in chunks:
            h_values = self._process_chunk(chunk)

    def _process_chunk(self, chunk):
        # Split chunk into 16 32-bit words (16x32 = 512)
        w_n = 16
        words = [chunk[i:i+w_n] for i in range(0, len(chunk), w_n)]
        # Extend chunk into 80 words...create 4 words from every word.
        print words

    def _pad_and_chunk_message(self, input_msg):
        final_message = self._pad_given_message(input_msg)
        return self._split_msg_into_chunks(final_message)

    def _convert_text_to_ascii_codes(self, input_text):
        return [ord(c) for c in input_text]

    def _convert_ascii_to_binary(self, ascii_codes):
        return [bin(x)[2:].zfill(8) for x in ascii_codes]

    def _pad_given_message(self, original_msg):
        # Add 1 to the end.
        edited_msg = original_msg + '1'
        # Add zeros to the end until the length of the edited message is congruent to 448 mod 512.
        # -> After dividing the length by 512, there will be 448 characters left.
        remainder = len(edited_msg) % 512
        if remainder <= 448:
            n_of_zeros = 448 - remainder
        else:
            n_of_zeros = 1024 - remainder
        edited_msg += '0' * n_of_zeros
        # Append original message length
        bin_len = bin(len(original_msg))[2:].zfill(64)
        edited_msg += bin_len
        return edited_msg

    def _split_msg_into_chunks(self, msg):
        n = 512
        return [msg[i:i+n] for i in range(0, len(msg), n)]




