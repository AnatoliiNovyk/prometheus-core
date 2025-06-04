import pytest
from dash.testing.application_runners import import_app
import time

@pytest.fixture
def app_runner():
    runner = import_app("ui.app")  # ui/app.py
    yield runner
    runner.stop()

def test_ui_layout(app_runner):
    app_runner.start()
    dash_duo = app_runner.find_dash_duo()
    assert "text" in dash_duo.driver.title.lower()

def test_generate_button_exists(app_runner):
    app_runner.start()
    dash_duo = app_runner.find_dash_duo()
    button = dash_duo.find_element("#generate")
    assert button is not None

def test_inputs_exist(app_runner):
    app_runner.start()
    dash_duo = app_runner.find_dash_duo()
    assert dash_duo.find_element("#archetype") is not None
    assert dash_duo.find_element("#topic") is not None

def test_prompt_generation_flow(app_runner):
    app_runner.start()
    dash_duo = app_runner.find_dash_duo()

    # Заполняем поля
    dash_duo.find_element("#archetype").send_keys("trickster")
    dash_duo.find_element("#topic").send_keys("freedom test")
    dash_duo.find_element("#risk").send_keys("high")
    dash_duo.find_element("#memory").send_keys("session log")

    # Нажимаем кнопку
    dash_duo.find_element("#generate").click()

    # Ожидаем появления результата
    time.sleep(2)  # можно заменить на ожидание по элементу

    # Проверяем что появился текст в output
    output_value = dash_duo.find_element("#output").get_attribute("value")
    assert output_value is not None
    assert len(output_value) > 10  # или любой разумный порог

    print(f"Generated prompt: {output_value}")
