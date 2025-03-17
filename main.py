import logging
import os

from dotenv import load_dotenv
from seleniumbase import SB

from check_email import check_email

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


# Login and by pass cloudflare
# https://stackoverflow.com/questions/77577929/how-to-handle-cloudflare-turnstile-on-form-recaptcha-with-selenium-seleniumbas
try:
    with SB(uc=True, headed=True, xvfb=True) as sb:
        sb.uc_open_with_reconnect("https://visa.vfsglobal.com/gbr/en/ita/login", reconnect_time=12)
        sb.sleep(30)

        sb.uc_click("#onetrust-reject-all-handler")
        sb.sleep(10)

        sb.click("//*[@id='mat-input-4']")
        sb.sleep(10)

        for ch in list(password_vfs):
            if ch == " ":
                sb.click('//*[@name="{space}"]')

            elif ch in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                sb.click(f'//button[@name="{ch}"]')

            elif ch in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                sb.click_if_visible('//*[@name="{shift}"]')
                sb.click(f'//*[@name="{ch}"]')
                sb.click_if_visible('//*[@name="{shift}"]')

            elif ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                      '9', ")", "@", ";", "-", ":", "/", '"', "$", "(", "&"
                      ".", "?", ",", "'", "!"
            ]:
                sb.click_if_visible('//*[@name="{numeric}"]')
                sb.click(f'//*[@name="{ch}"]')
                sb.click_if_visible('//*[@name="{alphabetic}"]')

            elif ch in ["[", "]", "{", "}", "#", "%", "^", "*", "+", "=", "_"
                      "\"", "|" , "~" , "<" , ">", "€", "¥", "£", "•", ".", ","
                      ,"?", "!", "'"
            ]:
                sb.click_if_visible('//*[@name="{numeric}"]')
                sb.click_if_visible('//*[@name="{symbolic}"]')
                sb.click(f'//*[@name="{ch}"]')
                sb.click_if_visible('//*[@name="{alphabetic}"]')


        sb.type('//*[@id="email"]', email_vfs)
        sb.sleep(10)

        # sb.uc_click(submit_button, reconnect_time=4)
        sb.save_screenshot("screenshot1.png")

        sb.uc_gui_click_captcha()

        sb.save_screenshot("screenshot2.png")

        sb.click('//button[contains(@class, "btn-brand-orange")]')
        # AVOID BOT DETECTION
        sb.disconnect()

        sb.sleep(60)

        sb.reconnect()
        otp = check_email(gmail_email, gmail_password)

        sb.type("//*[@id='mat-input-5']", otp)
        sb.save_screenshot("screenshot3.png")

        sb.uc_gui_click_captcha()

        sb.save_screenshot("screenshot4.png")

        sb.click('//button[contains(@class, "btn-brand-orange")]')

        sb.save_screenshot("screenshot5.png")
        sb.disconnect()

        # Book Appointment
        sb.reconnect()
        sb.click('//button[contains(@class, "btn-brand-orange")]')
        sb.sleep(20)
        sb.disconnect()

        sb.reconnect()
        sb.click('//mat-form-field[contains(@class, "ng-tns-c75-4")]')
        sb.disconnect()

        sb.sleep(20)

        sb.reconnect()
        if application_centre == "Italy Visa Application Centre Edinburgh":
            sb.click("//mat-option[@id='ITLYEDN']")  # Italy Visa Application Centre Edinburgh
        elif application_centre == "Italy Visa Application Centre, London":
            sb.click("//mat-option[@id='ILON']")  # Italy Visa Application Centre, London
        elif application_centre == "Italy Visa Application Centre, Manchester":
            sb.click("//mat-option[@id='IMAN']")  # Italy Visa Application Centre, Manchester
        else:
            raise Exception("Invalid Application Centre")
        sb.click('//mat-form-field[contains(@class, "ng-tns-c75-8")]')
        sb.disconnect()

        sb.sleep(20)

        sb.reconnect()
        if application_category == "Italy UK VisaCategory":
            sb.click("//mat-option[@id='UKITVED']")  # Italy UK VisaCategory
        elif application_category == "Long Stay Catogery":
            sb.click("//mat-option[@id='UKITLSC']")  # Long Stay Catogery
        else:
            raise Exception("Invalid Application Appointment")
        sb.disconnect()

        # driver.click('//mat-form-field[contains(@class, "ng-tns-c75-6")]')
        # driver.sleep(120)
        # div class="alert mt-5 mb-20 alert-info border-0 rounded-0 border-left-5-solid form-info alert-info-blue ng-star-inserted"

        # Your Details
        input("Your Details")
        sb.sleep(60)

        # Date Of Birth*
        sb.type("//input[@id='dateOfBirth']", date_of_birth)  # "20032001" 20/03/2001

        # Current Nationality*
        sb.click('//mat-form-field[contains(@class, "ng-tns-c75-14")]')
        sb.click(f"//span[text()=' {current_nationality} ']")  # ALGERIA

        # FORM
        sb.type("//input[@id='mat-input-6']", first_name)
        sb.type("//input[@id='mat-input-7']", last_name)

        # Gender*
        sb.click('//div[contains(@class, "ng-tns-c75-12")]')
        if gender == "Female":
            sb.click("//mat-option[@id='mat-option-248']")  # Female
        elif gender == "Male":
            sb.click("//mat-option[@id='mat-option-249']")  # Male
        else:
            sb.click("//mat-option[@id='mat-option-250']")  # Others/Trans

        sb.type("//input[@id='mat-input-8']", passport_number)

        sb.type("//input[@id='passportExpirtyDate']", passport_expiration_date)

        sb.type("//input[@id='mat-input-9']", contact_code)

        sb.type("//input[@id='mat-input-10']", contact_number)

        sb.type("//input[@id='mat-input-11']", email_form)


except Exception as e:
    sb.save_screenshot("screenshot_error.png")
    logger.error(f"Error: {e}. Please review the error image.")

