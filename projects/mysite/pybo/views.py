# Create your views here.
from .models import Project
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


class IndexView(ListView):
    def get_queryset(self):
        return Project.objects.order_by('-created_at')

class DetailView(DetailView):
    model = Project
    template_name = 'pybo/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk

        context['prev'] = Project.objects.filter(pk__lt=pk).order_by('-pk').first()
        context['next'] = Project.objects.filter(pk__gt=pk).order_by('pk').first()

        # 마크다운 설명
        context['description_html'] = markdown.markdown(
            self.object.description,
            extensions=[
                'fenced_code',
                CodeHiliteExtension(linenums=False),
                'tables',
                'toc',
                'nl2br',
                'sane_lists',
            ]
        )

        # ✅ extra_block 생성 (이 안에서 해야 self.object 사용 가능)
        project = self.object
        project_img_html = ""
        if project.project_img:
            project_img_html = f'<img src="{project.project_img.url}" class="w-full h-auto max-h-[400px] object-cover rounded mb-6">'

        tech_stack_html = ""
        if project.tech_stack_tag.exists():
            tech_stack_html = '<div class="mb-4"><h2 class="text-xl font-semibold mb-2">🛠 기술 스택</h2><div class="flex flex-wrap gap-2">'
            for tag in project.tech_stack_tag.all():
                tech_stack_html += f'<span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs mr-1">{tag.name}</span>'
            tech_stack_html += '</div></div>'

        # ✅ context에 추가
        context['extra_html'] = project_img_html + tech_stack_html

        return context


class ProjectCreateView(CreateView):
    model = Project
    fields = ['title', 'description', 'tech_stack_tag', 'project_img', 'github_url'] # 실제 필드명으로 변경 필요
    template_name = 'pybo/project_form.html'
    success_url = reverse_lazy('pybo:index')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['title', 'description', 'tech_stack_tag', 'project_img', 'github_url']  # 실제 필드명으로 변경 필요
    template_name = 'pybo/project_form.html'
    success_url = reverse_lazy('pybo:index')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'pybo/project_confirm_delete.html'
    success_url = reverse_lazy('pybo:index')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('pybo:auth')
        return super().dispatch(request, *args, **kwargs)
    
def auth_check(request):
    if request.method == 'POST':
        if request.POST.get('password') == settings.ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('pybo:index')
        else:
            return render(request, 'pybo/auth.html', {'error': '비밀번호가 틀렸습니다.'})
    return render(request, 'pybo/auth.html')

def logout_view(request):
    try:
        del request.session['is_admin']
    except KeyError:
        pass  # 세션에 is_admin이 없어도 무시

    return redirect('pybo:auth')
