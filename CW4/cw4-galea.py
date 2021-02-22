tags = dict()
with open('twitter_data.txt', 'r', encoding='utf8') as f:
    lines = f.readlines()
words = []
for line in lines:
    lis = line.split(" ")
    for word in lis:
        words.append(word)

hashtags = []
for word in words:
    if (len(word) > 0):
        if word[0] == "#":
            hashtags.append(word)
for tag in hashtags:
    tag = tag.lower()
    if (tag in tags.keys()):
        tags[tag]+=1
    else:
        tags[tag] = 1
tagCount = []
for key in tags.keys():
    numTags = tags[key]
    tup = (key, numTags)
    ctr = 0
    while(ctr < len(tagCount)):
        if (tagCount[ctr][1] < tup[1]):
            break
        ctr+=1
    if ctr == len(tagCount):
        tagCount.append(tup)
    else:
        tagCount.insert(ctr, tup)

print("The top 5 hashtags are as follows:")
for k in range(5):
    print("\"" + tagCount[k][0] + "\" has " + str(tagCount[k][1]) + " occurrences")