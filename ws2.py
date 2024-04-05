"""
1. re-birth from online_FIRs
2. major changes are - a. loggingg
b. iterating over year by creating outer loop.
3. new approach - try is /except is added if error occurs.
So if exception is encoutered - the same date range will start over.


Further Actions:
1. module names as per style guide
2. use classes to by more pythonic - object oriented
3. change file structure.


"""

import datetime
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import districtModule
import pageScrolModule
import ws_module_v1
from ws_module_proxy_v1 import list_of_proxies


def main():
    # 1.a base directory
    base_directory = r'/home/sangharsh/Documents/PoA/data/FIR/y_23'

    # 1. constants
    # 1.b logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=os.path.join(base_directory, 'debug.log'),
                        format='%(name)s:: %(levelname)s:: %(asctime)s - %(message)s',
                        level=logging.INFO)
    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    logger.addHandler(ch)

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
    end = datetime.date(2023, 3, 31)

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
        # add 3 days to start date to create to date
        d2 = start + datetime.timedelta(3)
        # covert to string
        from_date = start.strftime("%d%m%Y")
        to_date = d2.strftime("%d%m%Y")
        #logging- set at warning level to take console output
        logger.warning(f"start {from_date}")
        # constant for outer loop
        # download directory path
        download_directory = os.path.join(base_directory,
                                          "copies", f'{from_date} _ {to_date}')
        # create directory if not available.
        if not download_directory:
            os.mkdir(download_directory)

        # 3. inner loop for each district
        for name in ALL_Districts:
            # variables
            number_of_cases_on_all_pages = []
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
            try:
                driver = webdriver.Firefox(options=options, proxy=proxy)
                open_page()
                # enter the date
                ws_module_v1.enter_date(date1=from_date, date2=to_date, driver=driver)
                # enter district
                ws_module_v1.district_selection(name, driver=driver)
                logger.warning(f'{name} Started')
                # creation of list. These lists will be converted to dictionary to write to csv
                # call the value of records to view @ 50
                time.sleep(3)
                ws_module_v1.view_record(driver)
                # call search
                ws_module_v1.search(driver=driver)
                # view 50 records, that is max, per page
                record = ws_module_v1.number_of_records(driver=driver)
                if record != '':
                    pass
                else:
                    logger.warning(f"completed {name}\n. No records Founds\n")
                    driver.close()
                    continue
                scroll_pages = pageScrolModule.scrollPages(
                    record=record, name=name, driver=driver,
                    from_date=from_date, to_date=to_date)
                if scroll_pages:
                    continue
                else:
                    driver.close()
                    while True:
                        try:

                            logger.warning("the error code has started")
                            districtModule.districtWithProblem(
                                name_of_problem=name, from_date=from_date, to_date=to_date)
                            driver.close()
                            break
                        except:
                            logger.warning("the error code starting second time")
                            districtModule.districtWithProblem(
                                name_of_problem=name, from_date=from_date, to_date=to_date)
                            driver.close()

            except Exception as e:
                while True:
                    try:
                        logger.warning("entering error code without entering pageScrollModule")
                        second_name, from_date, to_date = districtModule.districtWithProblem(
                            name_of_problem=name, from_date=from_date, to_date=to_date)
                        break
                    except:
                        second_name, from_date, to_date = districtModule.districtWithProblem(
                            name_of_problem=name, from_date=from_date, to_date=to_date)
                        districtModule.districtWithProblem(name_of_problem=second_name,
                                                           from_date=from_date,
                                                           to_date=to_date)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
