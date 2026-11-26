# django se hum forms import kar rhe hai kuch built-in hoga
from django import forms
# same subfolder se models.py se Complaint class import kar rhe hai
from .models import Students, Mentors

# forms.ModelForm: Creates a form using an existing Django model.
class StudentsForm(forms.ModelForm) :

    # class Meta: Provides configuration for the form.
    class Meta :
        model = Students # this line specifies which model this form is connected to
        #fields: Specifies which model fields should appear in the form.
        fields = ['stud_name']

class MentorForm(forms.ModelForm) :

    # class Meta: Provides configuration for the form.
    class Meta :
        model = Mentors # this line specifies which model this form is connected to
        #fields: Specifies which model fields should appear in the form.
        fields = ['mentor_name']



