from django.shortcuts import render, redirect
from .forms import EditProfileForm

# Create your views here.
def profile_view(request):
    profile = request.user.profile
    return render(request, 'a_users/profile.html', {'profile': profile})


def profile_edit(request):
    form = EditProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    return render(request, 'a_users/profile_edit.html', {'form': form})
