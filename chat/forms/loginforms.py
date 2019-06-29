from django import  forms
class loginForm(forms.Form):
    username=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'input100' ,'type':"text" ,'name':"username" ,'placeholder':"Username"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':"input100",'type':"password",'name':"pass", 'placeholder':"Password"})
    )
class signupForm(forms.Form):
    firstname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'input100' ,'type':"text" ,'name':"firstname" ,'placeholder':"Firstname"})
    )
    lastname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'input100' ,'type':"text" ,'name':"lastname" ,'placeholder':"Lastname"})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'input100' ,'type':"text" ,'name':"username" ,'placeholder':"Username"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'input100' ,'type':"password" ,'name':"pass" ,'placeholder':"Password"})
    )