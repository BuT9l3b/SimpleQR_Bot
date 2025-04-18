from pystyle import Colors, Colorate
import logging


INFO_COLOR = Colors.cyan
SUCCESS_COLOR = Colors.green
WARNING_COLOR = Colors.yellow
ERROR_COLOR = Colors.red

# Enable colored output (works only in the console)
logging._levelToName = {
    logging.CRITICAL: '[!] CRITICAL',
    logging.ERROR: Colorate.Color(ERROR_COLOR, "[-] ERROR"),
    logging.WARNING: Colorate.Color(WARNING_COLOR, "[!] WARNING"),
    logging.INFO: Colorate.Color(SUCCESS_COLOR, "[+] INFO"),
    logging.DEBUG: Colorate.Color(INFO_COLOR, '[#] DEBUG'),
    logging.NOTSET: 'NOTSET',
}

logging.basicConfig(
    # filename="log.log",
    level=logging.INFO,
    format='%(levelname)-15s | %(asctime)s | %(name)-18s | %(lineno)-4d | %(funcName)-10s | %(message)s',
    datefmt='%H:%M:%S',
    filemode="w"
)