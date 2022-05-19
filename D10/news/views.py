from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import datetime
from .models import *
from .forms import PostForm
from .filters import PostFilter
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives # send_mail
from NewsPaper.settings import ALLOWED_HOSTS
from NewsPaper.tasks import mail_new_post

class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.all().count()
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        pk = str(self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=pk)
        return context

    def post(self, request, *args, **kwargs):
        return redirect('/news/')

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    template_name = 'post/post_create.html'
    model = Post
    form_class = PostForm
    success_url = '/news/'



    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            post = Post.objects.latest('pk')


            mail_new_post.delay(post.id)

            return redirect('/news/')


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    template_name = 'post/post_create.html'
    model = Post
    form_class = PostForm
    success_url = '/news/'

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    template_name = 'post/post.html'
    model = Post
    form_class = PostForm
    success_url = '/news/'

class PostSearchView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/posts_search.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['post_count'] = Post.objects.all().count()
        order_by = self.request.GET.get('order_by', '-id')
        PP = self.get_queryset().order_by(order_by)
        context['filter'] = PostFilter(self.request.GET, queryset=PP)
        return context

class CatSubView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'post/subscribe.html'
    context_object_name = 'cats'
    queryset = Category.objects.order_by('id')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:

            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['cats_count'] = Category.objects.all().count()
        context['time_now'] = datetime.utcnow()
        user_cats = []
        for subs in Subscribe.objects.filter(user_id=request.user.id):
            user_cats.append(subs.category_id)
        context['user_cats'] = user_cats
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_cats = []
        for subs in Subscribe.objects.filter(user_id=request.user.id):
            user_cats.append(subs.category_id)

        for cat in Category.objects.all():

            if (not (cat.id in user_cats)) and (request.POST.get(str(cat.id)) is not None):

                subscribe = Subscribe(
                    user_id=request.user.id,
                    category_id=cat.id
                )
                subscribe.save()

            if ((cat.id in user_cats)) and (request.POST.get(str(cat.id)) is None):

                Subscribe.objects.filter(user_id=request.user.id, category_id=cat.id).delete()
        return redirect('/news/')
