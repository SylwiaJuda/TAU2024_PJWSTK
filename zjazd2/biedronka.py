from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.biedronka.pl/pl"
browsers = {
    "Chrome": webdriver.Chrome,
    "Edge": webdriver.Edge,
    "Firefox": webdriver.Firefox
}

def checkBiedronkaShopping(browser_name, driver):
    driver.get(url)

    # Krok 1: Akceptacja polityki prywatności (jeśli jest wyświetlana)
    try:
        privacy_accept_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        assert privacy_accept_button.is_displayed(), f"{browser_name}: Przyciski akceptacji polityki prywatności nie jest widoczny"
        privacy_accept_button.click()
    except:
        print(f"{browser_name}: Przyciski akceptacji polityki prywatności nie pojawił się")

    # Asercja 1: Sprawdzenie, czy strona główna załadowała się poprawnie poprzez weryfikację tytułu
    assert "Biedronka" in driver.title, f"{browser_name}: Tytuł strony nie zawiera słowa 'Biedronka'"

    # Asercja 2: Sprawdzenie, czy na stronie jest widoczna sekcja "Gazetka"
    flyer_section = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Gazetka"))
    )
    assert flyer_section.is_displayed(), f"{browser_name}: Sekcja 'Gazetka' nie jest widoczna"
    flyer_section.click()

    # Asercja 3: Sprawdzenie, czy strona gazetki załadowała się poprawnie
    assert WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "catalogs-title"))
    ), f"{browser_name}: Strona gazetki nie załadowała się poprawnie"

    # Asercja 4: Sprawdzenie widoczności obrazka pierwszej strony gazetki
    first_page = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@alt='Strona 1']"))
    )
    assert first_page.is_displayed(), f"{browser_name}: 'Strona 1' gazetki nie jest widoczna"
    first_page.click()

    # Asercja 5: Weryfikacja funkcji przejścia do następnej strony
    next_page_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Następna strona']"))
    )
    assert next_page_button.is_displayed(), f"{browser_name}: Przycisk następnej strony nie jest widoczny"
    next_page_button.click()

    # Asercja 6: Sprawdzenie, czy wyświetlana jest druga strona gazetki
    assert WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@alt='Strona 2']"))
    ), f"{browser_name}: 'Strona 2' gazetki nie jest widoczna"

    # Asercja 7: Powrót do poprzedniej strony
    previous_page_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Poprzednia strona']"))
    )
    assert previous_page_button.is_displayed(), f"{browser_name}: Przycisk poprzedniej strony nie jest widoczny"
    previous_page_button.click()

    # Finalna asercja: Powrót do pierwszej strony gazetki
    assert WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@alt='Strona 1']"))
    ), f"{browser_name}: Powrót do 'Strony 1' nie działa poprawnie"

    # Zakończenie testu
    driver.quit()

# Przeprowadzenie testu dla każdej przeglądarki
for browser_name, browser_driver in browsers.items():
    driver = browser_driver()
    checkBiedronkaShopping(browser_name, driver)
