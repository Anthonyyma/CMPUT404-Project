from django.shortcuts import render
from .forms import PostForm

def editPost(request): 
    # create object of form
    form = PostForm()

    if request.method == "POST":
        print(request.POST)
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, "editPost.html", context)

 
# def homepage(request):
# 	if request.method == "POST":
# 		movie_form = MovieForm(request.POST, request.FILES)
# 		if movie_form.is_valid():
# 			movie_form.save()
# 			messages.success(request, ('Your movie was successfully added!'))
# 		else:
# 			messages.error(request, 'Error saving form')
		
		
# 		return redirect("main:homepage")
# 	movie_form = MovieForm()
# 	movies = Post.objects.all()
# 	return render(request=request, template_name="editPost.html", context={'movie_form':movie_form, 'movies':movies})