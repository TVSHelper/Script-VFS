from seleniumbase import Driver
import logging
import os

from dotenv import load_dotenv

driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://visa.vfsglobal.com/gbr/en/ita/login", 4)
driver.disconnect()
load_dotenv()
logger = logging.getLogger(__name__)


gmail_email = os.getenv("GMAIL_EMAIL")
gmail_password = os.getenv("GMAIL_PASSWORD")

email_vfs = os.getenv("EMAIL_VFS")
password_vfs = os.getenv("PASSWORD_VFS")

application_centre = os.getenv("APPLICATION_CENTRE")
application_category = os.getenv("APPOINTMENT_CATEGORY")
appointment_sub_category = os.getenv("APPOINTMENT_SUB_CATEGORY")

first_name = os.getenv("FIRST_NAME")
last_name = os.getenv("LAST_NAME")
gender = os.getenv("GENDER")
date_of_birth = os.getenv("DATE_OF_BIRTH")
current_nationality = os.getenv("CURRENT_NATIONALITY")
passport_number = os.getenv("PASSPORT_NUMBER")
passport_expiration_date = os.getenv("PASSPORT_EXPIRATION_DATE")
contact_number = os.getenv("CONTACT_NUMBER")
contact_code = os.getenv("CONTACT_CODE")
email_form = os.getenv("EMAIL_FORM")

input()
# Book Appointment
driver.reconnect()
driver.sleep(20)
driver.click("//button[.//span[text()=' Start New Booking ']]")
driver.sleep(20)
driver.disconnect()

driver.reconnect()
driver.click("//div[.//span[text()='Choose your Application Centre']]")
driver.disconnect()

driver.sleep(20)

driver.reconnect()
if application_centre == "Italy Visa Application Centre Edinburgh":
    driver.click("//mat-option[@id='ITLYEDN']")  # Italy Visa Application Centre Edinburgh
elif application_centre == "Italy Visa Application Centre, London":
    driver.click("//mat-option[@id='ILON']")  # Italy Visa Application Centre, London
elif application_centre == "Italy Visa Application Centre, Manchester":
    driver.click("//mat-option[@id='IMAN']")  # Italy Visa Application Centre, Manchester
else:
    raise Exception("Invalid Application Centre")

driver.click('//mat-form-field[contains(@class, "ng-tns-c75-8")]')
driver.disconnect()

driver.sleep(20)

driver.reconnect()
if application_category == "Italy UK VisaCategory":
    driver.click("//mat-option[@id='UKITVED']")  # Italy UK VisaCategory
elif application_category == "Long Stay Catogery":
    driver.click("//mat-option[@id='UKITLSC']")  # Long Stay Catogery
else:
    raise Exception("Invalid Application Appointment")
driver.disconnect()

# driver.click('//mat-form-field[contains(@class, "ng-tns-c75-6")]')
# driver.sleep(120)
# div class="alert mt-5 mb-20 alert-info border-0 rounded-0 border-left-5-solid form-info alert-info-blue ng-star-inserted"

# Your Details
input("Your Details")
driver.sleep(60)

# Date Of Birth*
driver.type("//input[@id='dateOfBirth']", date_of_birth)  # "20032001" 20/03/2001

# Current Nationality*
driver.click('//mat-form-field[contains(@class, "ng-tns-c75-14")]')
driver.click(f"//span[text()=' {current_nationality} ']")  # ALGERIA

# FORM
driver.type("//input[@placeholder='Enter Given Name/ First Name/ Other Name']", first_name)
driver.type("//input[@placeholder='Enter Last Name/ Surname/ Family Name.']", last_name)


# Gender*
driver.click("mat-select[role='combobox']")
if gender == "Female":
    driver.click("//mat-option[.//span[text()=' Female ']]")
elif gender == "Male":
    driver.click("//mat-option[.//span[text()=' Male ']]")
else:
    driver.click("//mat-option[.//span[text()=' Others / Transgender ']]")


driver.type("//input[@id='mat-input-8']", passport_number)

driver.type("//input[@id='passportExpirtyDate']", passport_expiration_date)

driver.type("//input[@id='mat-input-9']", contact_code)

driver.type("//input[@id='mat-input-10']", contact_number)

driver.type("//input[@id='mat-input-11']", email_form)

driver.click("//button[.//span[text()=' Save ']]")


driver.click("//button[.//span[text()=' Continue ']]")

driver.click("//button[.//span[text()=' Generate OTP ']]")
driver.type("//input[@placeholder='OTP']", "123456")
driver.click("//button[.//span[text()=' Verify ']]")
driver.click("//button[.//span[text()=' Continue ']]")


driver.click("//a[@aria-label='March 20, 2025']")

driver.click("//div[@id='d0']")

driver.click("//button[.//span[text()=' Continue ']]")

driver.save_screenshot("Review and Pay.png")

# Agree
checkbox_ids = ["#mat-mdc-checkbox-1-input", "#mat-mdc-checkbox-2-input"]

for checkbox_id in checkbox_ids:
    driver.wait_for_element_visible(checkbox_id, timeout=10)  # Ensure visibility
    driver.click(checkbox_id)  # Click the checkbox