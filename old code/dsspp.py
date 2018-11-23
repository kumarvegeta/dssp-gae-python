
# This Python file uses the following encoding: utf-8

import cgi

#from google.appengine.api import users

import webapp2

#import jinja2

import paste

import webob

import os

#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.spatial.distance import cosine
from scipy.sparse import csr_matrix
from gensim.models.word2vec import Word2Vec
import gensim

from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import json, glob
import re, math, operator
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


from sklearn.preprocessing import normalize

import pickle

from random import randint

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

results = []


## The handler function that generates the main page 
def mainPage(request):
    #return webapp2.Response("index.html")
    return webapp2.Response("""<!doctype html>
<html lang="en">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. On Python for GAE</title>
 </head>
 <body>
   <h1>Welcome to the DSSPP. Please choose your language:</h1>
   <form action="new_proc_form" method="POST">
     <table>
       <tr>
         <th>Language:</th>
         <td>English<input type="radio" name="language" value="English" checked="yes" /><br />
           Spanish<input type="radio" name="language" value="Spanish" /><br />
         </td>
       </tr>
     </table>
     <input type="submit" value="Submit" />
   </form>
 </body>
</html>
""")



## Corpus selection pages -rewritten


def CorpusSelection_English(request):

    #return webapp2.Response("index.html")
    return webapp2.Response("""<!doctype html>
<html lang="en">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. On Python for GAE</title>
 </head>
 <body>
   <h1>Thank you for choosing English. Please choose your corpus domain:</h1>
   <form action="proc_form_english_domain_corpus" method="POST">
     <table>
       <tr>
         <thCorpus:</th>
         <td>Literature<input type="radio" name="domain" value="Literature" checked="yes" /><br />
           News<input type="radio" name="domain" value="News" /><br />
	   Technology<input type="radio" name="domain" value="Technology" /><br />
         </td>
       </tr>
     </table>
     <input type="submit" value="Submit" />
   </form>
 </body>
</html>
""")


def CorpusSelection_Spanish(request):

    #return webapp2.Response("index.html")
    return webapp2.Response("""<!doctype html>
<html lang="es">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. En Python para GAE</title>
 </head>
 <body>
   <h1>Gracias por elegir español. Por favor elige tu dominio de corpus:</h1>
   <form action="proc_form_spanish_domain_corpus" method="POST">
     <table>
       <tr>
         <thCuerpo:</th>
         <td>Literatura<input type="radio" name="domain" value="Literatura" checked="yes" /><br />
           Noticias<input type="radio" name="domain" value="Noticias" /><br />
	   Tecnología<input type="radio" name="domain" value="Tecnología" /><br />
         </td>
       </tr>
     </table>
     <input type="submit" value="Enviar" />
   </form>
 </body>
</html>
""")


def proc_form_english_domain_corpus(request):

    domain = request.params.get(cgi.escape('domain'))
    if domain == "Literature":
        return webapp2.Response("""<!doctype html>
<html lang="en">
<head>  <meta charset="utf-8">

<title> D.S.S.P.P. On Python For GAE </title>

</head>

  <body>
        <h3>Enter the word in English to find similar words for:</h3>
        <form method="GET" action="eng_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Submit">
        </form>

  </body>
</html>
""" )

    if domain =="News":
        return webapp2.Response("""<!doctype html>
<html lang="en">
<head>  <meta charset="utf-8">

<title> D.S.S.P.P. On Python For GAE </title>

</head>

  <body>
        <h3>Enter the word in English to find similar words for:</h3>
        <form method="GET" action="eng_news_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Submit">
        </form>

  </body>
</html>
""" )


    if domain == "Technology":
        return webapp2.Response("""<!doctype html>
<html lang="en">
<head>  <meta charset="utf-8">

<title> D.S.S.P.P. On Python For GAE </title>

</head>

  <body>
        <h3>Enter the word in English to find similar words for:</h3>
        <form method="GET" action="eng_tech_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Submit">
        </form>

  </body>
</html>
""" )



## Spanish part



