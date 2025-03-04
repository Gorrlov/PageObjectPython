import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Опции командной строки.
    В командную строку передается параметр вида '--language="es"'
    По умолчанию передается параметр, включающий английский интерфейс в браузере
    """
    parser.addoption("--language", action="store", default="en", help="Choose language")
    parser.addoption('--browser_name', action='store', default="chrome",
                    help="Choose browser: chrome or firefox")

@pytest.fixture(scope="function")
def browser(request):
    # В переменную user_language передается параметр из командной строки
    user_language = request.config.getoption("language")
    browser_name = request.config.getoption("browser_name")# В переменную browser_name передается параметр из командной строки
    # Инициализируются опции браузера
    browser = None
    if browser_name == "chrome":  
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference('intl.accept_languages', user_language)
        browser = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    print(f"\nstart {browser_name} browser for test..")
    yield browser
    print("\nquit browser..")
    browser.quit()
