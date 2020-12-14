# entry point of CLI
import click
import base64
import sys
from monitor import core


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
    pageEntry = dict()
    URL = base64.b64encode(
          click.prompt('Please enter URL', type=str).encode('ascii'))
    pageEntry['URL'] = URL.decode()
    pageEntry['name'] = click.prompt(
        'Enter a name for this entry for user purposes', type=str, default='')
    try:
        result = core.add(pageEntry)
    except core.BadURL as err:
        click.echo("%s" % err)
    except Exception as err: # Exception here will catch anything signalling program errors # noqa e501
        click.echo("Unknown error adding page to data store: '%s'" % err) # noqa e501
        sys.exit(1)
    pass


@main.command()
@click.argument('listing', default='')
def listing(listing):
    """
    List all of the entries in data store
    """
    listing = core.listing()
    for k in listing:
        click.echo("%s: %s" % (k, listing[k]))
    pass


@main.command()
@click.argument('check', default='')
def check(check):
    """
    Check all entries in data store for changes
    """
    try:
        updateResults = core.update(check)
    except core.EmptyListError as err:
        click.echo("%s" % err, err=True)
        return
    for entry in updateResults:
        click.echo("%s changed" % entry)
    pass


@main.command()
@click.argument('update', default='')
def update(update):
    """
    Updated designated URL
    """
    raise NotImplementedError("Update has not been implemented")
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
        pass
    try:
        core.delete(delete)
    except KeyError:
        click.echo(
          'That doesnt appear to be a valid entry',
          err=True)
        sys.exit(1)
    except Exception as err:
        click.echo(
          "There was an issue performing the deletion: %s" % repr(err),
          err=True)
        sys.exit(1)
    pass


if __name__ == "__main__":
    main()
