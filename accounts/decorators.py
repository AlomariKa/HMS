from django.shortcuts import redirect

def provider_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'healthcareprovider'):
            return redirect('accounts:login')  # Redirect if the user is not a provider
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'administrativestaff'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'patient'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def new_provider_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_type = request.user.userprofile.user_type
        if not hasattr(request.user, 'userprofile') or not user_type == 'provider' or hasattr(request.user.userprofile,'healthcareprovider'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def new_admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_type = request.user.userprofile.user_type
        if not hasattr(request.user, 'userprofile') or not user_type == 'admin' or hasattr(request.user.userprofile,'administrativestaff'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
def new_patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_type = request.user.userprofile.user_type
        if not hasattr(request.user, 'userprofile') or not user_type == 'patient' or hasattr(request.user.userprofile,'patient'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

