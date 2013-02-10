/* 
 * Group: display and modify the real (GID) and effective (EGID) group ID of the
 *       process.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc group.c
 * See "man 2 getgid", "man 2 getegid" and "man 2 setgid" for more info
 *
 */

#include <stdio.h>
#include <unistd.h>

int main(int argc, char * argv[])
{


    // ////////////////////// //
    
    fprintf(stdout, "Run the two following commands as root to test this program:\n"
                    "chown 1000.1000 %s\n"
                    "chmod g+s %s\n\n", argv[0], argv[0]);

    gid_t real_group_id = getgid();
    gid_t effective_group_id = getegid();

    fprintf(stdout, "Real group ID of the process (GID) = %u\n", getgid());
    fprintf(stdout, "Effective group ID of the process (EGID) = %u\n", getegid());

    // Lost privileges: Effective GID -> Real GID

    int result;

    result = setgid(real_group_id);
    fprintf(stdout,
            "\nSet EGID to the GID (lose privileges): setgid(%u) = %d [%s]\n\n",
            real_group_id, result, result==0 ? "success" : "failure");

    fprintf(stdout, "Real group ID of the process (GID) = %u\n", getgid());
    fprintf(stdout, "Effective group ID of the process (EGID) = %u\n", getegid());

    // Gain back privileges: Real GID -> Effective GID

    result = setgid(effective_group_id);
    fprintf(stdout,
            "\nSet EGID to the former EGID (gain back privileges): setgid(%u) = %d [%s]\n\n",
            effective_group_id, result, result==0 ? "success" : "failure");

    fprintf(stdout, "Real group ID of the process (GID) = %u\n", getgid());
    fprintf(stdout, "Effective group ID of the process (EGID) = %u\n", getegid());


    return 0;
}
