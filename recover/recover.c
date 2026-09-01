#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    if (card == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // Keep track of JPEG number
    int jpeg_count = 0;

    // File pointer for current JPEG
    FILE *jpg = NULL;

    // Filename
    char filename[8];

    // Read the memory card block by block
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check if this is the start of a JPEG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous JPEG
            if (jpg != NULL)
            {
                fclose(jpg);
            }

            // Create filename
            sprintf(filename, "%03i.jpg", jpeg_count);

            // Open new JPEG
            jpg = fopen(filename, "w");

            jpeg_count++;
        }

        // Write block to JPEG
        if (jpg != NULL)
        {
            fwrite(buffer, 1, 512, jpg);
        }
    }

    // Close last JPEG
    if (jpg != NULL)
    {
        fclose(jpg);
    }

    // Close memory card
    fclose(card);

    return 0;
}
