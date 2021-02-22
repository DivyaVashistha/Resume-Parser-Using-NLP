"""
Get all files information from the folder and use it to extract and visualise candidate information.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

from text_keyword_extractor import TextKeywordExtractor


def get_path(folder_path):
    """
    Method to extract all files location from the given folder.
    :param folder_path: raw string, path of the folder where resumes are saved
    :return: list of raw strings, paths of all the files in the folder if extracted,
    otherwise None.
    """
    all_resumes_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                        if os.path.isfile(os.path.join(folder_path, f))]
    if all_resumes_path:
        return all_resumes_path
    else:
        return None


def get_all_candidate_info(all_resumes_path):
    """
    Method to extract candidate information from their resume as per requirement.
    :param all_resumes_path: list of raw strings, paths of all resumes.
    :return: pandas dataframe, details of all candidates mapped with requirement.
    """
    candidate_df = pd.DataFrame()
    i = 0

    while i < len(all_resumes_path):
        file = all_resumes_path[i]
        extract = TextKeywordExtractor(file)
        profile_data = extract.generate_candidate_profile()
        candidate_df = candidate_df.append(profile_data)
        i += 1

    print(candidate_df)
    return candidate_df


def count_words_under_category(candidate_df):
    """
    Method to count words under each category for all candidates and save it to csv.
    :param candidate_df: pandas dataframe, information about mapped words from resumes for all candidates.
    :return: pandas dataframe, all candidates with count of mapped words under each section.
    """
    updated_candidate_df = candidate_df['Keyword'].groupby(
        [candidate_df['Candidate Name'], candidate_df['Subject']]).count().unstack()
    updated_candidate_df.reset_index(inplace=True)
    updated_candidate_df.fillna(0, inplace=True)
    final_candidate_info_df = updated_candidate_df.iloc[:, 1:]
    final_candidate_info_df.index = updated_candidate_df['Candidate Name']

    # save all candidate info to csv file
    save_to_csv(final_candidate_info_df)

    return final_candidate_info_df


def visualize_candidates_info(candidate_df):
    """
    Visualize candidate information using matplotlib.
    :param candidate_df: pandas dataframe, information of all candidates for visualization
    :return: None
    """
    plt.rcParams.update({'font.size': 10})
    ax = candidate_df.plot.barh(title="Resume keywords by category", legend=False, figsize=(25, 7), stacked=True)
    labels = []
    for j in candidate_df.columns:
        for i in candidate_df.index:
            label = str(j) + ": " + str(candidate_df.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    plt.savefig('fig.png')


def save_to_csv(candidate_data_df):
    """
    Method to save dataframe to csv file with all candidate information.
    :param candidate_data_df: pandas dataframe, information that needs to be saved into a csv file.
    :return: True, if conversion is successful, False otherwise
    """
    try:
        candidate_data_df.to_csv('final_candidate_data.csv')
        return True
    except Exception as e:
        print(e)
        return False


path = r"Folder path"  # path of the folder where resumes are saved
all_resume_location_list = get_path(path)
all_candidates_df = get_all_candidate_info(all_resume_location_list)
final_candidate_df = count_words_under_category(all_candidates_df)
visualize_candidates_info(final_candidate_df)
# todo: unit tests
