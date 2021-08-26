# Hypotheses Testing: 2020 Presidential Election
--------

## Overview

The American National Election Studies (ANES) conducts surveys of voters in the United States, with a flagship survey occurring immediately before and after each presidential election. In this project, we will use the ANES data to answer questions about voters in the US.

This project consists of three research questions.  For each question, we will conduct a statistical analysis and generate a written report in pdf format. The pdf were generated from knitting the Rmd files, where most of the codes have been hidden.


## Data 

Data for the project were drawn from the 2020 American National Election Studies (ANES). You can access this data at [https://electionstudies.org](https://electionstudies.org). This is the official site of the ANES, a project that has [been ongoing since](https://en.wikipedia.org/wiki/American_National_Election_Studies) 1948, and federally funded by the National Science Foundation since 1977. 

There are two forms of data that are available, data that is stored in a `.dta` format, and data that is stored in a `.sav` format. In this project we've used the `.dta` format, the data will not be uploaded to Github due to exceeding the size limit. However, the codebook will be uploaded to aid understanding of the data. Because all of the variables are marked as something like, `V200002` -- which isn't very descriptive without the codebook. 

Like many modern surveys, the ANES includes survey weights, which are used to correct for differences between how frequently demographic groups appear in the sample compared to the US population (often ultimately relying on US census data).  These weights are beyond the scope of this project.

## The Research Questions

The research questions are as follows:

1. Are Democratic voters older or younger than Republican voters in 2020?
2. Did Democratic voters or Republican voters report experiencing more difficulty voting in the 2020 election?
3. Are people who believe that science is is important for making government decisions about COVID-19 more likely to disapprove of the way their governor is handling the pandemic?
