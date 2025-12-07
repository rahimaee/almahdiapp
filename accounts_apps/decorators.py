from functools import wraps
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator


def feature_required(feature_name, redirect_to_view='access_denied'):
    """
    Decorator that checks if the user has a specific feature.
    If not authenticated or unauthorized, redirects to a view name.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            user = request.user
            redirect_url = resolve_url(redirect_to_view)
            
            if not user.is_authenticated:
                return redirect(f"{redirect_url}?reason=unauthenticated")
            if user.is_superuser == False:
                if not hasattr(user, 'has_feature') or not user.has_feature(feature_name):
                    return redirect(f"{redirect_url}?reason=unauthorized&feature={feature_name}")


            
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def class_view_feature_required(feature_name, redirect_to_view='access_denied'):
    """
    Same as feature_required but for class-based views.
    """
    return method_decorator(feature_required(feature_name, redirect_to_view), name='dispatch')
