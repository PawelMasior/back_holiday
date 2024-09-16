import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import whisper # pip install -U openai-whisper
model = whisper.load_model("base")

def _df_elements_title(driver):
    # elements_title = driver.find_elements(By.XPATH, "*")
    elements_title = driver.find_elements(By.XPATH, "//*[@title]")
    df_elements_title = pd.DataFrame([
        {
            'title': el.get_attribute('title'),
            'id': el.get_attribute('id'),
            'id2': el.id,
            'aria_role': el.aria_role,
            'role': el.aria_role,
            'name': el.accessible_name, 
            'text': el.text,
            'class': el.get_attribute('class'),
            'name': el.get_attribute('name'),
            'href': el.get_attribute('href'),  # For links
            'src': el.get_attribute('src'),  # For images
            'alt': el.get_attribute('alt'),  # For images with alt text
            'x': el.location['x'],
            'y': el.location['y'],
            'height': el.size['height'],
            'width': el.size['width'],
        }
        for el in elements_title
    ])
    return df_elements_title
# df_elements_title = _df_elements_title(driver)
# =============================================================================
# df_elements_title['aria_role'] = 'article'
# df_elements_title['role'] = 'article'
# elements_draw(driver, df_elements_title)
# =============================================================================

def click_reCAPTCHA(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()
# click_reCAPTCHA(driver); time.sleep(1)

def click_recaptcha_audio_button(driver, df_elements_title):
    for i,r in df_elements_title.iterrows():
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, f".//iframe[@title='{r['title']}']"))
            driver.find_element(By.ID, "recaptcha-audio-button").click()
            # print('clicked audio')
        except: 0
#click_recaptcha_audio_button(driver); time.sleep(1)

def transcribe(url):
    with open('.temp', 'wb') as f: f.write(requests.get(url).content)
    result = model.transcribe('.temp')
    return result["text"].strip()
#text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))

def solve_audio_captcha(driver, text):
    driver.find_element(By.ID, "audio-response").send_keys(text)
    time.sleep(2)
    driver.find_element(By.ID, "recaptcha-verify-button").click()
#solve_audio_captcha(driver, text)

def solve_recapcha(driver):
    msg = ''
    try:
        df_elements_title = _df_elements_title(driver)
        click_reCAPTCHA(driver)
        time.sleep(3)
        click_recaptcha_audio_button(driver, df_elements_title)
        time.sleep(3)
        text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
        solve_audio_captcha(driver, text)
        msg = 'Success: solved capcha with audio'
    except Exception as e:
        msg = f"Error: {str(e)[:200]}"
    return msg
