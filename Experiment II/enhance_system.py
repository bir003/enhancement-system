# -*- coding: utf-8 -*-


import traceback
from IPython.core import ultratb
import datetime
import json
import inspect
import Edit_distance
from IPython.core.display import display, Markdown

_builtin_types = {'bool':bool, 'dict':dict, 'int':int, 'list':list, 'map':map, 'set':set, 'str':str, 'tuple':tuple}

      
class Enhance_system:
    def __init__(self, userid):
        self.userid = userid
        self.helpful = True
        try:
            self.logfile = open('experiment_2.json', 'a')
        except:
            self.logfile = None
    
    def check(self, func, *args, obj = None):
        '''Checks if the function runs, if not print_error will be called. Takes the function with it's arguments, and when dealing with a non-builtin class, an object'''
        
        error = None
        ans = None
        help_txt = None
        src = None
        try:
            name = func.__name__    
            variables = func.__code__.co_varnames
            src = inspect.getsource(func)
        except:
            src = None
        try:
            ans = func(*args)
            
        except Exception as e:
            try:
                self.print_error(e, variables, obj, src)
            except:
                print('Sorry an error occurred.')
    
        self._log_info(func=name, err= error, ans = None, help=help_txt, src=src)
    
    
    def feedback_ex_1(self, func, ans):
        '''Checks if the answer was correct for the 8 functions in ex_1 '''
        function_ans ={'find_index_of_X':[11, 44], 'get_last_digit':'99', 'shorten_string':'Descri...', 'get_treat_divisions':None, 'get_last_character':'😎', 'create_n_random_coordinate_points':None, 'find_biggest_X_mas_treat_ever':(1245, 67), 'create_dict':None}
        
        if ans == function_ans[func.__name__]:
            print('Woop! Good job! 😎')
        else:
            print('It runs! Not too sure it works as expected though.. ')
               
    
    def print_error(self, err, func_vars, obj, src):
        traceback.tb = ultratb.VerboseTB(tb_offset=1)
        traceback.tb() 
        
        enhancer = Enhancer(err, func_vars, obj, src)
        help_txt = enhancer.get_enhancement()
        
        if self.helpful and help_txt:
            display(Markdown("<div class='alert alert-block alert-info'><img class='pull-left obligator' src='obligator-64.png' alt='🐊' /><h2 style='color:blue'>Maybe this can help? </h2></div>"))
            print(self.format_return_text(help_txt))
    
            return help_txt
        else:
            return None
        
    def format_return_text(self, text):
            max_len = 120
            text = text.split(' ')
            formated_text = ''
            line = ''
            for c in text:
                if  '\n' in c:
                    if c == '\n':
                        formated_text += line + '\n'
                        line = ''
                    c = c.split('\n')
                    
                    if len(c[0])+len(line) + 1 < max_len:
                        formated_text+= line +  c[0] + '\n' 
                        line = c[1] + ' '
                    else :
                        formated_text += line + '\n' + c[0] + '\n'
                        line = c[1] + ' '
    
                elif len(line)+len(c) + 1 < max_len:
                    line += c + ' '
                else:
                    formated_text += line + '\n'
                    line = c + ' '
            formated_text += line
            return formated_text
    
    def _log_info(self, *args, **kwargs):
        entry = kwargs
        entry['time'] = datetime.datetime.now().isoformat()
        entry['username'] = self.userid
        if len(args) > 0:
            entry['values'] = args
    
        if self.logfile != None:
            print(json.dumps(entry, default=lambda x: repr(x)), file=self.logfile)
            self. logfile.flush()


        
