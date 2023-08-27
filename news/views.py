from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache


class PostsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news.html'
    context_object_name = 'news'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post

    template_name = 'post.html'

    context_object_name = 'post'
    
    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно

      obj = cache.get(f'post-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

      #если объекта нет в кэше, то получаем его и записываем в кэш

      if not obj:
         obj = super().get_object(queryset=self.queryset)
         cache.set(f'post-{self.kwargs["pk"]}', obj)

      return obj

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-time_create'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'news' in self.request.path:
            cur_type = 'NW'
        elif 'articles' in self.request.path:
            cur_type = 'AR'
        self.object.post_type = cur_type
        return super().form_valid(form)
    

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'

@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(id=int(request.GET['category-id']))
    category.subscribers.add(user)
    return redirect('/categories/')


@login_required
def unsubscribe(request):
    user = request.user
    category = Category.objects.get(id=int(request.GET['category-id']))
    category.subscribers.remove(user)
    return redirect('/categories/')