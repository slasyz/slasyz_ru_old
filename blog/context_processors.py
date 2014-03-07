#from django.core.context_processors import request
from slasyz_ru.settings import BLOG_TITLE

def default(request):
    return {'blog_title': BLOG_TITLE}
