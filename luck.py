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
def luck(league_id, week, debug):
    """This script connects to the Yahoo Fantasy Sports API for the
    league given LEAGUE_ID and calculates the luck factor for each
    team for week WEEK."""
    if not debug:
        oauth_logger = logging.getLogger('yahoo_oauth')
        oauth_logger.disabled = True

    oauth = OAuth1(None, None, from_file='config.json')

    if not oauth.token_is_valid():
        oauth.refresh_access_token()


    url = "http://fantasysports.yahooapis.com/fantasy/v2/league/{0}/scoreboard;week={1}".format(league_id, week)
    response = oauth.session.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        teams = []
        for matchup in soup.find_all('matchup'):
            winner = matchup.winner_team_key.contents[0]
            for team in matchup.find_all('team'):
                ateam = {}
                ateam['id'] = team.team_id.contents[0]
                ateam['name'] = team.contents[5].contents[0]
                ateam['team_key'] = team.team_key.contents[0]
                ateam['score'] = float(team.team_points.total.string)
                if winner == team.team_key.contents[0]:
                    ateam['WL'] = 'W'
                else:
                    ateam['WL'] = 'L'
                teams.append(ateam)
        sortedteams = sorted(teams, key=operator.itemgetter("score"))
        index = 0

        results = []
        for ateam in sortedteams:
            if ateam['WL'] == 'W':
                ateam['luck'] = float("{0:.2f}".format( (((len(sortedteams) - 1) - index) / (len(sortedteams) - 1)) * 100))
            else:
                ateam['luck'] = float("{0:.2f}".format( ((0 - (index + 1)) / (len(sortedteams) - 1)) * 100))

            if debug:
                print(ateam)
            results.append(ateam)
            index = index + 1
        sortedresults = sorted(results, key=operator.itemgetter("luck"))
        for t in sortedresults:
            print("%s:\t\t%s" % (t['name'], t['luck']))
    else:
        print("Error contacting Yahoo API: ", response.status_code, response.reason)

if __name__ == '__main__':
    luck()


