from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Votre compte a été créé avec succès! Vous êtes maintenant connecté.')
            return redirect('blog-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return render(request, 'blog/logout_success.html')
    return render(request, 'blog/logout.html')

def home(request):
    context = {
        'posts': Post.objects.all().order_by('-date_posted'),
        'categories': Category.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(user=self.request.user)
        context['comments'] = self.object.comments.all().order_by('-date_posted')
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.views += 1
        self.object.save()
        return response

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Votre article a été créé!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Votre article a été mis à jour!')
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Votre article a été supprimé!')
        return super().delete(request, *args, **kwargs)

class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            messages.success(request, 'Votre commentaire a été ajouté!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm(user=request.user)
    
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})
