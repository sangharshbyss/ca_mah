"""
1. module of ws3.py
2. creates csv of remaining districts with dates (from and to).
"""
from pathlib import Path
import logging
import pandas as pd



logger = logging.getLogger(__name__)

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


def districtWithProblem(name_of_problem, from_date, to_date):
    # create a dictionary by iterating over list of districts
    for name in ALL_Districts[ALL_Districts.index(name_of_problem):]:
        dictionary = {'District': [name], 'from_date': [from_date], 'to_date': [to_date]}
        file_name = f'remaining_district_{from_date}_{to_date}.csv'
        dir_name = Path(f'/home/sangharsh/Documents/PoA/data/FIR/y_23/remaining_districts')
        dir_name.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame.from_dict(dictionary)
        df.to_csv(dir_name/file_name, mode='a', index=False, header=False)

    logger.info("file for remaining districts created")
