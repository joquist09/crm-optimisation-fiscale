import os

template_dir = r"c:\Users\JordanQuist\OneDrive - SFLDFSI\Documents\OF\crm-optimisation-fiscale\core\templates\core"

templates_config = [
    ('revenus_dividendes', 'Revenus dividendes', 'coins'),
    ('fond_pension_cd', 'Fonds pension CD', 'piggy-bank'),
    ('fond_pension_rre', 'Fonds pension RRE', 'vault'),
    ('projection_rre', 'Projections RRE', 'chart-line'),
    ('fond_pension_pd', 'Fonds pension PD', 'university'),
    ('cotisation_compte_personnel', 'Cotisations compte personnel', 'wallet'),
    ('budget_extraordinaire', 'Budgets extraordinaires', 'money-bill-alt'),
    ('projection_assurance_vie', 'Projections assurance vie', 'heartbeat'),
    ('informations_fiscales_societe', 'Informations fiscales société', 'file-invoice-dollar'),
    ('profil_investisseur', 'Profils investisseur', 'user-tie'),
    ('actif', 'Actifs', 'building'),
    ('flux_monetaire', 'Flux monétaires', 'exchange-alt')
]

form_template = """{{%extends 'core/base.html' %}}
{{% block title %}}{{{{ title }}}} - CRM OF{{% endblock %}}
{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="page-title mb-0"><i class="fas fa-edit"></i> {{{{ title }}}}</h1>
    <a href="{{% url '{list_url}' %}}" class="btn btn-outline-secondary"><i class="fas fa-arrow-left me-2"></i> Retour</a>
</div>
<div class="row justify-content-center">
    <div class="col-md-10"><div class="card"><div class="card-body">
        <form method="post">{{% csrf_token %}}
            {{% for field in form %}}
            <div class="mb-3">
                <label for="{{{{ field.id_for_label }}}}" class="form-label fw-bold">{{{{ field.label }}}}</label>
                {{{{ field }}}}
                {{% if field.errors %}}<div class="text-danger small">{{{{ field.errors.0 }}}}</div>{{% endif %}}
            </div>
            {{% endfor %}}
            <div class="d-flex justify-content-between">
                <a href="{{% url '{list_url}' %}}" class="btn btn-secondary"><i class="fas fa-times me-2"></i> Annuler</a>
                <button type="submit" class="btn btn-success"><i class="fas fa-save me-2"></i> Enregistrer</button>
            </div>
        </form>
    </div></div></div>
</div>
{{% endblock %}}"""

list_template = """{{% extends 'core/base.html' %}}
{{% block title %}}{title} - CRM OF{{% endblock %}}
{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="page-title mb-0"><i class="fas fa-{icon}"></i> {title}</h1>
    <a href="{{% url '{create_url}' %}}" class="btn btn-primary"><i class="fas fa-plus me-2"></i> Nouveau</a>
</div>
<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-dark"><tr><th>ID</th><th>Détails</th><th>Actions</th></tr></thead>
                <tbody>
                    {{% for item in {var_name} %}}
                    <tr><td>{{{{ item.id }}}}</td><td>{{{{ item }}}}</td><td><button class="btn btn-sm btn-outline-primary"><i class="fas fa-eye"></i></button></td></tr>
                    {{% empty %}}
                    <tr><td colspan="3" class="text-center text-muted">Aucun élément trouvé</td></tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </div>
    </div>
</div>
{{% endblock %}}"""

for url_name, title, icon in templates_config:
    list_url = f"{url_name}_list"
    create_url = f"{url_name}_create"
    
    # Déterminer le nom de variable
    if url_name == 'actif':
        var_name = 'actifs'
    elif url_name == 'flux_monetaire':
        var_name = 'flux'
    elif url_name.endswith('s'):
        var_name = url_name
    else:
        var_name = url_name + 's'
    
    # Créer le template de liste
    list_content = list_template.format(
        title=title,
        icon=icon,
        create_url=create_url,
        var_name=var_name
    )
    list_file = os.path.join(template_dir, f"{url_name}_list.html")
    with open(list_file, 'w', encoding='utf-8') as f:
        f.write(list_content)
    print(f"Created: {url_name}_list.html")
    
    # Créer le template de formulaire
    form_content = form_template.format(list_url=list_url)
    form_file = os.path.join(template_dir, f"{url_name}_form.html")
    with open(form_file, 'w', encoding='utf-8') as f:
        f.write(form_content)
    print(f"Created: {url_name}_form.html")

print(f"\n✅ Created {len(templates_config) * 2} templates!")
