# -*- coding: utf-8 -*-

from django.shortcuts import render


def view_test(request):
    return render(request, 'panel/index.html')


def dashboard(request):
    pass