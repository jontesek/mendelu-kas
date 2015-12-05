import sys

word1 = '0100000100100000'
word2 = '0101010001100101'
new_word = list('00010101111')
#print new_word

# rotate left 3
n = 3
removed_left_items = new_word[0:n]
new_word = new_word[n:]
new_word += removed_left_items
#print new_word

word = 0b111100
print word[4]
bin_word = bin(word)[2:].zfill(8)


