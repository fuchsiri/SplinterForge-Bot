import asyncio
import psutil
from selenium import webdriver
import multiprocessing
import linecache
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyfiglet import Figlet
import datetime
import json
import time
import os
import sys
import ctypes
from prettytable import PrettyTable
from tabulate import tabulate
from colorama import init

init(convert=True)
STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetConsoleTitleW("SplinterForge Bot")
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_GREEN = 0x02  # green.
FOREGROUND_RED = 0x04  # red.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_Pink = 0x0d  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_DARKBLUE = 0x01  # dark blue.


def printDarkBlue(message):
    set_cmd_text_color(FOREGROUND_DARKBLUE)
    sys.stdout.write(message)
    resetColor()


def printGreen(message):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(message)
    resetColor()


def printSkyBlue(message):
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    sys.stdout.write(message)
    resetColor()


def printRed(message):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(message)
    resetColor()


def printYellow(message):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(message)
    resetColor()


def printPinky(message):
    set_cmd_text_color(FOREGROUND_Pink)
    sys.stdout.write(message)
    resetColor()


def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


class log_info():
    @staticmethod
    def time():
        return str(datetime.datetime.now().replace(microsecond=0))

    @staticmethod
    def normal(message):
        print(f"{message}")

    @staticmethod
    def success(userName, message):
        printGreen(f"[{log_info.time()}] {userName}: {message}\n")

    @staticmethod
    def error(userName, message):
        printRed(f"[{log_info.time()}] {userName}: {message}\n")

    @staticmethod
    def alerts(userName, message):
        print(f"[{log_info.time()}] {userName}: {message}")

    @staticmethod
    def status(userName, message):
        printYellow(f"[{log_info.time()}] {userName}: {message}\n")

    @staticmethod
    def verify(userName, message):
        printDarkBlue(f"[{log_info.time()}] {userName}: {message}\n")


def printResultBox(userName, data, selectResult):
    table = PrettyTable(["Card", "ID", "Name", "Selection Results"])
    for row in data:
        table.add_row(row)
    dataToPrint = table.get_string(sortby="Card")
    if selectResult:
        log_info.success(userName, "Card selection results:")
        printGreen(f"{dataToPrint}\n")
    else:
        log_info.status(userName, "Card selection results:")
        printYellow(f"{dataToPrint}\n")


def printConfigSettings(totallaccounts, headless, close_driver_while_sleeping, start_thread, start_thread_interval, show_forge_reward, show_total_forge_balance, print_system_usage, check_system_usage_frequency):
    data = [['TOTAL_ACCOUNTS_LOADED', totallaccounts],
            ['HEADLESS', headless],
            ['CLOSE_DRIVER_WHILE_SLEEPING', close_driver_while_sleeping],
            ['START_THREAD', start_thread],
            ['START_THREAD_INTERVAL(seconds)', start_thread_interval],
            ['SHOW_FORGE_REWARD', show_forge_reward],
            ['SHOW_TOTAL_FORGE_BALANCE', show_total_forge_balance],
            ['PRINT_SYSTEM_USAGE', print_system_usage],
            ['CHECK_SYSTEM_USAGE_FREQUENCY(seconds)',
             check_system_usage_frequency]
            ]
    print(tabulate(data, headers=['Setting', 'Value'], tablefmt='grid'))


def start_font():
    f = Figlet(font='smkeyboard', width=150)
    text = f.renderText('SplinterForge\n\/\Bot-Beta\/\n\@lil_astr_0/')
    return f"{text}"


def file_len(file_path):
    with open(file_path, 'r') as rf:
        record = 0
        for line in rf:
            if line.strip():  # Check if the line is not empty after stripping whitespaces
                record += 1
        return record


def getAccountData(file_path, line_number):
    acctinfo = linecache.getline(file_path, int(line_number)+1).strip()
    time.sleep(1)
    userName = acctinfo.split(":")[0]
    postingKey = acctinfo.split(":")[1]
    return userName, postingKey


