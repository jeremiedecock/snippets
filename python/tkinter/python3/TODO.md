# TODO

Reference guide:
- http://effbot.org/tkinterbook/tkinter-index.htm
- "Tkinter GUI Application Development HOTSHOT" Bhaskar Chaudhary (Packt Publishing Ltd) 2013

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
- [x] Entry
- [x] Checkbutton
- [x] Radiobutton
- [x] Scale
- [x] BitmapImage
- [x] PhotoImage
- [x] Menu
    - [x] toplevel menu
    - [x] pulldown menu
    - [x] popup menu
- [x] Listbox
- [x] Text
- [x] PanedWindow
- [x] LabelFrame
- [x] ScrolledText
- [ ] Canvas
    - [ ] Export to PS file (+ ps2png.sh, ps2svg.sh, ps2vp8.sh, ps2h264.sh, ps2theora.sh, ...)
    - [ ] Modify lines, ovals, ...
    - [ ] Polygons
    - [ ] Bezier curves (see the "smooth" parameter of lines: http://python4kids.brendanscott.com/2012/09/19/quadratic-bezier-curves/)
- [ ] Scrollbar
- [ ] Menubutton
- [ ] OptionMenu
- [ ] Spinbox
- [ ] Dialog
    - [x] tk_chooseColor
    - [ ] tk_chooseDirectory
    - [ ] tk_dialog
    - [ ] tk_getOpenFile
        - [ ] Default file
        - [ ] Default default directory
        - [ ] Default file extension
        - [ ] Open directory instead file
        - [ ] Save (file or directory) instead open
    - [ ] tk_messageBox http://effbot.org/tkinterbook/tkinter-standard-dialogs.htm http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/tkMessageBox.html
    - [ ] tk_popup

## Misc

- [ ] Full app template http://effbot.org/tkinterbook/tkinter-application-windows.htm
- [ ] How to get arguments in callbacks functions
- [ ] How to make tkinter multithread to work with pyserial, opencv, ... (cf. the Oreilly's "Python Cookbook 2nd edition" p.439)
- [ ] Bind
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
- [ ] Export canvas to files (cf. pyarm)
- [ ] Canvas animations (e.g. a clock)
- [ ] Dual screen with pyglet
- [ ] Alternatives canvas: http://wiki.tcl.tk/22235
- [ ] Web browser widget ? (webkit, ...)

