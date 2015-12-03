import sys

word1 = '0100000100100000'
word2 = '0101010001100101'
new_word = list('1001010')
#print new_word

removed_left_item = new_word[0]
new_word = new_word[1:]
new_word.append(removed_left_item)
#print new_word

word = 0b111100
bin_word = bin(word)[2:].zfill(8)
print sys.getsizeof(word)

