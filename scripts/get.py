#!/usr/bin/python

"""
Comment getter.

Just dump one line on stdout.
"""

import sqlite3
from random import random


def get_random_line():
    conn = sqlite3.connect("clever_lines.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM lines
        """)
    count = cur.fetchone()[0]
    offset = int(random() * count)

    cur.execute("""
        SELECT line
        FROM lines
        LIMIT 1
        OFFSET %d
        """ % offset)
    line = cur.fetchone()[0]

    cur.close()
    conn.close()

    return line

if __name__ == '__main__':
    print(get_random_line())
