import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def chrome_browser_instance(request):
    """
    Provide a selenium webdriver instance.
    """
    options = Options()
    options.headless = False
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    yield browser
    browser.close()
