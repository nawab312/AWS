### Scenario ###
Your company has a web application where users upload large video files to an Amazon S3 bucket. The requirement is to automatically transcode these videos into multiple formats (e.g., 720p, 1080p) for better playback on different devices.

**Question**
- How would you design a serverless, event-driven architecture using AWS Lambda to process video files automatically?
- Since video transcoding is a compute-intensive task, would you use AWS Lambda or an alternative AWS service? Why?
- How would you ensure that this solution scales efficiently to handle thousands of uploads per day?
- What happens if the video file is too large and exceeds the AWS Lambda payload or execution time limits? How would you handle this?
- How would you implement a retry mechanism if the transcoding process fails for a particular file?
