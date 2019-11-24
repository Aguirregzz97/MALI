# MALI Language

MALI is an imperative, procedural, object-oriented programming language,
compiled through Python and executed through a Python implemented virtual
machine.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<!-- **Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)* -->

- [Program structure](#program-structure)
- [Data Types](#data-types)
  - [Primitive types](#primitive-types)
    - [Literals](#literals)
  - [Class types](#class-types)
- [Scopes](#scopes)
- [Global Space Members](#global-space-members)
  - [Global Variables](#global-variables)
  - [Functions](#functions)
- [Classes](#classes)
  - [Class Members](#class-members)
  - [Access Types](#access-types)
  - [Defining a Class](#defining-a-class)
    - [Defining a Class with Inheritance](#defining-a-class-with-inheritance)
    - [Member overriding](#member-overriding)
- [Statements](#statements)
  - [Calling Functions](#calling-functions)
  - [Instantiating Classes](#instantiating-classes)
- [Control Statements](#control-statements)
  - [Condition Statement](#condition-statement)
  - [Loop Statement](#loop-statement)
- [Expressions](#expressions)
  - [Arithmetic Operators](#arithmetic-operators)
  - [Logical Operators](#logical-operators)
  - [Relational Operators](#relational-operators)
  - [Assignment Operatos](#assignment-operatos)
  - [Associativity](#associativity)
  - [Precedence](#precedence)
    - [Modifying Precedence of Operators](#modifying-precedence-of-operators)
  - [Logical Arithmetic](#logical-arithmetic)
    - [Rules to consider](#rules-to-consider)
- [Special Functions](#special-functions)
    - [Write](#write)
    - [Read](#read)
- [Comments](#comments)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Program structure

A MALI program starts with all class delcarations, followed by the declaration
of global variables, then the delcaration of functions, and finally the main
program. The only mandatory structure in a program is the main block.

1. Class Declarations
2. Global Variables Declarations
3. Functions
4. Main Function

## Data Types

### Primitive types

The MALI language allows for the following primitive types:

* Integer: positive or negative numbers, without decimals, of unlimited length.
  * E.g.: -1, 0, 1, 2, 3.
* Float: positive or negative numbers that can contain decimals.
  * E.g.: -1.5, 0, 1.5, 2.0, 3.75.
* Char: stores the unicode value for a char.
  * E.g.: '\0', 'a', 'b', 'c'.
* Bool: stores true (1) or false (0).
  * E.g.: true, fasle.

The language follows arithmetic logic: [Logical Arithmetic](#logical-arithmetic)

#### Literals

The following table explains how to represent literals:

Data Type | Representation | Example
--------- | -------------- | -------
Integer | Numeric value | 0, 1, 2, ...
Float | Numeric value with decimal points | 0, 1, 2.0, 3.5, ...
Char | Single char with single quotes | 'a', 'b', '\n'
Bool | | true, false

### Class types

Besides the primitive types, MALI allows to define class instances.

    ClassName instanceName;
    instanceName.attribute;
    instanceName.method();

* For more information on how to define classes: [Classes](#classes) <br>
* For more information on how to call instance members:
  [Instantiating Classes](#instantiating-classes)

## Scopes

The MALI language allows for both global variables and function-local variables.

## Global Space Members

### Global Variables

Global variables can be defined with the following syntax:

*data_type* = *var_name*

    var {
      int int_var1;
      float float_var;
      char char_var;
      bool bool_var;
    }

You can also declare multiple variables of the same type with the following
syntax.

    var {
      int var1, var2, var;
    }

### Functions

Functions can be defined with the following syntax:

func *return_type* *func_name* (*param1*, *param2*) { <br>
&nbsp;&nbsp; *statements* <br>
}

    func void hello_word() {
      write "Hello World!";
    }

Functions can return any primitive data type.

    func int get_one() {
      return 1;
    }

Functions can receive paramaters.

    func int calculate_area(int height, int width) {
      return height * width;
    }

## Classes

### Class Members

Class members include:

* Attributes: which are variable values owned by the class.
* Methods: which are procedures that can be executed by the class.

### Access Types

Access types for class members include:

* Public: public members can be accessed by external procedures instantiating
  the class and other classes extending it
* Private: private members cannot be accesed outside of the class.
* Protected: protected members can only be accessed outside of the class, from
  other classes extending it.

### Defining a Class

Classes can be defined with the following syntax:

class *class_name* { <br/>
&nbsp;&nbsp; \# Attributes <br>
&nbsp;&nbsp; attr { <br>
&nbsp;&nbsp;&nbsp;&nbsp;  *access_type* *data_type* *var_name*; <br>
&nbsp;&nbsp; } <br>
&nbsp;&nbsp; \# Class constructor <br>
&nbsp;&nbsp; init (*params*) { <br>
&nbsp;&nbsp;&nbsp;&nbsp; *statements* <br>
&nbsp;&nbsp; } <br>
&nbsp;&nbsp; \# Methods <br>
&nbsp;&nbsp; *acces_type* *return_type* *method_name* (*params*) { <br>
&nbsp;&nbsp;&nbsp;&nbsp; *statements* <br>
&nbsp;&nbsp; } <br>
}

    class Rectangle {
      attr {
        private float height;
        private int width;
      }

      init (int h, int w) {
        height = h;
        width = w;
      }

      public float get_area() {
        return height * width;
      }
    }

#### Defining a Class with Inheritance

You can define classes that extend other classes:

    class Square extends Rectangle {
      init (int side) : Rectangle(side, side) {

      }
    }

#### Member overriding

You can override members from inherited classes:

    class Animal {
      init () {

      }
      public void print_diet() {
        write "Omnivore";
      }
    }

    class Lion extends Animal {
      init () {

      }
      public void print_diet() {
        write "Carnivore";
      }
    }

    class Cow extends Animal {
      init () {

      }
      public void print_diet() {
        write "Hervibore";
      }
    }

## Statements

### Calling Functions

You can call functions using the following syntax:

*func_name*(*expressions*);

    calculate_area(1, 2);

### Instantiating Classes

You can instantiate classes using the dot token. You can call either methods or
attributes:

    rectangle.calculate_area(rectangle.height, rectangle.get_width());

You can instanciate instances within instances:

    client.receipt.get_total();

## Control Statements

### Condition Statement

Condition statements can be defined with the following syntax:

if (*condition*) { <br>
&nbsp;&nbsp; *statements* <br>
}

    if (2 > 1) {
      write true;
    };

You can include an else block:

    if (2 > 1) {
      write true;
    } else {
      write false;
    };

You can also include else-if blocks:

    if (a > 1) {
      write "More than 1";
    } elif (a > 2) {
      write "More than 2";
    } elif (a > 3) {
      write "More than 3";
    } else {
      write "Less than everything!";
    };

### Loop Statement

Loop statements can be defined with the following syntax:

while (*condition*) { <br>
&nbsp;&nbsp; *statements* <br>
}

    while (cont < 10) {
      write "Cycle";
      cont = cont + 1;
    };

## Expressions

### Arithmetic Operators

* Binary operators

  Operation | Token
  --------- | -----
  Addition | +
  Substraction | -
  Multiplication | *
  Division | /

* Unary operators

  Operation | Token
  --------- | -----
  Positive | +
  Negative | -

### Logical Operators

* Binary operators

  Operation | Token
  --------- | -----
  And | and
  Or | or

* Unary operators

  Operation | Token
  --------- | -----
  Not | not

### Relational Operators

* Binary operators

  Operation | Token
  --------- | -----
  More Than | >
  Less Than | <
  More or Equal Than | >=
  Less or equal Than | <=
  Equal To | ==
  Different From | <>

### Assignment Operatos

* Binary Operator

  Operation | Token
  --------- | -----
  Equal | =

### Associativity

All operators are left associative, excepto for the assignment operator, which
is right associative.

### Precedence

The next list shows the precedence of operator from higher to lower:

* not
* or
* and
* +, - (unary)
* *, /
* +, -
* \>, <, >=, <=, ==, <>
* =

#### Modifying Precedence of Operators

Use parenthesis to modify the precedence of operators in expression:

    a = 2 + 3 * 4;      # a = 14
    a = (2 + 3) * 4;    # a = 20

### Logical Arithmetic

The language follows logical arithmetic, this allows to perform any operation
with any primitive data type:

    int a;
    a = 1 + 1.5 + 'a' + true;   # The result will be caster to an integer.

#### Logical Arithmetic Rules to Consider

* Any operation can be performed with any primitive data type.
* Assigning the result of an expression will cast the result to the assigning
  data type.

      int a;
      a = 1.5;    # a will be casted to 1.

* A value of any primitive type can be assigned to any data type.

      func void foo(char c) {...}
      main {
        foo(65);
      }

    ```
    if (1) {...};

    if ('\0') {...};
    ```

  * Boolean values are casted in the following way:

      Data Type | True Values | False Values
      --------- | ----------- | ------------
      Integer | Non-zero values | zero
      Float | Non-zero values | zero
      char | Any character but null character | null character '\0'


## Special Functions

The language provides the following special functions:

#### Write

Allows you to print elements to console:

write *expressions*;

    write var_name, 1, 1.5, 'a', true, "string";

* Note that literal strings can only be used for printing. They should be
  enclosed by double quotes.

#### Read

Allows you to read user input from the console:

*var_name* = read;

    a = read;

## Comments

Use the '\#' token to write comments:

    # This is a comment.
    a = b + c;    # This is also a comment.