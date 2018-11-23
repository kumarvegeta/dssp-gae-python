# dssp-gae-python
DSSPP In Python On GAE and / or Amazon Web Services

Description:  Domain Specific Context Sensitive Semantic Processing Portal (DSSPP) is a web service that can be utilized by other projects that involve semantic processing tasks on vector space models. Depending on the application, one can use and / or customize the framework freely to better suit the requirement. It by default, comes with support for training models on any generalized language corpus relevant to the project that is trying to use it, using LSA semantic encoding method. The application can be used in such a way that it reaches out to servers that have already performed semantic processing tasks on the corpora used by the project(s) and gets the term vectors stored in memory, and retrieve, on demand by the user of the portal, all relevant filtered results that are semantically similar to the given search word entered as input. Furthermore, its possible to extend this capability to find semantically similar results for not only words, but also a group or collection of words, such as sentences, paragraphs, and even whole documents. It all depends on what type of function is desired. An application of this nature can find use in a variety of Natural Language Processing tasks, and in domains such as computer-aided learning, medical transcription, library management systems, and even filtration software, among many others.

As mentioned previously, the term vectors are pre-computed and stored in memory already, prior to querying by the user.

a) Core functions: The tool takes the input word (along with language selection and domain selection by the user) in a web page from the user, and then immediately returns a set of words that closely related to the given word as a listing along with respective cosine similarities in the result web page. One thing to note, however, is that there is a limit on the number of results returned. If the limit is raised, more results will be returned, not just the top ten most similar words.
b) Multi-language support: The tool is capable of supporting multiple languages and multiple language corpora as a result of the same. For this version, the languages supported are English and Spanish.
c) Domain Specific: The tool has the capability to provide search results from multiple domains, implemented by way of categorized corpora. The search results are domain specific and corpus-dependent, with the size and quality of the corpus playing an important role in the accuracy and efficiency of the tool. The domains being utilized for this version are news and literature.
d) Context Sensitive: The results are also context sensitive, meaning the actual usage of the term in a sentence is considered, as is its relation to other words that are used in the same sense as the entered word.
e) Word Sense Disambiguation: The tool is inherently capable of Word Sense Disambiguation due to internal logic by way of utilizing the gensim package.
f) Speed: The current version of the tool is very fast at churning processed results to the user by virtue of precomputed results and pre-trained models.
g) Accuracy: The tool’s returned results for any given word on a language support currently implemented are very accurate with respect to the corpus. Bugs, if any are constantly being worked on and removed at the earliest possible opportunity.

The application requires Google Oauth 2.0 sign-in to be completed, with Google sharing the user's name, email address, and profile picture with the application in order to authorize it to work for the user.

For more information, please contact me at girish.hbk@gmail.com

