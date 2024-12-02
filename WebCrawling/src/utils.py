from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def click_button(driver, wait, xpath):
    """주어진 XPath의 버튼을 클릭."""
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ActionChains(driver).click(button).perform()

def scrape_content(wait, common_path, relative_loc):
    """모달에서 콘텐츠를 추출."""
    content_dict = {}
    for key, value in relative_loc.items():
        try:
            if key == 'img':
                content_dict[key] = wait.until(EC.presence_of_element_located((By.XPATH, common_path + value))).get_attribute('src')
            else:
                content_dict[key] = wait.until(EC.presence_of_element_located((By.XPATH, common_path + value))).text
        except Exception as e:
            print(f"Error fetching {key}: {e}")
    return content_dict

def extract_elements(driver, content, common_path, elements_path):
    """
    모델에서 여러값을 가진 콘텐츠를 리스트로 추출
    :param content: dict, 콘텐츠가 담김
    :param elements_path: dict, genre와 stars의 여러 요소가 포함된 XPATH가 담겨있음
    """
    
    for key, xpath_template in elements_path.items():
        elements = []
        i = 1
        while True:
            try:
                # 요소를 찾기 위한 전체 XPATH
                xpath = f"{common_path}{xpath_template.format(i)}"
                element = driver.find_element(By.XPATH, xpath)
                elements.append(element.text)
                i += 1
            except Exception:  # 더이상 요소가 발견되지 않으면 멈춤
                break
        content[key] = elements
    
    return content