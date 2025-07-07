import pytest
from django.urls import reverse
from wagtail.models import Page
from home.models import HomePage # coloco ess dentro de home do projeto

# @pytest.mark.django_db
# def test_ciclo_1_pagina_com_readonly_panel_falha(client, admin_user):
#     """Verifica que o sistema quebra ao tentar editar uma página com TitleFieldPanel read-only."""
#     client.force_login(admin_user)
#     homepage = Page.get_first_root_node().add_child(
#         instance=HomePage(title="Página de Teste", slug="pagina-de-teste")
#     )
#     edit_url = reverse("wagtailadmin_pages:edit", args=[homepage.pk])
    
#     response = client.get(edit_url)
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_ciclo_2_pagina_com_readonly_panel_nao_quebra(client, admin_user):
#     """Após a correção inicial, verifica se a página carrega sem erros (status 200)."""
#     client.force_login(admin_user)
#     homepage = Page.get_first_root_node().add_child(
#         instance=HomePage(title="Página de Teste", slug="pagina-de-teste")
#     )
#     edit_url = reverse("wagtailadmin_pages:edit", args=[homepage.pk])

#     response = client.get(edit_url)
#     assert response.status_code == 200

@pytest.mark.django_db
def test_ciclo_3_readonly_panel_renderiza_texto_estatico(client, admin_user):
    """Verifica se o painel read-only:
    1. NÃO renderiza um campo <input>.
    2. SIM, renderiza o título como texto estático."""
    client.force_login(admin_user)
    homepage = Page.get_first_root_node().add_child(
        instance=HomePage(title="Título Estático de Teste", slug="titulo-estatico")
    )
    edit_url = reverse("wagtailadmin_pages:edit", args=[homepage.pk])
    response = client.get(edit_url)
    content_html = response.content.decode("utf-8")

    # Garante que o input de formulário NÃO está presente.
    assert '<input type="text" name="title"' not in content_html
    
    # Garante que o valor do título APARECE como texto no HTML.
    # Esta asserção falhará com a correção mínima.
    assert '>Título Estático de Teste</' in content_html