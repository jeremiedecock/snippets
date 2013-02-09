/* 
 * Fork: display and modify the real (UID) and effective (EUID) user ID of the
 *       process.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc user.c
 * See "man 2 getuid", "man 2 geteuid" and "man 2 setuid" for more info
 *
 */

#include <stdio.h>
#include <unistd.h>

int main(int argc, char * argv[])
{
    fprintf(stdout, "Run the two following commands as root to test this program:\nchown 1000.1000 %s\nchmod u+s %s\n\n", argv[0], argv[0]);

    uid_t real_user_id = getuid();
    uid_t effective_user_id = geteuid();

    fprintf(stdout, "Real user ID of the process (UID) = %u\n", getuid());
    fprintf(stdout, "Effective user ID of the process (EUID) = %u\n", geteuid());

    // Lost privileges: Effective UID -> Real UID

    fprintf(stdout, "\nSet EUID to the UID: setuid(%u) = %d\n\n", real_user_id, setuid(real_user_id));

    fprintf(stdout, "Real user ID of the process (UID) = %u\n", getuid());
    fprintf(stdout, "Effective user ID of the process (EUID) = %u\n", geteuid());

    // Gain back privileges: Real UID -> Effective UID

    fprintf(stdout, "\nSet EUID to the former EUID: setuid(%u) = %d\n\n", effective_user_id, setuid(effective_user_id));

    fprintf(stdout, "Real user ID of the process (UID) = %u\n", getuid());
    fprintf(stdout, "Effective user ID of the process (EUID) = %u\n", geteuid());


    return 0;
}
