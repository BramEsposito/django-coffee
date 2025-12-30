from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_dashboard(request):
    """
    Example admin-only view.
    This view is only accessible to staff members.
    """
    context = {
        'title': 'Coffee Admin Dashboard',
    }
    return render(request, 'coffee_admin/dashboard.html', context)
