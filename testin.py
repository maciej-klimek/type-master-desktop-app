import logging

# Utworzenie loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Utworzenie handlera do logowania do pliku
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Utworzenie handlera do logowania na konsolę
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
