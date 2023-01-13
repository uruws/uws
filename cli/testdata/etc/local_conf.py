import uwscli

from uwscli_conf import App

uwscli.app['local_conf'] = App(False)
uwscli.cluster['local_conf'] = {'region': 'testing'}
