import operator


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
        # Prepare variables
        letter_variables = {
            'A': self.h_values['h0'],
            'B': self.h_values['h1'],
            'C': self.h_values['h2'],
            'D': self.h_values['h3'],
            'E': self.h_values['h4']
        }
        # Process all words
        new_words = []
        for i, word in enumerate(words):
            if 0 <= i <= 19:
                (F, K) = self._process_letters_1(letter_variables)
            elif 20 <= i <= 39:
                (F, K) = self._process_letters_2(letter_variables)
            elif 40 <= i <= 59:
                (F, K) = self._process_word_3(letter_variables)
            else:
                (F, K) = self._process_word_4(letter_variables)
            new_words.append(word)
        exit()



    def _do_XOR_for_words(self, i, words):
        # first doing [i-3]XOR[i-8]
        new_word = self._apply_binary_operator('XOR', words[i-3], words[i-8])
        # then XOR'ing that by [i-14]
        new_word = self._apply_binary_operator('XOR', new_word, words[i-14])
        # and that again by [i-16]
        new_word = self._apply_binary_operator('XOR', new_word, words[i-16])
        # result
        return new_word

    def _apply_binary_operator(self, str_op, word1, word2):
        new_word = []
        # Choose the right operator.
        if str_op == 'XOR':
            apply_op = operator.xor
        elif str_op == 'AND':
            apply_op = operator.and_
        elif str_op == 'OR':
            apply_op = operator.or_
        # Apply operator on the two words.
        for i in range(0, len(word1)):
            new_word.append(apply_op(int(word1[i]), int(word2[i])))
        # result
        return new_word

    def _negate_word(self, word):
        new_word = []
        # Apply operator on the word.
        for i in range(0, len(word)):
            new_str = 1 if int(word[i]) == 0 else 0
            new_word.append(new_str)
        # result
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

    def _process_letters_1(self, letters):
        """
        1. set the variable 'f' equal to: (B AND C) or (!B AND D)
        2. set the variable 'k' equal to: 01011010100000100111100110011001
        """
        # 1. B and C
        b_and_c = self._apply_binary_operator('AND', letters['B'], letters['C'])
        # 2. (!B and D)
        not_b_and_d = self._apply_binary_operator('AND', self._negate_word(letters['B']), letters['D'])
        # 1 or 2
        F = self._apply_binary_operator('OR', b_and_c, not_b_and_d)
        K = '01011010100000100111100110011001'
        # result
        print(''.join([str(x) for x in F]))
        return (F, K)

    def _process_letters_2(self, letters):
        """
        1. set the variable 'f' equal to: B XOR C XOR D
        2. set the variable 'k' equal to: 01101110110110011110101110100001
        """
        # 1. B xor C
        b_xor_c = self._apply_binary_operator('XOR', letters['B'], letters['C'])
        #print(self._list_to_string(letters['B']))
        #print(self._list_to_string(letters['C']))
        #print(''.join([str(x) for x in b_xor_c]))
        #exit()
        # 1 xor D
        F = self._apply_binary_operator('AND', b_xor_c, letters['D'])
        K = '01011010100000100111100110011001'
        # result
        exit(''.join([str(x) for x in F]))
        return (F, K)


    def _list_to_string(self, my_list):
        return ''.join([str(x) for x in my_list])