def getCardSettingData(file_path, line_number):
    acctinfo = linecache.getline(file_path, int(line_number)+1).strip()
    heroesType = acctinfo.split(":")[0]
    bossId = acctinfo.split(":")[1]
    playingSummoners = acctinfo.split(":")[2].split(',')
    playingMonster = acctinfo.split(":")[3].split(',')
    timeSleepInMinute = acctinfo.split(":")[4]
    return heroesType, bossId, playingSummoners, playingMonster, timeSleepInMinute


def getConfig(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        headless = None
        close_driver_while_sleeping = None
        start_thread = None
        start_thread_interval = None
        show_forge_reward = None
        show_total_forge_balance = None
        print_system_usage = None
        check_system_usage_frequency = None
        for line in lines:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                if key == 'HEADLESS':
                    headless = value
                elif key == 'CLOSE_DRIVER_WHILE_SLEEPING':
                    close_driver_while_sleeping = value
                elif key == 'START_THREAD':
                    start_thread = value
                elif key == 'START_THREAD_INTERVAL':
                    start_thread_interval = value
                elif key == 'SHOW_FORGE_REWARD':
                    show_forge_reward = value
                elif key == 'SHOW_TOTAL_FORGE_BALANCE':
                    show_total_forge_balance = value
                elif key == 'PRINT_SYSTEM_USAGE':
                    print_system_usage = value
                elif key == 'CHECK_SYSTEM_USAGE_FREQUENCY':
                    check_system_usage_frequency = value
        return (headless,
                close_driver_while_sleeping,
                start_thread,
                start_thread_interval,
                show_forge_reward,
                show_total_forge_balance,
                print_system_usage,
                check_system_usage_frequency)


def getCardData(userName, cardID):
    with open('data/cardsDetails.json') as json_file:
        data = json.load(json_file)
    found = False
    for i in range(len(data)):
        if int(cardID) == int(data[i]['id']):
            found = True
            name = data[i]['name']
            break
    if found:
        return name
    else:
        log_info.error(userName, "Card with ID {} not found".format(cardID))


def _init(accountNo):
    try:
        userName, postingKey = getAccountData("config/accounts.txt", accountNo)
        if userName == "" or postingKey == "":
            log_info.error(userName,
                           "Error in loading accounts.txt, please add username or posting key and try again.")
            log_info.error(userName,
                           "Terminating in 10 seconds...")
            time.sleep(10)
            sys.exit()
    except:
        print("error loading accounts.txt, retrying...")
        time.sleep(10)
        sys.exit()
    try:
        cardSelection = []
        playingSummonersList = []
        playingMonsterList = []
        heroesType, bossId, playingSummoners, playingMonster, timeSleepInMinute = getCardSettingData(
            "config/cardSettings.txt", accountNo)
        for i in playingSummoners:
            cardName = getCardData(userName, i)
            playingSummonersList.append({
                "playingSummonersDiv": f"//div/img[@id='{i}']",
                "playingSummonersId": f"{i}",
                "playingSummonersName": f"{cardName}"
            })
        for i in playingMonster:
            cardName = getCardData(userName, i)
            playingMonsterList.append({
                "playingMontersDiv": f"//div/img[@id='{i}']",
                "playingMonstersId": f"{i}",
                "playingMonstersName": f"{cardName}"
            })
        cardSelection.append({
            "bossId": f"{bossId}",
            "playingSummoners": playingSummonersList,
            "playingMonsterId": playingMonsterList
        })
        timeSleepInMinute = int(timeSleepInMinute) * 60
    except:
        print("error loading cardSettings.txt file")
        print("Terminating in 10 seconds...")
        time.sleep(10)
        sys.exit()
    return userName, postingKey, heroesType, cardSelection, timeSleepInMinute


def selectSummoners(userName, seletedNumOfSummoners, cardDiv, driver):
    scroolTime = 0
    result = False
    time.sleep(1)
    while scroolTime < 5:
        try:
            WebDriverWait(driver, 0.75).until(
                EC.presence_of_element_located((By.XPATH, cardDiv)))
            time.sleep(1)
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, cardDiv))).click()
            time.sleep(1)

            selectNumber = driver.find_element(
                By.XPATH, "/html/body/app/div[1]/slcards/div[5]/section[1]/div/div[1]/div[2]/div[1]/div[1]/h3/span[2]").text
            if seletedNumOfSummoners == int(selectNumber.split("/")[0]):
                result = True
                break
        except:
            driver.execute_script("window.scrollBy(0, 180)")
            scroolTime += 1
    if not result:
        log_info.error(userName, "Error in selecting summoners, retrying...")
    driver.execute_script("window.scrollBy(0, -4000)")
    time.sleep(1)
    return result


