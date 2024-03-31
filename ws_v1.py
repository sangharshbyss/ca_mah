"""
1. re-birth from online_FIRs
2. major changes are - a. loggingg
b. iterating over year by creating outer loop.

"""

import os
import time
import pandas as pd
import datetime
import logging
import ws_module_v1


from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from ws_module_proxy_v1 import list_of_proxies

# 1. constants

# 1.a base directory
base_directory = r'/home/sangharsh/Documents/PoA/data/FIR/y_23'
# 1.b logging
logging.basicConfig(filename=os.path.join(base_directory, 'loggingg_info.log'),
                    format='%(asctime)s - %(message)s', level=logging.DEBUG)

# 1.c url of basic page
main_url = r'https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx'

# 1.d lists for taking cvs output
poa_dir_district = []
poa_dir_police = []
poa_dir_year = []
poa_dir_FIR = []
poa_dir_date = []
poa_dir_sec = []

# 1.e start to end dates for year
start = datetime.date(2023, 1, 1)
end = datetime.date(2023, 12, 31)

# 1.f ist of districts
ALL_Districts = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI CITY', 'AMRAVATI RURAL', 'BEED', 'BHANDARA', 'BULDHANA',
                 'CHANDRAPUR', 'CHHATRAPATI SAMBHAJINAGAR CITY', 'CHHATRAPATI SAMBHAJINAGAR (RURAL)',
                 'DHARASHIV', 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA',
                 'KOLHAPUR', 'LATUR', 'Mira-Bhayandar, Vasai-Virar Police Commissioner',
                 'NAGPUR CITY', 'NAGPUR RURAL', 'NANDED', 'NANDURBAR',
                 'NASHIK CITY', 'NASHIK RURAL', 'NAVI MUMBAI', 'PALGHAR', 'PARBHANI',
                 'PIMPRI-CHINCHWAD', 'PUNE CITY', 'PUNE RURAL', 'RAIGAD',
                 'RAILWAY MUMBAI', 'RAILWAY NAGPUR', 'RAILWAY PUNE', 'RATNAGIRI', 'SANGLI', 'SATARA',
                 'SINDHUDURG', 'SOLAPUR CITY', 'SOLAPUR RURAL', 'THANE CITY', 'THANE RURAL', 'WARDHA',
                 'WASHIM', 'YAVATMAL']

# 1.g function for opening page. can it be shifted to module?
def open_page():
    """
    open page and refresh it. without refreshing it dose not work
    """
    driver.get(main_url)
    driver.refresh()

