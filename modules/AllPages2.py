"""
1. from pageScrollModule.py
2. sub folder with changed file name
3. due to change in main module
4. additional change - remaining district added and pages structure changed adding if statement
"""

from modules import remainingDistricts3
from modules import MainModule3
import logging

# logging
logger = logging.getLogger(__name__)
# it takes record as an argument which indicates output from other function.
# and name suggesting district name from main function
# another argument is driver - which is from main program and named same.


def scroll_pages(record, name, driver, from_date, to_date):
    number_of_cases_on_all_pages = []
    if int(record) > 0:
        logger.info('trying to create file for all cases')
        MainModule3.df_to_file(driver=driver, name=name,
                               from_date=from_date, to_date=to_date,)
        logger.info('file created for all cases')
        logger.info("p1")
        MainModule3.check_the_act(driver)

    else:
        logger.info("0 cases")
        remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                from_date=from_date,
                                                to_date=to_date,
                                                record=record)


    if int(record) > 50:
        # p2
        second_page = MainModule3.second_page(driver)
        # if scroll page is false, break and write the district to remaining distircts
        if not second_page:
            logger.info("problem loading p2")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act(driver)
    else:
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 100:
        # opening p3
        third_page = MainModule3.third_page(driver)
        if not third_page:
            logger.info("problem loading p3")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act(driver)

    else:
        driver.close()
        # logging
        logger.warning(f"{name} finished\n")
        # tell the outer program, all went well.
        return True

    if int(record) > 150:
        # opening p4
        fourth_page = MainModule3.forth_page(driver)
        if not fourth_page:
            logger.info("problem loading p4")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            logger.info("p4")
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act(driver)
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 200:
        # p5
        fifth_page = MainModule3.fifth_page(driver)
        # cheking for PoA
        if not fifth_page:
            logger.info("problem at p5")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            logger.info('p5')
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act()
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 250:
        # p6
        sixth_page = MainModule3.sixth_page(driver)
        if not sixth_page:
            logger.info("problem loading p6")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            logger.info("p6")
            # cheking for PoA and downloading
            MainModule3.check_the_act(driver)
    else:
        # logging
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 300:
        # p7
        seventh_page = MainModule3.seventh_page(driver)
        if not seventh_page:
            logger.info("problem loading p7")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            logger.info('p7')
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act(driver)
    else:
        # loggingg
        logger.warning(f"{name} finished\n")
        driver.close()
        # tell the outer program, all went well.
        return True

    if int(record) > 350:
        # p8
        eighth_page = MainModule3.eighth_page(driver)
        if not eighth_page:
            logger.info("problem loading p8")
            remainingDistricts3.districtWithProblem(name_of_problem=name,
                                                    from_date=from_date,
                                                    to_date=to_date,
                                                    record=record)
            return False
        else:
            logger.info('p8')
            MainModule3.df_to_file(driver=driver, name=name, from_date=from_date, to_date=to_date)
            MainModule3.check_the_act(driver)
            logger.info("all pages finished")
    else:
        driver.close()
        # loggingg
        logger.warning(f"{name} finished\n")
        return True
