"""
Parsing resumes with various extensions to extract text from them.
"""
import docx2txt
from pdfminer.high_level import extract_text


class FileTextParser:
    """
    Parses and cleans text into strings from files with extensions- .docx,.pdf,.txt and .doc.
    """

    def __init__(self, file_path):
        """
        Constructor to initialize class variable with file path and validate extension to call required method.
        :param file_path: raw string, system path of the file whose text needs to be parsed into string.
        """
        self.file_path = file_path
        self.text = ""
        self.execute_parser_by_extension()

    def execute_parser_by_extension(self):
        """
        Method to call parsers as per file extensions.
        :return: string in lower case if file with proper extension is parsed,
        otherwise none.
        """
        if str(self.file_path).endswith('.pdf'):
            self.text = self.extract_pdf()
        elif str(self.file_path).endswith('.docx'):
            self.text = self.extract_docx()
        elif str(self.file_path).endswith('.doc'):
            self.text = self.extract_doc()
        elif str(self.file_path).endswith('.txt'):
            self.text = self.extract_text()
        else:
            self.text = None

    def extract_text(self):
        """
        Extract text from a file with extension '.txt'.
        :return: returns clean string if text has been parsed,
        otherwise None
        """
        with open(self.file_path, 'r') as file:
            txt = file.read()
        if txt:
            return txt.encode('ascii', 'ignore').decode("utf-8").replace('\f', ' ').replace('\n', ' ') \
                .replace('\t', ' ').replace(u'\xa0', ' ').replace('\u200b', ' ').replace('  ', ' ').lower()

    def extract_pdf(self):
        """
        Extract text from a file with extension '.pdf'.
        :return: returns clean string if text has been parsed,
        otherwise None
        """
        txt = extract_text(self.file_path)
        if txt:
            return txt.encode('ascii', 'ignore').decode("utf-8").replace('\f', ' ').replace('\n', ' ') \
                .replace('\t', ' ').replace(u'\xa0', ' ').replace('\u200b', ' ').replace('  ', ' ').lower()
        return None

    def extract_docx(self):
        """
        Extract text from a file with extension '.docx'.
        :return: returns clean string if text has been parsed,
        otherwise None
        """
        txt = docx2txt.process(self.file_path)
        if txt:
            return txt.encode('ascii', 'ignore').decode("utf-8").replace('\f', ' '). \
                replace('\n', ' ').replace('\t', ' ').replace(u'\xa0', ' ').replace('\u200b', ' ').lower()

        return None

    def extract_doc(self):
        """
        Extract text from a file with extension '.doc'.
        "Antiword" has to be installed in the system for these old file extensions.
        :return: returns clean string if text has been parsed,
        otherwise None
        """
        # todo: need to use antiword [WIP]
        return self.text


if __name__ == '__main__':
    resume_path = r'path'
    file_text_parser = FileTextParser(resume_path)
    # file_text_parser.extract_pdf()

    # file_text_parser.extract_docx()

    # file_text_parser.extract_doc()

    # file_text_parser.extract_text()
