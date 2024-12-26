import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure le logger
logging.basicConfig(filename='instagram_comparison.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter sans interface graphique
    service = Service('/path/to/chromedriver')  # Remplacer par le chemin vers le chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)
    
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Attendre que la connexion soit complète

def get_followers(driver, profile_url):
    driver.get(profile_url)
    time.sleep(3)
    
    # Clic sur le nombre d'abonnés
    driver.find_element(By.PARTIAL_LINK_TEXT, 'followers').click()
    time.sleep(2)
    
    # Récupérer les abonnés
    followers = set()
    while True:
        followers_list = driver.find_elements(By.CLASS_NAME, 'FPmhX')
        for user in followers_list:
            followers.add(user.text)
        
        # Scroller vers le bas pour charger plus de profils
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", driver.find_element(By.CLASS_NAME, 'isgrP'))
        time.sleep(2)
        
        if len(followers_list) == len(followers):
            break
    
    return followers

def get_following(driver, profile_url):
    driver.get(profile_url)
    time.sleep(3)
    
    # Clic sur le nombre d'abonnements
    driver.find_element(By.PARTIAL_LINK_TEXT, 'following').click()
    time.sleep(2)
    
    # Récupérer les abonnements
    following = set()
    while True:
        following_list = driver.find_elements(By.CLASS_NAME, 'FPmhX')
        for user in following_list:
            following.add(user.text)
        
        # Scroller vers le bas pour charger plus de profils
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", driver.find_element(By.CLASS_NAME, 'isgrP'))
        time.sleep(2)
        
        if len(following_list) == len(following):
            break
    
    return following

def compare_and_log(followers, following):
    not_mutual = followers.symmetric_difference(following)
    
    # Log des utilisateurs non mutuels
    logging.info("Utilisateurs non mutuels:")
    for user in not_mutual:
        logging.info(user)

def main():
    # Demander à l'utilisateur de saisir son nom d'utilisateur et mot de passe
    username = input("Entrez votre nom d'utilisateur Instagram : ")
    password = input("Entrez votre mot de passe Instagram : ")
    
    profile_url = f'https://www.instagram.com/{username}/'

    driver = init_driver()
    
    try:
        login(driver, username, password)
        followers = get_followers(driver, profile_url)
        following = get_following(driver, profile_url)
        
        compare_and_log(followers, following)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()