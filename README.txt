README

Project is written using Python version 2.7.5

SETTING UP THE PROJECT

1. Setting up a virtual environment

1.1 Install virtualenv via pip 
    $ pip install virtualenv
    
1.2 go into project root dir, create virtual environment with python2.7 interpreter
    $ cd AggressivenessClassification
    $ virtualenv -p /usr/bin/python2.7 venv
   
1.3 Activate Virtual Environment, get all dependencies
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
1.4 Test code
    $ python runClassifier.py # TODO: DATEINAME ERSETZEN !!!!
    # TODO: weitere ANWEISUNGEN
1.5 Deactivate virtual environment
    $ deactivate
    
    To re-enter the virtual environment, simply activate it again from the project root dir
    and continue testing/coding:
    $ source venv/bin/activate
    
    Read more about virtualenv here:
    http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref
    

====================================================================================

   PROBLEMS ?
   Got an error message that looks something like this?

   Resource u'corpora/brown' not found.  Please use the NLTK
     Downloader to obtain the resource:  >>> nltk.download()
  
   Open python REPL, type in:
   >>> import nltk
   >>> nltk.download()
   
   This will open a new window. Find the missing resource (see error your error msg), download it. Done!
   
   
   PyCharm specific Trouble-Shooting
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   If you are running the code from PyCharm, make sure the working directory for each file is set to the root directory:
   Run file that throws error, then go to Run -> Edit Configurations and fill in / change working directory to root
   (yes... there might be a better way to do this...)

    To use venv in PyCharm choose the 2.7.5 virtualenv Project Interpreter that is located in the project root dir:
    PyCharm -> Preferences -> Project: AggressivenessClassification -> Project Interpreter
  
  