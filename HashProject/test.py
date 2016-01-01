# -*- coding: utf-8 -*-
from src.Sha1Algo import Sha1Algo

sa = Sha1Algo()
# Short text: 8f0c0855915633e4a7de19468b3874c8901df043
#sa.hash_text('A Test')
sa.hash_text('Příliš žluťoučký kůň úpěl ďábelské ódy')  # 8f8d965195fdaf4375fd5ad58e0a1f91329ad30f

# Long text: 100 bytes: c6d7501f54c1099833b6b19558b48dc2fc84c14c
# sa.hash_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel massa sem. Nullam commodo nullam')

# Small file: 302 bytes: 0293b9ad9d2468e758ea72e2aef39cd3c74cdfc2
# sa.hash_file('tests/h_file.txt')
# Medium file: 57 kB...57 679 bytes: 8304d2221bdb3f3498eccad4436a2c98a3be5c25
# sa.hash_file("tests/h_file.pdf")
# -> aaah it's too slow (15 secs)
