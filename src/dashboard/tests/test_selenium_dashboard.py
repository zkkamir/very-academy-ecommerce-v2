import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# @pytest.mark.selenium
# def test_create_new_admin_user(create_admin_user):
#     assert create_admin_user.__str__() == "admin"


@pytest.mark.selenium
def test_dashboard_admin_login(
    chrome_browser_instance, db_fixture_setup, live_server
):
    """Test if the user can log in using the admin page."""
    browser = chrome_browser_instance

    browser.get(f"{live_server.url}/admin/login/")

    user_name = browser.find_element(By.NAME, "username")
    passsword = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')

    user_name.send_keys("admin")
    passsword.send_keys("admin123")
    submit.send_keys(Keys.RETURN)

    assert "Django administration" in browser.page_source
