import logging
from app.webscraping.judicatura import Judicatura


def init_log():
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - %(message)s')


def main():
    init_log()
    logging.info(f"starting!")
    scraping_judicatura = Judicatura(values=["0968599020001"])
    scraping_judicatura.search()


if __name__ == "__main__":
    main()
