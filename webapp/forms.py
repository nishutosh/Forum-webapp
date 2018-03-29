from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.models import User

def name_validator(value):
   if not(value.isalpha()):
      raise ValidationError("all should be characters")
def username_validator(value):
    if User.objects.only("username").filter(username=value):
           raise ValidationError("username already exist")
def password_validator(value):

    if (value.isalpha() or value.isdigit()):
            raise ValidationError("enter a valid password")
class searchbox(forms.Form):
  searchinfo=forms.CharField(max_length=150,widget=forms.TextInput(attrs={"placeholder":"SEARCH YOUR QUESTION","autocomplete":"off"}))            
class Signup(forms.Form):
  username=forms.CharField(min_length=8,max_length=15,widget=forms.TextInput(attrs={"placeholder":"username"}),validators=[username_validator])
  password=forms.CharField(min_length=8,max_length=15,validators=[password_validator],widget=forms.PasswordInput(attrs={"placeholder":"password"}))
  confirm_password=forms.CharField(min_length=8,max_length=15,widget=forms.PasswordInput(attrs={"placeholder":"confirm password"}))
  email=forms.EmailField(max_length=30,widget=forms.EmailInput(attrs={"placeholder":"email","autocomplete":"off"}))
  first_name=forms.CharField(max_length=20,validators=[name_validator ],widget=forms.TextInput(attrs={"placeholder":"first name"}))
  last_name=forms.CharField(max_length=20,validators=[name_validator ],widget=forms.TextInput(attrs={"placeholder":"last name"})) 
  
  def clean(self):
    cleaned_data=super(Signup, self).clean()
    password=cleaned_data.get("password")
    confirmp=cleaned_data.get("confirm_password")
    if  password or confirmp:
         if  password !=confirmp:
                self.add_error ("confirm_password","confirm password does not match with password")                                   
class Login(forms.Form):
  user_name=forms.CharField(min_length=8,max_length=15,widget=forms.TextInput(attrs={"placeholder":"username"}))
  login_password=forms.CharField(min_length=8,max_length=15,widget=forms.PasswordInput(attrs={"placeholder":"password"}))
  
class Ask(forms.Form):
  user_question=forms.CharField(max_length=60)
  question_body=forms.CharField(widget=forms.Textarea(attrs={"rows":"15","cols":"70" ,"placeholder":"Enter your text here"}))
  question_code=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":"15","cols":"83","placeholder":"Enter your code here"}))
class Answer(forms.Form):
  answer=forms.question_body=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter your text here"}))
  answer_code=forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your code here"}))
  
class editpasswordform(forms.Form):
  edit_cpassword=forms.CharField(min_length=8,max_length=15,validators=[password_validator],widget=forms.PasswordInput(attrs={"placeholder":"Old Password"}))
  edit_npassword=forms.CharField(min_length=8,max_length=15,validators=[password_validator],widget=forms.PasswordInput(attrs={"placeholder":"New Password"}))  
  edit_conpassword=forms.CharField(min_length=8,max_length=15,validators=[password_validator],widget=forms.PasswordInput(attrs={"placeholder":"Confirm New Password"}))  

  def clean(self):
    cleaned_data=super(editpasswordform, self).clean()
    password=cleaned_data.get("edit_npassword")
    confirmp=cleaned_data.get("edit_conpassword")
    if  password or confirmp:
         if  password !=confirmp:
                self.add_error ("edit_conpassword","confirm password does not match with password")                            
class editanswer(forms.Form):
   abody=forms.CharField(widget=forms.Textarea()) 
   acode=forms.CharField(required=False,widget=forms.Textarea())
class emailform(forms.Form):
  user_mail=forms.EmailField(max_length=30,widget=forms.EmailInput()) 
class deleteaccount(forms.Form):
  user_password=forms.CharField(min_length=8,max_length=15,validators=[password_validator],widget=forms.PasswordInput(attrs={"placeholder":"Enter your old password"}))
class aboutyou(forms.Form):
  more=forms.CharField(required=False,max_length=700,widget=forms.Textarea(attrs={"placeholder":"Enter text here..."}))  