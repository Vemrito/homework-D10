from django.forms import ModelForm
from .models import Post



class PostForm(ModelForm):


    class Meta:
        model = Post
        fields = ['author', 'cats', 'post_type', 'title', 'text']
        labels = {'author': ('Автор'), 'cats': 'Категория', 'title': 'Заголовок', 'text': 'Текст'}
        #exclude = ('author',)
        #help_texts = {'author': ('Автор статьи'), }
        #help_texts = {'author': ('Автор статьи'), }
        #initial = {'author': self.user.username }
