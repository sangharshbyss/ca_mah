"""
1. re-birth from online_FIRs
2. major changes are - a. logging
b. iterating over year by creating outer loop.

"""

import traceback
import os
import time
from sys import argv

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

import ws_module_v1
from ws_module_proxy_v1 import list_of_proxies

# calculate the time spent
start = time.time()
# constants
# define download directory
base_directory = r'/home/sangharsh/Documents/PoA/data/FIR/feb_24'
download_directory = os.path.join(base_directory, "copies", f'{argv[1]} _ {argv[2]}')

if not download_directory:
    os.mkdir(download_directory)

main_url = r'https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx'

# list of districts
ALL_Districts = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI CITY', 'AMRAVATI RURAL', 'BEED', 'BHANDARA', 'BULDHANA',
                 'CHANDRAPUR', 'CHHATRAPATI SAMBHAJINAGAR CITY', 'CHHATRAPATI SAMBHAJINAGAR (RURAL)',
                 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA',
                 'KOLHAPUR', 'LATUR', 'Mira-Bhayandar, Vasai-Virar Police Commissioner',
                 'NAGPUR CITY', 'NAGPUR RURAL', 'NANDED', 'NANDURBAR',
                 'NASHIK CITY', 'NASHIK RURAL', 'NAVI MUMBAI', 'OSMANABAD', 'PALGHAR', 'PARBHANI',
                 'PIMPRI-CHINCHWAD', 'PUNE CITY', 'PUNE RURAL', 'RAIGAD',
                 'RAILWAY MUMBAI', 'RAILWAY NAGPUR', 'RAILWAY PUNE', 'RATNAGIRI', 'SANGLI', 'SATARA',
                 'SINDHUDURG', 'SOLAPUR CITY', 'SOLAPUR RURAL', 'THANE CITY', 'THANE RURAL', 'WARDHA',
                 'WASHIM', 'YAVATMAL']


def open_page():
    """
    open page and refresh it. without refreshing it dose not work
    """
    driver.get(main_url)
    driver.refresh()
    # checking
    print('page opened and refreshed')


# lists for taking cvs output
poa_dir_district = []
poa_dir_police = []
poa_dir_year = []
poa_dir_FIR = []
poa_dir_date = []
poa_dir_sec = []


# terminal output
print(f'{argv[1]}\n')

for name in ALL_Districts:
    try:
        # temporary print statment
        print(f'\n{name}\n')
        # variables
        number_of_cases_on_all_pages = []
        poa_dictionary = []
        district_dictionary = {"Unit": '', "Police_Station": '',
                               "Number of Records": '', "PoA Cases": '',
                               "Other Cases": ''}

        # set profile for saving directly without pop-up ref -
        # https://stackoverflow.com/a/29777967
        options = Options()
        options.set_preference("browser.download.panel.shown", False)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.helperApps.neverAsk.openFile","application/pdf")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_directory)
        # to go undetected
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) "
                               "Gecko/20100101 Firefox/82.0")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference('useAutomationExtension', False)
        options.set_preference("pdfjs.disabled", True)
        service = Service('C:\\BrowserDrivers\\geckodriver.exe')
        options.headless = True

        # change IP
        myProxy = list_of_proxies()
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy[ALL_Districts.index(name)],
            'ftpProxy': myProxy[ALL_Districts.index(name)],
            'sslProxy': myProxy[ALL_Districts.index(name)],
            'noProxy': ''  # set this value as desired
        })

        driver = webdriver.Firefox(options=options, proxy=proxy)
        open_page()
        # enter the date through terminal argument
        ws_module_v1.enter_date(date1=argv[1], date2=argv[2], driver=driver)
        # checking
        print('date entered.')
        # enter the name of the district. select one from the list

        ws_module_v1.district_selection(name, driver=driver)
        # creation of list. These lists will be converted to dictionary to write to csv
        # check
        print('district name entered\n')
        # dist_name.append(name)
        # call the value of records to view @ 50
        time.sleep(5)
        try:
            ws_module_v1.view_record(driver)
        except NoSuchElementException:
            print('page not loading')
            continue
        # call search
        ws_module_v1.search(driver=driver)
        # check
        print('searched clicked now view 50 records')
        record = ws_module_v1.number_of_records(driver=driver)
        # for terminal output and separate file output
        if record != '':
            print('record found')
        else:
            print('record not found')
            driver.close()
            continue

        if int(record) > 0:
            # check
            print('\ncheking the act')
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            time.sleep(3)
            # this is very rare
            # no records on page so the PoA cases on page will be 0.
            # this 0 needs to be added as the list will be converted to dictionary
            continue

        if int(record) > 50:
            # check
            print('\ncheking the act')
            ws_module_v1.second_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)

            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            # append the list of dist PoAs with total sum of number of cases on all pages
            # for records up to 50 it will be only one record
            # - that is from 0 to 50, if at all available
            driver.close()
            continue

        if int(record) > 100:
            # check
            print('\ncheking the act on p3')
            ws_module_v1.third_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )

        else:
            driver.close()
            continue

        if int(record) > 150:
            # check
            print('\ncheking the act on p4')
            ws_module_v1.forth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.quit()
            continue

        if int(record) > 200:
            # check
            print('\ncheking the act on p5')
            ws_module_v1.fifth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 250:
            # check
            print('\ncheking the act on p6')
            ws_module_v1.sixth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 300:
            # check
            print('\ncheking the act on p7')
            ws_module_v1.seventh_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 350:
            # check
            print('\ncheking the act on p8')
            ws_module_v1.eightth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 400:
            # check
            print('\ncheking the act on p9')
            ws_module_v1.ninenth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 450:
            # check
            print('\ncheking the act')
            ws_module_v1.tenth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 500:
            # check
            print('\ncheking the act p11')
            ws_module_v1.next_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 550:
            # check
            print('\ncheking the act p12')
            ws_module_v1.twelth_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 600:
            # check
            print('\ncheking the act on p13')
            ws_module_v1.thirteen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 650:
            # check
            print('\ncheking the act p14')
            ws_module_v1.fourteen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 700:
            # check
            print('\ncheking the act p15')
            ws_module_v1.next_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 750:
            # check
            print('\ncheking the act p16')
            ws_module_v1.sixteen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 800:
            # check
            print('\ncheking the act p17')
            ws_module_v1.seventeen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 850:
            # check
            print('\ncheking the act p18')
            ws_module_v1.eighteen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 900:
            # check
            print('\ncheking the act p19')
            ws_module_v1.ninteen_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            continue

        if int(record) > 950:
            # check
            print('\ncheking the act p20')
            ws_module_v1.twenty_page(driver)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
        else:
            driver.close()
            # check
            print('all pages finished')

    except Exception:
        print(traceback.format_exc())
        # needs something for terminal output.
        continue

# 29.03.24 for now there is problem in terminal output and statesticla summary
# as the exception is not adding data to the basic structure. like 0 or skiped etc
poa_dir = {"District": poa_dir_district, "Police_Station": poa_dir_police,
           "FIR": poa_dir_FIR, "Date_&_Time": poa_dir_date, "Acts_&_Sections": poa_dir_sec}
df = pd.DataFrame(
    {key: pd.Series(value) for key, value in poa_dir.items()})
df.to_csv(
    os.path.join(base_directory, "poa_summary", f'{argv[3]}_from_{argv[1]}_to_{argv[2]}.csv'))
end = time.time()
print(f'\n{end - start}\n')
