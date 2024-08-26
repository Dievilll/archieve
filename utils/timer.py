from instance.database import timer_deletion
from utils.logger_api import scheduler, py_logger
from fastapi.responses import ORJSONResponse
timers = 0

def set_timer_api(timer:int):
    global timers
    if timer >= 0 and timer <= 3:
        timers = timer
        py_logger.info(f"|||API --> Установлен новый таймер: {timer}\n0 - 1 день, 1 - 7 дней, 2 - 14 дней, 3 - 30 дней")
        try:
            scheduler.pause()
            scheduler.remove_all_jobs()
            scheduler.add_job(timer_deletion, 'interval', args = [timer], hours=1)
            scheduler.resume()
            return True
        except:
            scheduler.add_job(timer_deletion, 'interval', args = [timer], hours=1)
            scheduler.start()
            return True
        
    else:
        py_logger.error('|||API --> Значение таймера неверно. Возможные значения: 0, 1, 2, 3')
        return False
        
def get_timer_api():
    global timers
    return timers
