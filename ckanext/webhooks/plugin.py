import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging

import db
import actions
import requests

import ckan.model as model
from ckan.model.domain_object import DomainObjectOperation

log = logging.getLogger(__name__)

class WebhooksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDomainObjectModification, inherit=True)
    plugins.implements(plugins.IActions, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'webhooks')

    #IDomainObjectNotification & #IResourceURLChange
    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            if (operation == DomainObjectOperation.new or not operation):
                pass
                #notify all registered parties of new resource

            if (operation == DomainObjectOperation.changed):
                pass
                #notify all of change in resource

            elif (operation == DomainObjectOperation.deleted):
                pass
                #notify all of resource deletion

        if isinstance(entity, model.Package):
            if (operation == DomainObjectOperation.new):
                self._notify_package_create(entity)

            elif (operation == DomainObjectOperation.changed):
                pass
                #notify all of change in dataset

            elif (operation == DomainObjectOperation.deleted):
                pass
                #notify all of dataset delete

    def get_actions(self):
        actions_dict = {
            'webhook_create': actions.webhook_create,
            'webhook_delete': actions.webhook_delete,
            'webhook_show': actions.webhook_show
        }
        return actions_dict

    #Notification functions be here
    def _notify_package_create(self, package):
        log.info("Notifying webhooks for package create")
        webhooks = db.Webhook.find(topic='dataset/create')
        for hook in webhooks:
            url = hook.address
            payload = {
                'entity': package,
                'webhook_id': hook.id
            }

            requests.post(url, data=payload)
