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

        self.description = ("All partners")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Partners matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx

   
    # model = Boutique
    # template_name = "dashboard/boutique/boutique_list.html"
    # context_object_name = "boutique_list"
    # paginate_by = 20
    # filterform_class = DashboardBoutiqueSearchForm
    # def get_title(self):
    #     data = getattr(self.filterform, 'cleaned_data', {})
    #     name = data.get('name', None)
    #     city = data.get('city', None)
    #     if name and not city:
    #         return gettext('Boutiques matching "%s"') % (name)
    #     elif name and city:
    #         return gettext('Boutiques matching "%s" near "%s"') % (name, city)
    #     elif city:
    #         return gettext('Boutiques near "%s"') % (city)
    #     else:
    #         return gettext('Boutiques')
    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['filterform'] = self.filterform
    #     data['queryset_description'] = self.get_title()
    #     return data
    # def get_queryset(self):
    #     qs = self.model.objects.all()
    #     self.filterform = self.filterform_class(self.request.GET)
    #     if self.filterform.is_valid():
    #         qs = self.filterform.apply_filters(qs)
    #     return qs


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