from yahoo_oauth import OAuth1
from lxml import etree
import operator
from bs4 import BeautifulSoup
import click
import logging

@click.command()
@click.argument('league_id')
@click.argument('week')
@click.option('--debug', is_flag=True)
def coaching(league_id, week, debug):
    """This script connects to the Yahoo Fantasy Sports API for the
    league given LEAGUE_ID and calculates the coaching efficiency for each
    team for week WEEK."""
    if not debug:
        oauth_logger = logging.getLogger('yahoo_oauth')
        oauth_logger.disabled = True

    oauth = OAuth1(None, None, from_file='config.json')

    if not oauth.token_is_valid():
        oauth.refresh_access_token()


    url = "http://fantasysports.yahooapis.com/fantasy/v2/team/{0}.t.3/roster/players;week={1}".format(league_id, week)
    response = oauth.session.get(url)

    if response.status_code == 200:
        print(response.content)
    else:
        print("Error contacting Yahoo API: ", response.status_code, response.reason)

if __name__ == '__main__':
    coaching()
