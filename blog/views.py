from django.shortcuts import redirect, render
from blog.models import Post, Category, Comment
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator


def blogList(request):
    blog_count = Post.objects.filter(status="published")
    blog = Post.objects.filter(status="published").order_by("-id")
    featured_blog = Post.objects.filter(featured=True, status="published").order_by("-id")[:6]
    categories = Category.objects.filter(active=True)

    query = request.GET.get("q")
    if query:
        blog = blog.filter(
            Q(title__icontains=query)).distinct()

    paginator = Paginator(blog, 15)
    page_number = request.GET.get('page')
    blog = paginator.get_page(page_number)
    
    

    context = {
        "query": query,
        "categories": categories,
        "blog_count": blog_count,
        "blog": blog,
        "featured_blog": featured_blog,
    }
    return render(request, 'blog/post-lists.html', context)

def blogDetail(request, pid):
    post = Post.objects.get(status="published", pid=pid)
    comment = Comment.objects.filter(post=post, active=True)
    blogs = Post.objects.filter(status="published").order_by("-id")[:10]
    related_blogs = Post.objects.filter(category=post.category).order_by("-id")[:12]

    post.views += 1
    post.save()


    if request.method == "POST":
        full_name = request.POST.get("full_name")
        comment = request.POST.get("comment")
        email = request.POST.get("email")

        Comment.objects.create(full_name=full_name, email=email ,comment=comment, post=post)
        messages.success(request, f"Hey {full_name}, your comment have been sent for review.")
        return redirect("blog:blog-detail", post.pid)

    context = {
        "post": post,
        "comment": comment,
        "blogs": blogs,
        "related_blogs":related_blogs
    }
    return render(request, 'blog/post-detail.html', context)


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    blog_count = Post.objects.filter(category=category, status="published")
    blog = Post.objects.filter(category=category, status="published")
    categories = Category.objects.filter(active=True)
    
    query = request.GET.get("q")
    if query:
        blog = blog.filter(
            Q(title__icontains=query)).distinct()

    paginator = Paginator(blog, 15)
    page_number = request.GET.get('page')
    blog = paginator.get_page(page_number)
    
    

    context = {
        "blog_count": blog_count,
        "query": query,
        "blog": blog,
        "category": category,
        "categories": categories,
    }
    return render(request, 'blog/category-detail.html', context)
