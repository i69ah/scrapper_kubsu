from django.views.generic import ListView, DetailView
from articles.models import Article


class ArticleListView(ListView):
    queryset = Article.objects.all()
    template_name = 'article_list.html'
    paginate_by = 10


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
