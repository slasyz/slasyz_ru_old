#from django.core.context_processors import request
from slasyz_ru.settings import TITLE

def default(request):
    return {'TITLE': TITLE}
