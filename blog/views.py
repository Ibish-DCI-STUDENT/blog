from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import logging

logger = logging.getLogger("mydjangologger")

from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]


class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")


class TestView(TemplateView):
    template_name = "test.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["text"] = text
    #     return context

    def render_to_response(self, context, **response_kwargs):
        # this is an example of using data from cookie and from session
        # this method is overriden iot access to the response and add a cookie

        # first part of text sent to the template is got by the cookie
        # second part of number of visits by the session stored variable

        # the cookie data
        visited = self.request.COOKIES.get("visited")
        text = "You have visited this page before"

        # the session data
        visit = self.request.session.get("visit", 0) + 1
        self.request.session["visit"] = visit

        if not visited:
            text = "You have not visited this page before"

        context["text"] = text + f"\n This is actually your visit No: {visit}"

        # render the response
        response = super().render_to_response(context, **response_kwargs)

        # if needed add a cookie
        if not visited:
            response.set_cookie("visited", True)

        return response


class TestView2(TemplateView):
    template_name = "test2.html"

    def get_context_data(self, **kwargs):
        logger.debug("get context data called for test2")
        context = super().get_context_data(**kwargs)
        context["list"] = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        return context
