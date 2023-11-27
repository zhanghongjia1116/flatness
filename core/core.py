import sys
from collections.abc import Iterable
from importlib import import_module
from time import time

from loguru import logger


def preimport(*moduleNames):
    for moduleName in moduleNames:
        if isinstance(moduleName, str):
            # 如果模块已经导入，记录信息日志
            if moduleName in sys.modules:
                logger.info("[Note]:{} already imported.".format(moduleName))
            else:
                # 记录导入开始时间
                timeStart = time()
                try:
                    # 尝试导入模块
                    import_module(moduleName)
                except ModuleNotFoundError:
                    # 如果模块未找到，记录警告日志
                    logger.warning("import {} ... ".format("'" + moduleName + "'") + " ModuleNotFound.")
                except:
                    # 如果出现其他异常，记录错误日志
                    logger.error("import {} ... ".format("'" + moduleName + "'") + "Unexpected error happened")
                else:
                    # 记录导入成功信息和耗时
                    logger.info("import {} ... ".format("'" + moduleName + "'") + " successfully in {:.2}s.".format(
                        time() - timeStart))
        elif isinstance(moduleName, Iterable):
            # 如果参数是可迭代的，则递归调用 preimport
            preimport(*moduleName)
        else:
            # 如果参数类型不是 str 或可迭代，记录错误日志
            logger.error("import error, moduleName must be str or Iterable.")
