import pandas as pd
import numpy as np
from collections import defaultdict


def autolabel(bars):
  for bar in bars.patches:

    # Using Matplotlib's annotate function and
    # passing the coordinates where the annotation shall be done
    # x-coordinate: bar.get_x() + bar.get_width() / 2
    # y-coordinate: bar.get_height()
    # free space to be left to make graph pleasing: (0, 8)
    # ha and va stand for the horizontal and vertical alignment

    bars.annotate(str(np.round(bar.get_width(), 1)) + '%',
                  xy=(bar.get_width(),
                      bar.get_y() + bar.get_height() / 2),
                  ha='left', va='center',
                  xytext=(5, 0),
                  textcoords='offset points', fontsize=12)


def change_width(ax, new_value):
  for patch in ax.patches:
    current_width = patch.get_height()
    diff = current_width - new_value

    # we change the bar width
    patch.set_height(new_value)

    # we recenter the bar
    patch.set_y(patch.get_y() + diff)


def total_count(df, col1, col2, look_for):
  '''
  INPUT:
  df - the pandas dataframe you want to search
  col1 - the column name you want to look through
  col2 - the column you want to count values from
  look_for - a list of strings you want to search for in each row of df[col]

  OUTPUT:
  new_df - a dataframe of each look_for with the count of how often it shows up
  '''

  new_df = defaultdict(int)
  # loop through list of ed types
  for val in look_for:
    # loop through rows
    for idx in range(df.shape[0]):
      # if the ed type is in the row add 1
      if val in df[col1][idx]:
        new_df[val] += int(df[col2][idx])
  new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
  new_df.columns = [col1, col2]
  new_df.sort_values('count', ascending=False, inplace=True)

  return new_df


def clean(df, col, vals, label):
  '''
  INPUT
      df - a dataframe holding the EducationTypes column
      title - string the title of your plot
      axis - axis object
      plot - bool providing whether or not you want a plot back

  OUTPUT
      study_df - a dataframe with the count of how many individuals
      Displays a plot of pretty things related to the CousinEducation column.
  '''
  study = df[col].value_counts().reset_index()
  study.rename(columns={'index': label, col: 'count'}, inplace=True)
  study_df = total_count(study, label, 'count', vals)
  study_df.set_index(label, inplace=True)
  props_study_df = study_df / study_df.sum() * 100
  return props_study_df


def total_count_modified(df, col1, col2, hue, look_for):
  '''
  INPUT:
  df - the pandas dataframe you want to search
  col1 - the column name you want to look through
  col2 - the column you want to count values from
  look_for - a list of strings you want to search for in each row of df[col]

  OUTPUT:
  new_df - a dataframe of each look_for with the count of how often it shows up
  '''

  combined_df = pd.DataFrame()
  for i in df[hue].unique():
    new_df = defaultdict(int)
    # loop through list of ed types
    for val in look_for:
      # loop through rows
      for idx in range(df.shape[0]):
        # if the ed type is in the row add 1
        if val in df[col1][idx]:
          if i == df[hue][idx]:
            new_df[val] += int(df[col2][idx])
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1, col2]
    new_df[hue] = i
    new_df.sort_values('count', ascending=False, inplace=True)
    combined_df = pd.concat([combined_df, new_df])
  return combined_df


def pctByAttr(df, col1, col2, var):
  count_df = df.groupby([col1, col2]).agg({'Respondent': 'count'})
  count_df.columns = ['count']
  count_df.reset_index(inplace=True)
  total_count_df = total_count_modified(count_df, col2, 'count', col1, var)

  sum_df = total_count_df.groupby([col1, col2]).agg({'count': 'sum'})
  pct_df = sum_df.groupby(level=0).apply(lambda x: 100 * x / x.sum())
  pct_df.columns = ['Percentage']
  pct_df.reset_index(inplace=True)
  pct_df.sort_values('Percentage', ascending=False, inplace=True)
  return pct_df
