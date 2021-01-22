from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Adds a site to the website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            help='domain name of the site'
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help='Name of the site',
        )

    def handle(self, *args, **options):
        domain = options.get('domain')
        if not domain:
            domain = os.environ.get('API_DOMAIN')
        if Site.objects.filter(domain=domain):
            self.stdout.write(self.style.ERROR(f'Site {domain} already exists'))
            return
        site = Site.objects.create(
            domain=domain,
            name=options.get('name') or domain
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created site {site.domain}'))
