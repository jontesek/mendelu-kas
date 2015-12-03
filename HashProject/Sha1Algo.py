

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
        w_size = 32
        words = [chunk[i:i+w_size] for i in range(0, len(chunk), w_size)]
        # Extend chunk into 80 words...create 4 words from every word.
        for i in range(16, 80):
            #print '===%d===' % i
            # 1. XOR selected words
            new_word = self._do_XOR_for_words(i, words)
            # 2. Left rotate 1
            removed_left_item = new_word[0]
            new_word = new_word[1:]
            new_word.append(removed_left_item)
            # Save word to the list.
            words.append(''.join([str(x) for x in new_word]))
        # show
        print words
        exit()


    def _do_XOR_for_words(self, i, words):
        # first doing [i-3]XOR[i-8]
        new_word = self._XOR_two_words(words[i-3], words[i-8])
        # then XOR'ing that by [i-14]
        new_word = self._XOR_two_words(new_word, words[i-14])
        # and that again by [i-16]
        new_word = self._XOR_two_words(new_word, words[i-16])
        # result
        return new_word

    def _XOR_two_words(self, word1, word2):
        new_word = []
        for i in range(0, len(word1)):
            new_word.append(int(word1[i]) ^ int(word2[i]))
        return new_word


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




