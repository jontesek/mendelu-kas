import operator
import os.path

class Sha1Algo(object):

    def __init__(self):
        self.h_values = [
            '01100111010001010010001100000001',  # 0x67452301
            '11101111110011011010101110001001',  # 0xEFCDAB89
            '10011000101110101101110011111110',  # 0x98BADCFE
            '00010000001100100101010001110110',  # 0x10325476
            '11000011110100101110000111110000',  # 0xC3D2E1F0
        ]

    def hash_text(self, input_text):
        # Convert text to binary string
        ascii_codes = self._convert_text_to_ascii_codes(input_text)
        binary_numbers = self._convert_ascii_to_binary(ascii_codes)
        bin_together = ''.join(binary_numbers)
        # hash string
        print('<<<HASH VALUE>>>')
        print self._hash_bit_string(bin_together)

    def hash_file(self, file_path):
        # Read file
        file_obj = open(os.path.abspath(file_path), 'rb')
        bin_string = ''
        file_bytes = (ord(b) for b in file_obj.read())
        for byte in file_bytes:
            bin_string += bin(byte)[2:].zfill(8)
        # hash string
        print('<<<HASH VALUE>>>')
        print self._hash_bit_string(bin_string)

    def _hash_bit_string(self, bin_string):
        # Prepare and chunk message
        chunks = self._pad_and_chunk_message(bin_string)
        h_values = self.h_values
        #print('Number of chunks: %d') % len(chunks)
        # Process all chunks
        for i, chunk in enumerate(chunks):
            print('======CHUNK %d======') % i
            if i == 0:
                h_values = self._process_chunk(chunk, h_values)
            else:
                h_values = self._process_chunk(chunk, self._bin_to_string_list(h_values))
        # Convert last h values to hexadecimal numbers.
        hex_values = [hex(x)[2:-1].zfill(8) for x in h_values]
        # Join the numbers together
        final_hash = ''.join(hex_values)
        # result
        return final_hash

    def _process_chunk(self, chunk, h_values):
        # Split chunk into 16 32-bit words (16x32 = 512)
        w_size = 32
        words = [chunk[i:i+w_size] for i in range(0, len(chunk), w_size)]
        # Extend chunk into 80 words...create 4 words from every word.
        for i in range(16, 80):
            #print '===%d===' % i
            # 1. XOR selected words
            new_word = self._do_xor_for_words(i, words)
            # 2. Left rotate 1
            new_word = self._left_rotate_word(new_word, 1)
            # Save word to the list.
            words.append(new_word)
        # Initialize variables
        letters = {
            'A': h_values[0],
            'B': h_values[1],
            'C': h_values[2],
            'D': h_values[3],
            'E': h_values[4]
        }
        # Process all words
        new_words = []
        for i, word in enumerate(words):
            #print '===word %d===' % i
            #print letters
            if len(word) != 32:
                exit(word)
            if 0 <= i <= 19:
                (F, K) = self._process_letters_1(letters)
                letters = self._update_letters(word, letters, F, K)
            elif 20 <= i <= 39:
                (F, K) = self._process_letters_2(letters)
                letters = self._update_letters(word, letters, F, K)
            elif 40 <= i <= 59:
                (F, K) = self._process_letters_3(letters)
                letters = self._update_letters(word, letters, F, K)
            else:
                (F, K) = self._process_letters_2(letters)
                K = '11001010011000101100000111010110'
                letters = self._update_letters(word, letters, F, K)
            new_words.append(word)
        # calculate new h values (truncate longer than 32 bits)
        updated_h_values = [
            self._sum_bit_numbers([int(h_values[0], 2), int(letters['A'], 2)]) & 0xFFFFFFFF,
            self._sum_bit_numbers([int(h_values[1], 2), int(letters['B'], 2)]) & 0xFFFFFFFF,
            self._sum_bit_numbers([int(h_values[2], 2), int(letters['C'], 2)]) & 0xFFFFFFFF,
            self._sum_bit_numbers([int(h_values[3], 2), int(letters['D'], 2)]) & 0xFFFFFFFF,
            self._sum_bit_numbers([int(h_values[4], 2), int(letters['E'], 2)]) & 0xFFFFFFFF
        ]
        return updated_h_values

    def _do_xor_for_words(self, i, words):
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
        # Apply operator on every character of the two words.
        for i in range(0, len(word1)):
            new_word.append(apply_op(int(word1[i]), int(word2[i])))
        # result
        return self._list_to_string(new_word)

    def _negate_word(self, word):
        new_word = []
        # Apply operator on the word.
        for i in range(0, len(word)):
            new_str = 1 if int(word[i]) == 0 else 0
            new_word.append(new_str)
        # result
        return self._list_to_string(new_word)

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
        return (F, K)

    def _process_letters_2(self, letters):
        """
        1. set the variable 'f' equal to: B XOR C XOR D
        2. set the variable 'k' equal to: 01101110110110011110101110100001
        """
        # 1. B xor C
        b_xor_c = self._apply_binary_operator('XOR', letters['B'], letters['C'])
        # 1 xor D
        F = self._apply_binary_operator('XOR', b_xor_c, letters['D'])
        K = '01101110110110011110101110100001'
        # result
        return (F, K)

    def _process_letters_3(self, letters):
        """
        1. set the variable 'f' equal to: (B AND C) OR (B AND D) OR (C AND D)
        2. set the variable 'k' equal to: 10001111000110111011110011011100
        """
        # 1. B and C
        b_and_c = self._apply_binary_operator('AND', letters['B'], letters['C'])
        # 2. 1 or (B and D)
        b_and_d = self._apply_binary_operator('AND', letters['B'], letters['D'])
        exp_2 = self._apply_binary_operator('OR', b_and_c, b_and_d)
        # 3. 2 or (C and D)
        c_and_d = self._apply_binary_operator('AND', letters['C'], letters['D'])
        F = self._apply_binary_operator('OR', exp_2, c_and_d)
        K = '10001111000110111011110011011100'
        # result
        return (F, K)

    def _update_letters(self, word, letters, F, K):
        # temp = (A left rotate 5) + F + E + K + (the current word)
        a_left_5 = self._left_rotate_word(letters['A'], 5)
        temp = self._sum_bit_numbers([int(a_left_5, 2), int(F, 2), int(letters['E'], 2), int(K, 2), int(word, 2)])
        # truncate temp
        temp &= 0xFFFFFFFF
        # add leading zeroes
        temp_str = bin(temp)[2:].zfill(32)
        # update letters
        new_letters = {
            'E': letters['D'],
            'D': letters['C'],
            'C': self._left_rotate_word(letters['B'], 30),
            'B': letters['A'],
            'A': temp_str
        }
        return new_letters

    def _left_rotate_word(self, word, n):
        removed_left_items = word[0:n]
        word = word[n:]
        word += removed_left_items
        return word

    def _sum_bit_numbers(self, bin_list):
        total_sum = 0
        for i in range(0, len(bin_list)-1):
            #print bin(bin_list[i])
            if i == 0:
                total_sum = bin_list[i] + bin_list[i+1]
            else:
                total_sum += bin_list[i+1]
            #print(bin(total_sum))
        # result
        return total_sum

    def _bin_to_string_list(self, bin_list):
        new_vals = [bin(x)[2:].zfill(32) for x in bin_list]
        return new_vals

    def _list_to_string(self, my_list):
        return ''.join([str(x) for x in my_list])

    # http://stackoverflow.com/questions/2576712/using-python-how-can-i-read-the-bits-in-a-byte
    def _read_bits_from_file(self, f):
        bytes = (ord(b) for b in f.read())
        for b in bytes:
            for i in xrange(8):
                yield (b >> i) & 1

