# Reveal.js snippets

Official web sites:
* https://github.com/hakimel/reveal.js
* http://lab.hakim.se/reveal-js/

## (Efficient) Reveal.js installation

The "official" way to install Reveal.js is described there:
https://github.com/hakimel/reveal.js#installation

But this official procedure is not very convenient as complained *docwhat* in
https://github.com/hakimel/reveal.js/issues/511:

> Currently, the workflow for a new slide deck is a bit of a pain:
> 
> 1. Clone the repo.
> 2. Edit the index.html
>   1. Set the author and description.
>   2. Edit the configuration if desired.
>   3. Remove all the demo slides.
>   4. Reformat if you don't like the HTML indentation.
> 3. Remove the .git directory.
> 4. git init
> 5. Commit your initial state.
> 6. Start working on the slides.
> 
> Updating reveal.js on a slide deck you've already created is also a pain
> (because of above).

*Berteh* exposed a clever solution to this problem (on the same page): 

> To me a good workflow includes using reveal as a submodule, not simply
> forking... and including this single instance of reveal.js as the engine for
> all the presentations you would create (with a global setting of some kind).
> (Thus a simple location to update).
>
> I'd typicall suggest to those that want to use github to manage their own
> presentations to 1) create a new repository, 2) clone it, 3) add reveal.js as
> a submodule, 4) make a new "blank.html" from from Hakim's index.html with
> their favorite settings, name and 5) duplicate this template for each of their
> presentation into a standalone html presentation file.
>
> in code-someting-like (for those wishing to store their own presentation in
> github)
>
> git clone https://github.com/yourUser/presentationsStockName.git
> cd presentationsStockName
> git submodule add https://github.com/hakimel/reveal.js.git reveal.js
> git submodule init
> cp reveal.js/index.html blank.html
> edit blank.html 
>
> Put in blank.html your name, favorite settings, typical title, content and
> conclusion sections, and prepend "reveal.js/" to all "css/" "lib/" "js/" and
> "plugin/"
>
> Every once in a while update your reveal.js engine with a quick git submodule
> update

But there are some drawbacks as *Jonhoo* replied:

> The big drawback of this is that speak notes don't work as the Gruntfile
> expects the presentation to be in the same directory as reveal.

An alternative is to use symlinks to keep separated the Reveal.js source code
and the slides.
