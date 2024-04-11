from django.shortcuts import redirect

def redirect_view(request):
    return redirect('/chat/')  # Redirects users to /chat/
