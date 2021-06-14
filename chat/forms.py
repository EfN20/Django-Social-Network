from django import forms

from .models import Room
from users.models import User


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'members')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RoomForm, self).__init__(*args, **kwargs)
        print(self.user)
        # self.fields['members'] = forms.ModelMultipleChoiceField(queryset=User.objects.get(phone_number=self.user)
        #                                                         .friend_list.all())
        self.fields['members'].widget = forms.CheckboxSelectMultiple()
        self.fields['members'].queryset = User.objects.get(phone_number=self.user).friend_list.all()
