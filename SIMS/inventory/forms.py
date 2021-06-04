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
                  #'manufacturer_serienumber',
                  #'website',
                  'contractor',
                  'contractor_partnumber',
                  #'contractor_serienumber',
                  ]
        widgets = {
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control', 'id':'manufacturer'
            }),
             'manufacturer_partnumber': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'manufacturer_partnumber'
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
        CHARACTERISTIC_CHOICE = (
            ('Sim Part', 'Sim part', 'sim part'),
            ('Consumable', 'consumable'),
            ('Tool', 'tool'),
            ('PPE', 'ppe'),
            ('Office', 'office'),
            ('Building', 'building'),
        )
        model = Item
        fields = ['article_related',
                  'cae_partname',
                  #'CAEPartNumber',
                  #'CAESerialNumber',
                  'item_model',
                  #'Description',
                  #'Comment',
                  #'Documentation',
                  #'Type',
                  #'characteristic',
                  ]
        widgets = {
            'article_related': forms.TextInput(attrs={
                'class': 'form-control', 'id':'article_related'
            }),
            'cae_partname': forms.TextInput(attrs={
                'class': 'form-control', 'id':'cae_partname'
            }),
             'item_model': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'item_model'
            })
        }





