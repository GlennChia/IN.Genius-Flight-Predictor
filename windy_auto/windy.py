from time import sleep
import datetime
from selenium import webdriver
import pandas as pd
import re

driver = webdriver.Chrome("chromedriver.exe")

# If the page does not respond within the timelimit, it will throw an error
driver.set_page_load_timeout(30)

# Define a list of altitudes
alt_ls = ["", "100m,", "950h,", "925h,", "900h,", "850h,", "800h,", "700h,", "600h,", "500h,", "400h,", "300h,", "250h,", "200h,", "150h,"]
alt_ls2 = ["Surface", "100m", "600m", "750m", "900m", "1500m", "2000m", "3000m", "4200m", "5500m", "7000m", "9000m", "10km", "11.7km", "13.5km"]

# Store the current date because Windy does not have a date requirement if it is today and within a certain range
now = datetime.datetime.now()
stored_date = str(now.year) + "-" +  str(now.day) + "-" + str(now.month)
print("Today's date is " + stored_date)
current_hour = str(now.time().hour)
print("Current hour is " + current_hour)
ls_forbid = [stored_date + current_hour]

# Set a wait time for every element (In seconds)
driver.implicitly_wait(20)


# Pre-condition: Desired date and time (Singapore time)
# Post-condition: Direction and speed
def get_wind(date, set_time):
    # Sample Answer: "W 60kt
    # Sample Answer: "SE 8kt
    ans_ls = []
    for i in range(len(alt_ls)):
        sub_ls = []
        print("Finding the value number " + str(i) + " which is at altitude " + alt_ls2[i])
        driver.get("https://www.windy.com/-23.928/133.906?" + alt_ls[i] + date + "-" + set_time + ",-24.649,133.648,8,m:cZiajSl")
        sleep(3)
        print("Searching")
        c = driver.find_element_by_xpath("//*[@id='map-container']/div[1]/div[4]/div[4]/div[3]/span/big")
        print("Found " + c.text)
        print("Extracting values")
        direction = re.findall('([A-Z]+)', c.text)  # returns ['SE']
        print("The Wind Direction is " + direction[0])  # returns SE
        sub_ls.append(direction[0])
        num = re.findall(('[0-9]+'), c.text)
        print("The Speed of the wind in knots is " + num[0])
        sub_ls.append(num[0])
        sleep(2)
        ans_ls.append(sub_ls)
    driver.quit()
    return ans_ls


# Pre-condition: Singapore Date and Time
# Post-condition: Windy Date and Time as an array
def convert_windy_date(date_i, time_i):
    if 7 <= int(time_i) <= 9:
        current_time = 0
        current_time_str = "00"
    elif 10 <= int(time_i) <= 12:
        current_time = 3
        current_time_str = "03"
    elif 13 <= int(time_i) <= 15:
        current_time = 6
        current_time_str = "06"
    elif 16 <= int(time_i) <= 18:
        current_time = 9
        current_time_str = "09"
    elif 19 <= int(time_i) <= 21:
        current_time = 12
        current_time_str = "12"
    elif 22 <= int(time_i) or  int(time_i) <= 0:
        current_time = 15
        current_time_str = "15"
    # TODO: Will be the previous date
    elif 1 <= int(time_i) <= 3:
        current_time = 18
        current_time_str = "18"

        # TODO: Adjust the date
        # Sample Date: "2019-12-05"
        #               0123456789
        # Case where it is a 1-9 or 11-19 or 21-29 or 31
        if 0 < int(date_i[5:7]) < 10 or 10 < int(date_i[5:7]) < 20 or 20 < int(date_i[5:7]) < 30 :
            date_i = date_i[:6] + str(int(date_i[6])-1) + date_i[7:]
        # Case where it is 10 or 20 or 30
        elif int(date_i[5:7]) % 10 == 0:
            date_i = date_i[:5] + str(int(date_i[6])-1) + "9" + date_i[7:]
        # Case where it is 0
        # TODO: Consider the change in year
        else:
            # Case where there are 31 days in the previous month. Months after those 31 are 02, 04, 06, 08, 09, 11, 01
            if(date_i[8:] == "02" or date_i[8:] == "04" or date_i[8:] == "06" or date_i[8:] == "08" or
                       date_i[8:] == "09" or date_i[8:] == "11"):
                date_i = date_i[:5] + "31" + date_i[7:9] + str(int(date_i[9])-1)
            # Case where we change the year
            elif date_i[8:] == "01":
                date_i = date_i[:3] + "20-31-12" # FOR NOW WE HARD CODE IT TO 2020
            # Case where there are 30 days in the previous month. Months after those 30 are 05, 07, 10, 12
            elif(date_i[8:] == "05" or date_i[8:] == "07" or date_i[8:] == "10" or date_i[8:] == "12"):
                if date_i[8:] == "10":
                    date_i = date_i[:5] + "30-09"
                else:
                    date_i = date_i[:5] + "30" + date_i[7:9] + str(int(date_i[9]) - 1)
            # Case where there are 28 days in the previous month. Months after is 03
            elif date_i[8:] == "03":
                date_i = date_i[:5] + "28-02" # FOR NOW WE HARD CODE IT TO 2020
    elif 4 <= int(time_i) <= 6:
        current_time = 21
        current_time_str = "21"
        # TODO: Adjust the date
        # Sample Date: "2019-12-05"
        #               0123456789
        # Case where it is a 1-9 or 11-19 or 21-29 or 31
        if 0 < int(date_i[5:7]) < 10 or 10 < int(date_i[5:7]) < 20 or 20 < int(date_i[5:7]) < 30:
            date_i = date_i[:6] + str(int(date_i[6]) - 1) + date_i[7:]
        # Case where it is 10 or 20 or 30
        elif int(date_i[5:7]) % 10 == 0:
            date_i = date_i[:5] + str(int(date_i[6]) - 1) + "9" + date_i[7:]
        # Case where it is 0
        # TODO: Consider the change in year
        else:
            # Case where there are 31 days in the previous month. Months after those 31 are 02, 04, 06, 08, 09, 11, 01
            if (date_i[8:] == "02" or date_i[8:] == "04" or date_i[8:] == "06" or date_i[8:] == "08" or
                        date_i[8:] == "09" or date_i[8:] == "11"):
                date_i = date_i[:5] + "31" + date_i[7:9] + str(int(date_i[9]) - 1)
            # Case where we change the year
            elif date_i[8:] == "01":
                date_i = date_i[:3] + "20-31-12"  # FOR NOW WE HARD CODE IT TO 2020
            # Case where there are 30 days in the previous month. Months after those 30 are 05, 07, 10, 12
            elif (date_i[8:] == "05" or date_i[8:] == "07" or date_i[8:] == "10" or date_i[8:] == "12"):
                if date_i[8:] == "10":
                    date_i = date_i[:5] + "30-09"
                else:
                    date_i = date_i[:5] + "30" + date_i[7:9] + str(int(date_i[9]) - 1)
            # Case where there are 28 days in the previous month. Months after is 03
            elif date_i[8:] == "03":
                date_i = date_i[:5] + "28-02"  # FOR NOW WE HARD CODE IT TO 2020
    return [date_i,current_time_str]


# TODO: Call the functions and get the results
# Put the desired date and time in terms of SG timing
# Change these
local_date = "2019-16-05"
local_time = "06"
converted_date_time = convert_windy_date(local_date, local_time)
print("After conversion we get " + str(converted_date_time))

print(get_wind(converted_date_time[0], converted_date_time[1]))


