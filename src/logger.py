import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    log_format = '[{asctime}] [{levelname:<8}] {name}: {message}'
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, dt_fmt, style='{')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger

