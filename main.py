import logging
import uvicorn
from subprocess import run
from config.conf import settings


def main():
    """
    """
    try:
        if settings.debug:
            uvicorn.run(
                "config.app:application",
                host="0.0.0.0",
                port=8000,
                reload=True,
            )
        else:
            run(f"gunicorn config.app:application -w 4 -b 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker".split(' '))

    except KeyboardInterrupt:
        logging.warning("Se cierra aplicación.")
        exit()

    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main()
