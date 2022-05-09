from app.models.currentConfig import Current_config
from app.models.moduleConfig import Module_config
from sqlalchemy import asc, desc


class Paginator():
    @classmethod
    def paginate(cls, collection, t_class, page):
        per_page= Current_config.get_results_per_page()
        orden= Module_config.get_module_config(f"{t_class.__name__}_module")
        direction = desc if orden.order == 'desc' else asc

        return collection.order_by(direction(getattr(t_class, orden.sort_field))).paginate(page,per_page,error_out=False)