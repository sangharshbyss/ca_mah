"""
issue:
1. sometimes - it downloads same FIR twice
2. sometimes it dosen't goes to page 2 and just creates df for page 1 repeatedly.
description:
1. from ws2.py
2. approached changed so file changed
3. if the exception is raised,
a csv file with name of remaining districts and dates will be created.
This file will be run separately to cover those districts for those dates.
This may need writing a new module.
Currently, in the first step is to create csv output.
4. No summary of PoA cases.

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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from modules import AllPages2

from modules import remainingDistricts3, MainModule3
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

    # 1.e start to end dates for year
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 3, 31)

    # 1.f ist of districts
    all_districts = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI CITY', 'AMRAVATI RURAL', 'BEED', 'BHANDARA', 'BULDHANA',
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
        # logging- set at warning level to take console output
        logger.warning(f"\n\nstart {from_date}")
        # constant for outer loop
        # download directory path
        download_directory = os.path.join(base_directory,
                                          "copies", f'{from_date} _ {to_date}')
        # create directory if not available.
        if not download_directory:
            os.mkdir(download_directory)

        # 3. inner loop for each district
        for name in all_districts:
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
            # service = Service('C:\\BrowserDrivers\\geckodriver.exe')
            options.headless = True

            # change IP
            my_proxy = list_of_proxies()
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': my_proxy[all_districts.index(name)],
                'ftpProxy': my_proxy[all_districts.index(name)],
                'sslProxy': my_proxy[all_districts.index(name)],
                'noProxy': ''  # set this value as desired
            })
            # check - pycharm saying argument 'proxy' is unexpected
            try:
                driver = webdriver.Firefox(options=options, proxy=proxy)
                open_page()
                # enter the date
                MainModule3.enter_date(date1=from_date, date2=to_date, driver=driver)
                # enter district
                MainModule3.district_selection(name, driver=driver)
                logger.warning(f'{name} Started')
                # creation of list. These lists will be converted to dictionary to write to csv
                # call the value of records to view @ 50
                time.sleep(3)
                MainModule3.view_record(driver)
                # call search
                MainModule3.search(driver=driver)
                # how many cases in district?
                record = MainModule3.number_of_records(driver=driver)
                if record != '':
                    pass
                else:
                    logger.warning(f"completed {name}\n. No records Founds\n")
                    remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                            from_date=from_date,
                                                            to_date=to_date,
                                                            record=record)
                    driver.close()
                    continue
                AllPages2.scroll_pages(record=record, name=name, driver=driver,
                                       from_date=from_date, to_date=to_date)
            except (NoSuchElementException, StaleElementReferenceException):
                # logging
                logger.warning('did not even enter page scroll\n'
                               'writing to remaining district', exc_info=True)
                # write to the file for remaining districts.
                remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                        from_date=from_date,
                                                        to_date=to_date,
                                                        record="0")
                continue
        start += datetime.timedelta(4)


if __name__ == '__main__':
    main()
