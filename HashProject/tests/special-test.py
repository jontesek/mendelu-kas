# -*- coding: utf-8 -*-
import sys

import hashlib

my_str = unicode('Příliš žluťoučký kůň úpěl ďábelské ódy', 'utf-8')

m = hashlib.sha1()
m.update(my_str.encode('utf-8'))
print m.hexdigest()



