from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains




def click_button(driver, wait, xpath):
    """
    Clicks a button specified by its XPATH.

    :param driver: WebDriver instance used to control the browser
    :param wait: WebDriverWait instance for setting timeout
    :param xpath: XPATH of the button to be clicked
    :return: None
    """
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ActionChains(driver).click(button).perform()




def scrape_modal_content(wait, base_xpath, relative_xpaths):
    """
    Extracts content from a modal dialog.

    :param wait: WebDriverWait instance for setting timeout
    :param base_xpath: Common XPATH shared by all elements
    :param relative_xpaths: Dictionary mapping element names to their relative XPATHs
    :return: Dictionary where keys are element names and values are their extracted content
    """
    extracted_content = {}
    for element_name, relative_xpath in relative_xpaths.items():
        try:
            full_xpath = base_xpath + relative_xpath
            if element_name == 'img':
                # Fetch 'src' attribute for images
                extracted_content[element_name] = wait.until(
                    EC.presence_of_element_located((By.XPATH, full_xpath))
                ).get_attribute('src')
            else:
                # Fetch text content for other elements
                extracted_content[element_name] = wait.until(
                    EC.presence_of_element_located((By.XPATH, full_xpath))
                ).text
        except Exception as e:
            print(f"Error fetching {element_name}: {e}")
    return extracted_content




def scrape_modal_data(driver, base_xpath, relative_xpaths):
    """
    Extracts multiple values from a modal dialog using dynamic XPATHs.

    :param driver: WebDriver instance used to control the browser
    :param base_xpath: Base XPATH shared by all elements
    :param relative_xpaths: Dictionary where keys are element names and values are XPATH templates for each element
    :return: Dictionary where keys are element names and values are lists of extracted contents
    """
    extracted_data = {}

    for element_name, xpath_template in relative_xpaths.items():
        values = []
        index = 1
        while True:
            try:
                # Generate the full XPATH for the current element
                full_xpath = f"{base_xpath}{xpath_template.format(index)}"
                element = driver.find_element(By.XPATH, full_xpath)
                values.append(element.text)
                index += 1

            # Stop when no more elements are found
            except Exception:
                break
        extracted_data[element_name] = values
    
    return extracted_data