def selectMonsterCards(userName, seletedNumOfMonsters, cardId, cardDiv, driver):
    scroolTime = 0
    result = False
    time.sleep(1)
    while scroolTime < 15:
        try:
            WebDriverWait(driver, 0.75).until(
                EC.presence_of_element_located((By.XPATH, cardDiv)))
            time.sleep(1)
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, cardDiv))).click()
            time.sleep(1)

            selectNumber = driver.find_element(
                By.XPATH, "/html/body/app/div[1]/slcards/div[5]/div[1]/h3/span[2]/div[1]/button/span").text
            selectNumber = int(selectNumber)
            print("selectNumber", selectNumber)
            print("seletedNumOfMonsters", seletedNumOfMonsters)
            if seletedNumOfMonsters == selectNumber:
                result = True
                # log_info.success(
                #     userName, f"Monster card ID {cardId} selected successful!")
                break
        except:
            driver.execute_script("window.scrollBy(0, 450)")
            scroolTime += 1
            pass
        # log_info.error(userName,
        #                f"Error select card ID: {cardId}, skipped this card...")
    driver.execute_script("window.scrollBy(0, -10000)")
    time.sleep(1)
    return result


def check(driver):
    try:
        WebDriverWait(driver, 1.2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/success-modal/section/div[1]/div[4]/div/button"))).click()
    except:
        pass
    try:
        WebDriverWait(driver, 1.2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/login-modal/div/div/div/div[2]/div[3]/button"))).click()
    except:
        pass


def heroSelect(heroesType, userName, driver):
    log_info.alerts(userName,
                    f"Selecting heros type...")
    check(driver)
    try:
        hero_types = ['Warrior', 'Wizard', 'Ranger']
        hero_type = hero_types[int(heroesType) - 1]
        xpath = "/html/body/app/div[1]/splinterforge-heros/div[3]/section/div/div/div[2]/div[1]"

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[1]/a[4]"))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{xpath}/ul/li[{heroesType}]"))).click()
        log_info.success(userName, f"Selected hero type: {hero_type}.")
    except:
        log_info.error(userName, f"Error in selecting hero type, continue...")
        pass
    time.sleep(10)
    log_info.success(userName,
                     f"Participating in battles...")


def login(userName, postingKey, driver):
    driver.get(
        "chrome-extension://jcacnejopjdphbnjgfaaobbfafkihpep/popup.html")
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[4]/div[2]/div[5]/button"))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div/input"))).send_keys("Aa123Aa123!!")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div[2]/div/input"))).send_keys("Aa123Aa123!!")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/button/div"))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/button[1]/div"))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[1]/div/input"))).send_keys(userName)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[2]/div/input"))).send_keys(postingKey)
        time.sleep(2)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[2]/div/input"))).send_keys(Keys.ENTER)
        if WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div"))).text == "HIVE KEYCHAIN":
            log_info.success(userName,
                             "Login successful!")
    except:
        log_info.error(userName,
                       "Login failure! Please check your username and posting key in the accounts.txt file and try again.")
        time.sleep(15)
        driver.close()
    driver.get("https://splinterforge.io/#/")
    driver.set_window_size(1920, 1080)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/success-modal/section/div[1]/div[4]/div/button"))).click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div/div/a/div[1]"))).click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/login-modal/div/div/div/div[2]/div[2]/input"))).send_keys(userName)
    time.sleep(1)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/login-modal/div/div/div/div[2]/div[3]/button"))).click()
    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div"))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[3]/div[2]/button[2]/div"))).click()
            driver.switch_to.window(driver.window_handles[0])
            break
        except:
            pass


