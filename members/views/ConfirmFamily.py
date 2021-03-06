import uuid

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.urlresolvers import reverse

from members.models.family import Family
from members.models.person import Person
from members.models.waitinglist import WaitingList


def ConfirmFamily(request, unique):
    try:
        unique = uuid.UUID(unique)
    except ValueError:
        return HttpResponseBadRequest("Familie id er ugyldigt")

    family = get_object_or_404(Family, unique=unique)
    persons = Person.objects.filter(family=family)
    subscribed_waiting_lists = WaitingList.objects.filter(person__family=family)

    if request.method == 'POST':
        ''' No data recieved - just set confirmed_dtm date to now '''
        family.confirmed_dtm = timezone.now()
        family.save()
        return HttpResponseRedirect(reverse('family_detail', args=[unique]))
    else:
        context = {
            'family':family,
            'persons':persons,
            'subscribed_waitinglists': subscribed_waiting_lists
        }
        return render(request, 'members/family_confirm_details.html',context)
