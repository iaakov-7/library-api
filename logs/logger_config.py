import logging

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s",
                    level=logging.INFO,
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])

logger = logging.getLogger()