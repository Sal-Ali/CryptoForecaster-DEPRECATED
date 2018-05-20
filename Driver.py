#Driver to run the code
#
#Keep in mind, RPY is pretty annoying to copy on your machine as many things like environment variable and package versions etc will differ
#If you are on a MAC, R 3.3 and Python 3.6 with PIP *SHOULD* suffice
#You will also need to install every package I have imported and the TTR package in R
#
#The powerpoint provided should allow for enough insight
#
from coin import coin

import time
import gspread
from contextlib import suppress

last_time = time.time()
def run():
    try:
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



        while overcount < 10000:

            for x in cryptos_array:
                x.main()
                count = count + 1
                if count % 500 == 0:
                    for z in cryptos_array:
                        z.advanceOptiuon()

        # ensure program is actually alive
            overcount = overcount + 1
        #    print(overcount)
            #client login issue

            # if overcount % 100 == 0:
            #     for n in cryptos_array:
            #         print(n.tally())
    except (gspread.exceptions.AuthenticationError, gspread.GSpreadException,
            gspread.exceptions.GSpreadException, gspread.RequestError,
            gspread.exceptions.RequestError):
        pass
    finally:
        fail_time = time.time() - last_time
        print("it took this many seconds to fail: " + str(fail_time))
        run()


    # print(overcount)
    # print(count)

#Tallies the results after 6h

# for n in cryptos_array:
#     print(n.tally())
#
run()
# btc.advanceOptiuon()






