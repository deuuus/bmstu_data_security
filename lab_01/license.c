#include "license.h"

int get_key(char *key)
{
    FILE *f = fopen(PATH_TO_ID, "r");
    if (!f) 
    {
        printf("Error while fopen in get_key().\n");
        return ERR_FOPEN;
    }

    int rc = fscanf(f, "%s", key);
    if (rc != 1) 
    {
        printf("Error while fscanf in get_key().\n");
        return ERR_FSCANF;
    }

    fclose(f);

    return EXIT_SUCCESS;
}

int write_key()
{
    FILE *f = fopen(KEY_FILENAME, "w");
    if (!f) 
    {
        printf("Error while fopen in write_key().\n");
        return ERR_FOPEN;
    }

    char key[LEN_ID];
    int rc = get_key(key);
    if (rc) {
        fclose(f);
        return rc;
    }

    fprintf(f, "%s", key);
    fclose(f);

    return EXIT_SUCCESS;
}

int cmp_key() 
{
    char src_key[LEN_ID];
    char dst_key[LEN_ID];

    int rc = get_key(src_key);
    if (rc) {
        return rc;
    }

    FILE *f = fopen(KEY_FILENAME, "r");
    if (!f) 
    {
        printf("Error while fopen in cmp_key().\n");
        return ERR_FOPEN;
    }

    fseek(f, 0, SEEK_END);
    long pos = ftell(f);
    if (pos == 0)
    {
        printf("Error: key file is empty.\n");
        return ERR_FEMPTY;
    }

    rewind(f);

    fscanf(f, "%s", dst_key);

    fclose(f);

    return strcmp(src_key, dst_key);
}