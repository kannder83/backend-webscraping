import time
import json
import random
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


from config.database import db_client

URL: str = "https://procesosjudiciales.funcionjudicial.gob.ec/expel-busqueda-inteligente"
list_of_data: list = ["0968599020001"]


def init_log():
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - %(message)s')


def data_submission(driver: webdriver, data: str):
    """
    """
    input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[formcontrolname="cedulaActor"]'))
    )

    # Envia los datos
    input_element.send_keys(data)

    # Busca que el boton para realizar la busqueda
    button_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button.boton-buscar'))
    )
    ActionChains(driver).move_to_element(button_element).click().perform()


def quantity_of_records(driver: webdriver):
    """
    """
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
    # Espera que se cargue el elemento div con la clase "mat-mdc-paginator-range-label"
    wait = WebDriverWait(driver, 10)
    div_element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.mat-mdc-paginator-range-label')))

    # Obtener el texto del elemento
    texto = div_element.text

    # Extraer la cantidad de páginas
    cantidad_paginas = texto.split()[-1]

    return int(cantidad_paginas)


def detail_info_process(driver: webdriver):
    """
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    diccionario = {}
    try:
        time.sleep(1)

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
    elementos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "causa-individual")))
    ventana_principal = driver.current_window_handle

    for elemento in tqdm(elementos):
        acciones = ActionChains(driver)
        enlace_detalle = elemento.find_element(By.TAG_NAME, "a")
        acciones.move_to_element(enlace_detalle).key_down(
            Keys.COMMAND).click(enlace_detalle).perform()

        time.sleep(1)
        ventanas = driver.window_handles
        time.sleep(1)
        driver.switch_to.window(ventanas[-1])
        time.sleep(1)
        get_detail_info = detail_info_process(driver)

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

        # Esperar a que se cargue la información de la lista
        all_data.append(obtain_data_causa(driver))

        # Esperar a que el botón esté presente y sea clicleable
        wait = WebDriverWait(driver, 10)
        boton = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button.mat-mdc-paginator-navigation-next')))

        # Hacer clic en el botón
        boton.click()

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
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # Intentos y contador
    max_retries = 3
    retries = 0
    wait_time = 5  # Tiempo de espera entre reintentos

    while retries < max_retries:
        user_agent = random.choice(user_agents)
        try:
            chrome_options = Options()
            chrome_options.add_argument(f'user-agent={user_agent}')
            chrome_options.add_argument("--disable-application-cache")
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=chrome_options)

            driver.implicitly_wait(wait_time)

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

            logging.info(f"Conexion a la base de datos...")
            collection = db_client.judicatura
            collection.insert_one(save_document)
            logging.info(f"Se almacena información correctamente.")

            with open("archivo.txt", 'w') as f:
                json.dump(save_document, f)

            driver.implicitly_wait(1)
            driver.close()
            logging.info(f"Finaliza el proceso.")
            break

        except Exception as error:
            logging.error(f" {error}")
            retries += 1
            logging.error(f'Reintentando... Intento #{retries}')
            time.sleep(wait_time)
            if retries == 3:
                logging.error('Maximo de intentos configurados.')


def start_webscraping():
    advance_search()


def main():
    logging.info(f"starting!")
    start_webscraping()


if __name__ == "__main__":
    init_log()
    main()
