from django import template
from news.models import Russian_mat, Comment

register = template.Library()

@register.filter(name='multiply')  # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg):
    # первый аргумент здесь — это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|multiply:arg
    if isinstance(value, str) and isinstance(arg, int):
        # проверяем, что value — это точно строка, а arg — точно число, чтобы не возникло курьёзов
        return str(value) * arg  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
        #  в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку

@register.filter(name='censor')
def censor(value):
    res = value
    if isinstance(value, str):
        xx = list()
        for ww in Russian_mat.objects.all():
            xx.append(ww.word)
        for ss in value.split():
             if ss.lower() in xx:
                 res = value.replace(ss, 'x' * len(ss) )
        return res
    else:
        raise ValueError(f'Нельзя фильтровать {type(value)}')

@register.filter(name='comment_count')
def comment_count(value):
    id = int(value)
    res = Comment.objects.filter(post_id=id).count()
    return res
