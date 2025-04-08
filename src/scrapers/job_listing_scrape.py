from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import time
import pandas as pd # type: ignore
from typing import List, Tuple, Dict, Any
import argparse

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://jobs.lever.co/cardless/4af33618-2c94-420c-9337-a1ea2ae92801/")
time.sleep(3)  # Initial page load wait

try:
    bodyyy = driver.find_element(By.TAG_NAME, "body").text
    # description_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "_descriptionText_4fqrp_201"))
    # )
    print("Found job description body:", bodyyy )
except Exception as e:
    print(f"Page is not scrapable: {str(e)}")



driver.quit()