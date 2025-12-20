
from pyplc.platform import plc,hw
from pyplc.utils.logging import logger
from project import name as project_name,version as project_version

logger.info(f'Запуск проекта {project_name} {project_version}')

if plc: plc.run(instances=(),ctx=globals())
