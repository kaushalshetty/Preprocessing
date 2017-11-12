'''
PREPROCESSING WRAPPER
---------------------
Created on 27/09/2017
A Preprocessing wrapper class for basic preprocessing steps
Author: GAA
---------------------
'''

import string
import re
import json
import os
from collections import OrderedDict
class Preprocessing:
    """
        Preprocessing class
    """
    def __init__(self,lower=True,remove_punct=True,threshold=None,remove_digits=True,verbose = 0,*args,**kwargs):
        """
            Parameters
            -----------
            lower :Boolean, 
                If True = string lowercased, Default set to True
            remove_punct:Boolean, 
                If True all punctuations removed ,Default set to True
            threshold: tuple(lower_limit,upper_limit),
                Words of length lesser than lower_limit and greater than upper_limit will be chopped off. Default is set to None
            remove_digits:Boolean, 
                If True all digits including digits from alphanumerics removed, Default set to True
            verbose: 0 or 1
        """

        self.lower = lower
        self.remove_punct = remove_punct
        self.threshold = threshold
        self.remove_digits = remove_digits
        self.verbose = verbose
        self.regex_dict = OrderedDict()
        self.file_name = ''
        self.is_regex_saved = False
        if self.verbose == 1:
                print("Values of the parameters set lower :{} remove_punctuation:{} remove_digits:{} threshold:{} ".format(self.lower,self.remove_punct,self.remove_digits,self.threshold))
        
    
    
    def print_regex(self,regex_dict):
        """
            Prints regex_dictionary
            
            Parameters
            ----------
            regex_dict:dict,
                Key being the pattern to be replaced and value is the replacement pattern.
                
                
        """
        
        print(self.regex_dict)
        
    
    
    def save_regex(self,file_name,regex_dict):
        """
            Saves the regex_dict so that it can be used later.
            
            Parameters
            ----------
            file_name:string,
                Name of the JSON file to be saved. Must be a json file.
            regex_dict:dict,
                regex json to be saved.
        
        """

        self.file_name = file_name
        if isinstance(regex_dict,dict) is False:
            raise Exception("Input must be a dictionary with key as 'pattern_to_be_replaced' and value 'replaced_by'")
   
        if '.json' not in self.file_name and len(self.file_name.split('.')[0])>0:
            raise Exception("Please enter a json file")
        
        if regex_dict:
            with open(self.file_name,"w") as f:
                json.dump(regex_dict,f)
                self.is_regex_saved = True
        else:
            raise Exception("No regex dictionary created.Please create one.")
            
    
    def load_regex(self):
        """
            Loads the saved regex json file. Json must have been created and saved.
         
        """
        if self.is_regex_saved:
            with open(self.file_name,'r') as f:
                self.regex_dict = json.load(f)
                print("Regex is loaded")
            return self.regex_dict
        else:
            raise Exception("Regex is not created and saved.Please create one and save using 'save_regex' method")
        
        
        
    def set_regex(self,regex_dict):
        """
            Sets the regex dictionary with key as 'pattern_to_be_replaced' and value 'replaced_by'
            Example:{'a':'b','c':'d'}(Replace a with b and c with d)
        
            Parameters
            ----------
            regex_dict:dict,
                Key being the pattern to be replaced and value is the replacement pattern.
  
        """
        if isinstance(regex_dict,dict):
            self.regex_dict = regex_dict
        else:
            raise Exception("Input must be a dictionary with key as 'pattern_to_be_replaced' and value 'replaced_by'")
        
            
    
    def preprocess(self,s):
        """
            Preprocesses the input string 
        
            Parameters
            ----------
            s : string to be cleaned
            
            RETURNS
            -------
            self : preprocessed string 
        """
        
        if self.lower:
            s = s.lower()
                
        if self.regex_dict:
            for key,val in self.regex_dict.items():
                regex_pattern = re.compile(key)
                regex_replace = val
                s = re.sub(regex_pattern,regex_replace,s)
      
        if self.remove_digits:
            s = re.sub(r'\d+','',s)
        s = re.sub(r'[^\x00-\x7F]+',' ', s)
        
        if self.remove_punct:
            s = ''.join([i for i in s if i not in frozenset(string.punctuation)])
        
        if self.threshold is not None:
            s = " ".join([w for w in s.split() if len(w)<self.threshold[1] and len(w)>self.threshold[0]])
            
        s = s.strip()

        return s
