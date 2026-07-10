from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

STREAMLIT_URLS = [
    os.environ.get("STREAMLIT_APP_URL_1", "https://mutual-fund-screener.streamlit.app/"),
    os.environ.get("STREAMLIT_APP_URL_2", "https://zomato-complaint-resolution.streamlit.app/"),
]

def wake_app(driver, url):
    print(f"\n--- Checking: {url} ---")
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    try:
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
        )
        print("Wake-up button found. Clicking...")
        button.click()

        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
            print(f"Button disappeared, app booting...")
    
    # Wait for app to actually load (60 seconds max)
            import time
            time.sleep(60)
            print(f"App waking up ✅")
    
        except TimeoutException:
            print(f"Button clicked but didn't disappear ❌")
            return False

    except TimeoutException:
        print(f"No wake-up button — app already awake ✅")

    return True

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    failed = []
    try:
        for url in STREAMLIT_URLS:
            success = wake_app(driver, url)
            if not success:
                failed.append(url)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()
        print("\nScript finished.")

    if failed:
        print(f"\nFailed URLs: {failed}")
        exit(1)

if __name__ == "__main__":
    main()