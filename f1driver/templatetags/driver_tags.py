from django import template
from f1driver.models import Category, Driver

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('driver/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('driver/list_menu.html')
def show_menu():
    menu = [{'title': 'О сайте', 'url_name': 'driver:about'},
            {'title': "Добавить статью", 'url_name': 'driver:add_page'},
            {'title': "Обратная связь", 'url_name': 'driver:contact'},
            {'title': "Войти", 'url_name': 'driver:login'}]
    return {'menu': menu}
