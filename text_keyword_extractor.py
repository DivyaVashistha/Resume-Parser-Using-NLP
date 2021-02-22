"""
Extract and match keywords from requirement and text from resumes.
"""
from spacy.matcher import PhraseMatcher
import os
from collections import Counter
from io import StringIO

import en_core_web_sm
import pandas as pd

from file_text_parser import FileTextParser

nlp = en_core_web_sm.load()


class TextKeywordExtractor:
    """
    Extracts necessary details from text of files using nltk.
    """

    def __init__(self, file_path):
        """
        Constructor to initialise class variables for keyword extraction from files.
        :param file_path: raw string, system path of the file whose text will be used for keyword extraction.
        """
        self.parsed_text = FileTextParser(file_path).text
        self.file_path = file_path
        current_path = os.path.abspath(os.getcwd())
        self.keyword_dict = pd.read_csv(current_path + r'\keyword_database.csv')

    def extract_contact(self):
        pass

    def generate_candidate_profile(self):
        """
        Method to generate a profile for each candidate.
        :return:
        """
        # initialise phrase matcher
        matcher = self.initialise_matcher()

        # match and count the frequencies of keywords from resumes
        keywords = self.match_count_keywords(matcher)
        # todo: map final dataframe with unique id of candidate not names bcz of duplicates
        # converting string of keywords to dataframe of counts of words
        df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Subject', 'Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
        df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)
        df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

        base = os.path.basename(self.file_path)
        filename = os.path.splitext(base)[0]

        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()

        # converting str of candidate name to dataframe for final storing and analysis
        name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])

        final_df = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
        final_df['Candidate Name'].fillna(final_df['Candidate Name'].iloc[0], inplace=True)

        return final_df

    def match_count_keywords(self, matcher: PhraseMatcher):
        """
        Method to match the keywords from candidate resume against the keywords database and count their frequency.
        :param matcher: phase-matcher object, spacy's nlp object to match the resume with keyword database
        :return: string, containing frequencies of keywords under each category.
        """
        doc = nlp(self.parsed_text)
        # match and count the keywords of resume
        d = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = doc[start: end]  # get the matched slice of the doc
            d.append((rule_id, span.text))
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())
        return keywords

    def initialise_matcher(self):
        """
        Method to initialize the matcher object with all required keyword categories.
        :return: PhaseMatcher object, containing list of requirements to be mapped from keyword database.
        """
        front_end_words = [nlp(text) for text in self.keyword_dict['Front-End'].dropna(axis=0)]
        python_words = [nlp(text) for text in self.keyword_dict['Python Language'].dropna(axis=0)]
        mobile_words = [nlp(text) for text in self.keyword_dict['Mobile'].dropna(axis=0)]
        java_words = [nlp(text) for text in self.keyword_dict['Java Language'].dropna(axis=0)]
        c_sharp_words = [nlp(text) for text in self.keyword_dict['C# Language'].dropna(axis=0)]
        sql_words = [nlp(text) for text in self.keyword_dict['SQL-Database'].dropna(axis=0)]
        nosql_words = [nlp(text) for text in self.keyword_dict['NoSQL-Databases'].dropna(axis=0)]
        data_engineering_words = [nlp(text) for text in self.keyword_dict['Data Engineering'].dropna(axis=0)]
        dev_words = [nlp(text) for text in self.keyword_dict['Development'].dropna(axis=0)]

        # initialise phrase matcher with lists for each requirement column
        matcher = PhraseMatcher(nlp.vocab)
        matcher.add('Front-End', None, *front_end_words)
        matcher.add('Mobile', None, *mobile_words)
        matcher.add('Java', None, *java_words)
        matcher.add('C#', None, *c_sharp_words)
        matcher.add('SQL', None, *sql_words)
        matcher.add('NoSQL', None, *nosql_words)
        matcher.add('Development', None, *dev_words)
        matcher.add('Python', None, *python_words)
        matcher.add('Data Engineering', None, *data_engineering_words)

        return matcher


if __name__ == '__main__':
    path = r'path'
    text_keyword_extractor = TextKeywordExtractor(path)
    text_keyword_extractor.generate_candidate_profile()
