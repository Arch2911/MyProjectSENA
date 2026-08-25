from playwright.sync_api import Page, expect

class Base:

    def __init__(self, page: Page):

        self.page = page

    def texto_visible(self, texto):
        expect(self.page.get_by_text(texto)).to_be_visible()