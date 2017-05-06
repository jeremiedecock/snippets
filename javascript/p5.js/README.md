# P5.js

* Official web site: http://p5js.org/
* Source code: https://github.com/processing/p5.js
* Main alternative: http://processingjs.org/

## Documentation

* Get started: http://p5js.org/get-started/
* Reference: http://p5js.org/reference/
* Libraries: http://p5js.org/libraries/
* Tutorials: http://p5js.org/tutorials/
* Examples: http://p5js.org/examples/
* Books: http://p5js.org/books/

## Installation

First you have to download the *p5.js* file in this directory from
http://p5js.org/download/.
Then, to test each snippets, simply open its *index.html* file with your web
browser.

## Processing.js vs P5.js

Here is an interesting analysis taken from http://www.sitepoint.com/processing-js-vs-p5-js-whats-difference/:

    "P5.js is a direct JS port of the Processing language. Processing.js is a
    converter which interprets pure Processing code into JS on the fly. The
    latter requires you to learn Processing, but not JS, and vice versa.
    
    Live compilation vs Language Translation: Processing.js is a library which
    takes raw Processing code (which is similar to Java, with types and all) and
    converts it to JavaScript on the fly. The examples you see running in your
    browser on the Processing.js website are, in fact, pure Processing code
    translated live into JS. [...]
    
    In Processing.js, you need to define a canvas area with a data source which
    leads to a PDE file (a file with Processing source code) [...]. In P5, you
    write JS code directly, and it gets executed like any other JS file you
    include on your website.
    
    Extending: Another difference is that P5 can be extended with addon libraries.
    For example, the p5.dom.js library addition adds the option of creating and
    manipulating HTML elements with P5, adding sliders, buttons, form elements and
    much more to your sketches [...].
    
    Note that of the two, only P5 is officially supported by the Processing
    Foundation [...].
    
    The advantages of using P5 over Processing.js are:
    
    - Writing JS code you’re probably already familiar with
    - Officially supported by the Processing Foundation
    - HTML DOM manipulation with the DOM library addon
    - [...]
                    
    The advantage of using Processing.js:
                    
    - You learn Processing and can use it in environments
    - [...]"