def proc_form_spanish_domain_corpus(request):

    domain = request.params.get(cgi.escape('domain'))
    if domain == "Literatura":
        return webapp2.Response("""<!doctype html>
<html lang="es">
<head> <meta charset="utf-8">

<title> D.S.S.P.P. En Python para GAE </title>

</head>

  <body>
        <h3> Ingrese la palabra en español para encontrar palabras similares para: </h3> 
         <form method="GET" action="esp_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Enviar">
        </form>

  </body>
</html>
""" )

    if domain =="Noticias":
        return webapp2.Response("""<!doctype html>
<html lang="es">
<head> <meta charset="utf-8">

<title> D.S.S.P.P. En Python para GAE </title>

</head>

  <body>
        <h3> Ingrese la palabra en español para encontrar palabras similares para: </h3> 
         <form method="GET" action="esp_news_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Enviar">
        </form>

  </body>
</html>
""" )


    if domain == "Tecnologia":
        return webapp2.Response("""<!doctype html>
<html lang="es">
<head> <meta charset="utf-8">

<title> D.S.S.P.P. En Python para GAE </title>

</head>

  <body>
        <h3> Ingrese la palabra en español para encontrar palabras similares para: </h3> 
         <form method="GET" action="esp_tech_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Enviar">
        </form>

  </body>
</html>
""" )



def proc_form(request):

    language = request.params.get(cgi.escape('language'))

    if language == "English":
        return webapp2.Response("""<!doctype html>
<html lang="en">
<head>  <meta charset="utf-8">

<title> D.S.S.P.P. On Python For GAE </title>

</head>

  <body>
        <h3>Enter the word in English to find similar words for:</h3>
        <form method="GET" action="eng_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Submit">
        </form>

  </body>
</html>
""" )

    if language =="Spanish":
        return webapp2.Response("""<!doctype html>
<html lang="es">
<head> <meta charset="utf-8">

<title> D.S.S.P.P. En Python para GAE </title>

</head>

  <body>
        <h3> Ingrese la palabra en español para encontrar palabras similares para: </h3> 
         <form method="GET" action="esp_results">

          <input type="text" name="word_string"><br />

          <input type="submit" name ="Enviar">
        </form>

  </body>
</html>
""" )


def new_proc_form(request):

    language = request.params.get(cgi.escape('language'))
    if language == "English":
        return webapp2.redirect('/CorpusSelection_English')

    if language =="Spanish":
        return webapp2.redirect('/CorpusSelection_Spanish')



def eng_results(request):
	rendered = ""
	#word = request.params.get(cgi.escape('word_string'))
	word = request.params.get(cgi.escape('word_string'))
	model = gensim.models.Word2Vec.load('English_Literature.w2v')
	results = model.most_similar(word)
	for result in results:
      	    rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0], result[1])
        return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. On Python For GAE </title>

          </head>

            <body>
                  
                  <h1>List of similar words to the given word:</h1>
                  <table>
                  <tr>
                  	<th>Word</th>
                    <th>Score</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)


def eng_news_results(request):
	rendered = ""
	#word = request.params.get(cgi.escape('word_string'))
	word = request.params.get(cgi.escape('word_string'))
	model = gensim.models.Word2Vec.load('English_News.w2v')
	results = model.most_similar(word)
	for result in results:
      	    rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0], result[1])
        return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. On Python For GAE </title>

          </head>

            <body>
                  
                  <h1>List of similar words to the given word:</h1>
                  <table>
                  <tr>
                  	<th>Word</th>
                    <th>Score</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)


def eng_tech_results(request):
	rendered = ""
	#word = request.params.get(cgi.escape('word_string'))
	word = request.params.get(cgi.escape('word_string'))
	model = gensim.models.Word2Vec.load('English_Literature.w2v')
	results = model.most_similar(word)
	for result in results:
      	    rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0], result[1])
        return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. On Python For GAE </title>

          </head>

            <body>
                  
                  <h1>List of similar words to the given word:</h1>
                  <table>
                  <tr>
                  	<th>Word</th>
                    <th>Score</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)




