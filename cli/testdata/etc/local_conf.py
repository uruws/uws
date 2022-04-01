import uwscli
import uwscli_user

from uwscli_conf import App
from uwscli_user import AppUser

uwscli.app['local_conf'] = App(False)
uwscli.cluster['local_conf'] = {'region': 'testing'}

uwscli_user.user['tuser'] = AppUser(
	uid = 5000,
	groups = ['tapp', 'tapp1'],
	is_admin = True,
)
