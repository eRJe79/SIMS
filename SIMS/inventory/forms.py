from django import forms

from .models import Article, Item, Spare

class MainUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class LambdaUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


# Article form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['manufacturer',
                  'manufacturer_partnumber',
                  'website',
                  'contractor',
                  'contractor_partnumber',
                  ]
        widgets = {
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control', 'id':'manufacturer'
            }),
             'manufacturer_partnumber': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'manufacturer_partnumber'
            }),
             'website': forms.URLInput(attrs={
                'class': 'form-control', 'id': 'website'
            }),
             'contractor': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'contractor'
            }),
             'contractor_partnumber': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'contractor_partnumber'
            })
        }

# Item form
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['article_related',
                  'cae_partname',
                  'cae_partnumber',
                  #'CAESerialNumber',
                  'item_model',
                  'description',
                  #'Comment',
                  'documentation',
                  'item_type',
                  'item_characteristic',
                  'principal_location',
                  ]
        widgets = {
            'article_related': forms.Select(attrs={
                'class': 'form-control', 'id':'article_related'
            }),
            'cae_partname': forms.TextInput(attrs={
                'class': 'form-control', 'id':'cae_partname'
            }),
            'cae_partnumber': forms.TextInput(attrs={
                'class': 'form-control', 'id':'cae_partnumber'
            }),
             'item_model': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'item_model'
            }),
             'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            }),
             'documentation': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'documentation'
            }),
            'item_type': forms.Select(attrs={
                'class': 'form-control', 'id':'item_type'
            }),
            'item_characteristic': forms.Select(attrs={
                'class': 'form-control', 'id':'item_characteristic'
            }),
            'principal_location': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'principal_location'
            })
        }





