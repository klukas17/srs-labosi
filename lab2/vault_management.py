def init():
    f = open('vault.txt', 'w')
    f.close()

def read_vault():
    try:
        f = open('vault.txt', 'r')
    except FileNotFoundError:
        init()
        f = open('vault.txt', 'r')

    d = f.read()
    vault = {}

    records = d.split('\n')
    
    for record in records:
        s = record.split(" ")
        if len(s) == 1:
            continue
        vault[s[0]] = (s[1], s[2], s[3])

    return vault

def write_vault(vault):
    f = open('vault.txt', 'w')

    for key in vault:
        f.write(f'{key} {vault[key][0]} {vault[key][1]} {vault[key][2]}\n')

    f.close()