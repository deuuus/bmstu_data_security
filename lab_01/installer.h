#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERR_FOPEN  -1
#define ERR_FSCANF -2

#define LEN_ID 128

#define PATH_TO_ID "/var/lib/dbus/machine-id"
#define KEY_FILENAME "key.txt"

int get_key(char key[LEN_ID]);
int write_key();
int cmp_key();