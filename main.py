
import logging
import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

URL: str = "https://procesosjudiciales.funcionjudicial.gob.ec/expel-busqueda-inteligente"
list_of_data: list = ["0968599020001"]


def init_log():
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - %(message)s')


def data_submission(driver: webdriver, data: str):
    """
    """
    time.sleep(0.3)
    #  Busca el input para agregar los datos
    input_element = driver.find_element(
        By.CSS_SELECTOR, 'input[formcontrolname="cedulaActor"]')

    # Envia los datos
    input_element.send_keys(data)

    # Busca que el boton para realizar la busqueda
    time.sleep(0.3)
    button_element = driver.find_element(
        By.CSS_SELECTOR, 'button.boton-buscar')
    ActionChains(driver).move_to_element(button_element).click().perform()
    time.sleep(0.3)


def quantity_of_records(driver: webdriver):
    """
    """
    time.sleep(0.2)
    # Espera que se cargue la página para obtener la cantidad de registros
    wait = WebDriverWait(driver, 10)
    cantidad_element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'section.registros-encontrados p.cantidadMovimiento')))
    cantidad_registros = cantidad_element.text.strip()
    valor = cantidad_registros.split(":")[1].strip()

    return int(valor)


def quantity_of_pages(driver: webdriver):
    """
    """
    time.sleep(0.2)
    # Encontrar el elemento div con la clase "mat-mdc-paginator-range-label"
    div_element = driver.find_element(
        'css selector', '.mat-mdc-paginator-range-label')

    # Obtener el texto del elemento
    texto = div_element.text

    # Extraer la cantidad de páginas
    cantidad_paginas = texto.split()[-1]

    return int(cantidad_paginas)


def detail_info(elemento):
    """
    """
    # Encontrar el enlace dentro del elemento actual
    enlace_detalle = elemento.find_element(By.TAG_NAME, "a")

    # Hacer clic en el enlace
    enlace_detalle.click()
    time.sleep(0.8)


def detail_info_process(html):
    """
    """
    soup = BeautifulSoup(html, 'html.parser')
    diccionario = {}
    try:
        time.sleep(0.5)

        columnas = soup.select('.cabecera div')
        valores = soup.select(
            '.lista-movimiento .lista-movimiento-individual div')

        datos = {}

        for columna, valor in zip(columnas, valores):
            datos[columna.text.strip()] = valor.text.strip()

        diccionario["movimientos"] = datos

        return diccionario
    except Exception as error:
        logging.error(f"ERROR >>>> {error}")


def obtain_by_window(driver: webdriver):
    """
    """
    detalle = []
    elementos = driver.find_elements(By.CLASS_NAME, "causa-individual")
    ventana_principal = driver.current_window_handle

    for elemento in elementos:
        acciones = ActionChains(driver)
        enlace_detalle = elemento.find_element(By.TAG_NAME, "a")
        acciones.move_to_element(enlace_detalle).key_down(
            Keys.COMMAND).click(enlace_detalle).perform()

        time.sleep(0.5)
        ventanas = driver.window_handles
        time.sleep(0.5)
        driver.switch_to.window(ventanas[-1])
        time.sleep(0.5)
        get_detail_info = detail_info_process(driver.page_source)

        driver.close()

        driver.switch_to.window(ventana_principal)

        #  Guardar get_detail_info en la base de datos
        detalle.append(get_detail_info)

    return detalle


def next_page(driver: webdriver, quantity_of_pages: int):
    """
    """
    all_data = []
    for page_number in range(1, quantity_of_pages):
        logging.info(f"Página >>> {page_number} / {quantity_of_pages}")
        time.sleep(0.5)

        # Obtiene la información de la lista
        all_data.append(obtain_data_causa(driver))

        # Encontrar el botón por clase CSS
        time.sleep(0.5)
        boton = driver.find_element(
            By.CSS_SELECTOR, 'button.mat-mdc-paginator-navigation-next')

        # Hacer clic en el botón
        time.sleep(0.5)
        boton.click()

    time.sleep(0.8)
    logging.info(f"Página >>> {quantity_of_pages} / {quantity_of_pages}")
    all_data.append(obtain_data_causa(driver))

    return all_data


def obtain_data_causa(driver):
    """
    """
    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    elementos_causa = soup.find_all(class_="causa-individual")

    # Crear una lista para almacenar los diccionarios de datos
    datos = []

    # Iterar sobre los elementos de causa y extraer los datos
    for causa in elementos_causa:
        # Crear un diccionario para almacenar los datos de cada causa
        datos_causa = {}

        # Obtener el número
        numero = causa.find(class_="id").get_text(strip=True)
        datos_causa['No.'] = numero

        # Obtener la fecha
        fecha = causa.find(class_="fecha").get_text(strip=True)
        datos_causa['Fecha de ingreso'] = fecha

        # Obtener el número de proceso
        numero_proceso = causa.find(
            class_="numero-proceso").get_text(strip=True)
        datos_causa['No. proceso'] = numero_proceso

        # Obtener la acción/infracción
        accion_infraccion = causa.find(
            class_="accion-infraccion").get_text(strip=True)
        datos_causa['Acción/Infracción'] = accion_infraccion

        # Agregar el diccionario de datos a la lista
        datos.append(datos_causa)

    # Incluir la información de detalle por cada causa
    get_detalle = obtain_by_window(driver)

    if len(datos) >= len(get_detalle):
        for i in range(len(get_detalle)):
            datos[i]["detalle"] = get_detalle[i]

    # logging.info(f"final obtain_data >>> {datos}")
    return datos


def advance_search():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(
            "https://procesosjudiciales.funcionjudicial.gob.ec/expel-busqueda-avanzada")

        # Se envia la inforamción
        data_submission(driver, list_of_data[0])

        # Se obtiene la cantidad de registros
        records = quantity_of_records(driver)
        logging.info(f"Cantidad de registros: {records}")

        # Se obtiene la cantidad de páginas
        pages = quantity_of_pages(driver)
        logging.info(f"Cantidad de páginas: {pages}")

        # En cada página se obtienen los datos requeridos
        scrapy_data = next_page(driver, pages)

        save_document = {
            "actor/ofendido": list_of_data[0],
            "procesos": scrapy_data
        }

        with open("archivo.txt", 'w') as f:
            json.dump(save_document, f)

        time.sleep(0.5)
        driver.close()
        logging.info(f"Finaliza el proceso.")

    except Exception as error:
        logging.error(f" {error}")


def start_webscraping():
    advance_search()


def main():
    logging.info(f"starting!")
    start_webscraping()


if __name__ == "__main__":
    init_log()
    main()
