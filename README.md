# PicCloneDetect
Find and remove clone images from an image repository

A bit of back story:
My external hard drive where I stored all the pictures I took during my whole life got wiped accidentally (thanks to Microsoft Windows 10).
I used a commercial software to recover all the information that was recoverable on that hard drive. As you guessed it, I ended up with a huge number of files with random names which was impossible to sort. As the hard drive was constantly used for reading and writing information, what I noticed was that I could delete a considerable amount of the files as they were duplicates of other files with the same or different dimensions.
Due to the large number of files, I had to write a code that could automatically compare images and delete the duplicates.

What this code does:
This code uses the hash value to detect duplicate images, as identical images (even with different sizes) have the same hash values.
