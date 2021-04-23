from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views import generic
from oscar.core.loading import get_class, get_model, get_classes
from oscar.views import sort_queryset

Partner = get_model('partner', 'Partner')
(
    PartnerSearchForm, PartnerCreateForm, PartnerAddressForm,
    NewUserForm, UserEmailForm, ExistingUserForm
) = get_classes(
    'dashboard.partners.forms',
    ['PartnerSearchForm', 'PartnerCreateForm', 'PartnerAddressForm',
     'NewUserForm', 'UserEmailForm', 'ExistingUserForm'])
Boutique = get_model('boutique', 'Boutique')
BoutiqueCreateUpdateForm = get_class(
    'boutique.dashboard.forms', 'DashboardBoutiqueCreateUpdateForm')
DashboardBoutiqueSearchForm = get_class(
    'boutique.dashboard.forms', 'DashboardBoutiqueSearchForm')


class DashboardBoutiqueListView(generic.ListView):
    model = Partner
    context_object_name = 'partners'
    template_name = 'dashboard/boutique/boutique_list.html'
    form_class = PartnerSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])

        self.description = ("All boutiques")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Boutiques matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx

class DashboardBoutiqueCreateView(generic.CreateView):
    model = Partner
    template_name = 'dashboard/boutique/boutique_update.html'
    success_url = reverse_lazy('boutique-dashboard:boutique-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Create new partner')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Boutique '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:partner-list')


class DashboardBoutiqueUpdateView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = "dashboard/boutique/boutique_update.html"
    form_class = PartnerAddressForm
    success_url = reverse_lazy('boutique-dashboard:boutique-list')

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        address = self.partner.primary_address
        if address is None:
            address = self.partner.addresses.model(partner=self.partner)
        return address

    def get_initial(self):
        return {'name': self.partner.name}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Partner '%s' was updated successfully.") %
            self.partner.name)
        self.partner.name = form.cleaned_data['name']
        self.partner.save()
        return super().form_valid(form)


class PartnerDeleteView(generic.DeleteView):
    model = Partner
    template_name = 'oscar/dashboard/partners/partner_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Partner '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:partner-list')


class DashboardBoutiqueCreateView(generic.CreateView):
    model = Boutique
    template_name = 'dashboard/boutique/boutique_update.html'
    form_class = BoutiqueCreateUpdateForm
    success_url = reverse_lazy('boutique-dashboard:boutique-list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Create new boutique')
        return ctx
    def forms_invalid(self, form, inlines):
        messages.error(
            self.request,
            "Your submitted data was not valid - please correct the below errors")
        return super().forms_invalid(form, inlines)
    def forms_valid(self, form, inlines):
        response = super().forms_valid(form, inlines)
        msg = render_to_string('dashboard/boutique/messages/boutique_saved.html',
                               {'boutique': self.object})
        messages.success(self.request, msg, extra_tags='safe')
        return response


class DashboardBoutiqueUpdateView(generic.UpdateView):
    model = Boutique
    template_name = "dashboard/boutique/boutique_update.html"
    form_class = BoutiqueCreateUpdateForm
    success_url = reverse_lazy('boutique-dashboard:boutique-list')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx
    def forms_invalid(self, form, inlines):
        messages.error(
            self.request,
            "Your submitted data was not valid - please correct the below errors")
        return super().forms_invalid(form, inlines)
    def forms_valid(self, form, inlines):
        msg = render_to_string('dashboard/boutique/messages/boutique_saved.html',
                               {'boutique': self.object})
        messages.success(self.request, msg, extrforms_valida_tags='safe')
        return super().forms_valid(form, inlines)


class DashboardBoutiqueDeleteView(generic.DeleteView):
    model = Boutique
    template_name = "dashboard/boutique/boutique_delete.html"
    success_url = reverse_lazy('boutique-dashboard:boutique-list')