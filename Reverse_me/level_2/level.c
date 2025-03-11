#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
void ok(void)
{
    puts("Good job.");
    return;
}

void no(void)
{
    puts("Nope.");
    exit(1);
}

int main()
{
    int ret_scanf; // ebp-0xc
    char buffer2[9]; //ebp-0x1d
    char buffer[24]; //ebp-0x35
    char buffer3[4]; //ebp-0x40
    printf("Please enter key: ");
    ret_scanf = scanf("%23s", buffer);
    if (ret_scanf != 1)
    {
        no();
    }
    if (buffer[1] != '0')
    {
        no();
    }
    if (buffer[0] != '0')
    {
        no();
    }
    fflush(0);

    memset(buffer2, 0, 9);
    buffer2[0] = 'd';
    buffer3[3] = '\0';
    int value2; //ebp-0x10
    int value1; //ebp-0x14
    value1 = 2;
    value2 = 1;
    while(true)
    {
        size_t len_buffer = strlen(buffer2);
        bool status = false;
        if (len_buffer < 8)
        {
            len_buffer = strlen(buffer);
            status = value1 < len_buffer;
        }
        if (!status)
            break;
        buffer3[0] = buffer[value1];
        buffer3[1] = buffer[value1 + 1];
        buffer3[2] = buffer[value1 + 2];
        buffer2[value2] = atoi(buffer3);
        value1 +=3;
        value2++;
    }
    buffer2[value2] = '\0';

    if(!strcmp(buffer2, "delabre"))
        ok();
    else    
        no();
    return(0);
}
