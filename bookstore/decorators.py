def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirect to index page if the user is authenticated
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
