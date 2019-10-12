# Automated Tester for Guerrilla Mail Website

An automated test script using Python and Selenium Webdriver to check the emailing capabilities of the Guerrilla Mail website (composing, sending, and deleting an email). This script is designed to be modular in order to properly assess every part of the test.

## Getting Started

### Prerequisites

Python 3 needs to be installed on the host machine. It can be downloaded from [here](https://www.python.org/).

### Installation

Once Python is installed, use the package manager [pip](https://pip.pypa.io/en/stable/) to install selenium webdriver. Run the following command in an open terminal.

```bash
pip install selenium
```

## Included Files

* **gm_test_runner.py** - Main test code and various test cases.
* **test_logger.py** - Custom test logger helper module that is used by gm_test_runner.py.
* **gm_test_runner.txt** - Man page for how to run the main script.

## Usage

 In an open terminal, navigate to the project folder containing all the included files. Once inside the directory, run this command to start the automated test of the website:

```bash
python gm_test_runner.py
```

## Test Examples

The script is designed to be able to test various aspects of the test process. Here are some examples of the code that show how to run different test cases:

```python
# Create instance of tester module
tester = GuerrillaMailAutomatedTester()

# Run test using default values
tester.run_tests()

# Can also specify a test name to differentiate between test cases in the output
tester.run_tests(test_run_name="Test #2")

# Can change some of the default test variables' values
test_vars = {
    'site_name': "https://www.guerrillamail.com/",
    "web_driver": Firefox(),
    'email_subject': "Email Subject",
    'email_body': "Email body.",
    'wait_for_email_time': 30,
}
tester.run_tests(test_variables=test_vars, test_run_name="Test #3")
```

**Note:**
* The values shown in the 'test_vars' dictionary above are the actual default values of the script. Note that Firefox is the default browser and must be installed. If not, the test case needs to use another browser on the host machine. To be able to use different browsers (e.g. Chrome) for the test, the associated browser drivers need to installed properly on the host machine.

* Test case runs can be run multiple times directly after one another without any conflict. To test different aspects, simply alter the values of the 'test_vars' dictionary and pass that changed version to the next call of the 'run_tests()' method.

## Future Improvements

* Be able to handle multi-line email body verification. The suggested steps to solve this problem can be found in the code (see 'gm_test_runner.py' file, 'test_verify_email()' method).

* When waiting for the self-sent email to appear in the inbox, use Selenium 'WebDriverWait' functionality to minimize wait time, instead of having a set timeout period.

* Test multiple test cases at once by implementing a multi-threaded architecture. Waiting for the email to appear in the inbox is the performance bottleneck of this automated test. It slows down the process tremendously when executing a lot of test cases sequentially.

* Perform more comprehensive tests (e.g. inputting very long email subjects or bodies).

## Author

* **Shawn Bhagat**