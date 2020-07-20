# Automating-job-searching-and-filtering

I am currently looking for a new job. What bothers me most about the job searching process is that I spend a lot of time on reading through the job descriptions of all the job posts that match my search keywords. At the same time, less than one in twenty of those jobs really matches my background or my interests. In other words, I spend most of my job searching time on scanning through those job positions that I will never apply for. Base on some background knowledge on web scraping and natural language processing (NLP), I have come up with a solution to this problem that, to the best of my knowledge, has never been reported before. I am posting this solution here to hopefully help fellow job seekers spend less time on job searching and more on other value-added activities.

Briefly, 

indeed_job_search_autosave_one_per_day_upload_github.py searchs for jobs on Indeed and save the job posts to my local computer.

daily_job_scraping_Kingson.csv is a sample of data collected by indeed_job_search_autosave_one_per_day_upload_github.py

Job Posts Screening_to_share.py compares the job posts saved locally to a dictionary I defined, which describes my work experience, skills and career expection, and scores / ranks the job posts according to how much they matches my profile.

daily_job_scraping_Kingson_scored.csv is a sample of the scored, sorted job posts data file.

I use the above two Python scripts to search and filter jobs for me daily on indeed, so that I don't need to read through the irrelevant jobs myself manually.

A walk through of the code can be found in this blog: 
https://medium.com/@ziyouguxing/automating-job-searching-and-filtering-d1ae0838c1fd


