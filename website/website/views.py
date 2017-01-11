from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.utils.text import slugify

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import random
import string

from .models import *
from .forms import *
# # Create your views here.


class AdminLogInView(View):
    def get(self, request):
        form = LogInForm()
        context = {
            'form': form,
        }
        return render(request, 'website/adminLogIn.html', context)

    def post(self, request):
        form = LogInForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                messages.success(request, "Logged In Successfully")
                login(request, user)
                return redirect('website:dashboard')
        messages.warning(request, "Log In Failure")
        context = {
            'form': form,
        }
        return render(request, 'website/adminLogIn.html', context)


class AdminLogOutView(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(request)
        messages.success(request, "Logged Out Successfully")
        return redirect('website:adminLogIn')


class DashboardView(TemplateView):
    template_name = 'website/dashboard.html'


class ItemCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ItemCategory
    template_name = 'website/itemCategoryCreate.html'
    form_class = ItemCategoryForm
    success_url = reverse_lazy("website:itemCategoryList")
    success_message = "Item Category Successfully Added"


class ItemCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ItemCategory
    template_name = 'website/itemCategoryUpdate.html'
    form_class = ItemCategoryForm
    success_url = reverse_lazy("website:itemCategoryList")
    success_message = "Item Category Successfully Updated"


class ItemCategoryDetailView(DetailView):
    model = ItemCategory
    template_name = 'website/itemCategoryDetail.html'


class ItemCategoryListView(ListView):
    model = ItemCategory
    template_name = 'website/itemCategoryList.html'
    context_object_name = 'itemCategories'

    def get_queryset(self):
        return ItemCategory.objects.filter(deleted_at=None)


class ItemCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = ItemCategory
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:itemCategoryList")
    success_message = "Item Category Successfully Deleted"


class PageCreateView(SuccessMessageMixin, CreateView):
    model = Page
    template_name = 'website/pageCreate.html'
    form_class = PageForm
    success_url = reverse_lazy("website:pageList")
    success_message = "Page Successfully Added"


class PageUpdateView(SuccessMessageMixin, UpdateView):
    model = Page
    template_name = 'website/pageUpdate.html'
    form_class = PageForm
    success_url = reverse_lazy("website:pageList")
    success_message = "Page Successfully Updated"


class PageDetailView(DetailView):
    model = Page
    template_name = 'website/pageDetail.html'


class PageListView(ListView):
    model = Page
    template_name = 'website/pageList.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return Page.objects.filter(deleted_at=None)


class PageDeleteView(SuccessMessageMixin, DeleteView):
    model = Page
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:pageList")
    success_message = "Page Successfully Deleted"


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'website/productCreate.html'
    form_class = ProductForm
    success_url = reverse_lazy("website:productList")
    success_message = "Product Successfully Added"


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'website/productUpdate.html'
    form_class = ProductForm
    success_url = reverse_lazy("website:productList")
    success_message = "Product Successfully Updated"


class ProductDetailView(DetailView):
    model = Product
    template_name = 'website/productDetail.html'


class ProductListView(ListView):
    model = Product
    template_name = 'website/productList.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(deleted_at=None)


class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:productList")
    success_message = "Product Successfully Deleted"


class QuotationCreateView(SuccessMessageMixin, CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'website/quotationCreate.html'
    success_url = reverse_lazy("website:quotationList")
    success_message = "Quotation Successfully Added"

    def dispatch(self, request, *args, **kwargs):
        id = kwargs['id']
        self.requested_product = RequestedProduct.objects.get(pk=id)
        return super(QuotationCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        form.instance.quoted_by = self.request.user
        form.instance.requested_product = self.requested_product
        form.save()
        self.requested_product.quoted = True
        self.requested_product.save()
        return super(QuotationCreateView, self).form_valid(form, *kwargs)


class QuotationUpdateView(SuccessMessageMixin, UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'website/quotationUpdate.html'
    success_url = reverse_lazy("website:quotationList")
    success_message = "Quotation Successfully Updated"


class QuotationListView(ListView):
    model = Quotation
    template_name = 'website/quotationList.html'
    context_object_name = 'quotations'

    def get_queryset(self):
        return Quotation.objects.filter(deleted_at=None)


class QuotationDetailView(DetailView):
    model = Quotation
    template_name = 'website/quotationDetail.html'


class QuotationDeleteView(SuccessMessageMixin, DeleteView):
    model = Quotation
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:quotationList")
    success_message = "Quotation Successfully Deleted"


class ProductCreateFromQuoatationView(View):
    def get(self, request, **kwars):
        quotation = get_object_or_404(Quotation, pk=kwars['pk'])
        if quotation:
            slug = slugify(quotation.requested_product.title) + \
                "-" + str(quotation.id)
            if not Product.objects.filter(slug=slug):
                product = Product()
                product.title = quotation.requested_product.title
                product.slug = slug
                product.category = quotation.category
                product.price = quotation.price
                product.approx_taxes = quotation.approx_taxes
                product.domestic_shipping = quotation.domestic_shipping
                product.height = quotation.height
                product.length = quotation.length
                product.width = quotation.width
                product.weight = quotation.weight
                product.link = quotation.requested_product.link
                product.save()
                form = ProductForm(instance=product)
            else:
                messages.error(
                    request, "Product can be created only once. Only editing is possible.")
                return redirect("website:productUpdate", slug=slug)

        context = {
            "form": form,
        }
        return render(request, "website/productCreateFromQuotation.html", context)

    def post(self, request, **kwargs):
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
        return redirect("website:productList")


class RequestedProductListView(ListView):
    model = RequestedProduct
    template_name = 'website/requestProductList.html'
    context_object_name = 'requestProducts'

    def get_queryset(self):
        return RequestedProduct.objects.filter(deleted_at=None)


class RequestedProductDetailView(DetailView):
    model = RequestedProduct
    template_name = 'website/requestProductDetail.html'


class RequestedProductDeleteView(SuccessMessageMixin, DeleteView):
    model = RequestedProduct
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:requestProductList")
    success_message = "Requested Product Successfully Deleted"


class ShopCreateView(SuccessMessageMixin, CreateView):
    model = Shop
    template_name = 'website/shopCreate.html'
    form_class = ShopForm
    success_url = reverse_lazy("website:shopList")
    success_message = "Shop Successfully Added"


class ShopUpdateView(SuccessMessageMixin, UpdateView):
    model = Shop
    template_name = 'website/shopUpdate.html'
    form_class = ShopForm
    success_url = reverse_lazy("website:shopList")
    success_message = "Shop Successfully Updated"


class ShopDetailView(DetailView):
    model = Shop
    template_name = 'website/shopDetail.html'


class ShopListView(ListView):
    model = Shop
    template_name = 'website/shopList.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.filter(deleted_at=None)


class ShopDeleteView(SuccessMessageMixin, DeleteView):
    model = Shop
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:shopList")
    success_message = "Shop Successfully Deleted"


class SiteConfigCreateView(SuccessMessageMixin, CreateView):
    model = SiteConfig
    template_name = 'website/siteConfigCreate.html'
    form_class = SiteConfigForm
    success_url = reverse_lazy("website:siteConfigList")
    success_message = "Site Config Successfully Added"


class SiteConfigUpdateView(SuccessMessageMixin, UpdateView):
    model = SiteConfig
    template_name = 'website/siteConfigUpdate.html'
    form_class = SiteConfigForm
    success_url = reverse_lazy("website:siteConfigList")
    success_message = "Site Config Successfully Updated"


class SiteConfigDetailView(DetailView):
    model = SiteConfig
    template_name = 'website/siteConfigDetail.html'


class SiteConfigListView(ListView):
    model = SiteConfig
    template_name = 'website/siteConfigList.html'
    context_object_name = 'siteConfigs'

    def get_queryset(self):
        return SiteConfig.objects.filter(deleted_at=None)


class SiteConfigDeleteView(SuccessMessageMixin, DeleteView):
    model = SiteConfig
    template_name = 'website/delete.html'
    success_url = reverse_lazy("website:siteConfigList")
    success_message = "Site Config Successfully Deleted"


class StaffCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'website/staffCreate.html'
    form_class = StaffForm
    success_url = reverse_lazy("website:staffList")
    success_message = "Staff Successfully Added"

    def post(self, request, *args, **kwargs):
        form = StaffForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation)
                                for n in range(18)])
            user.set_password(password)
            user.save()
            grp = Group.objects.get(name='Staff')
            grp.user_set.add(user)
        return HttpResponseRedirect(self.success_url)


class StaffEmailChangeView(SuccessMessageMixin, FormView):
    template_name = 'website/staffEmailChange.html'
    form_class = EmailForm
    success_url = reverse_lazy("website:staffList")
    success_message = "Email Successfully Changed"

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['pk'])
        return super(StaffEmailChangeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        email = form.cleaned_data.get('email')
        self.user.email = email
        self.user.save()
        return super(StaffEmailChangeView, self).form_valid(form, **kwargs)


class StaffToggleGroupView(View):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        if user.groups.all().first().name == 'Staff':
            grp = Group.objects.get(name='Staff')
            grp.user_set.remove(user)
            grp = Group.objects.get(name='Admin')
            grp.user_set.add(user)
        else:
            grp = Group.objects.get(name='Admin')
            grp.user_set.remove(user)
            grp = Group.objects.get(name='Staff')
            grp.user_set.add(user)
        return redirect(reverse_lazy("website:staffList"))


class StaffListView(ListView):
    model = User
    template_name = 'website/staffList.html'
    context_object_name = 'staffs'


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'website/profileDetail.html'
    context_object_name = 'userProfile'


class ProfileListView(ListView):
    model = UserProfile
    template_name = 'website/profileList.html'
    context_object_name = 'profiles'


class MembershipActivateDeactivateView(View):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        membership = Membership.objects.filter(
            user=user, deleted_at=None).first()
        if membership.is_active:
            membership.is_active = False
        else:
            membership.is_active = True
            membership.valid_from = timezone.now()
            membership.valid_to = timezone.now() + timedelta(days=30)
        membership.save()
        return redirect(reverse_lazy("website:profileList"))


class MembershipApproveDisapproveView(View):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        membership = Membership.objects.filter(
            user=user, deleted_at=None).first()
        if membership.is_approved:
            membership.is_approved = False
        else:
            membership.is_approved = True
        membership.save()
        return redirect(reverse_lazy("website:profileList"))


class UserRequestedProductCreateView(SuccessMessageMixin, CreateView):
    model = RequestedProduct
    form_class = RequestedProductForm
    template_name = 'website/userRequestProductCreate.html'
    success_message = "Product Request Successfully Made"
    success_url = reverse_lazy("website:userRequestProductCreate")

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        membership = Membership.objects.filter(
            user=self.request.user, is_active=True).first()
        form.instance.membership = membership.get_type_display()
        return super(UserRequestedProductCreateView, self).form_valid(form, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserRequestedProductCreateView,
                        self).get_context_data(**kwargs)
        context['requestedProducts'] = RequestedProduct.objects.filter(
            user=self.request.user)
        return context


class UserQuotationDetailView(DetailView):
    model = Quotation
    template_name = 'website/userQuotationDetail.html'
    context_object_name = 'quotation'


class UserItemCategoryListView(ListView):
    model = ItemCategory
    template_name = 'website/userItemCategoryList.html'
    context_object_name = 'itemCategories'

    def get_queryset(self):
        return ItemCategory.objects.filter(deleted_at=None)


class UserItemCategoryDetailView(FormView):
    template_name = 'website/userItemCategoryDetail.html'
    form_class = EstimateForm

    def dispatch(self, request, *args, **kwargs):
        self.itemCategory = ItemCategory.objects.filter(
            slug=kwargs['slug']).first()
        return super(UserItemCategoryDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserItemCategoryDetailView,
                        self).get_context_data(**kwargs)
        context['itemCategory'] = self.itemCategory
        return context

    def get_success_url(self):
        return reverse("website: userItemCategoryDetailView", kwargs={'slug': self.itemCategory.slug})


class UserShopListView(ListView):
    model = Shop
    template_name = 'website/userShopList.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.filter(deleted_at=None)


class ContactView(SuccessMessageMixin, FormView):
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_message = "Email Sent Successfully"
    success_url = reverse_lazy("website:contactView")


class ProfileUpdateView(View):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        instance = UserProfile.objects.get(pk=pk)
        userForm = UserForm(instance=instance.user)
        profileForm = ProfileForm(instance=instance)
        context = {
            'userProfile': instance,
            'userForm': userForm,
            'profileForm': profileForm,
        }
        return render(request, 'website/profileUpdate.html', context)

    def post(self, request, **kwargs):
        pk = kwargs['pk']
        instance = UserProfile.objects.get(pk=pk)
        user_form = UserForm(request.POST or None, instance=instance.user)
        profile_form = ProfileForm(
            request.POST or None, request.FILES or None, instance=instance)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy("website:dashboard"))
        else:
            print(user_form.errors, profile_form.errors)
        context = {
            "instance": instance,
        }
        return render(request, 'website/profileUpdate.html', context)


