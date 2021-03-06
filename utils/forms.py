#
# Freesound is (c) MUSIC TECHNOLOGY GROUP, UNIVERSITAT POMPEU FABRA
#
# Freesound is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Freesound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     See AUTHORS file.
#

from django import forms
from utils.text import clean_html, is_shouting
from django.conf import settings
from recaptcha.client import captcha
from utils.tags import clean_and_split_tags
from HTMLParser import HTMLParseError

class HtmlCleaningCharField(forms.CharField):
    def clean(self, value):
        value = super(HtmlCleaningCharField, self).clean(value)

        if is_shouting(value):
            raise forms.ValidationError('Please moderate the amount of upper case characters in your post...')
        try:
            return clean_html(value)
        except HTMLParseError:
            raise forms.ValidationError('The text you submitted is badly formed HTML, please fix it')


class TagField(forms.CharField):
    def clean(self, value):
        tags = clean_and_split_tags(value)

        if len(tags) < 3:
            raise forms.ValidationError('Your should at least have 3 tags...')
        elif len(tags) > 30:
            raise forms.ValidationError('There can be maximum 30 tags, please select the most relevant ones!')

        return tags


class RecaptchaWidget(forms.Widget):
    """ A Widget which "renders" the output of captcha.displayhtml """
    def render(self, *args, **kwargs):
        return captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY).strip()


class DummyWidget(forms.Widget):
    """
    A dummy Widget class for a placeholder input field which will
    be created by captcha.displayhtml
    """

    # make sure that labels are not displayed either
    is_hidden=True
    def render(self, *args, **kwargs):
        return ''


class RecaptchaForm(forms.Form):
    """
    A form class which uses reCAPTCHA for user validation.
    If the captcha is not guessed correctly, a ValidationError is raised
    for the appropriate field
    """
    recaptcha_challenge_field = forms.CharField(widget=DummyWidget)
    recaptcha_response_field = forms.CharField(widget=RecaptchaWidget, label="Please prove you are not a robot:")

    def __init__(self, request, *args, **kwargs):
        super(RecaptchaForm, self).__init__(*args, **kwargs)
        self._request = request

        # move the captcha to the bottom of the list of fields
        recaptcha_fields = ['recaptcha_challenge_field', 'recaptcha_response_field']
        self.fields.keyOrder = [key for key in self.fields.keys() if key not in recaptcha_fields] + recaptcha_fields

    def clean_recaptcha_response_field(self):
        if 'recaptcha_challenge_field' in self.cleaned_data:
            self.validate_captcha()
        return self.cleaned_data['recaptcha_response_field']

    def clean_recaptcha_challenge_field(self):
        if 'recaptcha_response_field' in self.cleaned_data:
            self.validate_captcha()
        return self.cleaned_data['recaptcha_challenge_field']

    def validate_captcha(self):
        rcf = self.cleaned_data['recaptcha_challenge_field']
        rrf = self.cleaned_data['recaptcha_response_field']
        ip_address = self._request.META['REMOTE_ADDR']
        check = captcha.submit(rcf, rrf, settings.RECAPTCHA_PRIVATE_KEY, ip_address)
        if not check.is_valid:
            raise forms.ValidationError('You have not entered the correct words')
