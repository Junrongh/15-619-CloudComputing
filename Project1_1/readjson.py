import json

with open('namespace.json','r') as load_f:
    load_dic = json.load(load_f)

data = load_dic['query']['namespaces']
blocklist = []

for i in data:
    if i != '0':
        if '*' not in data[i]:
            s = data[i]['canonical']
        else:
            s = data[i]['*'].replace(' ', '_')
        blocklist.append(s.lower()+':')

if __name__ == '__main__':
    for i in blocklist:
        print (i)
