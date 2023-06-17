from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post

class HomeView(ListView):

    model = Post
    template_name = 'blog/home.html'

    def get(self, request):
        current_user = self.request.user
        queryset = self.model.objects.all()

        context = {
            'posts':queryset, 
            'user':current_user,
            'title':'Home',
        }

        return render(request, self.template_name, context)


class GetMyPostsView(LoginRequiredMixin, ListView):

    login_url = 'user:login'

    model = Post
    template_name = 'blog/my-blogs.html'

    def get(self, request):
        current_user = self.request.user

        # get all posts for the current user
        queryset = self.model.objects.filter(author=current_user)

        context = {
            'myposts':queryset, 
            'title':'My Posts',
        }

        return render(request, self.template_name, context)


class GetPostDetail(LoginRequiredMixin, DetailView):

    login_url = 'user:login'

    model = Post
    template_name = 'blog/blog-detail.html'
    context_object_name = 'post'

    def get(self, request, pk):
        current_user = self.request.user
        post = self.model.objects.get(pk=pk)
        post_author = post.author

        context = {
            'post':post,
            'cam_update_delete':True,
        }

        if current_user == post_author and current_user.is_superuser:
            context['can_update_delete'] = True
        else:
            context['can_update_delete'] = False

        return render(request, self.template_name, context)


class CreatePost(LoginRequiredMixin, CreateView):

    login_url = 'user:login'

    model = Post
    fields = ['title', 'content', 'blog_picture']
    template_name = 'blog/blog-form.html'
    success_url = reverse_lazy('blog:home')
    context_object_name = 'posts'

    def post(self, request):
        # retrieve current user
        current_user = self.request.user
        title = request.POST['title']
        content = request.POST['content']
        blog_picture = request.FILES.get('blog-picture')

        # check if blog_picture exists
        if blog_picture is not None:
            post = self.model.objects.create(title=title, content=content, blog_picture=blog_picture, author=current_user)
        else:
            post = self.model.objects.create(title=title, content=content, author=current_user)

        messages.success(request, 'New Blog Post Created')

        return redirect(self.success_url)
    

class UpdatePost(LoginRequiredMixin, UpdateView):

    login_url = 'user:login'

    model = Post
    fields = ['title', 'content', 'blog_picture']
    template_name = 'blog/update-blog-form.html'
    success_url = reverse_lazy('blog:my-posts')
    context_object_name = 'post'

    def post(self, request, pk):
        current_user = self.request.user
        post_object = self.model.objects.get(pk=pk)

        # Access existing values and update them to user input
        post_object.title = request.POST['title']
        post_object.content = request.POST['content']
        post_object.blog_picture = request.FILES.get('blog-picture')
        
        post_author = post_object.author

        # check if current logged in user is the same as the author of the post
        if current_user == post_author:
            post_object.save()
            
            messages.success(request, 'Blog post updated successfully')
            return redirect(self.success_url)
        else:
            messages.error(request, 'You cannot update a post that is not yours')
            return redirect(self.success_url)


class DeletePost(LoginRequiredMixin, DeleteView):
    
    login_url = 'user:login'

    model = Post
    template_name = 'blog/delete-blog.html'
    success_url = reverse_lazy('blog:my-posts')
    context_object_name = 'post'

    def post(self, request, pk):
        current_user = self.request.user
        post = self.model.objects.get(pk=pk)
        post_author = post.author

        if current_user == post_author:
            post.delete()
            messages.success(request, 'Blog post deleted successfully')
            return redirect(self.success_url)
        else:
            messages.error(request, 'You cannot delete a post that is not yours')
            return redirect(self.success_url)