class Enhancer:
    def __init__(self, error, func_vars, obj, src):
        self.err_type = error
        self.error = str(error)
        self.func_vars = func_vars
        self.obj = obj
        self.obj_type = obj
        self.src = src
        
        
    def get_enhancement(self):   
        if type(self.err_type).__name__ == "TypeError":
            return self._type_error_help()
    
        if type(self.err_type).__name__ == "IndexError":
            return self._index_error_help()
    
        if type(self.err_type).__name__ == "NameError":
            return self._name_error_help()
    
        if type(self.err_type).__name__ == "ZeroDivisionError":
            return self._zero_div_error_help()
        
        if type(self.err_type).__name__ == "AttributeError":
            return self._attribute_error_help()
        
        if type(self.err_type).__name__ == "KeyError":
            return self._key_error_help()
        
        if type(self.err_type).__name__ == "ValueError":
            return self._value_error_help()
       
        #Compilation errors only caught when run with eval or exec!
        if type(self.err_type).__name__ == "IndentationError":
            return self._index_error_help()
    
        if type(self.err_type).__name__ == "SyntaxError":
            return self._syntax_error_help() 

        
    def _syntax_error_help(self):
        if 'default' and 'argument' and 'before' in self.error:
            return 'All arguments given a default value (in the def function(..)) must come last in the parentheses.'
    
    def _key_error_help(self):
        return("KeyError occurs when you try to use an invalid key, meaning it probably doesn't exist. This error can be avoided by a check like for instance; if 'key_name' in dictionary.keys().")
        
    def _zero_div_error_help(self): 
        divisor_or_modular = 'divisor'
        if 'modular' or 'modulo' in self.error:
            divisor_or_modular = 'modulo'
            
        msg = 'Is the ' + divisor_or_modular + ' set to 0 somewhere by mistake? If you received the ' + divisor_or_modular + ' by parameter from outside of this function you must make sure to check that it is not zero before using it! This can be done by the following check: "if val != 0", val being the value used to divide.'
        return msg
        
        
    def _value_error_help(self):
        if 'base 10' in self.error:
            e = self.error.split("'")
            non_digit = ''
            if len(e) > 0:
                non_digit = [x for x in e[1] if x.isdigit() is False]
                val = str(e[1])
                non_digit = str(non_digit)
                non_digit = non_digit.replace('[','').replace(']','')

                msg = 'Unable to convert ' + non_digit + ' in ' + val + ' into a number. Did you mean to convert that part, if not you should remove this before attempting to convert. If it is a string you can slice out what is not a digit by using slicing - call get_meaning("slicing") to see how.'
                
                return msg
        if 'unpack' in self.error:
            return 'Unpacking values will fail if the number of values do not match the total number of values available. Check the length to see how many there is.'
        
        
    def _name_error_help(self):
        erroneous_name = self.error.split("'")
        ed = Edit_distance.Edit_distance(erroneous_name[1],self.func_vars)
        ed = ed.edit_dist()
        
        msg = 'Typical things that cause NameError is: \n1. Forgetting to give the variable a value before using it \n2. Misspelling the variable or function \n3. Simply not putting "" around the string text \n4. Not importing the module.\n\nIn case you misspelled an existing variable name, our algoritm found the following existing variable name in the function most similar: '
        msg += str(ed[0][0])
        return msg
    
    
    def _attribute_error_help(self): 
        name = ''
        obj_info = self.error.split("'") # 'int' object has no attribute 'split'
        
        obj_attribute = obj_info[3] #split
        if obj_info[1] in _builtin_types.keys():
            self.obj_type = _builtin_types[obj_info[1]] # int else custom class from tasks 
            name = self.obj_type.__name__
        else: 
            name = self.obj_type.__class__.__name__
            
        ed = Edit_distance.Edit_distance(obj_attribute,dir(self.obj_type))
        ed = ed.edit_dist()
        min_edits = ed[0][1]
        msg = 'Here it seems you trying to use an attribute on an object that does not support it, or the attribute "'+ obj_attribute +'" is misspelled. '
        if min_edits >= len(obj_attribute)-1:
            msg+= 'According to our algoritm, there are no similar attribute names available for the object ' + name
        else:
            msg+= 'According to our algoritm, this is the closest attribute option for the object ' + name + ': \n"' + str(ed[0][0]) + '". \n'
        
        msg += 'Not a misspelling? Then the type of object is most likely incorrect. Attempting to use the split function on a int value will give the same error since split() can only be used on string types. If you are unsure what type each object is, you can test it by printing type(object_name_here) or print the object itself.'
        return msg
    
        
    def _indenation_error_help(self):
        msg = 'Remember that all code should be located one indent out from the above (closest) codeline ending on : '   
        if 'unindent' in self.error:
            msg+= 'Unindent means that the following line is should have less indentation. '
        else:
            msg+= 'Did you put in correct indentation around the given error line? '
        return msg
    
    def _index_error_help(self):
        msg = ''
        if 'out of range' in self.error:
            return 'The solution can be found by checking the length of the list (f.ex: print(len(list_name))) and the index value used inside the loop. No solution? Check for potential changes done to the list that could change the expected length. '
        else:
            msg += 'The solution can be found by checking the length of the list (f.ex: len(list_name)) against the index value used. ' 
        return msg
     
    def _type_error_help(self):
        msg = ''
        
        if '<' in self.error or '>' in self.error:
            msg+= '<, >, >=, <= can only be used to compare two objects that are comparable. For example one value of type str and one of type int are not!Make sure that the values being compared are initialized correctly. '
            
        elif 'not callable' in self.error:
            text = self.error.split("'")
            self.obj_type = text[1]
            msg = 'It probably means that you are trying to call a function when a variable with the same name is available. F.ex:\n str = "hello"\n userid = 352790\n username = str(userid) -> this code gives the same error since str is now a variable equal to "hello" and not a function. '
            msg += '\nRemember that you can double check the object type by: print(type(object_or_variable_name)).'
            return msg
        
        elif 'unsupported operand' in self.error:
            types = self.error.split("'")
            type1 = types[1]
            type2 = types[3]
            msg = 'It seems that you are trying to perform an operation between the types ' + type1 + ' and ' + type2 + '. Might you have to change one of them? '
            return msg
        
        elif 'argument' in self.error and 'takes' in self.error:
                    
            if 'class' and 'self' in self.src:
                msg += "\nDid you forget to add 'self' in the parameters? (Only when you are creating a function inside a class). \nIf not:\n"
            
            msg+= 'Based on the error messages it seems you are giving too many arguments to the given function. Make sure to check how many values a function takes in input: f.ex add(a,b) takes two arguments a and b. To check what arguments a function take, run this: \nfrom inspect import signature\nprint(signature(func_name))'
            return msg 
       
        elif 'argument' in self.error and 'missing' in self.error:
            msg+= 'It seems you are not giving enough input parameters to the function you are trying to use. Make sure to check how many values a function takes in input, f.ex add(a,b) takes two arguments a and b! '        
        
        elif ('type' and 'subscriptable') in self.error:
            msg+= 'The [] notation is used to subscript objects (usually lists, dicts, etc), str(), int(), len(), range() etc are all functions and are not subscriptable. '
        
        elif 'not iterable' in self.error:
           # type_of_obj = self.error.split("'")[1]
            msg+= 'It seems you are trying to iterate over a type that is not iterable! Remember range(int) makes a digit iterable, and range(len(list_str_name)) makes a list or a string iterable. If that did not work maybe you shold double check that you are trying to iterate over the correct value? '
        
        else:
            msg+= 'TypeError occurres when the program is expecting a certain type, but got something else! '
            if ('must be str' in self.error):
                msg += 'Maybe you should try to put str() surrounding the object. '
            else:
                msg += 'Have you forgotten to add a function like len(), or int() surrounding the value? ' 
        msg +='\nIf you are unsure what type each object is, you can test it by printing type(object_name_here) or print the object itself.'
        
        return msg
