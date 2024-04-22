This is the code for my final project in CMPINF1205. The code is designed to go through my personal files and categorize them.

**Objectives**
This research project is designed to undertake a comprehensive examination and comparison of personal data management and privacy policies implemented by leading digital platforms, including Instagram, Twitter/X, Google, and Amazon. It aims to scrutinize the variety of data collected by these platforms. The study will leverage personal data downloaded from these platforms, with the support of GPT-3.5, to conduct a detailed categorization of the data types involved. The language model will only access the files in txt.txt, as it can only receive text input.

**Methodology**
The project leverages Python scripts and large language models, primarily OpenAI's GPT-3.5, to categorize and analyze personal data types collected by digital platforms. The initial approach involved providing the language model with file contents and a list of data categories, which were refined across iterations to improve the categorization accuracy and reduce redundancies.

**Results**
The analysis resulted in a comprehensive list of 93 data categories, significantly refined from the initial 2000 categories. This categorization helps in understanding the extent and specificity of data collection by digital platforms. The research also included a manual review of privacy laws in Canada, Germany, and the United States, comparing the level of consumer protections provided.

**How to Use**
To use, go to config.ini and replace YOUR_KEY_HERE with your OpenAI API key.
You will need to provide your files and a list of directories (delimited by newlines) in txt.txt.
Then run `python main.py`.

For detailed information, please read Final.pdf.
