from django.contrib import messages
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.stories.models import Story
from apps.stories.forms import StoryForm


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Setting the form in context
        form = StoryForm(self.request.POST or None)
        context['form'] = form
        context.update(csrf(self.request))

        # Setting the stories in context by page
        stories = Story.objects.all().order_by('-created')
        paginator = Paginator(stories, 10)
        page = self.request.GET.get('page')
        try:
            stories = paginator.page(page)
        except PageNotAnInteger:
            stories = paginator.page(1)
        except EmptyPage:
            stories = paginator.page(paginator.num_pages)
        context['stories'] = stories
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if form.is_valid():
            form.save()
            messages.success(request, 'Your story has been posted')
        else:
            messages.error(request, 'Sorry, something went wrong with your story submission. Email kevin@imkevinxu.com for help')

        return redirect('core:home')

home = HomeView.as_view()


class StoryView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(StoryView, self).get_context_data(**kwargs)

        # Setting the form in context
        form = StoryForm(self.request.POST or None)
        context['form'] = form
        context.update(csrf(self.request))

        # Setting the story in context or redirect
        uuid = self.kwargs.get('uuid')
        try:
            story = Story.objects.get(uuid=uuid)
            context['stories'] = [story]
        except ObjectDoesNotExist:
            messages.error(self.request, 'Sorry, couldn\'t find a story with that ID')
            return redirect('core:home')
        return context

story = StoryView.as_view()
