from django.shortcuts import render


def about(request):
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    template = 'pages/rules.html'
    return render(request, template)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_permission_denied(request, *args, **kwargs):
    return render(request, 'pages/403csrf.html', status=403)


def server_failure(request):
    return render(request, 'pages/500.html', status=500)
