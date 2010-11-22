import re

def format_number(n, thousands=",", decimal="."):
    parts = str(n).split(".")
    parts[0] = re.sub(
        R"(\d)(?=(\d\d\d)+(?!\d))", 
        R"\1%s" % thousands, 
        parts[0])
    return decimal.join(parts)
