# entry point of CLI
import click
import base64
from Monitor import core


@click.group()
def main():
    """
    A command line tool for keeping an eye on designated web pages
    """
    pass


@main.command()
@click.argument('add', default='')
def add(add):
    """
    Wizard for adding webpages to the list to watch
    """
    URL = base64.b64encode(
          click.prompt('Please enter URL', type=str).encode('ascii'))
    pageEntry = [URL.decode('ascii'), '']
    try:
        core.add(pageEntry)
    except Exception as err: # Exception here will catch anything signalling program errors # noqa e501
        click.echo("Unknown error adding page to data store: '%s'" % err, err=True) # noqa e501
    pass


@main.command()
@click.argument('check', default='')
def check(check):
    """
    Run through and check all of the webpages, printing out any with changes.
    """
    listing = core.listing()
    for k in listing:
        click.echo("%s: %s" % (k, listing[k]))
    pass


@main.command()
@click.argument('update', default='')
def update(update):
    """
    Updated designated URL
    """
    pass


@main.command()
@click.argument('delete', default='')
def delete(delete):
    """
    Delete designated URL
    """
    if delete == '':
        click.echo(
          "after delete keyword you need to entry the URL to delete", err=True)
    b64 = base64.b64encode(delete.encode('ascii'))
    try:
        core.delete(b64.decode())
    except Exception as err:
        click.echo(
          "There was an issue performing the deletion: %s" % repr(err),
          err=True)
    pass


if __name__ == "__main__":
    main()
