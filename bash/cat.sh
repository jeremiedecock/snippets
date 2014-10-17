#!/bin/sh

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
