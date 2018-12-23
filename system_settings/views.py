# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import CtmTestForm
from objects.models import League
from common.utils import CtmChestGenerate
from django.contrib.auth.models import User


# Create your views here.


def test_ctm(request):
    lst_result = []
    len_header = 0
    if request.method == 'POST':
        form = CtmTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            league = League.objects.get(pk=int(cd['league']))

            for i in range(1, int(cd['count'])):
                user = User.objects.get(pk=cd['player'])
                chest = CtmChestGenerate(user, chest_type=str(cd['chest']), league=league)
                result = chest.generate_chest()
                lst_result.append(result)
                len_header = len(result['units'])

    else:
        form = CtmTestForm()

    return render(
        request, 'admin/test_ctm.html',
        {
            'form': form,
            'len_header': len_header,
            'result': lst_result
        }
    )