def battle(cardSelection, userName, driver, show_forge_reward, show_total_forge_balance):
    try:
        check(driver)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[1]/a[5]/div[1]"))).click()
        for j in range(len(cardSelection)):
            bossIdToSelect = cardSelection[j]['bossId']
            while True:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@tabindex='{bossIdToSelect}']"))).click()
                if "BOSS IS DEAD" != WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/slcards/div[5]/section[1]/div/div[1]/div[2]/button"))).text:
                    time.sleep(1)
                    break
                else:
                    log_info.error(userName,
                                   "The selected boss has been defeated, selecting another one automatically...")
                    if int(bossIdToSelect) < 17:
                        bossIdToSelect = str(int(bossIdToSelect) + 1)
                    else:
                        bossIdToSelect = "14"
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[1]/a[5]/div[1]"))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/slcards/div[5]/section[1]/div/div[1]/div[2]/button"))).click()
            log_info.alerts(
                userName, "Selecting cards for summoners and monsters, this process could be lengthy...")
            printData = []
            seletedNumOfSummoners = 1
            for i in cardSelection[j]['playingSummoners']:
                summonersInfo = i
                cardId = summonersInfo["playingSummonersId"]
                cardDiv = summonersInfo["playingSummonersDiv"]
                cardName = summonersInfo["playingSummonersName"]
                resultSeletetSummoners = selectSummoners(
                    userName, seletedNumOfSummoners, cardDiv, driver)
                seletedNumOfSummoners += 1
                if resultSeletetSummoners:
                    printData.append(
                        [f"Summoners #{int(cardSelection[j]['playingSummoners'].index(i)) + 1}", cardId, cardName, "success"])
                else:
                    log_info("restarting...")
            # log_info.success(
            #     userName, "Summoners selected successful!")
            seletedNumOfMonsters = 1
            selectResult = True
            for i in cardSelection[j]['playingMonsterId']:
                monstersInfo = i
                cardId = monstersInfo["playingMonstersId"]
                cardDiv = monstersInfo["playingMontersDiv"]
                cardName = monstersInfo["playingMonstersName"]
                resultSeletetMonsters = selectMonsterCards(
                    userName, seletedNumOfMonsters, cardId, cardDiv, driver)
                if resultSeletetMonsters:
                    printData.append(
                        [f"Monsters #{int(cardSelection[j]['playingMonsterId'].index(monstersInfo))+1}", cardId, cardName, "success"])
                    seletedNumOfMonsters += 1
                else:
                    selectResult = False
                    printData.append(
                        [f"Monsters #{int(cardSelection[j]['playingMonsterId'].index(monstersInfo))+1}", cardId, cardName, "error"])
            printResultBox(userName, printData, selectResult)
            manaUsed = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/slcards/div[5]/div[2]/div[1]/div[1]/button/span"))).text
            totalManaHave = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[2]/div[1]/a[2]/div[1]/span"))).text
            if int(manaUsed) <= 15:
                log_info.error(
                    userName, "The selected monster cards do not meet the required mana, please adjust your cardSettings.txt, however, bot is retrying...")
            elif int(totalManaHave.split('/')[0]) > int(manaUsed):
                try:
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/slcards/div[5]/button[1]/div[2]/span"))).click()
                    if show_forge_reward:
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/slcards/div[4]/div[2]/button[2]/span")))
                        if show_total_forge_balance:
                            forgebalance = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[2]/div[1]/a[1]/div[1]/span"))).text
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/slcards/div[4]/div[2]/button[2]/span")))
                        WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/app/div[1]/slcards/div[4]/div[2]/button[2]/span"))).click()
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/slcards/div[5]/div[1]/replay/section/rewards-modal/section/div[1]/div[1]/p[1]")))
                        time.sleep(2)
                        reward = driver.find_element(
                            By.XPATH, "/html/body/app/div[1]/slcards/div[5]/div[1]/replay/section/rewards-modal/section/div[1]/div[1]/p[1]").text
                        log_info.status(userName, reward)
                        if show_total_forge_balance:
                            log_info.status(
                                userName, f"Your total balance is {forgebalance} Forge tokens.")
                    else:
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/slcards/div[4]/div[2]/button[2]/span")))
                        forgebalance = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/app/div[1]/div[1]/app-header/section/div[4]/div[2]/div[2]/div[1]/a[1]/div[1]/span"))).text
                        log_info.status(
                            userName, f"Your total balance is {forgebalance} Forge tokens.")
                    log_info.success(
                        userName, "The battle has ended!")
                    return 1

                except:
                    log_info.success(
                        userName, "Encountering difficulty in reading the game results, but the battle has ended.")
                    return 1

            else:
                log_info.alerts(
                    userName, "Insufficient stamina, entering a rest state of inactivity for 1 hour...")
                return 2
    except:
        driver.get("https://splinterforge.io/#/")
        log_info.error(userName,
                       "There may be some issues with the server or your playing cards, retrying in 30 seconds...")
        time.sleep(15)
        driver.refresh()
        time.sleep(15)
        return 3


