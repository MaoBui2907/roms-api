with open('./test.txt', 'r') as f:
    links = f.read().split('\n')
categories = []
allowed_regex = []
for i in range(len(links)):
    categories.append(links[i].rsplit('/', 1)[-1])    
    allowed_regex.append("^" + links[i])
# print(categories)
print(len(allowed_regex))
print("done")