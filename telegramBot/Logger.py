import time
import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

HANDLED_STR = ['Unhandled', 'Handled']

"""
000 - Token is None
001 - Token is not availible
002 - все входящие сообщения
003 - задержка отправления
"""
Errors = {
    ZeroDivisionError: "Деление на 0",
    NameError: "Не найдено имя",
    TypeError: "Ошибка типов",

}


class LogMiddleware(BaseMiddleware):
    def __init__(self, logger=__name__):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger
        self._configured = False
        super(BaseMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get('_start', None)
        if start:
            del obj.conf['_start']
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_update(self, update: types.Update, data: dict):
        update.conf['_start'] = time.time()

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"002 ID:{update.update_id} // timeout:{timeout} ms)")

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"001 text:'{message.text}' // chat:[{message.chat.type}:{message.chat.id}]")

    async def on_pre_process_error(self, update: types.Update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.error(f"003 ID:{update.update_id} // error:{error} // timeout:{timeout}")
            if type(error) in Errors:
                await update.message.reply(f"Возникла ошибка: {Errors[type(error)]}.")
            else:
                await update.message.reply("Возникла неизвестная ошибка, перепроверьте запрос.")

class DefaultLogger:

    @staticmethod
    def set_logger(_format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, filename=u'mylog.log'):
        logging.basicConfig(format=_format, level=level, filename=filename)

    @staticmethod
    def set_level(names, level="CRITICAL"):
        if isinstance(names, list):
            for name in names:
                logging.getLogger(name).setLevel(level)
        else:
            logging.getLogger(names).setLevel(level)