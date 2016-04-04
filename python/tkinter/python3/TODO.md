# TODO

## Geometry managers

- [ ] Pack Geometry Manager (fill, expand, ...) http://effbot.org/tkinterbook/pack.htm and http://www.gigante.be/python/didact_002.php
    - [ ] With 1 widget: anchor, expand, fill, ipadx, ipady, padx, pady, side
    - [ ] With 3 widgets (label): anchor, expand, fill, ipadx, ipady, padx, pady, side
    - [ ] With 4+ widgets (label): anchor, expand, fill, ipadx, ipady, padx, pady, side
- [ ] Grid Geometry Manager http://effbot.org/tkinterbook/grid.htm
- [ ] Place Geometry Manager

## Widgets

- [x] Label
- [x] Button
- [x] Frame
- [x] Checkbutton
- [x] Radiobutton
- [x] Scale
- [x] BitmapImage
- [x] PhotoImage
- [x] Menu
    - [x] toplevel menu
    - [x] pulldown menu
    - [x] popup menu
- [x] OptionMenu
- [x] Listbox
- [x] Text
- [x] PanedWindow
- [x] LabelFrame
- [x] ScrolledText
- [ ] Canvas
    - [x] Export to PS file
        - [x] ps2png.sh
        - [x] ps2pdf.sh
        - [ ] ps2svg.sh
        - [ ] ps2gif.sh
        - [ ] ps2vp8.sh
        - [ ] ps2h264.sh
        - [ ] ps2theora.sh
    - [x] Modify lines, ovals, ...
    - [x] Polygons
    - [x] Tags
    - [ ] Fix chessboard
    - [x] Item's state
    - [x] Item's activefill, activewidth, ...
    - [x] Canvas items (shapes) events (e.g. mouse clic within a polygon)
    - [ ] Mouse click event on canvas
        - [ ] Move a shape
    - [ ] Mouse event on canvas
        - [ ] Let a shape follow the mouse cursor
    - [ ] Mouse drag and drop event on items :
        - [ ] Draw (+ clean) 
        - [ ] Drag a circle
        - [ ] Drag a circle + spring effect when drop
        - [ ] Drag a circle + spring effect when drop with 4 circles (graph entièrement connecté) 
    - [ ] Mouse wheel event on canvas
    - [ ] Methods canvas.find_closest(x, y)
    - [ ] Bezier curves (see the "smooth" parameter of lines: http://python4kids.brendanscott.com/2012/09/19/quadratic-bezier-curves/)
    - [ ] TopWindow (widgets)
    - [ ] Scrollbar/scrollregion
    - [ ] Line: joinstyle, smooth, splinesteps, stipple
    - [ ] Methods canvas.canvasx(...), canvas.canvasy(...) 
    - [ ] Methods canvas.lift(...), canvas.lower(...) 
- [ ] Scrollbar
- [ ] Menubutton
- [ ] Entry
    - [ ] Validate / callback
    - [ ] Set value
    - [ ] Password
- [ ] Spinbox
    - [ ] set value
    - [ ] validate=...
    - [ ] validatecommand=...
    - [ ] invalidcommand=...
- [ ] Dialog
    - [x] tk_chooseColor
    - [ ] tk_dialog
    - [x] tk_getOpenFile
        - [x] Default file
        - [x] Default default directory
        - [x] Default file extension
        - [x] Open directory instead file
        - [x] Open multiple files
        - [x] Return file descriptor VS file path
        - [x] Save (file or directory) instead open
    - [ ] tk_messageBox http://effbot.org/tkinterbook/tkinter-standard-dialogs.htm http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/tkMessageBox.html
    - [ ] tk_popup

## Bind

- [ ] Bind

## Misc

- [ ] Full app template http://effbot.org/tkinterbook/tkinter-application-windows.htm
    - [ ] Write some application examples from "Tkinter GUI Application Development HOTSHOT" Bhaskar Chaudhary (Packt Publishing Ltd) 2013 (chess, music player, ...)
    - [ ] Find and analyse some trustworthy open source Tk apps
- [ ] How to get arguments in callbacks functions
- [ ] How to make tkinter multithread to work with pyserial, opencv, ... (cf. the Oreilly's "Python Cookbook 2nd edition" p.439)
- [ ] Colors
    - [x] Named
    - [ ] Hexa
    - [ ] Hexa + alpha
    - [ ] Tuple (?)
- [x] Matplotlib
- [x] PIL/Pillow
- [x] Fullscreen
- [x] Keyboard events
- [x] Canvas animations (e.g. a clock)
- [ ] Extensions
    - [ ] TTK extension (https://docs.python.org/3/library/tkinter.ttk.html)
        - [ ] Combobox
        - [ ] Notebook
        - [ ] Progressbar
        - [ ] Separator
        - [ ] Sizegrip
    - [ ] Zinc extension
    - [ ] TkPath extension
    - [ ] Alternatives canvas: http://wiki.tcl.tk/22235
    - [ ] Web browser widget ? (webkit, ...)
- [ ] Draw windows without frame (to make desklets) + transparent background
- [ ] Get clic coordonates (on images, canvas, frame, ...)
- [x] Dual screen with pyglet

