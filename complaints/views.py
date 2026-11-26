from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# same subfolder se forms.py se ComplaintForm class import kar rhe hai
from .forms import ComplaintForm

from django.views.decorators.csrf import csrf_exempt
from .models import Complaint


# STATUS = ['OPEN','CLOSED','IN_PROGRESS','RESOLVED']
# TRANSITIONS_ALLOWED = {
#     'OPEN' : ['IN_PROGRESS'],
#     'IN_PROGRESS' : ['RESOLVED'],
#     'RESOLVED' : ['IN_PROGRESS','CLOSED'],
#     'CLOSED' : []
# }
# Create your views here.

def home(response) :
    return render(response, 'home.html')

# function banaya hai parameter client request hai
@csrf_exempt
def create_complaint(request):

    # agar request ka method POST hai (mtlb create karna hai kuch)
    if request.method == "POST" :

        # toh form object banado using ComplaintForm class
        form = ComplaintForm(request.POST) 

        # check karo jo form banaya hai wo valid hai, saari fields sahi hai if yes toh save karlo
        if form.is_valid():
            # form.save() works here because we are using ModelForm, not an ordinary Form
            form.save()
            # aur batado ki submit hogya hai
            return redirect("complaint_list")

    # if request ka method POST nhi hai toh
    else:
        # blank form create karo aur wahi return kardo
        form = ComplaintForm()

        # Renders an HTML template with context
        return render(request,"complaints/complaint_form.html", {"form" : form})

# ab yaha humne function banaya hai jisse hum saari complaints dekh rhe hai 
def complaint_list(request) :
    # this will return all complaints and assign it to complaint variable
    complaints = Complaint.objects.all()

    # here , we are rendering to the complaint_list.html (aur render() ke 3 parameter hote hai)
    return render(request, 'complaints/complaint_list.html', { 'complaints' : complaints})

# yaha hum ek record ko fetch kar rhe hai request GET hai pk is path parameter 
# konsi complaint chahiye wo pk se milegi
def complaint_details(request, pk) :
    # Complaint.objects.get(pk=pk) bhi use kar skte the kyun nhi kiya iska reason hai 
    # isiliye nhi kiya kyunki it will return ComplainNotFound if no record is found that will give 500 (internal server error)
    # so we use get_object_or_404(Model, pk=pk) , if record not found it will return 404 Not Found status code
    # also error aaya tha ek kyunki parameter galat daal diya tha mene get_object_or_404() ka
    complaint = get_object_or_404(Complaint, pk=pk)

    # simply rendering the templates jaha details dekh sakte hai specific complaint ki
    return render(request, 'complaints/complaint_details.html', {'complaint':complaint})


