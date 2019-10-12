"""
Author:     Shawn Bhagat
Date:       7/23/19
Purpose:    An automated test using Selenium Webdriver to check emailing 
            capabilities of the Guerrilla Mail website.
"""

# Import selenium webdriver modules
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import argparse

# Import custom test logging module
import test_logger as tl


class GuerrillaMailAutomatedTester:
    """Class containing all tests for testing the Guerrilla Mail website."""

    class EmailVerificationError(Exception):
        """Custom exception for when an incoming expected email cannot be detected and verified."""
        
        def __init__(self):
            Exception.__init__(self, "Could not find and verify self-sent email within the timeout period.")
    
    def __init__(self):
        """Initialize logging and other needed test variables."""
        self.log = tl.TestLogger()
        
    def set_email_subject(self, subject="Email Subject"):
        """Set email subject value."""
        subject = str(subject)
        subject = subject.strip()
        subject = subject.replace('\n', '').replace('\r', '')
        self.email_subject = subject

    def set_email_body(self, body="Email body."):
        """Set email body value."""
        self.email_body = str(body)

    def run_tests(self, test_variables={}, test_run_name=""):
        """Set up custom test parameters and run all tests."""

        try:
            print(f"\n{'#' * 60}")
            this_test_run_name = test_run_name if test_run_name else "Test"
            print(f"{this_test_run_name}")
            self.log.print_header()
            self.log.print_test_name("Initialization")

            # Dictionary of temp variables persisting through different tests (reset for each run)
            self.persist_vars = {}

            # Set up common test variables and default values (can be changed for different test cases)
            self.site_name = test_variables.get("site_name") if test_variables and test_variables.get("site_name") else "https://www.guerrillamail.com/"
            self.driver = test_variables.get("web_driver") if test_variables and test_variables.get("web_driver") else Firefox()
            self.set_email_subject(test_variables.get("email_subject"))
            self.set_email_body(test_variables.get("email_body"))
            self.wait_for_email_period_in_seconds = test_variables.get("wait_for_email_time") if test_variables and test_variables.get("wait_for_email_time") else 30

            self.log.print_test_result(self.log.RESULT_PASS)

            # Run all tests in proper order
            self.test_go_to_site()
            self.test_get_email_address()
            self.test_go_to_compose_email()
            self.test_set_email_to_field()
            self.test_set_email_subject_field()
            self.test_set_email_body_field()
            self.test_send_email()
            self.test_wait_for_email()
            self.test_verify_email()
            self.test_delete_email()

        # If any errors occur in this test run, stop and print errors 
        except Exception as e:
            self.log.print_test_result(self.log.RESULT_FAIL)
            print("\nErrors:")
            self.log.print_separator(c='=')
            print(e)

        # If all tests pass without any failures
        else:
            print("\nAll tests passed.\n")

        # CLose browser GUI
        finally:
            self.driver.close()

    def test_go_to_site(self):
        """Navigate to specified website."""
        self.log.print_test_name("Go to site")
        self.driver.get(self.site_name)
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_get_email_address(self):
        """Find and store auto-generated email."""
        self.log.print_test_name("Get email address")
        email_address_elem =  self.driver.find_element_by_id("email-widget")
        email_address_text = email_address_elem.text
        self.persist_vars['email_address_text'] = email_address_text
        email_address_domain = email_address_text.split("@", 1)[1]
        self.persist_vars['email_address_domain'] = email_address_domain
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_go_to_compose_email(self):
        """Navigate to compose email portion of website."""
        self.log.print_test_name("Go to compose email")
        compose_email_button = self.driver.find_element_by_id("nav-item-compose")
        compose_email_button.click()
        temp = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "to"))
        )
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_set_email_to_field(self):
        """Set TO field in email composition page."""
        self.log.print_test_name("Set 'To' field")
        compose_email_to_field = self.driver.find_element_by_name("to")
        compose_email_to_field.clear()
        compose_email_to_field.send_keys(self.persist_vars.get("email_address_text"))
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_set_email_subject_field(self):
        """Set SUBJECT field in email composition page."""
        self.log.print_test_name("Set 'Subject' field")
        compose_email_subject_field = self.driver.find_element_by_name("subject")
        compose_email_subject_field.clear()
        compose_email_subject_field.send_keys(self.email_subject)
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_set_email_body_field(self):
        """Set BODY field in email composition page."""
        self.log.print_test_name("Set 'Body' field")
        compose_email_body_field = self.driver.find_element_by_name("body")
        compose_email_body_field.clear()
        compose_email_body_field.send_keys(self.email_body)
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_send_email(self):
        """Click the send email button to send email."""
        self.log.print_test_name("Send email")
        compose_email_send_button = self.driver.find_element_by_id("send-button")
        compose_email_send_button.click()
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_wait_for_email(self):
        """Wait for specified amout of time for self-sent email to appear in inbox."""
        self.log.print_test_name("Wait for email")
        time.sleep(self.wait_for_email_period_in_seconds)
        self.log.print_test_result(self.log.RESULT_PASS)

    def test_verify_email(self):
        """Search through whole inbox until self-sent email is found and verified."""
        self.log.print_test_name("Verify email")

        # Get list of all emails in inbox
        email_list = self.driver.find_elements_by_xpath("//tbody[@id='email_list']/tr[contains(@class, 'mail_row')]")
        for email in email_list:

            # Extract email subject and body from current email
            email_subject_and_body = email.find_element_by_xpath(".//td[@class='td3']")
            email_subject_and_body_text = email_subject_and_body.text
            email_subject_and_body_text = email_subject_and_body_text.strip()

            # Extract only subject and check against expected value
            email_subject_len = len(self.email_subject)
            email_subject = email_subject_and_body_text[:email_subject_len]
            verify_subject = self.email_subject == email_subject

            # Extract only body and check against expected value
            email_subject_and_body_text = email_subject_and_body_text[email_subject_len:]
            email_subject_and_body_text = email_subject_and_body_text.strip()
            email_body_len = len(self.email_body)
            email_body = email_subject_and_body_text[:email_body_len]

            """
            FIXME: Multi-Line Email Body Verification Steps
            0) Find character limit of initial email body that fits in inbox list.
            1) Check first portion of inbox email body with first portion of expected email body.
            2) If (1) fails, move on to next email. If (1) passes, click on that email to open it.
            3) Get full email body element text and write check against expected value.
            4) Go back to inbox and continue rest of verification process.
            """

            verify_body = self.email_body == email_body

            # Extract email sender from current email
            email_sender = email.find_element_by_xpath(".//td[@class='td2']")
            email_sender_text = email_sender.text

            # Check email sender against expected value
            email_sender_text = email_sender_text.split("@", 1)[0] + "@" + self.persist_vars.get("email_address_domain")
            verify_sender = self.persist_vars.get("email_address_text") == email_sender_text
            
            # Verify that all expected email parameters are met, pass if only all true
            if verify_sender and verify_subject and verify_body:
                self.persist_vars["self_sent_email_elem"] = email
                self.log.print_test_result(self.log.RESULT_PASS)
                return
            
        raise self.EmailVerificationError()

    def test_delete_email(self):
        """Select verified email and click delete button to delete it."""
        self.log.print_test_name("Delete email")
        delete_email_checkbox = self.persist_vars.get("self_sent_email_elem").find_element_by_xpath(".//td[@class='td1']")
        delete_email_checkbox.click()
        delete_email_button = self.driver.find_element_by_id("del_button")
        delete_email_button.click()
        self.log.print_test_result(self.log.RESULT_PASS)


