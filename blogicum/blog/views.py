from datetime import datetime
from django.shortcuts import render, get_object_or_404


from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        is_published=True,
        pub_date__lt=datetime.now(),
        category__is_published=True
    ).order_by(
        '-pub_date'
    )[:5]
    return render(request, template, {'post_list': post_list})


def category_posts(request, category_slug):
    template = 'blog/category.html'
    post_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        category__slug=category_slug,
        category__is_published=True,
        is_published=True,
        pub_date__lte=datetime.now()
    )
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'location',
            'author',
            'category',
        ).filter(
            pk=post_id,
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True,
        )
    )
    return render(request, template, {'post': post})
