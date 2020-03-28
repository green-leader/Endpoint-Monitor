# entry point of CLI
import click


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
    click.echo("Add")
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
