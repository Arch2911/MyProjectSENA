from playwright.sync_api import Page

class Pedidos:

    def __init__(self, page: Page):
        self.page = page

        self.ver_button = page.get_by_role("button", name="Ver")
        self.cerrar_button = page.get_by_role("button", name="Cerrar")
        self.logout_link = page.get_by_role("link", name="Logout")


    def ver_detalles(self):
        self.ver_button.click()

    def cerrar_detalles(self):
        self.cerrar_button.click()

    def cerrar_sesion(self):
        self.logout_link.click()