# 2. first loop defining date range
while start < end:
    d2 = start + datetime.timedelta(3)
    from_date = start.strftime("%d%m%Y")
    to_date = d2.strftime("%d%m%Y")

    # constant for outer loop
    # download directory path
    download_directory = os.path.join(base_directory, "copies", f'{from_date} _ {to_date}')
    # create directory if not available.
    if not download_directory:
        os.mkdir(download_directory)

    # 3. inner loop for each district
    for name in ALL_Districts:
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
        #check - pycharm saying argument 'proxy' is unexpected
        driver = webdriver.Firefox(options=options, proxy=proxy)
        open_page()
        # logging
        logging.debug("page opened", exc_info=True)
        # enter the date through terminal argument
        ws_module_v1.enter_date(date1=from_date, date2=to_date, driver=driver)
        # logging
        logging.debug(f"from {from_date} to {to_date}", exc_info=True)
        # enter the name of the district. select one from the list
        ws_module_v1.district_selection(name, driver=driver)
        # logging
        logging.debug(f"{name} district", exc_info=True)
        # creation of list. These lists will be converted to dictionary to write to csv
        # call the value of records to view @ 50
        time.sleep(5)
        ws_module_v1.view_record(driver)
        # loggingg
        logging.debug("what is it?", exc_info=True)
        # call search
        ws_module_v1.search(driver=driver)
        # loggingg
        logging.debug("search clicked", exc_info=True)
        # view 50 records, that is max, per page
        record = ws_module_v1.number_of_records(driver=driver)
        logging.debug("view 50", exc_info=True)
        # for terminal output and separate file output
        if record != '':
            logging.debug("records found", exc_info=True)
        else:
            logging.debug(f"records found for {name}", exc_info=True)
            driver.close()
            continue

        if int(record) > 0:
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            logging.debug("checking if PoA case", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                logging.debug("all FIRs downloaded", exc_info=True)
        else:
            driver.close()
            logging.debug(f"no PoA FIR {name}")
            time.sleep(3)
            # this is very rare
            # no records on page so the PoA cases on page will be 0.
            # this 0 needs to be added as the list will be converted to dictionary
            continue

        if int(record) > 50:
            ws_module_v1.second_page(driver)
            logging.debug("p2", exc_info=True)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)

            logging.debug("checking for PoA", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                logging.debug(f"no PoA{name}", exc_info=True)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                logging.debug("all FIRs downloaded", exc_info=True)
        else:
            logging.debug("no PoA on p2", exc_info=True)
            driver.close()
            continue

        if int(record) > 100:
            #opening p3
            ws_module_v1.third_page(driver)
            # logging
            logging.debug("p3", exc_info=True)
            #checking if PoA is available
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            # logging
            logging.debug("cheked if PoA on p3", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                logging.debug("no PoA on p3", exc_info=True)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)

        else:
            driver.close()
            # logging
            logging.debug(f"finished {name}", exc_info=True)
            continue

        if int(record) > 150:
            # opening p4
            ws_module_v1.forth_page(driver)
            # loggingg
            logging.debug(f"p4 opened for {name}", exc_info=True)
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            # loggingg
            logging.debug(f"checking for PoA in {name}", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                # logging
                logging.debug(f"no PoA on p4 at {name}", exc_info=True)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                #downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                # logging
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)
        else:
            # logging
            logging.debug(f"no PoA on p4 for {name}", exc_info=True)
            driver.close()
            continue

        if int(record) > 200:
            ws_module_v1.fifth_page(driver)
            # loggingg
            logging.debug(f"entered p5 for {name}", exc_info=True)
            # cheking for PoA
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            # logging
            logging.debug(f"checking for act on p5 for {name}", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                # logging
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)
        else:
            # logging
            logging.debug(f"no PoA on page 5 in {name}", exc_info=True)
            driver.close()
            continue

        if int(record) > 250:
            ws_module_v1.sixth_page(driver)
            # loggingg
            logging.debug(f"entered p6 of {name}", exc_info=True)
            # cheking for PoA
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            # loggingg
            logging.debug(f"checked for PoA on p6 for {name}", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                # logging
                logging.debug(f"no PoA on p6 at {name}", exc_info=True)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                # downloading FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                # loggingg
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)
        else:
            # logging
            logging.debug(f"no PoA on p6 for {name}", exc_info=True)
            driver.close()
            continue

        if int(record) > 300:
            ws_module_v1.seventh_page(driver)
            # loggingg
            logging.debug(f"entered p7 for {name}", exc_info=True)
            # cheking for PoA
            poa_cases = ws_module_v1.check_the_act(driver, poa_dir_district,
                                                  poa_dir_police,
                                                  poa_dir_year,
                                                  poa_dir_FIR,
                                                  poa_dir_date,
                                                  poa_dir_sec)
            # logging
            logging.debug(f"checked for PoA on p7 for {name}", exc_info=True)
            if not poa_cases:
                number_of_cases_on_all_pages.append(0)
                logging.debug(f"no PoA on p7 in {name}", exc_info=True)
            else:
                number_of_cases_on_page = int(len(poa_cases))
                number_of_cases_on_all_pages.append(number_of_cases_on_page)
                #downloading FIRs
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                # logging
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)
        else:
            # loggingg
            logging.debug(f"no PoA on p7 for {name}", exc_info=True)
            driver.close()
            continue

        if int(record) > 350:
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
                # downloading PoA FIR
                ws_module_v1.download_repeat(poa_cases, driver,
                                            )
                # loggingg
                logging.debug(f"all FIRs downloaded {name}", exc_info=True)
        else:
            driver.close()
            # loggingg
            logging.debug(f"closing dist {name}", exc_info=True)
            continue

    # loggingg
    logging.debug(f"creating file from {from_date} to {to_date}", exc_info=True)
    poa_dir = {"District": poa_dir_district, "Police_Station": poa_dir_police,
               "FIR": poa_dir_FIR, "Date_&_Time": poa_dir_date, "Acts_&_Sections": poa_dir_sec}
    # dictionary to data frame
    df = pd.DataFrame(
        {key: pd.Series(value) for key, value in poa_dir.items()})
    # taking csv output with date as part of file name
    df.to_csv(
        os.path.join(base_directory, "poa_summary", f'main_from_{from_date}_to_{to_date}.csv'))
    # loggingg
    logging.debug(f"csv file created", exc_info=True)
    # add 3 days to from_date and do again
    start += datetime.timedelta(3)

