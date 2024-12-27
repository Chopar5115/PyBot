from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd


def prepare_table(html_table):
    df = pd.read_html("<table>" + html_table + "/table")[0]
    df = df.drop(index=[0, 1, 2, 3])
    df = df.drop(df.columns[[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 19]], axis=1)
    df.columns = ['Discp', 'Name', 'Exam1', 'Test1', 'Exam2', 'Test2']
    disciplines = df[['Discp', 'Name', 'Exam1', 'Test1', 'Exam2', 'Test2']].values.tolist()
    names = df[['Discp', 'Name']].values.tolist()

    return disciplines, names


def parse_dv(names):
    dv_list = []
    count = 1
    for el in names:
        st = str(el[0]).split('.')
        if 'ДВ' not in st or len(st) < 5:
            continue
        dv = []
        if 'ДВ' in st and len(st) == 5:
            dv.append(count)
            dv.append(el[1])
            names.remove(el)
            for el2 in names:
                st2 = str(el2[0]).split('.')
                if 'ДВ' not in st2 or len(st2) < 5:
                    continue
                if st2[3] == st[3]:
                    dv.append(el2[1])
                    names.remove(el2)
            dv_list.append(dv)
        count = count + 1

    return dv_list


def fill_disciples(disciplines, dv_list):
    sem1_test = []
    sem1_exam = []
    sem2_test = []
    sem2_exam = []
    for el in disciplines:
        st = str(el[0]).split('.')
        if 'ДВ' in st:
            continue
        if el[2] == '+':
            sem1_exam.append(el[1])
        if el[3] == '+':
            sem1_test.append(el[1])
        if el[4] == '+':
            sem2_exam.append(el[1])
        if el[5] == '+':
            sem2_test.append(el[1])
    symb = '●️'
    for dv in dv_list:
        cur_dv = f'Блок дисциплин по выбору {dv[0]}'
        fl = True
        for el in disciplines:
            if el[1] in dv:
                if el[2] == '+':
                    if fl:
                        sem1_exam.append(cur_dv)
                        fl = False
                    sem1_exam.append(symb + el[1])
                if el[3] == '+':
                    if fl:
                        sem1_test.append(cur_dv)
                        fl = False
                    sem1_test.append(symb + el[1])
                if el[4] == '+':
                    if fl:
                        sem2_exam.append(cur_dv)
                        fl = False
                    sem2_exam.append(symb + el[1])
                if el[5] == '+':
                    if fl:
                        sem2_test.append(cur_dv)
                        fl = False
                    sem2_test.append(symb + el[1])

    return sem1_exam, sem1_test, sem2_exam, sem2_test


def response_text(sem1_exam, sem1_test, sem2_exam, sem2_test, course):
    course = int(course)
    text = f'Семестр {2*course-1} \n\nЗачеты:\n'
    for s in sem1_test:
        text = text + s + '\n'
    text = text + f'\nЭкзамены:\n'
    for s in sem1_exam:
        text = text + s + '\n'
    text = text + f'\nСеместр {2*course}\n\nЗачеты:\n'
    for s in sem2_test:
        text = text + s + '\n'
    text = text + f'\nЭкзамены:\n'
    for s in sem2_exam:
        text = text + s + '\n'

    return text


def form_processing(direction, plan, course):
    options = Options()
    options.add_argument('--headless=new')
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print('Ошибка webdriver')
        print(e)
    else:
        try:
            driver.get("https://shelly.kpfu.ru/e-ksu/study_plan_for_web?P_FACULTY=9&p_portal=1")
        except Exception as e:
            print('Сайт не доступен')
            print(e)
        else:
            select_element = driver.find_element(By.XPATH, "//*[@id='dim_content2']/div[2]/table/tbody/tr/td[2]/select")
            select = Select(select_element)
            select.select_by_value(direction)

            select_element = driver.find_element(By.XPATH, "//*[@id='dim_content2']/div[2]/table/tbody/tr[2]/td[2]/select")
            select = Select(select_element)
            select.select_by_value(plan)

            select_element = driver.find_element(By.XPATH,
                                                 "// *[ @ id = 'dim_content2'] / div[2] / table / tbody / tr[3] / td[2] / select")
            select = Select(select_element)
            select.select_by_value(course)

            driver.find_element(By.XPATH, "//*[@id='submit_ask']/input").click()

            table = driver.find_element(By.CLASS_NAME, 'T_TABLE')
            html_table = table.get_attribute('innerHTML')
            driver.quit()

            return html_table


def response(direction, plan, course):
    html_table = form_processing(direction, plan, course)

    disciplines, names = prepare_table(html_table)

    dv_list = parse_dv(names)

    sem1_exam, sem1_test, sem2_exam, sem2_test = fill_disciples(disciplines, dv_list)

    return response_text(sem1_exam, sem1_test, sem2_exam, sem2_test, course)
