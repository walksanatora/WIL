# Internal Keywords

- 00 - `CALL name [options...]` - used to denote a call to a function
- 01 - `CALLN name [options...]` - used to denote a call to a native function
- 02 - `STR constString` - used to refrence a string (string must be quoted if it contains spaces)
- 03 - `VAR variableName` - refrence to a variable (needs a name or number)
- 04 - `IF Value` - runs code if value is not NULL/`0`
- 05 - `OP` - see [OP codes](#op-codes) for a list of options, used for comparison
- 06 - `DEF` - opening of a function see [Defining a Function](#defining-a-function)
- 07 - `CDEF` - opening of a class see [Defining a Class](#defining-a-class)
- 08 - `EOF` - End Of File used to refrence the end of the file and determines
- 09 - `ES` - End Statment used to close a (C)DEF or IF block
- 0A - `LBL` `STR label` - label of where to jump to
- 0B - `GOTO` `STR label` - jumps to a label
- 0C - `MATH` `VAR variable` `op` `number` - performs math see 
- 0D - `IMPORT` `STR name` - imports the scripe see [Importing another file](#importing-another-file) for more information
- 0E - `RETURN` `value` - returns a value froma function/module


# Math Operations
if a number is divided and is a decimal it gets rounded to the nearest whole
if a number becomes negative it is 0
- `0` var = var + a
- `1` var = var - a
- `2` var = a - var
- `3` var = var * a
- `4` var = var / a
- `5` var =	a / var
- `6` var = var%a
- `7` var = a%var
- `8` var = var^a
- `9` var = a^var


# OP codes
IF statments go through if the value is not `0`
OP just is a builtin to make this easier
```
IF OP # A B
```
- `0` not A  #can be used to check if a variable is unset
- `1` A < B
- `2` A = B
- `3` A > B
- `4` A and B
- `5` A xor B

(no OR? just add two variables)

to allow OP codes on your classes give it a function like
```
DEF op_0 CDEF class self other
	RETURN 1
ES
```

# Defining a Function

function which takes then returns a string with unused number and class args
```
DEF function STR string number CDEF class Class #create a function named function
	RETURN string
EF #close the function
```

if you were to say omit any value aside from `string` (which would be understandable since they are not used)
it will use the default value which is
"" for string
0 for numbers
dependant on the class

Functions can accept *less* arguments then specified but never more

# Defining a Class

```
CDEF class #create a new class called name

	STR string = "ohno" #class has a STR object names string
	number = 123 #class has a number named number
	CDEF class customClass #class has a name object named customClass

	DEF name @name self STR string number CDEF name customClass #function to generate new class FUNCTION MUST HAVE ATLEAST ONE ARGUMENT FOR IT'S SELF
		self.string = string #set the string value
		self.number = number #set the number
		self.customClass = custom class #set the class
	ES
ES
```

# Importing another file

main.ils
```
IMPORT STR "module" #or IMPORT STR "module.ils" same diffrence
IMPORT STR "moduel" STR "duel" #import moduel under the name duel

CALLN STR "print" CALL module.hello 
CALLN STR "print" CALL duel.time

EOF
```
module.ils
```
CDEF module
	DEF hello
		RETURN STR "HELLO WORLD!" 
	ES
ES
RETURN module
EOF
```
moduel.ils
```
CDEF module
	DEF time
		RETURN STR "TIME TO DUEL!!!"
	ES
ES
RETURN module
EOF
```

when importing a module the `EOF` of the file will return the module