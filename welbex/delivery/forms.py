from django import forms

from .models import Location, Cargo, Car


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['postal_code'].required = True
        self.fields['latitude'].required = True
        self.fields['longitude'].required = True

    class Meta:
        model = Location
        fields = ['city', 'state', 'postal_code', 'latitude', 'longitude']

        widgets = {'city': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Город", 'type': 'text'}),
                   'state': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Штат", 'type': 'text'}),
                   'postal_code': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Почтовый индекс",
                                                         'type': 'number'}),
                   'latitude': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Широта",
                                                      'type': 'number', 'step': '.00001'}),
                   'longitude': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Долгота",
                                                       'type': 'number', 'step': '.00001'})
                   }


class CargoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pick_up_location'].required = True
        self.fields['delivery_location'].required = True
        self.fields['weight'].required = True
        self.fields['description'].required = True

    class Meta:
        model = Cargo
        fields = ['pick_up_location', 'delivery_location', 'weight', 'description']

        widgets = {'pick_up_location': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Pick-up",
                                                              'type': 'number'}),
                   'delivery_location': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Delivery",
                                                               'type': 'number'}),
                   'weight': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Вес",
                                                    'type': 'number', 'min': 1, 'max': 1000}),
                   'description': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Описание",
                                                         'type': 'text'}),
                   }


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].required = True
        self.fields['location'].required = True
        self.fields['weight'].required = True

    class Meta:
        model = Car
        fields = ['number', 'location', 'weight']

        widgets = {'number': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Номер", 'type': 'text'}),
                   'location': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Локация",
                                                      'type': 'number'}),
                   'weight': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Вес",
                                                    'type': 'number', 'min': 1, 'max': 1000}),
                   }


class SearchForm(forms.Form):
    object_type = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'required': True,
                                                                'placeholder': "Объект", 'hidden': True}))
    query = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'required': True,
                                                          'placeholder': "Поиск"}))
