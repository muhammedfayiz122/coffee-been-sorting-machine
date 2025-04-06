import logging

# Configure logging
logging.basicConfig(
    filename='coffee_beans_classification.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger
logger = logging.getLogger('coffee_beans_classification')

# Example usage
if __name__ == "__main__":
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')