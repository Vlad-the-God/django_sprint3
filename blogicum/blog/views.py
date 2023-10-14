from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category
from .constants import POSTS_LIMIT


def get_post_qs():
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lt=timezone.now(),
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    post_list = get_post_qs()[:POSTS_LIMIT]
    return render(request, template, {'post_list': post_list})


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.select_related(
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_post_qs(),
        pk=post_id
    )
    return render(request, template, {'post': post})
