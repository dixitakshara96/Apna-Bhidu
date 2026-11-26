from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# .models ka matlab hai: isi accounts app ke models.py se import karo.
from .models import Students

# complaints app ke Complaint model ko use kar rahe hai,
# kyunki student ke complaints database se nikalne hai.
from complaints.models import Complaint

# Forms user ka input validate karke model mein save karne mein help karte hai.
from .forms import StudentsForm, MentorForm


# csrf_exempt ka matlab hai is view par CSRF check temporarily skip karna.
# Postman se testing karte waqt CSRF token nahi hota, isliye yeh kaam aata hai.
# Production mein ise avoid karke proper CSRF token use karna safer hota hai.

@csrf_exempt
def create_student(request):
    # request ek HttpRequest object hai jisme method aur user ka data hota hai.
    if request.method == "POST":
        # POST body se student form bana rahe hai.
        # POST ka use database mein naya record create karne ke liye hota hai.
        form = StudentsForm(request.POST)

        # Form ke fields aur model rules check kar rahe hai.
        if form.is_valid():
            # Valid form ko database mein save kar rahe hai.
            form.save()

            # Har Django view ko HttpResponse return karna zaroori hai.
            return HttpResponse("form is saved")

    else:
        # GET request mein user ne abhi data submit nahi kiya,
        # isliye empty form object bana rahe hai.
        form = StudentsForm()

        # Is project mein abhi HTML form ki jagah simple text response bhej rahe hai.
        return HttpResponse("post was not there with the request")

    # Agar POST form invalid ho, toh pehle function None return kar raha tha.
    # Isi wajah se Django ka error aata hai:
    # "The view did not return an HttpResponse object. It returned None instead."
    # Form errors ko response mein dikha rahe hai.
    return HttpResponse(form.errors.as_text(), status=400)


@csrf_exempt
def create_mentor(request):
    # Mentor create karne ke liye POST request check kar rahe hai.
    if request.method == "POST":
        # Request ke POST data se mentor form bana rahe hai.
        form = MentorForm(request.POST)

        # Invalid data ko database mein save nahi karna chahiye.
        if form.is_valid():
            form.save()
            return HttpResponse("Mentor form is saved ab solve kariye")

    else:
        # GET request mein koi mentor data submit nahi hua.
        form = MentorForm()
        return HttpResponse("post was not there with the request")

    # Invalid POST par None return hone se bachne ke liye response bhej rahe hai.
    return HttpResponse(form.errors.as_text(), status=400)


@csrf_exempt
def get_details(request, pk):
    # GET ka use data read/fetch karne ke liye hota hai.
    if request.method != "GET":
        # 405 ka matlab hai: request method allowed nahi hai.
        return JsonResponse(
            {"error": "Only GET request is allowed"},
            status=405,
        )

    # pk URL se aane wala integer primary-key parameter hai.
    # student_id=pk ka matlab hai jis student ki id pk hai,
    # uske complaints filter karo.
    complaints = Complaint.objects.filter(student_id=pk).values(
        "id",
        "title",
        "description",
        "category",
        "status",
        "created_at",
    )

    # filter() QuerySet return karta hai, jo database results ka collection hai.
    # values() har record ko dictionary jaisa result banata hai.
    # list() isliye use kiya hai kyunki QuerySet directly JSON serializable nahi hota.
    # Dictionary ke andar list bhejne se JsonResponse safe=True ke saath kaam karta hai.
    return JsonResponse({"complaints": list(complaints)})


@csrf_exempt
def mentor_change_status(request, pk):
    # Yeh function abhi sirf declare kiya gaya hai; status-change logic abhi likhna baaki hai.
    # pass ka matlab hai: function ko temporarily empty rakhna.
    pass
