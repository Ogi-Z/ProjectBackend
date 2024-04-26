import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def send_mail(recipient_email, verificationKey):
    # Initialize the WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()
    
    # Navigate to Gmail
    driver.get('https://mail.google.com')
    
    # Enter the username
    username_field = driver.find_element_by_id("identifierId")
    username_field.send_keys("bubirddeneme@gmail.com")
    username_field.send_keys(Keys.RETURN)
    time.sleep(2)

    # Enter the password
    password_field = driver.find_element_by_name("password")
    password_field.send_keys("sereftirsenisevmekGS1905")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    # Compose email
    compose_button = driver.find_element_by_xpath("//div[text()='Compose']")
    compose_button.click()
    time.sleep(2)

    # Fill email details
    to_field = driver.find_element_by_name("to")
    to_field.send_keys(recipient_email)
    to_field.send_keys(Keys.RETURN)

    subject_field = driver.find_element_by_name("subjectbox")
    subject_field.send_keys("Verification Key: " + verificationKey)

    body_field = driver.find_element_by_xpath("//div[@aria-label='Message Body']")
    body_field.send_keys("Verification Key: " + verificationKey)

    # Send email
    send_button = driver.find_element_by_xpath("//div[text()='Send']")
    send_button.click()

    # Wait and close the browser
    time.sleep(5)
    driver.quit()
