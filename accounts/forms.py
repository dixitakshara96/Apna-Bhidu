# Django ke form classes import kar rahe hai.
# Isse forms.Form, CharField, ChoiceField aur ValidationError use kar sakte hai.
from django import forms


# make_password normal password ko hashed password mein convert karta hai.
# check_password entered password ko stored hashed password se compare karta hai.
from django.contrib.auth.hashers import make_password, check_password


# accounts app ke models import kar rahe hai.
from .models import Students, Mentors, Admin


# Signup ke liye normal Django form create kar rahe hai.
# forms.Form tab use hota hai jab form directly ek model se connected nahi hota.
class SignupForm(forms.Form):

    # Admin ka public signup allow nahi kar rahe hai.
    # Sirf student aur mentor signup kar sakte hai.
    ROLE_CHOICES = [
        # Database/form value "student" hogi, display value "Student" hogi.
        ("student", "Student"),

        # Database/form value "mentor" hogi, display value "Mentor" hogi.
        ("mentor", "Mentor"),
    ]

    # User ko role select karne ke liye dropdown field create kar rahe hai.
    # Isme sirf ROLE_CHOICES wali values allowed hongi.
    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    # Signup ke time username receive karne ke liye field.
    username = forms.CharField(
        max_length=100
    )

    # Password receive karne ke liye field.
    # PasswordInput browser mein password ko hide karta hai.
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    # Password ko dobara confirm karne ke liye second field.
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    # clean() form ki combined validation ke liye use hota hai.
    # Yeh method form.is_valid() call hone par automatically run hota hai.
    def clean(self):

        # Parent Form class ki default validation run kar rahe hai.
        # Isse validated values cleaned_data dictionary mein milti hai.
        cleaned_data = super().clean()

        # Cleaned data se password nikal rahe hai.
        password = cleaned_data.get("password")

        # Cleaned data se confirm password nikal rahe hai.
        confirm_password = cleaned_data.get("confirm_password")

        # Dono passwords same hone chahiye.
        if password != confirm_password:

            # Form ko invalid mark kar rahe hai.
            # Yeh error form ke top par display ho sakta hai.
            raise forms.ValidationError(
                "Passwords do not match."
            )

        # Validated data ko Django ke form system ko return kar rahe hai.
        return cleaned_data

    # save() signup data ko database mein save karne ke liye custom method hai.
    # Is method ko form.is_valid() ke baad call karna chahiye.
    def save(self):

        # Selected role cleaned data se nikal rahe hai.
        role = self.cleaned_data["role"]

        # Username cleaned data se nikal rahe hai.
        username = self.cleaned_data["username"]

        # Password cleaned data se nikal rahe hai.
        password = self.cleaned_data["password"]

        # Plain password ko database mein directly save nahi karna chahiye.
        # make_password password ko secure hash mein convert karta hai.
        hashed_password = make_password(password)

        # Agar selected role student hai.
        if role == "student":

            # Students table mein naya student create kar rahe hai.
            # Password ka hashed version save kar rahe hai.
            return Students.objects.create(
                stud_name=username,
                password=hashed_password,
            )

        # Agar selected role mentor hai.
        if role == "mentor":

            # Mentors table mein naya mentor create kar rahe hai.
            # Password ka hashed version save kar rahe hai.
            return Mentors.objects.create(
                mentor_name=username,
                password=hashed_password,
            )


# Login ke liye separate form create kar rahe hai.
class LoginForm(forms.Form):

    # Login ke time tino roles available honge.
    ROLE_CHOICES = [
        # Student login option.
        ("student", "Student"),

        # Mentor login option.
        ("mentor", "Mentor"),

        # Admin login option.
        ("admin", "Admin"),
    ]

    # Login karne wale user ka role receive kar rahe hai.
    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    # User ka name receive kar rahe hai.
    username = forms.CharField(
        max_length=100
    )

    # User ka password receive kar rahe hai.
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    # Form initialize hone par __init__ automatically call hota hai.
    def __init__(self, *args, **kwargs):

        # Parent forms.Form ka constructor call kar rahe hai.
        # Iske bina Django fields initialize nahi karega.
        super().__init__(*args, **kwargs)

        # Initially koi verified user nahi hai.
        # Isliye user_cache mein None store kar rahe hai.
        self.user_cache = None

    # clean() login ke complete data ko validate karta hai.
    def clean(self):

        # Parent form ki default validation run kar rahe hai.
        cleaned_data = super().clean()

        # Selected role form data se nikal rahe hai.
        role = cleaned_data.get("role")

        # Entered username form data se nikal rahe hai.
        username = cleaned_data.get("username")

        # Entered password form data se nikal rahe hai.
        password = cleaned_data.get("password")

        # Database lookup tabhi karenge jab tino values available hongi.
        if role and username and password:

            # Database lookup ke time agar user nahi mile toh exception aa sakta hai.
            try:

                # Agar role student hai.
                if role == "student":

                    # Students table mein username search kar rahe hai.
                    user = Students.objects.get(
                        stud_name=username
                    )

                    # Student ka hashed password nikal rahe hai.
                    stored_password = user.password

                # Agar role mentor hai.
                elif role == "mentor":

                    # Mentors table mein username search kar rahe hai.
                    user = Mentors.objects.get(
                        mentor_name=username
                    )

                    # Mentor ka hashed password nikal rahe hai.
                    stored_password = user.password

                # Agar role student ya mentor nahi hai,
                # toh yahan admin role handle hoga.
                else:

                    # Admin table mein admin name search kar rahe hai.
                    user = Admin.objects.get(
                        admin_name=username
                    )

                    # Admin ka hashed password nikal rahe hai.
                    stored_password = user.admin_pass

            # Agar username database mein nahi mila,
            # toh respective DoesNotExist exception aayega.
            except (
                Students.DoesNotExist,
                Mentors.DoesNotExist,
                Admin.DoesNotExist,
            ):

                # Generic error message use kar rahe hai.
                # Isse attacker ko nahi pata chalega ki username galat tha
                # ya password galat tha.
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            # Entered plain password ko stored hashed password ke saath verify kar rahe hai.
            if not check_password(
                password,
                stored_password
            ):

                # Password match nahi hua toh form invalid kar rahe hai.
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            # Username aur password valid hone ke baad
            # verified database object ko temporarily store kar rahe hai.
            self.user_cache = user

        # Validated data ko form system ko return kar rahe hai.
        return cleaned_data

    # View ko verified user object return karne ke liye helper method.
    def get_user(self):

        # clean() mein stored verified user return kar rahe hai.
        return self.user_cache