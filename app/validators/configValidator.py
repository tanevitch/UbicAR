from app.models.palette import Palette


class ConfigValidator():

    @classmethod
    def check_page_config(cls, args):
        input_p= args.get("paginas")
        if not input_p:
            return "El número de páginas es requerido"
        
        try: 
            input_p = int(input_p)
        except ValueError:
            return "El número de páginas debe ser un valor numérico"

        if input_p <= 0:
            return "El número de páginas debe ser un valor mayor a 0"

        if input_p > 100:
            return "El número debe ser menor o igual a 100"

    @classmethod
    def check_module_config(cls, fields_list, selected_sort_field, selected_order):
        return selected_sort_field in fields_list and selected_order in ["asc", "desc"]
    
    @classmethod
    def check_palette_config(cls, selected_color):
        return Palette.find_by_name(selected_color)