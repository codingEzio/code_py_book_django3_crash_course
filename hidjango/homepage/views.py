from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['first_name'] = 'Zhang'
        return context

    def say_hi(self):
        return 'Oh hi~'

