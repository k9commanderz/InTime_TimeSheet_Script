from datetime import datetime, timedelta
from selenium import webdriver
from account import User
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

today = datetime.now().date()
mondaysDate = today - timedelta(days=today.weekday())
mondaysDate = mondaysDate.strftime("%d/%m/%Y")

options = Options()
options.add_argument('--headless')


class FireFox(webdriver.Firefox):
    inTimeUrl = "https://bureau3.es.rsmuk.com/timesheetEntry/webEntry"

    def __init__(self):
        super().__init__(options=options)
        self.user = User()
        self.username = None
        self.password = None
        self.loginSuccess = False
        self.date = mondaysDate
        self.get(self.inTimeUrl)
        self.testLogin()


    def testLogin(self):
        while not self.loginSuccess:
            self.user.requestCredential()
            self.username = self.user.username
            self.password = self.user.password
            self.login()

    def login(self):
        usernameFrom = self.find_element_by_css_selector("#j_username")
        usernameFrom.send_keys(self.username)
        passwordForm = self.find_element_by_css_selector("#j_password")
        passwordForm.send_keys(self.password)
        submit = self.find_element_by_css_selector("#login-submit").click()

        try:
            # looks for the incorrect username and password
            self.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/div[1]/p")
            print("Username or Password is Incorrect")
            return False

        except NoSuchElementException:
            self.loginSuccess = True
            print("Login Successful")

    def placementSelection(self):
        placementOptions = self.find_element_by_css_selector('select.form-control').click()
        placementSelect = self.find_element_by_css_selector('select.form-control > option:nth-child(2)').click()

    def dateSelection(self):
        timeSheetPeriod = self.find_element_by_css_selector('#timesheetDate')
        timeSheetPeriod.send_keys(self.date)

    def fillTimeSheet(self):

        try:
            # check if the user has already submitted the time sheet
            self.find_element_by_css_selector(":tbody.slide-right:nth-child(3) > tr:nth-child(1) > td:nth-child(1)")
        except NoSuchElementException:
            print("This Week time sheet has already been submitted")
            self.quit()
            return False

        # waiting for the browser to load the time sheet to fill in , max wait time is 10 seconds
        try:
            firstDay = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "tbody.slide-right:nth-child(3) > tr:nth-child(1) > td:nth-child(9) > input:nth-child(1)"))
            )
        except NoSuchElementException:
            print("Element not found...possible slow internet")
            self.quit()

        for unitCell in range(3, 8):
            unit = f"tbody.slide-right:nth-child({unitCell}) > tr:nth-child(1) > td:nth-child(9) > input:nth-child(1)"
            self.find_element_by_css_selector(unit).send_keys("1")

        saveDraft = self.find_element_by_css_selector('input.btn:nth-child(12)').click()

        # saving the submit button for reference
        submitButton = "#ng-app > div > form > div > div.row > div > div > div.panel-body > div > div > input:nth-child(13)"

        self.find_element_by_css_selector(submitButton).click()

        print(f"Your time sheet is now complete and submitted for the following date {self.date}")

        self.quit()



if __name__ == "__main__":
    webDriver = FireFox()
    webDriver.placementSelection()
    webDriver.dateSelection()
    webDriver.fillTimeSheet()
