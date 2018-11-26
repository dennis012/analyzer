from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from .models import Post, Comment
from users.models import Profile
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#model imports
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.externals import joblib
# from sklearn.feature_extraction.text import CountVectorizer
#from .customized_dataset_using_naivebayes import *

# Create your views here.
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):#enable a user to view questions by a single person
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.kwargs['pk'])
        comment = Comment.objects.filter(post=self.kwargs['pk'])
        context['comment'] = comment
        return context

    # def get(request):
    #     return render(request, "post_form.html", {})

class CourseListView(ListView):
    model = User
    template_name = 'blog/course_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['content']
    success_url = '/'

    def form_valid(self,form):

        form.instance.author = self.request.user
        # print(form.data)
        #title = form.data["title"]
        content = form.data["content"]
        #result(title, content)
        data_dict = result(content)
        form.instance.title = data_dict[-1:][0]['category']

        print("## {}".format(super().form_valid(form)))
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
        model = Post
        fields = ['title','content']

        def form_valid(self,form):
            form.instance.author = self.request.user
            return super().form_valid(form)
        def test_func(self):#ensuring that the current user is the author of the post hence can update the post.
                post = self.get_object()
                if self.request.user == post.author:
                    return True
                return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):#ensuring that the current user is the author of the post hence can update the post.
            post = self.get_object()
            if self.request.user == post.author:
                return True
            return False
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            print(comment)
            return HttpResponseRedirect(reverse('post-detail', args=[pk]))

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def about(request):
    return render(request,'blog/about.html',{'title':'About'})

def result(content):
    # print(title)
    # print(content)
    display = []

    if content==content:
        ps = PorterStemmer()
        vj = joblib.load('/home/dennoh/Desktop/Natural_Language_Processing/test.pkl')
        mj = joblib.load('/home/dennoh/Desktop/Natural_Language_Processing/model_joblib.pkl')

        for u_content in content:
            # print("yes")
            u_content=[content]
            count_content = vj.transform(u_content)

            category = mj.predict(count_content)
            if category == 0:
                category = "Data Structures"
            else:
                category = "Object Oriented Programming"

            temp = {
                "question":content,
                "category":category
            }
            display.append(temp)

        print(display)
        # return render( content, 'blog/home.html',)
    # keywords = title + " " + content
    # print (keywords)

    return display