# Run main program and different test cases
if __name__ == "__main__":

    # Add command line argument functionality for more extensive debugging capabilities
    cli_parser = argparse.ArgumentParser(
        description="This is an automated test runner for testing the Guerrilla Mail website.", 
        usage="python gm_test_runner.py [-h]")
    cli_args = cli_parser.parse_args()

    try:

        tester = GuerrillaMailAutomatedTester()
        
        # Test case #1: Run with default values [EXPECT PASS]
        tester.run_tests()
        
        # Test case #2: Run with all valid and expected parameters [EXPECT PASS]
        test_2_variables = {
            'site_name': "https://www.guerrillamail.com/",
            "web_driver": Firefox(),
            'email_subject': "This is a test email subject!!!",
            'email_body': "This is a test email body!!!",
            'wait_for_email_time': 25,
        }
        tester.run_tests(test_variables=test_2_variables, test_run_name="Test #2: All Valid Values")

        # Test case #3: Run with invalid site URL [EXPECT FAIL]
        test_3_variables = {
            'site_name': "https://www.guerrrillamail.com/", # added extra 'r' in 'guerrilla'
            "web_driver": Firefox(),
            'email_subject': "This is a test email subject!!!",
            'email_body': "This is a test email body!!",
            'wait_for_email_time': 25,
        }
        tester.run_tests(test_variables=test_3_variables, test_run_name="Test #3: Invalid Site URL")

        # Test case #4: Run with Chrome driver [EXPECT PASS]
        # Note: Need to have Chrome driver executable in PATH to run correctly
        #       If installed properly, uncomment following lines to run test.
        """
        test_4_variables = {
            'site_name': "https://www.guerrillamail.com/",
            "web_driver": Chrome(),
            'email_subject': "This is a test email subject!!!",
            'email_body': "This is a test email body!!!",
            'wait_for_email_time': 25,
        }
        tester.run_tests(test_variables=test_4_variables, test_run_name="Test #4: Using Chrome Driver")
        """

        # Test case #5: Run with email subject with extra/invalid whitespace [EXPECT PASS]
        test_5_variables = {
            'site_name': "https://www.guerrillamail.com/",
            "web_driver": Firefox(),
            'email_subject': "  This is a test\n email subject!!!   ",
            'email_body': "This is a test email body!!!",
            'wait_for_email_time': 25,
        }
        tester.run_tests(test_variables=test_5_variables, test_run_name="Test #5: Email Subject With Extra Whitespace")
        
        # Test case #6: Run with email body with multiple lines [EXPECT PASS]
        # Note: Did not finish writing verification code, so mutli-line verification will FAIL.
        #       See thought process and steps to fix in method definition for "test_verify_email".
        test_6_variables = {
            'site_name': "https://www.guerrillamail.com/",
            "web_driver": Firefox(),
            'email_subject': "This is a test email subject!!!",
            'email_body': "This is a test email body!!!\n\n\nThis is the fourth line!",
            'wait_for_email_time': 25,
        }
        tester.run_tests(test_variables=test_6_variables, test_run_name="Test #6: Multi-Line Email Body")
        
        # Test case #7: Run with short wait time period for email to appear in inbox [EXPECT FAIL]
        test_7_variables = {
            'site_name': "https://www.guerrillamail.com/",
            "web_driver": Firefox(),
            'email_subject': "This is a test email subject!!!",
            'email_body': "This is a test email body!!!",
            'wait_for_email_time': 5,
        }
        tester.run_tests(test_variables=test_7_variables, test_run_name="Test #7: Short Wait For Email Period (5 sec)")
        
    except KeyboardInterrupt:
        print("\n\nExiting program...\n")
        exit(2)