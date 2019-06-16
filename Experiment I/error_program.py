# -*- coding: utf-8 -*-

import sys
import traceback
from IPython.core import ultratb
import datetime
import json
import os
import ipywidgets
import inspect

try:
    logfile = open('errors.log', 'a')
except:
    logfile = None

username = os.getenv('USERNAME', 'unknown')
using_puffin = os.getenv('PUFFIN', 'False')
import zlib
helpful = True #zlib.crc32(bytes(username, 'utf8')) % 2 == 1

def _log_info(what, *args, **kwargs):
    entry = kwargs
    entry['what'] = what
    entry['time'] = datetime.datetime.now().isoformat()
    entry['username'] = username
    entry['puffin'] = using_puffin == 'True'
    if len(args) > 0:
        entry['values'] = args

    if logfile != None:
        print(json.dumps(entry, default=lambda x: repr(x)), file=logfile)
        logfile.flush()

last_error = None
class LogFeedback:
    def __init__(self, widget, err, name):
        self.widget = widget
        self.name = name
        self.err = err
    
    def log(self, change):
        _log_info('FEEDBACK', func=self.name, value=self.widget.value, last_error=self.err)

def make_feedback_button(err, name):
    #try:
        b = ipywidgets.ToggleButtons(
            options=['Useful', 'Not needed', 'Not useful', 'Confusing'],
            #description='Assistance was...:',
            disabled=False,
            #value='',
            button_style='primary', #['success', 'info', 'warning', 'danger'], # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', '', ''],
            #icons=['check', 'check', 'times', 'question']
        )
        b.observe(LogFeedback(b, err, name).log, 'value', 'change')
       
        return ipywidgets.HBox([ipywidgets.Label('This bit of assistance was...'), b])
    #except:
    #    return None

    
def get_help(error):
    if type(error).__name__ == "TypeError":
        return type_error_help(str(error))
    if type(error).__name__ == "IndexError":
        return index_error_help(str(error))
    if type(error).__name__ == "NameError":
        return name_error_help(str(error))
    if type(error).__name__ == "ZeroDivisionError":
        return zero_div_error_help(str(error))
    
    #Compilation errors not caught.. :'(
    if type(error).__name__ == "IndentationError":
        return index_error_help(str(error))
    if type(error).__name__ == "AttributeError":
        return attribute_error_help(str(error))


def zero_div_error_help(error): 
    return 'Make sure to check if a value is zero before doing a division!\nA Simple solution is to add "if val != 0", val being the value used to divide'
    
def name_error_help(error):
    return 'Typical things that cause NameError is: \n1. Forgetting to give the variable a value before using it \n2. Misspelling the variable or function \n3. Simply not putting "" around the string text \n4. Not importing the module.'
    
def attribute_error_help(error):
    msg ='AttributeError is somewhat like a type error. Calling the given attribute fails. \nIs the spelling and type of object correct?.. The type can be checked by print(type(variable_name_here))'
    if 'has no attribute' in error:
        msg+='\n\nHere it seems you trying to use an attribute on a type that does not support it. \nFor instance: a = int(22).split() will give the same error since split() can only be used on string types. \nIf the type is correct then my second option is that the attribute is misspelled!'
    return msg
    #'AttributeError: str object has no attribute Capitalize'
    
def indenation_error_help(error):
    msg = 'Remember that all code should be located one indent out from the above (closest) codeline ending on :'   
    if 'unindent' in error:
        msg+= 'Unindent means that the following line is should have less indentation'
    else:
        msg+= 'Did you put in correct indentation around the given error line?'
    return msg

def index_error_help(error):
    msg = ''
    if 'out of range' in error:
        return 'The solution can be found by checking the length of the string (f.ex: len(str_name)) and the index value used. \
                \nNo solution? Check for potential changes done to the list that could change the expected length.'
    else:
        msg += 'The solution can be found by checking the length of the list (f.ex: len(list_name)) against the index value used.' 
    return msg
    
def type_error_help(error):
    msg = ''
    if '<' in error or '>' in error:
        msg+= '<, >, >=, <= can only be used to compare two objects that are comparable. \nFor example one value of type str and one of type int are not!\nMake sure that the values being compared are initialized correctly.'
    elif 'not callable' in error:
        msg = 'It probably means that you are trying to call a function when a variable with the same name is available. F.ex:\n str = "hello"\n userid = 352790\n username = str(userid) -> this code gives the same error since str is now a variable equal to "hello" and not a function. \n'
    elif 'argument' in error and 'missing' in error:
        msg+= 'It seems you are not enough input parameters to the function you are trying to use.\nMake sure to check how many values a function takes in input, f.ex add(a,b) takes two arguments a and b!'
    elif 'argument' in error and 'takes' in error:
        msg+= 'It seems you are giving too many arguments to the given function. \nMake sure to check how many values a function takes in input: \nf.ex add(a,b) takes two arguments a and b, \n     add(pair) will take one argument, containing a tuple [a,b]!'
    elif ('type' and 'subscriptable') in error:
        msg+= 'The [] notation is used to subscript objects (usually lists, dicts, etc), \nstr(), int(), len(), range() etc are all functions and are not subscriptable. '
    elif 'not iterable' in error:
        msg+= 'It seems you are trying to iterate over a type that is not iterable! \nMaybe you shold double check that you are trying to iterate over the correct value?'
    else:
        msg+= 'TypeError occurres when the program is expecting a certain type, but got something else! \nHave you forgotten to add a function like len(), or int() surrounding the value?'
    msg +='\nIt is possible to check the type of the variable you are trying to use by printing the value itself or its type with \nprint(type(variable_to_check))'
    return msg

def check(func, *args):
    name = func.__name__
    err = None
    ans = None
    help_txt = None
    try:
        src = inspect.getsource(func)
    except:
        src = None

    try:
        ans = func(*args)
            
        print_pos(func, ans)
        
    except Exception as err:
        help_txt = print_error(err, name)

    _log_info('CHECK', func=name, err=None, ans=None, help=help_txt, src=src)

def print_pos(func, ans):
    function_ans ={'find_index_of_X':[11, 44], 'get_last_digit':'99', 'shorten_string':'Descri...', 'get_treat_divisions':None, 'get_last_character':'😎', 'create_n_random_coordinate_points':None, 'find_biggest_X_mas_treat_ever':(1245, 67), 'create_dict':None}
    
    if ans == function_ans[func.__name__]:
        print('woop! it runs! 😎')
    else:
        print('it runs! 😎 not too sure about the answer though..')
           

def print_error(err, name):
    from IPython.core.display import display, Markdown
    traceback.tb = ultratb.VerboseTB(tb_offset=1)
    traceback.tb() 
    
    help_txt = get_help(err)
    if helpful and help_txt:
        display(Markdown("<div class='alert alert-block alert-info'><img class='pull-left obligator' src='obligator-64.png' alt='🐊' /><h2 style='color:blue'>Maybe this can help? </h2></div>"))
        print(help_txt)
        b = make_feedback_button(err, name)
        if b != None:
            display(b)
        return help_txt
    else:
        return None

def ask_feedback():
    ta = ipywidgets.Textarea(
        description='Comments:',
        placeholder='write other comments here',
        disabled=False,
        #value='',
        #button_style='', # 'success', 'info', 'warning', 'danger' or ''
        #tooltips=['', '', ''],
        #icons=['check', 'check', 'times', 'question']
    )
    ta.observe(LogFeedback(ta, None, 'Overall_Comments').log, 'value', 'change')
    b = make_feedback_button(None, 'Overall')
    display(ipywidgets.VBox([ta, b]))
    
    