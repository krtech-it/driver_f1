from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import Driver, Category
from .utils import DataMixin


class DriverHome(DataMixin, ListView):
    model = Driver
    template_name = 'driver/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', cat_selected=0)
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Driver.objects.filter(is_published=True).select_related('cat')

class DriverCategory(DataMixin, ListView):
    model = Driver
    template_name = 'driver/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=self.kwargs['cat_slug'])
        context = dict(list(context.items()) + list(c_def.items()))
        # context['cat_selected'] = self.kwargs['cat_slug']
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        return context

    def get_queryset(self):
        return Driver.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                     is_published=True)

class ShowPost(DataMixin, DetailView):
    model = Driver
    template_name = 'driver/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat.slug)
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = context['post']
        return context

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'driver/addpage.html'
    success_url = reverse_lazy('driver:home')
    login_url = reverse_lazy('driver:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = 'Добавление статьи'
        return context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'driver/register.html'
    success_url = reverse_lazy('driver:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('driver:home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'driver/login.html'

    # def get_success_url(self):
    #     return reverse_lazy('driver:home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

class AboutView(DataMixin, TemplateView):
    template_name = 'driver/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'driver/contact.html'
    success_url = reverse_lazy('driver:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('driver:home')

def logout_user(request):
    logout(request)
    return redirect('driver:login')
# def index(request):
#     posts = Driver.objects.all()
#     context = {'title': 'Главная страница',
#                'posts': posts,
#                'cat_selected': 0}
#     return render(request, 'driver/index.html', context=context)

# def about(request):
#     contact_list = Driver.objects.all()
#     paginator = Paginator(contact_list, 3)
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'driver/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('driver:home')
#     else:
#         form = AddPostForm()
#     return render(request, 'driver/addpage.html', {'title':'Добавление статьи',
#                                                    'form': form})


def contact(request):
    return HttpResponse('Обратная связь')


# def login(request):
#     return HttpResponse('Авторизация')


# def show_post(request, post_slug):
#     post = get_object_or_404(Driver, slug=post_slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat.slug
#     }
#     return render(request, 'driver/post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_category(request, cat_slug):
#     # posts = Driver.objects.filter(cat_id=cat_id)
#     posts = get_list_or_404(Driver, cat_id=Category.objects.get(slug=cat_slug).id)
#     # if len(posts) == 0:
#     #     raise Http404()
#
#     context = {'posts': posts,
#                'title': f'Главная страница',
#                'cat_selected': cat_slug}
#     return render(request, 'driver/index.html', context=context)