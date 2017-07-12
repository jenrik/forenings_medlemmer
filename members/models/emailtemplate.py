#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from members.models.emailitem import EmailItem
from members.models.person import Person
from members.models.department import Department
from members.models.family import Family
import members.models.emailitem
import members.models.person
import members.models.department
import members.models.family
from django.conf import settings
from django.template import Engine, Context
from functools import reduce


class EmailTemplate(models.Model):
    class Meta:
        verbose_name = 'Email Skabelon'
        verbose_name_plural = 'Email Skabeloner'
    idname = models.SlugField('Unikt reference navn',max_length=50, blank=False, unique=True)
    updated_dtm = models.DateTimeField('Sidst redigeret', auto_now=True)
    name = models.CharField('Skabelon navn',max_length=200, blank=False)
    description = models.CharField('Skabelon beskrivelse',max_length=200, blank=False)
    template_help = models.TextField('Hjælp omkring template variable', blank=True)
    from_address = models.EmailField()
    subject = models.CharField('Emne',max_length=200, blank=False)
    body_html = models.TextField('HTML Indhold', blank=True)
    body_text = models.TextField('Text Indhold', blank=True)
    def __str__(self):
        return self.name + " (ID:" + self.idname + ")"

    # Will create and put an email in Queue from this template.
    # It will try to to put usefull details in context, which in many cases can just be {}

    # context is always filled with:
    #  email, site

    # If possible it will also be filled with:
    #  person, family

    # recievers is expected to be a list of Person, Family or strings (email adresses)

    def makeEmail(self, recievers, context):

        if(type(recievers) is not list):
            recievers = [recievers]

        for reciever in recievers:
            if type(reciever) is members.models.person.Person:
                if reciever.family in recievers and reciever.email == reciever.family.email:
                    recievers.remove(reciever.family)

        map_addresses = {}
        # build map mapping email to person, family and department
        for reciever in recievers:
            if type(reciever) is Person \
                    and not reciever.family.dont_send_mails \
                    and reciever.email is not ""\
                    and receiver in map_addresses.get(receiver.email, {}).get("person", []):
                map_addresses.setdefault(receiver.email, {}).setdefault("person", []).append(reciever)
                if reciever.emil is not "" and receiver in map_addresses.get(receiver.email, {}).get("family", []):
                    # Adds family such that it can be used in the template
                    map_addresses.setdefault(receiver.email, {}).setdefault("family", []).append(reciever)
            elif type(reciever) is Family\
                    and not reciever.dont_send_mails\
                    and reciever.emil is not ""\
                    and receiver in map_addresses.get(receiver.email, {}).get("family", []):
                map_addresses.setdefault(receiver.email, {}).setdefault("family", []).append(reciever)
            elif type(reciever) is Department\
                    and reciever.responsible_contact is not "" \
                    and receiver in map_addresses.get(receiver.responsible_contact, {}).get("department", []):
                map_addresses.setdefault(receiver.responsible_contact, {}).setdefault("department", []).append(reciever)
            else:
                raise Exception("Reciever must be of type Person, Family or Department not " + str(type(reciever)))

        emails = []

        for destination_address, entities in recievers.items():
            # each reciever must be Person, Family or string (email)

            # Note - string specifically removed. We use family.dont_send_mails to make sure
            # we dont send unwanted mails.


            for k, v in entities.items():
                context[k] = v

            # figure out Person and Family is applicable
            if "person" in entities.keys():
                person = entities["person"]
            elif('person' in context):
                person = context["person"]
                if type(person) is not list:
                    person = [person]
            else:
                person = None

            # figure out family
            if "family" in entities.keys:
                family = entities["family"]
            elif 'family' in context:
                family = context['family']
                if type(family) is not list:
                    family = [family]
            else:
                family = None
            # Family is always set if their is a person, so their is no need to extract family from "person"

            # figure out activity
            if 'activity' in context:
                activity = context['activity']
            else:
                activity = None

            # department
            if "department" in entities.keys():
                department = entities["department"]
            elif 'department' in context:
                department = context['department']
                if type(department) is not list:
                    department = [department]
            else:
                department = None

            # fill out known usefull stuff for context
            if 'email' not in context: context['email'] = destination_address
            if 'site' not in context: context['site'] = settings.BASE_URL

            # Make real context from dict
            context = Context(context)

            # render the template
            html_template = Engine.get_default().from_string(self.body_html)
            text_template = Engine.get_default().from_string(self.body_text)
            subject_template = Engine.get_default().from_string(self.subject)

            html_content = html_template.render(context)
            text_content = text_template.render(context)
            subject_content = subject_template.render(context)

            email = EmailItem.objects.create(
                template = self,
                reciever = destination_address,
                person = person, # ToDo person is a list not a single instance
                family = family, # ToDo family is a list not a single instance
                activity = activity,
                department = department, # ToDo department is a lsit not a single instance
                subject = subject_content,
                body_html = html_content,
                body_text = text_content)
            email.save()
            emails.append(email)
        return emails
