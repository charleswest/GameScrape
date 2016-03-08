# GameScrape
Screen Scraper for a Video Game

This project requires opencv 3 and python 2.7.

Operation is as follows:

1.   Run CreateTestData to produce the list of correct output values for the screens we have
      captured.   This file is currently testfile.txt.

2.  Run CaptureDigits to obtain sample number from some of the screens.   We only need 0 thru 9.
    These will be written to the main directory.   They should be checked and moved to blobs.

3.  EvaluateGame looks at a screen and attempts to determine what numbers are on the screen.  It 
    returns a list of the numbers it finds.

4.  MainTestLoop runs EvaluateGame on every game to compare it's output to what we already have on
    testfile.txt.  MainTest keep a running total of correct results.

5.  AnalyseDigits runs a combination of CaptureDigits and EvaluateGame to allow faster
    experiment with:
        partitioning the input to accurately capture a digit
        thresholding the input to produce an accurate black and white mask
        different methods of comparing current possible digit with list of good digits

        current best result are 9/10 input screens correct -- on the Haar branch
 

