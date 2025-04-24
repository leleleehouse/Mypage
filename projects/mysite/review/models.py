from django.db import models

# Create your models here.
class PaperReview(models.Model):
    title = models.CharField(max_length=255)              # 논문 제목
    link = models.URLField(blank=True, null=True)         # 논문 링크
    content = models.TextField()                          # 마크다운 형식의 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일자

    def __str__(self):
        return self.title
