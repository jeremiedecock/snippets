#!/bin/sh

for FILE in *.dot
do
    dot -Tpng ${FILE} -o ${FILE}.png
done

# -delay 50 argument will cause a 50 hundredths of a second delay between each frame
# -loop 0 will cause the gif to loop over and over again
convert -delay 50 -loop 0 *.png digraph.gif
