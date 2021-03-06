<!---
This is a comment block.
Sadly, this may not work with some parser (like the one used by GitHub).
See: http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax
-->

[//]: # (This is an other comment.)
[//]: # ( Be prudent to insert a blank line before and after this type of comments.)
[//]: # (See: http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

# Markdown snippet

See:

* [github tutorial 1](https://help.github.com/articles/markdown-basics/)
* [github tutorial 2](https://guides.github.com/features/mastering-markdown/)
* [github tutorial 3](https://help.github.com/articles/writing-on-github/)

## Tools (on Debian Gnu/Linux)

* pandoc (a document converter that can write Markdown, reStructuredText, HTML,
  LaTeX, RTF, DocBook XML, and S5)

    pandoc -o output.html input.md

## Paragraphs

Paragraph 1, blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla

Paragraph 2, blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla


## Links

### External links

[external link](https://help.github.com/articles/markdown-basics/)

### <a name="sec_anchor"></a>Internal links and anchors

[internal link](#sec_anchor)


## Lists

### Unordered lists

* item 1
* item 2
* item 3

- item 1
- item 2
- item 3

### Nested unordered lists

* item 1
    * item 1.1
    * item 1.2
    * item 1.3
* item 2
    * item 2.1
    * item 2.2
    * item 2.3
* item 3
    * item 3.1
    * item 3.2
    * item 3.3

### Ordered lists

1. item 1
2. item 2
3. item 3

### Nested ordered lists

1. item 1
    1. item 1.1
    2. item 1.2
    3. item 1.3
2. item 2
    1. item 2.1
    2. item 2.2
    3. item 2.3
3. item 3
    1. item 3.1
    2. item 3.2
    3. item 3.3

### Nested ordered and unordered lists

1. item 1
    1. item 1.1
    2. item 1.2
    3. item 1.3
2. item 2
    * item 2.1
    * item 2.2
    * item 2.3
3. item 3
    * item 3.1
    * item 3.2
    * item 3.3

## Styling text

*Italic* or **bold** text.

_Italic_ or __bold__ text.

*Italic and __bold__* text.

_Italic and **bold**_ text.

**Bold and _italic_** text.

__Bold and *italic*__ text.

## Images

![JDHP logo](http://www.jdhp.org/medias/images/header.jpeg)

## Unformat

This is an example of `<html>` tag.

## Blockquotes

As Descartes said:

> Cogito,
> ergo sum

