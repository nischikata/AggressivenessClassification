README

This project is written in Python version 2.7.5 by Tina Schuh

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
	
1.4 Install Jupyter Notebook, but upgrade pip first
	$ pip install --upgrade pip
	$ pip install jupyter
       
1.5 To leave the virtual environment, run the deactivate command
    $ deactivate
    
    To re-enter the virtual environment, simply activate it again from the project root dir
    and continue testing/coding:
    $ source venv/bin/activate
    
    Read more about virtualenv here:
    http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref


2. Test installation / Use project

2.1 In the Terminal, location project root dir, virtual environment active, start the Jupyter Server:
	$ jupyter notebook
	
2.2	Open the Jupyter Server URL in your web browser (may happen automatically); find the URL in your Terminal window

2.2 Open any of the DEMO files, read instructions and experiment. Enjoy!
	
    

====================================================================================

   PROBLEMS ?

   Resources missing:
   ------------------
   Got an error message that looks something like this?

   Resource u'corpora/brown' not found.  Please use the NLTK
     Downloader to obtain the resource:  >>> nltk.download()
  
   Open python REPL, type in:
   >>> import nltk
   >>> nltk.download()
   
   This will open a new window. Find the missing resource (see error your error msg), download it. Done!


   Urban Dictionary
   ----------------
   The project utilizes the Urban Dictionary API. 
   Internet access (and permission if your computer asks for it) are required in ordered to make predictions.
   
   
   Lasso or SVM Warnings 
   ---------------------
   Occasionally, if values in the parameter grid of the GridSearch are to low, an f1-score cannot be computed (e.g. in cases 
   when precision and recall both amount to zero). This only means that the parameters are useless. Nevermind, it's not an 
   actual problem.
   
   