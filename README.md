interpreter
===========

stack based language, uses reverse polish notation mostly.
you can call another file that shares the same stack with @
if, for, while statements, these statemenst can also call another file.
this language has variables the can be named, retrieved and edited.
calls to another file

hello world example:

:hello $s :world .. .. echo

:4 - adds 4 to the stack

:hello - adds hello to the stack

$hello - fetches the variable hello and adds it to the stack

=hello - set hello to a value from the stack

@hello - run the file with the name hello

instructions:

echo - prints the last stack item to the console

rnd - pops 2 numbers, they specify the random number's min and max values then a random number is added to the stack

info - prints debugging info to the screen

math instructions:

plus - pops 2 numbers, adds them together then pushes the result

minus - pops 2 numbers, subtracts the right number from the left then pushes the result

multiply - pops 2 numbers, multiplies them together then pushes the result

divide - pops 2 numbers, divides the left number by the right then pushes the result

% - pops 2 numbers, pushes the remainder of the left number being divided by the right

** - pops 2 numbers, rises the left number by the right then pushes the result

or - if either of the values are true it evaluatates to true

! - turns a positive number negative and a negative number positive

sqrt - pops a number, pushes the square root of the number

cos - pops a number, pushes the cosine of the number

sin - pops a number, pushes the sine of the number

tan - pops a number, pushes the tangent of the number

dist - pops 4 numbers, x0 y0 x1 y1 pushes the distance between the sets of coordinates

string instructions:

.. - pops 2 strings, joins them together then pushes the result

sub - pops 3 strins, pushes the result of a substition regex

basic instructions:

dup - duplicates the last stack item by adding another to the stack

swap - swaps the last 2 values in the stack

branching/looping/equality instructions:

== - pops 2 values, pushes True onto the stack if the values are equal, else pushes False

!= - pops 2 values, pushes True onto the stack if the values are not equal, else pushes False

< - pops 2 values, pushes True if the left value is less than the right, else pushes False

> - pops 2 values, pushes True if the left value is greater than the right, else pushes False

<= - pops 2 values, pushes True if the left value is less than or equal to the right, else pushes False

>= - pops 2 values, pushes True if the left value is greater than or equal to the right, else pushes False

in - pushes user input

for - pops 3 values, the 1st is the memory index of the variable, the 2nd is the number to go to, the 3rd is the address to be looped over, increments variable until its greater or equal to the end variable

while - pops 2 values, the 1st is the memory index of the variable when it is false the loop ends, the 2nd is the file to be looped over

if - pops 2 values, the first is the condition, if it is true the 2nd value is used as an address of a file to be called

built in memory values:

true - True

false - False

pi - 3.14...

s - ' ' space to be concatenated onto strings








