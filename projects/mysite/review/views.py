from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

from .models import PaperReview

class ReviewListView(ListView):
    model = PaperReview
    template_name = 'review/review_list.html'
    context_object_name = 'review_list'
    ordering = ['-created_at']  # 최신순 정렬

class ReviewDetailView(DetailView):
    model = PaperReview
    template_name = 'review/review_detail.html'
    context_object_name = 'review'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        pk = review.pk
        context['review_html'] = markdown.markdown(
            self.object.content,
            extensions=['fenced_code', CodeHiliteExtension(linenums=False), 'tables']
        )
        # ✅ 이전/다음 리뷰
        context['prev'] = PaperReview.objects.filter(pk__lt=pk).order_by('-pk').first()
        context['next'] = PaperReview.objects.filter(pk__gt=pk).order_by('pk').first()

        return context
    
class ReviewCreateView(CreateView):
    model = PaperReview
    template_name = 'review/review_form.html'
    fields = ['title', 'link', 'content']
    success_url = '/review/'
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)
    
class ReviewUpdateView(UpdateView):
    model = PaperReview
    template_name = 'review/review_form.html'  # 작성이랑 같은 폼 사용
    fields = ['title', 'link', 'content']
    success_url = reverse_lazy('review:index')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)

class ReviewDeleteView(DeleteView):
    model = PaperReview
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review:index')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)