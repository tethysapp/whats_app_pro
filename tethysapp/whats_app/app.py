from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting


class WhatsApp(TethysAppBase):
    """
    Tethys app class for Whats App Messages.
    """

    name = 'Whats App Messages'
    index = 'whats_app:home'
    icon = 'whats_app/images/icon.gif'
    package = 'whats_app'
    root_url = 'whats-app'
    color = '#25D366'
    description = 'App shows messages from whatsapp'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='whats-app',
                controller='whats_app.controllers.home'
            ),
            UrlMap(
                name='bot',
                url='bot',
                controller='whats_app.controllers.bot'
            ),
            UrlMap(
                name='search/',
                url='search',
                controller='whats_app.controllers.search'
            ),
        )

        return url_maps

    def persistent_store_settings(self):
        """
        Define Persistent Store Settings.
        """
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='primary_db',
                description='primary database for whats app messages',
                initializer='whats_app.model.init_primary_db',
                required=True
            ),
        )

        return ps_settings
