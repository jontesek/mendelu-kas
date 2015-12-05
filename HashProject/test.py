from Sha1Algo import Sha1Algo

sa = Sha1Algo()
# Short text: 8f0c0855915633e4a7de19468b3874c8901df043
#sa.hash_text('A Test')

# Long text: 100 bytes: c6d7501f54c1099833b6b19558b48dc2fc84c14c
sa.hash_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel massa sem. Nullam commodo nullam')

# A file: 5 kB:

#n1 = sa._left_rotate_word('01100111010001010010001100000001',5)
n1 = int('11101000101001000110000000101100',2)
n2 = int('10011000101110101101110011111110',2)
n3 = int('11000011110100101110000111110000',2)
#out = sa._sum_bit_numbers([n1, n2, n3])

