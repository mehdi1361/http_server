# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def test_ctm(request):
    return render(request, 'admin/test_ctm.html')