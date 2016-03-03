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
- [ ] Entry
    - [ ] Validate / callback
    - [ ] Set value
    - [ ] Password
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
    - [ ] Export to PS file (+ ps2png.sh, ps2svg.sh, ps2vp8.sh, ps2h264.sh, ps2theora.sh, ps2gif.sh, ...)
    - [ ] Modify lines, ovals, ...
    - [ ] Polygons
    - [ ] Bezier curves (see the "smooth" parameter of lines: http://python4kids.brendanscott.com/2012/09/19/quadratic-bezier-curves/)
- [ ] Scrollbar
- [ ] Menubutton
- [ ] Spinbox
    - [ ] set value
    - [ ] validate=...
    - [ ] validatecommand=...
    - [ ] invalidcommand=...
- [ ] Dialog
    - [x] tk_chooseColor
    - [ ] tk_chooseDirectory
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

## Misc

- [ ] Full app template http://effbot.org/tkinterbook/tkinter-application-windows.htm
- [ ] How to get arguments in callbacks functions
- [ ] How to make tkinter multithread to work with pyserial, opencv, ... (cf. the Oreilly's "Python Cookbook 2nd edition" p.439)
- [ ] Bind
- [ ] Colors
    - [x] Named
    - [ ] Hexa
    - [ ] Hexa + alpha
    - [ ] Tuple (?)
- [x] Matplotlib
- [x] PIL/Pillow
- [x] Fullscreen
- [x] Keyboard events
- [ ] TTK extension (https://docs.python.org/3/library/tkinter.ttk.html)
- [ ] Zinc extension
- [ ] TkPath extension
- [ ] Write some application examples from "Tkinter GUI Application Development HOTSHOT" Bhaskar Chaudhary (Packt Publishing Ltd) 2013 (chess, music player, ...)
- [ ] Draw windows without frame (to make desklets)
- [ ] Get clic coordonates (on images, canvas, frame, ...)
- [x] Canvas animations (e.g. a clock)
- [ ] Dual screen with pyglet
- [ ] Alternatives canvas: http://wiki.tcl.tk/22235
- [ ] Web browser widget ? (webkit, ...)

