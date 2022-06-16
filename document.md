# Internal Keywords

- 0 - `CALL name [options...]` - used to denote a call to a function
- 1 - `CALLN name [options...]` - used to denote a call to a native function
- 2 - `STR constString` - used to refrence a string (string must be quoted if it contains spaces)
- 3 - `VAR variableName` - refrence to a variable (needs a name or number)
- 4 - `IF Value` - runs code if value is not NULL/`0`
- 5 - `OP` - see [OP codes](#op-codes) for a list of options, used for comparison
- 6 - `DEF` - opening of a function see [Defining a Function](#defining-a-function)
- 7 - `EOF` - End Of File used to refrence the end of the file (some padding afterwards to round to 8bits)
- 8 - `ES` - End Statment used to close a DEF or IF block
- 9 - `LBL` `STR label` - label of where to jump to
- A - `GOTO` `STR label` - jumps to a label
- B - `ADD` `VAR variable` `number` - adds
- C - `IMPORT` `STR name` calls the script (baisically copy/pasting it here)


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

(no OR? just add two variablesA)

# Defining a Function