def battleLoop(driver, userName, postingKey, heroesType, cardSelection, show_forge_reward, show_total_forge_balance, close_driver_while_sleeping, timeSleepInMinute):
    login(userName, postingKey, driver)
    heroSelect(heroesType, userName, driver)
    while True:
        try:
            battleResult = battle(
                cardSelection, userName, driver, show_forge_reward, show_total_forge_balance)
            if battleResult == 3:
                log_info("restarting...")
            if close_driver_while_sleeping:
                driver.quit()
            if battleResult == 2:
                time.sleep(3600)
            elif battleResult == 1 and timeSleepInMinute != 0:
                log_info.alerts(userName,
                                f"According to your configuration, this account will enter a state of inactivity for {int(timeSleepInMinute/60)} minutes.")
                time.sleep(timeSleepInMinute)
            if close_driver_while_sleeping:
                break
        except:
            pass


def start(i, accountNo, headless, close_driver_while_sleeping, show_forge_reward, show_total_forge_balance):
    while True:
        try:
            try:
                userName, postingKey, heroesType, cardSelection, timeSleepInMinute = _init(
                    accountNo)
                log_info.alerts(userName, "Initializing...")
                executable_path = "/webdrivers"
                os.environ["webdriver.chrome.driver"] = executable_path
                options = Options()
                options.add_extension('data/hivekeychain.crx')
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-setuid-sandbox")
                options.add_argument(
                    "--disable-backgrounding-occluded-windows")
                options.add_argument("--disable-background-timer-throttling")
                options.add_argument('--disable-translate')
                options.add_argument('--disable-popup-blocking')
                options.add_argument("--disable-infobars")
                # options.add_argument("--disable-gpu")
                options.add_argument(
                    '--disable-blink-features=AutomationControlled')
                options.add_argument("--mute-audio")
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--allow-running-insecure-content')
                options.add_experimental_option(
                    "excludeSwitches", ["enable-automation"])
                options.add_experimental_option(
                    'useAutomationExtension', False)
                options.add_experimental_option(
                    "prefs", {
                        "profile.managed_default_content_settings.images": 1,
                        "profile.managed_default_content_settings.cookies": 1,
                        "profile.managed_default_content_settings.javascript": 1,
                        "profile.managed_default_content_settings.plugins": 1,
                        "profile.default_content_setting_values.notifications": 2,
                        "profile.managed_default_content_settings.stylesheets": 2,
                        "profile.managed_default_content_settings.popups": 2,
                        "profile.managed_default_content_settings.geolocation": 2,
                        "profile.managed_default_content_settings.media_stream": 2,
                    }
                )
                options.add_argument("--window-size=300,600")
                if headless:
                    options.add_argument("--headless=new")
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
                try:
                    driver = webdriver.Chrome(options=options)
                except WebDriverException as e:
                    # Handle the error and hide it from the user
                    print("An error occurred while starting the WebDriver:", e)
            except:
                log_info("restarting...")
            battleLoop(driver, userName, postingKey, heroesType, cardSelection, show_forge_reward,
                       show_total_forge_balance, close_driver_while_sleeping, timeSleepInMinute)

        except:
            driver.quit()
            log_info.error(userName,
                           "Error in this thread, restarting now.")
            pass


