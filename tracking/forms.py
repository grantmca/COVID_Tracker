from django import forms
from .models import Case, Person, Test
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet


class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('id', 'name', 'phone_number', 'company', 'badge_number', 'shop', 'line', 'shift',)

CaseFormset = modelformset_factory(Case, fields = ("encounter_date", "concern", "discription",
                                                   "last_day_worked", "close_contact", "manager", "case_closed"),extra=1)
TestFormset = modelformset_factory(Test, fields = ('id','test_date', 'results_date', 'location', 'test_status',), extra=1)

CloseFormset = modelformset_factory(Person, fields = "__all__", extra=1)

ManagerFormset = modelformset_factory(Person, fields = ("name",), extra=1)