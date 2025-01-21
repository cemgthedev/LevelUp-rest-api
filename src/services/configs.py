import logging
import logging.config
import yaml
from utils.generate_logs import generate_logs

# Inicializando arquivos de logs
generate_logs();

# Carregar configuração do arquivo YAML
with open('./services/configs.logs.yaml', 'r') as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)

# Criar loggers específicos
users_logger = logging.getLogger("users")
courses_logger = logging.getLogger("courses")
user_courses_logger = logging.getLogger("user_courses")