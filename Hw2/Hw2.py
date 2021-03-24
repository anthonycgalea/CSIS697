import matplotlib.pyplot as plt
import random
def partyMonth(parties, presidents, data):
    avs = dict()
    for party in parties:
        ct = 0
        sum = 0
        for president in presidents:
            if president["party"] == party:
                for k in range(int(president["sDate"]),int(president["eDate"])):
                    for year in data:
                        if year[0] == str(k):
                            for l in range(1, 13):
                                sum+=int(year[l])
                                ct+=1
        avs[party] = int(sum/ct)
    for party in avs.keys():
        output.write("{left_aligned:<15}{right_aligned:>12}\n".format(
            left_aligned=party,
            right_aligned=avs[party]
        ))

def presidentialProgress(presidents, data):
    progs = []
    for president in presidents:
        lName = president["name"].split(" ")[-1].strip()
        for year in data:
            if year[0] == president["sDate"]:
                sJob = year[1].strip()
            if year[0] == str(int(president["eDate"])-1):
                eJob = year[-1].strip()
        difference = int(eJob)-int(sJob)
        pct = difference/int(sJob)*100
        progs.append((lName, sJob, eJob, difference, pct))
    output.write("{lAlign:<15}{sJobs:>20}{eJobs:>20}{diff:>20}{pct:>12}\n".format(
        lAlign="President",
        sJobs="First Month",
        eJobs="Last Month",
        diff="Difference",
        pct="Percentage"
    ))
    for pres in progs:
        output.write("{lAlign:<15}{sJobs:>20}{eJobs:>20}{diff:>20}{pct:>12}%\n".format(
        lAlign=pres[0],
        sJobs=pres[1],
        eJobs=pres[2],
        diff=str(pres[3]),
        pct="{pct:.2f}".format(pct=pres[4])
        ))


dataPrivate = []
govData = []
presidents = []
parties = set()

fpriv = open("private.csv")
fgov = open("gov.csv")
fpres = open("presidents.txt")
output = open("output.txt", "w")
fpriv.readline()
fgov.readline()

p = fpres.readlines()
for k in range(len(p)): #create president dicts to store data
    pData = p[k].split(",")
    pres = dict()
    pres["name"] = pData[0].strip()
    pres["sDate"] = pData[1].strip().split("-")[0]
    pres["eDate"] = pData[1].strip().split("-")[1]
    pres["party"] = pData[2].strip()
    parties.add(pres["party"])
    presidents.append(pres)

dataPrivate = [k.split(",") for k in fpriv.readlines()] #remember 0 is the year
govData = [k.split(",") for k in fgov.readlines()] #remember 0 is the year

output.write("Private employment average per month (thousands)\n")
partyMonth(parties, presidents, dataPrivate)

output.write("\nGovernment employment average per month (thousands)\n")
partyMonth(parties, presidents, govData)

output.write("\nPrivate employment average by president (thousands)\n")
presidentialProgress(presidents, dataPrivate)

output.write("\nGovernment employment average by president (thousands)\n")
presidentialProgress(presidents, govData)

output.close()
partyColors = dict()
for party in parties: #Do not have set colors in case of different parties, makes code work for more data
    r = random.random()
    b = random.random()
    g = random.random()
    color = (r, g, b)
    partyColors[party] = color
plt.ylabel("Total employment(millions)")
plt.xlabel("Year (AD)")
plt.title("Total Employment across all entities over years by party")
partiesindata = set()
for president in presidents:
    presData = []
    presYears = [int(president["sDate"])]
    counter = 0
    for k in range(int(president["sDate"]),int(president["eDate"])):
        for line in dataPrivate:
            if str(k) in line:
                for l in range(1, len(line)):
                    presData.append(int(line[l]))
                    presYears.append(presYears[-1]+(1/12))
        for line in govData:
            if str(k) in line:
                for l in range(1, len(line)):
                    presData[counter]+=int(line[l])
                    counter+=1  
    for k in range(len(presData)):
        presData[k]/=1000         
    lbl = ""
    pcolor = partyColors[president["party"]]
    if not president["party"] in partiesindata:
        lbl=president["party"]
        partiesindata.add(president["party"])
    plt.plot(presYears[:-1], presData, color=pcolor, label=lbl)
    plt.legend(loc="upper left")
plt.show()