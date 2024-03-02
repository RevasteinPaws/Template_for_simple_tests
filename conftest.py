import allure
import pytest
import requests

from pathlib import Path
from config.links import Links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    """
    Запускает тот или иной браузер в зависимости от переданных настроек
    """

    parser.addoption('--browser_name',
                     action='store',
                     default='chrome',
                     help='choose browser: chrome or firefox',
                     choices=('chrome', 'firefox'))

    parser.addoption('--window_size',
                     action='store',
                     default='1920,1080',
                     help='choose browser window size',
                     choices=('3840,2160',
                              '2560,1440', '2048,1152',
                              '1920,1080', '1920,1440', '1920,1200',
                              '1680,1050', '1680,900',
                              '1440,1050', '1440,900',
                              '1280,1024', '1280,960', '1280,800', '1280,768', '1280,720', '1280,600'))

    parser.addoption('--headless',
                     action='store',
                     default='true',
                     help='choose browser headless mode',
                     choices=('true', 'false'))

    parser.addoption('--url',
                     action='store',
                     default=Links.HOST,
                     help='URL to open in the browser')


@pytest.fixture(scope="function")
def driver(request):
    # Получение командных опций, переданных в Pytest
    browser_name = request.config.getoption('--browser_name')
    window_size = request.config.getoption('--window_size')
    headless = request.config.getoption('--headless')
    url = request.config.getoption('--url')

    # Инициализация WebDriver в зависимости от выбранного браузера
    if browser_name == 'chrome':
        print('\nЗапуск браузера Chrome для теста.')
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument(f"--window-size={window_size}")
        options.add_argument("--disable-dev-shm-usage")
        if headless == 'true':
            options.add_argument("-headless")

        # Функции для того, чтобы сделать бота менее заметным для сайтов
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == 'firefox':
        print('\nЗапуск браузера Firefox для теста.')
        options = webdriver.FirefoxOptions()
        options.add_argument(f"--width={window_size.split(',')[0]}")
        options.add_argument(f"--height={window_size.split(',')[1]}")
        if headless == 'true':
            options.add_argument("-headless")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise pytest.UsageError('-- выберите имя браузера и укажите его как параметр')

    driver.implicitly_wait(10)
    driver.get(url)
    yield driver

    if request.session.testsfailed:
        test_folder = Path(__file__).resolve().parent
        screenshot_folder = test_folder / "screenshots"
        screenshot_folder.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_folder / f"{request.node.name}_screenshot.png"
        driver.save_screenshot(str(screenshot_path))

    print('\nЗавершение работы браузера.')
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def setup_test_function(driver):
    response = requests.get(driver.current_url)
    assert response.status_code == 200, f"Failed to ping {driver.current_url}. Status code: {response.status_code}"
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Функция делает скриншот для отчета allure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and (rep.failed or rep.outcome == 'blocked'):
        try:
            if 'driver' in item.fixturenames:
                web_driver = item.funcargs['driver']

                logs = web_driver.get_log('browser')
                allure.attach(str(logs), name='browser_logs', attachment_type=allure.attachment_type.TEXT)

                error_details = f"Test failed: {rep.longreprtext}"
                allure.attach(error_details, name='error_details', attachment_type=allure.attachment_type.TEXT)

                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name='screenshot',
                    attachment_type=allure.attachment_type.PNG
                )

            else:
                print('Не удалось сделать скриншот, не найден активный драйвер')
        except Exception as e:
            print(f'Не удалось сделать скриншот: {e}')
