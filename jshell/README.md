JShell
======

JShell has been made to be used interactively; it hasn't been made to be used
as a regular Unix script... But a workaround exists:

- https://stackoverflow.com/questions/44916618/how-to-execute-a-java-script-with-jshell

The shebang `#!` causes errors but as stated in the first link
(https://stackoverflow.com/a/44925456), it can be replaced by the alternative
shebang syntax `//` when Bash is used (see
https://stackoverflow.com/questions/44916618/how-to-execute-a-java-script-with-jshell#comment76843544_44925456).

For the `/exit` at the end of each script, see https://stackoverflow.com/questions/43377787/how-to-shutdown-jshell-at-the-end-of-the-script
