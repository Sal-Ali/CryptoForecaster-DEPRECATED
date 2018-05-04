#Driver to run the code
#
#Keep in mind, RPY is pretty annoying to copy on your machine as many things like environment variable and package versions etc will differ
#If you are on a MAC, R 3.3 and the Pyhton 3.6 with PIP *SHOULD* suffice
#
#The powerpoint provided should allow for enough insight
#
from coin import coin

count = 0
overcount = 0
#create coins
btc = coin('bitcoin')
eth = coin('ethereum')
tron = coin('tron')
rip = coin('ripple')
iota = coin('iota')
#populate dataset and add metrics when necessary
cryptos_array = [btc, eth, tron, rip, iota]
while overcount < 100:

    for x in cryptos_array:
        x.basicInfo()
        count = count + 1
        #extra debugging
        print(x.count)
        if count % 500 == 0:
            for z in cryptos_array:
                z.advanceOptiuon()

# ensure program is actually alive
    overcount = overcount + 1
    print(count)
#
#Tallies the results after 6h
#
if count == 3000:
    for n in cryptos_array:
        print(n.tally())
