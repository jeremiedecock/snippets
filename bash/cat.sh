#!/bin/sh

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

cat << 'EOF' > foo
echo $SHELL
EOF

echo 
cat foo

cat << EOF >> foo
echo $SHELL
EOF

echo 
cat foo

cat << 'EOF' >> foo
echo $SHELL
EOF

echo 
cat foo

cat << 'EOF' > foo
echo $SHELL
EOF

echo 
cat foo

rm foo
