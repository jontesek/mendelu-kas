
word1 = '0100000100100000'
word2 = '0101010001100101'

for i in range(0, len(word1)-1):
    print int(word1[i]) ^ int(word2[i])