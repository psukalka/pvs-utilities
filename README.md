# If you can create it, you may break it

This is a repository to create and test utilities.
To test any hypothesis you generally need a playground or test environment.
Due to lack of this environment, there is initial friction and you can never test the hypothesis thus stalling the learning.

Purpose is to create utilities that are used in industry and store them in reusable form.
Whenever anything needs to be tested that can easily be deployed on EC2 and tested. 


## Copying data from local machine to docker or vice versa 
Sample where pg_test is the container and my_db.dump is the file to be copied 

`docker cp pg_test:/my_db.dump /home/ec2-user/my_db.dump`

`docker cp /home/ec2-user/my_db.dump pg_backup:/my_db.dump`
