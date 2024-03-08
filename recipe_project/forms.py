from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('name', 'username', 'password')
