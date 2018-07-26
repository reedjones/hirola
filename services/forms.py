from django import forms
from .models import ServiceOffer
from hirola import utils


class ServiceForm(forms.Form):

    def get_errors(self):
        data = []
        errors_ = self.errors
        for k in errors_.keys():
            if k != 'target_id':
                data.append({'name': k, 'error': errors_[k][0]})

        return data


class ServiceForm1(ServiceForm):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea,
                                  label="Add a short description (will add more details later)",
                                  max_length=200)
    category = forms.IntegerField(widget=forms.HiddenInput())


class ServiceForm2(ServiceForm):
    """
    """

    target_id = forms.IntegerField(widget=forms.HiddenInput())

    details = forms.CharField(widget=forms.Textarea,
                              label="Describe your offer in full-detail")

    price = forms.DecimalField(widget=forms.TextInput, label="Price (in Euro)", max_digits=4, decimal_places=2,
                               initial=5.00)

    # price.widget.attrs.update({
    #     'data-slider-min': '5.00',
    #     'data-slider-max': '200',
    #     'data-slider-step': '0.50',
    #     'data-slider-value': '5.00'
    # })
    # forms.FieldField(widget=forms.FileInput(attrs={'class': 'rounded_list'}))

    # tags = forms.Textarea()
    delivery_period = forms.ChoiceField(choices=ServiceOffer.time_choices, label="Delivery Period (Days or Hours)")
    delivery_time = forms.IntegerField(widget=forms.HiddenInput())


class ServiceForm3(forms.Form):
    main_image = forms.ImageField()
    gallery = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class OrderForm(forms.Form):
    target_id = forms.IntegerField()
    user_id = forms.IntegerField()


class TextForm(ServiceForm):
    value = forms.Textarea()


class CharForm(forms.Form):
    value = forms.CharField()


class IntForm(forms.Form):
    value = forms.IntegerField()


class ServiceFull(ServiceForm):
    target_id = forms.IntegerField()
    name = forms.CharField()
    description = forms.CharField()
    details = forms.Textarea()
    tags = forms.TextInput()

    def make_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(', ')
        return tags


class ServiceReviewForm(ServiceForm):
    target_id = forms.IntegerField()
    text = forms.Textarea()
    sid = forms.IntegerField()


class CheckoutForm(forms.Form):
    price = forms.DecimalField()
    paid = forms.IntegerField()
    platform = forms.CharField()
