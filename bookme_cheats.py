from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
import datetime
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from tkinter import *
from functools import partial
import re

ROOMS = {"LIB07": "1371", "LIB06": "1370"}


def inputs():
    def validate_login(username, password, tkwindow):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, username.get()):
            tkwindow.quit()
        else:
            print("Invalid Email")
        return

    tkWindow = Tk()
    tkWindow.title('SPY PROGRAM')
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)
    passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)
    validateLogin = partial(validate_login, username, password, tkWindow)
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)
    tkWindow.mainloop()
    return username.get(), password.get()


def create_order(driver, room, date, start_hour, finish_hour):
    endurl = f"https://bookme.technion.ac.il/booked/Web/reservation.php?rid={room}"
    driver.get(endurl)
    driver.find_element_by_id("reservationTitle").send_keys("Some Bullshit Title")
    delete = [Keys.BACK_SPACE] * 11
    enter_startdate = driver.find_element_by_id("BeginDate")
    enter_startdate.send_keys(*delete, date)
    enter_enddate = driver.find_element_by_id("EndDate")
    enter_enddate.send_keys(*delete, date)
    driver.find_element_by_xpath(f"//select[@name='beginPeriod']/option[text()='{start_hour}']").click()
    driver.find_element_by_xpath(f"//select[@name='endPeriod']/option[text()='{finish_hour}']").click()
    driver.find_element_by_xpath(r"/html/body/div[1]/div/div[1]/form/div[1]/div[2]/div[1]/button[2]").click()


def run_action(username, pw):
    prefered_Date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d/%m/%Y")
    pref_hour = int(datetime.datetime.now().strftime("%H"))
    if pref_hour == 10:
        pref_shour = f"0{pref_hour - 1}:30"
        pref_fhour = f"{pref_hour}:30"
    else:
        pref_shour = f"{pref_hour - 1}:30"
        pref_fhour = f"{pref_hour}:30"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    url = "https://bookme.technion.ac.il/booked/Web/dashboard.php"
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_id("i0116").send_keys(username)
    driver.find_element_by_id("idSIButton9").click()
    sleep(2)
    driver.find_element_by_id("i0118").send_keys(pw)
    sleep(2)
    driver.find_element_by_id("idSIButton9").click()
    sleep(2)
    driver.find_element_by_id("idSIButton9").click()
    sleep(2)
    create_order(driver, ROOMS["LIB07"], prefered_Date, pref_shour, pref_fhour)
    driver.quit()


if __name__ == '__main__':
    user, pw = inputs()
    run_action(user, pw)
