from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Fill in your username in UN and password in PW
UN = "USERNAME"
PW = "PASSWORD"

# Change ".Firefox" to what browser you will be using
# Change the path to your path of your webdriver
driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe')


def scrollAndFindElements(scrollPath):
    # This function scrolls through the follower/following window and then adds the name of the accounts to returnArray
    returnArray = []
    last_ht, ht = 0, 1
    scroll_box = driver.find_element_by_xpath(scrollPath)
    while last_ht != ht:
        last_ht = ht
        time.sleep(1)
        ht = driver.execute_script(
            """arguments[0].scrollTo(0,arguments[0].scrollHeight);return arguments[0].scrollHeight;""", scroll_box)
    links = scroll_box.find_elements_by_tag_name('a')
    for person in links:
        try:
            toAdd = person.text
            if toAdd != '':
                returnArray.append(toAdd)
        except:
            print("Exception")
    return returnArray


driver.get("https://instagram.com")

acceptCookies = driver.find_element_by_xpath(
    '/html/body/div[3]/div/div/button[1]').click()

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")))
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")))

username.send_keys(UN)
password.send_keys(PW)

time.sleep(2)

login = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]")))
ActionChains(driver).move_to_element(login).click().perform()

dontSave = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button")))
dontSave.click()

noNotations = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]")))
noNotations.click()

user = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[2]/div[1]/div")))
user.click()

followers = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")))
followers.click()

time.sleep(3)

# Add the accounts that are following you to followersArray
followersArray = scrollAndFindElements('/html/body/div[5]/div/div/div[2]')

time.sleep(3)

closeFollowers = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button")))
closeFollowers.click()

following = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")))
following.click()

time.sleep(3)

# Add the accounts that you are following to followingArray
followingArray = scrollAndFindElements('/html/body/div[5]/div/div/div[2]')
print("-----LENGTH OF FOLLOWINGARRAY-----")
print(len(followingArray))
notFollowingMeArray = []
meNotFollowingBackArray = []

# Compare the followers and following to see what accounts are not following you back and what accounts you are not following back.
for following in followingArray:
    for follower in followersArray:
        if not(following in followersArray):
            notFollowingMeArray.append(following)
        if not(follower in followingArray):
            meNotFollowingBackArray.append(follower)

# Remove duplicates
notFollowingMeArray = list(dict.fromkeys(notFollowingMeArray))
meNotFollowingBackArray = list(dict.fromkeys(meNotFollowingBackArray))

print("----- Not following me back ----- ")
for element in notFollowingMeArray:
    print(element)
print(" ")
print("----- I am not following back -----")
for element in meNotFollowingBackArray:
    print(element)
