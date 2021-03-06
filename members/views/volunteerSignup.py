from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

from members.forms import getLoginForm, vol_signupForm
from members.models.department import Department
from members.models.family import Family
from members.models.person import Person
from members.models.volunteer import Volunteer

@xframe_options_exempt
def volunteerSignup(request):
        if request.method == 'POST':
            # figure out which form was filled out.
            if request.POST['form_id'] == 'vol_signup':
                # signup has been filled
                getLogin = getLoginForm()
                vol_signup = vol_signupForm(request.POST)
                if vol_signup.is_valid():
                    # check if family already exists
                    try:
                        family = Family.objects.get(email__iexact=request.POST['volunteer_email'])
                        # family was already created - we can't create this family again
                        vol_signup.add_error('volunteer_email', 'Denne email adresse er allerede oprettet. Benyt "Gå til min side" ovenfor, for at få gensendt et link hvis du har mistet det')
                        return render(request, 'members/volunteer_signup.html', {'loginform' : getLogin, 'vol_signupform' : vol_signup})
                    except:
                        # all is fine - we did not expect any
                        pass
                    #create new family.
                    family = Family.objects.create(email = vol_signup.cleaned_data['volunteer_email'])
                    family.confirmed_dtm = timezone.now()
                    family.save()

                    #create volunteer
                    volunteer = Person.objects.create(
                        membertype = Person.PARENT,
                        name = vol_signup.cleaned_data['volunteer_name'],
                        zipcode = vol_signup.cleaned_data['zipcode'],
                        city = vol_signup.cleaned_data['city'],
                        streetname = vol_signup.cleaned_data['streetname'],
                        housenumber = vol_signup.cleaned_data['housenumber'],
                        floor = vol_signup.cleaned_data['floor'],
                        door = vol_signup.cleaned_data['door'],
                        dawa_id = vol_signup.cleaned_data['dawa_id'],
                        placename = vol_signup.cleaned_data['placename'],
                        email = vol_signup.cleaned_data['volunteer_email'],
                        phone = vol_signup.cleaned_data['volunteer_phone'],
                        birthday = vol_signup.cleaned_data['volunteer_birthday'],
                        gender = vol_signup.cleaned_data['volunteer_gender'],
                        family = family
                        )
                    volunteer.save()

                    # send email with login link
                    family.send_link_email()

                    # send email to department leader
                    department = Department.objects.get(name=vol_signup.cleaned_data['volunteer_department'])
                    vol_obj = Volunteer.objects.create(
                        person = volunteer,
                        department = department
                    )
                    vol_obj.save()
                    #department.new_volunteer_email(vol_signup.cleaned_data['volunteer_name'])

                    #redirect to success
                    return HttpResponseRedirect(reverse('login_email_sent'))
                else:
                    getLogin = getLoginForm()
                    return render(request, 'members/volunteer_signup.html', {'loginform' : getLogin, 'vol_signupform' : vol_signup})

            elif request.POST['form_id'] == 'getlogin':
                # just resend email
                vol_signup = vol_signupForm()
                getLogin = getLoginForm(request.POST)
                if getLogin.is_valid():
                    # find family
                    try:
                        family = Family.objects.get(email=getLogin.cleaned_data['email'])

                        if family.dont_send_mails:
                            getLogin.add_error('email', 'Du har frabedt dig emails fra systemet. Kontakt Coding Pirates direkte.')
                        else:
                            # send email to user
                            family.send_link_email()
                            return HttpResponseRedirect(reverse('login_email_sent'))

                    except Family.DoesNotExist:
                        getLogin.add_error('email', 'Denne addresse er ikke kendt i systemet. Hvis du er sikker på du er oprettet, så check adressen, eller opret dig via tilmeldings formularen først.')

                return render(request, 'members/volunteer_signup.html', {'loginform' : getLogin, 'vol_signupform' : vol_signup})

        # initial load (if we did not return above)
        getLogin = getLoginForm()
        vol_signup = vol_signupForm()
        return render(request, 'members/volunteer_signup.html', {'loginform' : getLogin, 'vol_signupform' : vol_signup})
