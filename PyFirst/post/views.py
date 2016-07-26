# from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post
# Create your views here.

def posts_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		#message success
		messages.success(request, "successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context_data = {
		"form": form,
	}
	return render(request,"post_form.html", context_data)

def posts_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	# share_string = quote_plus(instance.content)
	context_data = {
		"title": instance.title,
		"instance": instance,
		# "share_string": share_string,
	}
	return render(request,"post_detail.html", context_data)

def posts_list(request):
	queryset_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
	page_request_var = "xyz"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context_data = {
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
	}
	return render(request, "post_list.html", context_data)

def posts_update(request, id=None):
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		#message success
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context_data = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request,"post_form.html", context_data)


def posts_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "successfully Deleted")
	return redirect("post:list")
