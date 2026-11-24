from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# same subfolder se forms.py se ComplaintForm class import kar rhe hai
from .forms import ComplaintForm


from .models import Complaint

# Create your views here.

def home(response) :
    return render(response, 'home.html')

# function banaya hai parameter client request hai
def create_complaint(request):

    # agar request ka method POST hai (mtlb create karna hai kuch)
    if request.method == "POST" :

        # toh form object banado using ComplaintForm class
        form = ComplaintForm(request.POST) 

        # check karo jo form banaya hai wo valid hai, saari fields sahi hai if yes toh save karlo
        if form.is_valid() :
            # form.save() works here because we are using ModelForm, not an ordinary Form
            form.save()
            # aur batado ki submit hogya hai
            return redirect("complaint_list")

    # if request ka method POST nhi hai toh
    else :
        # blank form create karo aur wahi return kardo
        form = ComplaintForm

        # Renders an HTML template with context
        return render(request,'complaints/complaint_form.html', {'form' : form})


def complaint_list(request) :
    complaints = Complaint.objects.all()

    return render(request, 'complaints/complaint_list.html', { 'complaints' : complaints})

def complaint_details(request, pk) :
    complaint = get_object_or_404(Complaint, pk=pk)

    return render(request, 'complaints/complaint_details.html', {'complaint':complaint})


