from django.views import generic
from oscar.core.loading import get_model, get_classes
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
class BoutiqueListView(generic.ListView):
    model = Partner
    context_object_name = 'partners'
    template_name = 'boutique/boutique_list.html'
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
    # template_name = 'boutique/boutique_list.html'
    # context_object_name = 'boutique_list'
class BoutiqueDetailView(generic.DetailView):
    model = Boutique
    template_name = 'boutique/boutique_details.html'
    context_object_name = 'boutique'