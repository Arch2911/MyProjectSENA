from playwright.sync_api import Page, expect

class Autenticacion:

    def __init__(self, page: Page):
        self.page = page

        self.cedula_input = page.get_by_placeholder("Ingrese su número de identificación")
        self.continuar_button = page.get_by_role("button", name="Continuar")
        self.codigo_input = page.locator(".code-input").first
        self.verificar_button = page.get_by_role("button", name="Verificar")
        self.ok = page.get_by_role("button", name="OK")

    def abrir_pagina(self, url):
        self.page.goto(url)

    def consultar(self, cedula):
        self.cedula_input.fill(str(cedula))
        self.continuar_button.click()

    def verificar_otp(self, codigo):
        self.codigo_input.click()
        self.page.keyboard.type(codigo)
        self.verificar_button.click()


    def texto_visible(self, texto):
        expect(self.page.get_by_text(texto)).to_be_visible
        self.ok.click() # creo que debo aislar este click