def esp_results(request):

    rendered = ""
    word = request.params.get(cgi.escape('word_string'))
    model = gensim.models.Word2Vec.load('Spanish_Literature.w2v')
    results = model.most_similar(word)
    for result in results:
        rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0].encode('utf-8'), result[1])
    return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. En Python para GAE </title>

          </head>

            <body>
                  
                  <h1>Lista de palabras similares a la palabra dada:</h1>
                  <table>
                  <tr>
                  	<th>Palabra</th>
                    <th>Puntuación</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)


def esp_news_results(request):

    rendered = ""
    word = request.params.get(cgi.escape('word_string'))
    model = gensim.models.Word2Vec.load('Spanish_News.w2v')
    results = model.most_similar(word)
    for result in results:
        rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0].encode('utf-8'), result[1])
    return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. En Python para GAE </title>

          </head>

            <body>
                  
                  <h1>Lista de palabras similares a la palabra dada:</h1>
                  <table>
                  <tr>
                  	<th>Palabra</th>
                    <th>Puntuación</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)



def esp_tech_results(request):

    rendered = ""
    word = request.params.get(cgi.escape('word_string'))
    model = gensim.models.Word2Vec.load('Spanish_Literature.w2v')
    results = model.most_similar(word)
    for result in results:
        rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0].encode('utf-8'), result[1])
    return webapp2.Response("""<!doctype html>
          <html lang="en">
          <head>  <meta charset="utf-8">

          <style>
              td, th {
                text-align: center;
                border: 1px solid black;  
	      }
	      table {
                border-spacing: 0px;
              }
          </style>

          <title> D.S.S.P.P. En Python para GAE </title>

          </head>

            <body>
                  
                  <h1>Lista de palabras similares a la palabra dada:</h1>
                  <table>
                  <tr>
                  	<th>Palabra</th>
                    <th>Puntuación</th>
                  </tr>
                  %s
                  </table>

            </body>
          </html>
          """ % rendered)



def failure_en():

      return webapp2.Response("""<!doctype html>
<html lang="en">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. On Python for GAE</title>
 </head>
 <body>
   <h1>We are extremely sorry. The search word you entered was not found in the corpus. Please click on the link below to go back to the home page:</h1>
   <a href="mainPage">Home Page</a>
 </body>
</html>
""")

def failure_es():

    return webapp2.Response("""<!doctype html>
<html lang="en">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. En Python para GAE</title>
 </head>
 <body>
   <h1>Lo sentimos mucho. La palabra de búsqueda que ingresó no se encontró en el corpus. Haga clic en el siguiente enlace para volver a la página de inicio:</h1>
   <a href="mainPage">Página de inicio</a>
 </body>
</html>
""")


def render_image(request):
    img = open('images/eng_results.png')
    resp = webapp2.Response()
    resp.headers['Content-Type'] = 'img/png'
    resp.body_file.write(img.read())
    img.close()
    return resp


def render_es_image(request):
    img = open('images/esp_results.png')
    resp = webapp2.Response()
    resp.headers['Content-Type'] = 'img/png'
    resp.body_file.write(img.read())
    img.close()
    return resp

 
application = webapp2.WSGIApplication([
    ('/', mainPage),
    ('/images/eng_results', render_image),
    ('/images/eng_news_results', render_image),
    ('/images/eng_tech_results', render_image),
    ('/images/esp_results', render_es_image),
    ('/images/esp_news_results', render_es_image),
    ('/images/esp_tech_results', render_es_image),
    ('/proc_form',proc_form),
    ('/new_proc_form',new_proc_form),
    ('/proc_form_english_domain_corpus',proc_form_english_domain_corpus),
    ('/proc_form_spanish_domain_corpus',proc_form_spanish_domain_corpus),
    ('/CorpusSelection_English',CorpusSelection_English),
    ('/CorpusSelection_Spanish',CorpusSelection_Spanish),
    ('/eng_results',eng_results),
    ('/eng_news_results',eng_news_results),
    ('/eng_tech_results',eng_tech_results),
    ('/esp_results',esp_results),
    ('/esp_news_results',esp_news_results),
    ('/esp_tech_results',esp_tech_results)
], debug=True)

def main():

    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8080')

    application.run()

if __name__ == "__main__":
    main()
