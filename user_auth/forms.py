from django import forms
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserBankAccount, UserAddress
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'account_type', 'birth_date','gender', 'postal_code', 'city','country', 'street_address']
    
    def save(self, commit=True):
        current_user = super().save(commit=False)

        if commit == True:
            current_user.save()
            user_account_type = self.cleaned_data.get('account_type')
            user_birth_date = self.cleaned_data.get('birth_date')
            user_gender = self.cleaned_data.get('gender')
            user_street_address = self.cleaned_data.get('street_address')
            user_city = self.cleaned_data.get('city')
            user_postal_code = self.cleaned_data.get('postal_code')
            user_country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user = current_user,
                city = user_city,
                postal_code = user_postal_code,
                country = user_country,
                street_address = user_street_address
            )

            UserBankAccount.objects.create(
                user = current_user,
                account_type = user_account_type,
                birth_date = user_birth_date,
                account_no = 10000+current_user.id,
                gender=user_gender,
            )

        print(current_user.first_name)
        print(user_account_type)
        print(user_country)

        return current_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({

                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
    
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except:
                user_account = None
                user_address = None
        
        print(self.instance)

        if user_account:
            self.fields['account_type'].initial = user_account.account_type
            self.fields['gender'].initial = user_account.gender
            self.fields['birth_date'].initial = user_account.birth_date
            self.fields['street_address'].initial = user_address.street_address
            self.fields['city'].initial = user_address.city
            self.fields['postal_code'].initial = user_address.postal_code
            self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        current_user = super().save(commit=False)
        if commit == True:
            current_user.save()

            user_account, created = UserBankAccount.objects.get_or_create(user=current_user)
            user_address, created = UserAddress.objects.get_or_create(user=current_user)

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return current_user

