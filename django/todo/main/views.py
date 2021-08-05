
 
from django.shortcuts import redirect, render,HttpResponse 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,FormView,UpdateView

 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView  
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name='main/login.html'
    fields='__all__'
    redirect_authenticated_user=True
# ONCE LOGGED IN THE USER WILL BE AUTOMATICALLY BE DIRECTED TO THE HOMEPAGE
    def get_success_url(self):
        return reverse_lazy('tasks')
class RegisterPage(FormView):
    template_name='main/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')


    def form_valid(self, form ) :
        user=form.save()
        if user is not None:{
            login(self.request,user)
        }
        return super(RegisterPage,self).form_valid(form)

        # an authenticated user should not access the register page

    def get(self,*args,**kwargs):
            if self.request.user.is_authenticated:
                return redirect('tasks')
            return super(RegisterPage,self).get(*args,**kwargs)   




    
    
# you have to create a module html template with the suffix of what your class name was and _list i.e by default eg if my class was ProductList  html file woukd be product_form
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'
    #One USER CANNOT SEE THE TASKS FOR ANOTHER USER
    def get_context_data(self, **kwargs ):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(
                title__startswith=search_input
            )
            context['search_input']=search_input
        return context
# it looks for  a html file task_detail       
class TaskDetail(DetailView) :
    model= Task
    context_object_name='task' 
    # if I rename my html -detail name, I have to redirect it
    template_name='main/task.html' 
    # looks for a task_form html file
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description', 'complete'] 
    success_url= reverse_lazy('tasks') 
    # user can only create /add data related to them by use of form valid a built in function from create view

    def form_valid(self, form ) : 
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form) 

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task  
    fields=['title','description', 'complete']  
    success_url= reverse_lazy('tasks')
    # looks for a html file task_confirm_delete
class DeleteView(LoginRequiredMixin,DeleteView):
    model=Task  
    context_object_name='task'
    success_url= reverse_lazy('tasks')


