from selenium import webdriver

driver = webdriver.Firefox()

# Установить произвольный размер
driver.set_window_size(500, 500)

# Получить размеры внутренней области
inner_width = driver.execute_script("return window.innerWidth;")
inner_height = driver.execute_script("return window.innerHeight;")

print(f"Inner width: {inner_width}, Inner height: {inner_height}")