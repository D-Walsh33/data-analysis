import asyncio
import aiohttp
from understat import Understat

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

def shotsPitch(df, name):
    df[['xG', 'X', 'Y']] = df[['xG', 'X', 'Y']].apply(pd.to_numeric)
    df['X'] = df['X'] * 100
    df['Y'] = df['Y'] * 100

    total_shots = df.shape[0]
    total_goals = df[df['result'] == 'Goal'].shape[0]
    total_xG = df['xG'].sum()
    xG_per_shot = total_xG / total_shots
    points_avg_dist = df['X'].mean()
    actual_avg_dist = 120 - (df['X'] * 1.2).mean()

    background_color = '#0C0D0E'
    import matplotlib.font_manager as font_manager
    font_path = './playerTouchMap Project/fonts/Arvo-Regular.ttf'
    font_props = font_manager.FontProperties(fname = font_path)

    fig = plt.figure(figsize=(8,12))
    fig.patch.set_facecolor(background_color)

    ax1 = fig.add_axes([0, .7, 1, .2])
    ax1.set_facecolor(background_color)
    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1)
    ax1.set_axis_off()
    ax1.text(
        x=.5,
        y=.85,
        s= f'{name}',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax1.text(
        x=.5,
        y=.70,
        s= 'All shots in the Premier League 2024 Season',
        fontsize=14,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax1.text(
        x=.25,
        y=.5,
        s= 'Low Quality Chance',
        fontsize=12,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax1.scatter(
        x= .37,
        y= .53,
        s= 100,
        color = background_color,
        edgecolor='white',
        linewidth= .8
    )

    ax1.scatter(
        x= .42,
        y= .53,
        s= 200,
        color = background_color,
        edgecolor='white',
        linewidth= .8
    )

    ax1.scatter(
        x= .48,
        y= .53,
        s= 300,
        color = background_color,
        edgecolor='white',
        linewidth= .8
    )

    ax1.scatter(
        x= .54,
        y= .53,
        s= 400,
        color = background_color,
        edgecolor='white',
        linewidth= .8
    )

    ax1.scatter(
        x= .6,
        y= .53,
        s= 500,
        color = background_color,
        edgecolor='white',
        linewidth= .8
    )


    ax1.text(
        x=.75,
        y=.5,
        s= 'High Quality Chance',
        fontsize=12,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax1.text(
        x=.45,
        y=.28,
        s=f'Goal',
        fontsize=10,
        fontproperties=font_props,
        color='white',
        ha='right'
    )

    ax1.scatter(
        x=.47,
        y=.3,
        s=100,
        color='red',
        edgecolor='white',
        linewidth=.8,
        alpha=.7
    )
    ax1.scatter(
    x=.53,
    y=.3,
    s=100,
    color=background_color,
    edgecolor='white',
    linewidth=.8
    )   

    ax1.text(
        x=.55,
        y=.28,
        s=f'No Goal',
        fontsize=10,
        fontproperties=font_props,
        color='white',
        ha='left'
    )


    ax2 = fig.add_axes([.05, .25, .9, .5])
    ax2.set_facecolor(background_color)
    ax2.set_axis_off()

    pitch = VerticalPitch(
        pitch_type='opta',
        half=True,
        pitch_color=background_color,
        pad_bottom=.5,
        line_color='white',
        linewidth=.75,
        axis=True,
        label=True
    )
    pitch.draw(ax=ax2)

    ax2.scatter(
        x=90, 
        y=points_avg_dist, 
        s=100,
        color='white',
        linewidth=.8
    )

    ax2.plot([90,90], [100, points_avg_dist], color='white', linewidth=2)
    ax2.text(
        x=90,
        y= points_avg_dist - 4,
        s=f'Average Distance \n{actual_avg_dist: .1f} yards',
        fontsize=10,
        fontproperties = font_props,
        color='white',
        ha='center'
    )

    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x['X'],
            x['Y'],
            s= 300 * x['xG'],
            color = 'red' if x['result'] == 'Goal' else background_color,
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )

    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background_color)
    ax3.set_axis_off()

    ax3.text(
        x=.20,
        y=.5,
        s='Shots',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )
    ax3.text(
        x=.20,
        y=0,
        s=f'{total_shots}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='center'
    )

    ax3.text(
        x=.40,
        y=.5,
        s='Goals',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax3.text(
        x=.40,
        y=0,
        s=f'{total_goals}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='center'
    )


    ax3.text(
        x=.60,
        y=.5,
        s='xG',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax3.text(
        x=.60,
        y=0,
        s=f'{total_xG: .2f}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='center'
    )

    ax3.text(
        x=.80,
        y=.5,
        s='xG/Shot',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )

    ax3.text(
        x=.80,
        y=0,
        s=f'{xG_per_shot: .2f}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='center'
    )
    plt.show()

# Get player name from user
input_name = input("Please Enter a players name: ")

# Get player_id from understat
async def get_players(input_name):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        player = await understat.get_league_players(
            'epl', 2024,
            player_name = input_name
        )
        return player[0]['id']

loop = asyncio.get_event_loop()
player_id = loop.run_until_complete(get_players(input_name))

# get shot data from understat using player_id

async def get_shots_24(player_id):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        player_shots = await understat.get_player_shots(
            player_id, {'season': '2024'}
        )
        return player_shots

loop = asyncio.get_event_loop()
shots = loop.run_until_complete(get_shots_24(player_id))
if not shots:
    print(f'{input_name} has not had any shots in the 2024 premier league season!')
else:
    shotsDF = pd.DataFrame(shots)
    shotsPitch(shotsDF, input_name)
