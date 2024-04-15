from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from store.models import CartOrder, CartOrderItem, Product
from core.models import Wishlist, Address
from django.http import JsonResponse
from store.forms import AddressForm

import json
import random
import string