def kill_chromeanddriver():
    for process in psutil.process_iter():
        if process.name() == "chromedriver.exe":
            os.system(f"taskkill /pid {process.pid} /f > NUL")
    for proc in psutil.process_iter():
        if proc.name() == "chrome.exe":
            if "--remote-debugging-port" in " ".join(proc.cmdline()):
                os.system(f"taskkill /pid {proc.pid} /f > NUL")
                break


def startMulti(totallaccounts, headless, close_driver_while_sleeping, start_thread, start_thread_interval, show_forge_reward, show_total_forge_balance):
    # kill_chromeanddriver()
    chromedriver_autoinstaller.install()
    workers = []
    for i in range(totallaccounts):
        a = str(i + 1)
        workers.append(multiprocessing.Process(
            target=start, args=(a, a, headless, close_driver_while_sleeping, show_forge_reward, show_total_forge_balance)))
    current_threads = 0
    while workers or len(multiprocessing.active_children()) > 0:
        if current_threads < start_thread and workers:
            worker = workers.pop(0)
            try:
                multiprocessing.freeze_support()
                worker.start()
                current_threads += 1
                time.sleep(3)
            except:
                pass
        else:
            time.sleep(start_thread_interval)
            current_threads = 0


async def printSystemUsage(check_system_usage_frequency):
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"SplinterForge Bot | CPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%")
        await asyncio.sleep(check_system_usage_frequency)


async def main():
    multiprocessing.freeze_support()
    printSkyBlue(start_font())
    print("Welcome to SplinterForge Bot! To stay informed about updates and get access to helpful guides, please check out the Github page: https://github.com/Astr0-G/SplinterForge-Bot")
    try:
        headless, close_driver_while_sleeping, start_thread, start_thread_interval, show_forge_reward, show_total_forge_balance, print_system_usage, check_system_usage_frequency = getConfig(
            'config/config.txt')
        totallaccounts = int(file_len("config/accounts.txt")) - 1
    except:
        print("error reading config.txt located in the config folder.")
        print("Terminating in 10 seconds...")
        time.sleep(10)
        sys.exit()
    if totallaccounts < 1:
        print("You need to add accounts in accounts.txt located in the config folder.")
        print("Terminating in 10 seconds...")
        time.sleep(10)
        sys.exit()
    if totallaccounts < start_thread:
        start_thread = totallaccounts
    printConfigSettings(totallaccounts, headless, close_driver_while_sleeping, start_thread, start_thread_interval, show_forge_reward,
                        show_total_forge_balance, print_system_usage, check_system_usage_frequency)
    process_start_multi = multiprocessing.Process(target=startMulti, args=(
        totallaccounts, headless, close_driver_while_sleeping, start_thread, start_thread_interval, show_forge_reward, show_total_forge_balance))
    process_start_multi.start()
    if print_system_usage:
        await asyncio.gather(printSystemUsage(check_system_usage_frequency))

if __name__ == "__main__":
    asyncio.run(main())
