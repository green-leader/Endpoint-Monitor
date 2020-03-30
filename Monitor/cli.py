# entry point of CLI
import click
import base64


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
    URL = click.prompt('Please enter URL', type=str).encode('ascii')
    pageEntry = [base64.b64encode(URL), '']
    click.echo(pageEntry)
    pass


@main.command()
@click.argument('check', default='')
def check(check):
    """
    Run through and check all of the webpages, printing out any with changes.
    """
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
    pass


if __name__ == "__main__":
    main()