class MembershipListView(View):
    def get(self, request):
        membershipObj = SiteConfig.objects.filter(key='memberships').first()
        if membershipObj:
            membershipValue = membershipObj.value.split(';')
            indMembershipDetailObjs = []
            for membershipTitle in membershipValue:
                indMembershipDetailObj = SiteConfig.objects.filter(
                    key=membershipTitle + 'membership'
                ).first()
                indMembershipDetailList = [indMembershipDetailObj.key]
                for indValue in indMembershipDetailObj.value.split(';'):
                    indMembershipDetailList.append(indValue)
                indMembershipDetailObjs.append(indMembershipDetailList)
        context = {
            'indMembershipDetailObjs': indMembershipDetailObjs,
        }
        return render(request, "website/membershipList.html", context)


class BuyMembership(View):
    def get(self, request, **kwagrs):
        membership = kwagrs['slug']
        membershipObj = SiteConfig.objects.filter(key='memberships').first()
        userMemberships = Membership.objects.filter(user=request.user)
        for prevMembership in userMemberships:
            if not prevMembership.type == 0:
                prevMembership.is_active = False
                prevMembership.save()
                prevMembership.delete()
        userMembership = Membership()
        userMembership.user = request.user
        userMembership.type = membershipObj.value.split(
            ';').index(membership.replace('membership', ''))
        userMembership.save()
        return redirect(reverse_lazy("website:dashboard"))
