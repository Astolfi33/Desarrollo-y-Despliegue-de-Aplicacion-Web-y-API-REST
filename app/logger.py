import logging

logger = logging.getLogger("api_equipos")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('api.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)