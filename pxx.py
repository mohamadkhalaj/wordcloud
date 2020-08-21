lists = open("prox.txt", 'r')

pox = list()

for row in lists:
    row = row.strip('\n')
    pox.append('https://'+row)

