from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Complaint, Like, Comment
from .forms import ComplaintForm
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import HttpResponse

def community_feed(request):
   
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/index.html', {'complaints': complaints})





@login_required
def report_view(request):
    """Form to add new complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('complaints:home')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/report.html', {'form': form})


@login_required
def like_post(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    like, created = Like.objects.get_or_create(user=request.user, complaint=complaint)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    
    complaint.refresh_from_db()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': complaint.total_likes,  # now reflects updated count
        })

    return redirect('complaints:home')

@login_required
def add_comment(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        if text:
            Comment.objects.create(user=request.user, complaint=complaint, text=text)
    return redirect('complaints:home')


def detail_view(request, id):
    """Show full complaint details with comments"""
    complaint = get_object_or_404(Complaint, id=id)
    comments = complaint.comments.all()
    return render(request, 'complaints/detail.html', {
        'complaint': complaint,
        'comments': comments
    })


@login_required
def my_complaints(request):
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/my_complaints.html', {'complaints': user_complaints})

@staff_member_required
def admin_dashboard(request):
    if request.method == "POST":
        for complaint in Complaint.objects.all():
            status_key = f"status_{complaint.id}"
            dept_key = f"department_{complaint.id}"
            if status_key in request.POST and dept_key in request.POST:
                complaint.status = request.POST[status_key]
                complaint.assigned_department = request.POST[dept_key]
                complaint.save()
        messages.success(request, "Complaints updated successfully!")
        return redirect('complaints:admin_dashboard')

    complaints = Complaint.objects.all().order_by('-created_at')
    total_complaints = complaints.count()
    pending = complaints.filter(status='Pending').count()
    in_progress = complaints.filter(status='In Progress').count()
    resolved = complaints.filter(status='Resolved').count()

    category_data = list(
        complaints.values('category').annotate(count=Count('id')).order_by('-count')
    )
    departments = ['Water', 'Electricity', 'Road', 'Waste', 'Other']

    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'category_data': category_data,
        'departments': departments,
    }
    return render(request, 'complaints/admin_dashboard.html', context)


def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    messages.success(request, "Complaint deleted successfully.")
    return redirect('complaints:admin_dashboard')