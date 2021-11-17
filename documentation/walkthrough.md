# How to use Chainsail

1. sign up on the [Chainsail website](https://chainsail.io) by clicking the "Login" button or directly [this link](https://resaas-simeon-dev.ey.r.appspot.com/login)
2. [write us an email](mailto:support@chainsail.io) so we can authorize your account to use the computing resources
3. [implement a custom probability distribution](./defining_custom_probability.md) you want to sample or stick with the default example in the following step
4. create a new sampling job by on the [Chainsail website](https://chainsail.io) by click on "Create new job" and filling out the form. Here's some help for the form fields:
   - Job name: pick any job name you want.
   - Number of production samples: make some kind of estimate of how many samples you want to have produced in the end. Chainsail will produce that number of samples and write out every 5th of these samples.
   - Maximum number of replicas: the higher this number, the better the multimodal sampling will be, but the more computation resources you will burn. Start with the default value of 10 and increase if you suspect that sampling is not correct.
   - Probability definition: enter here the URL to which you uploaded your zipped custom `probability.py` or leave the default value to sample from an example distribution (a mixture of 2D Gaussians) 
   - Dependencies: using a comma-separated list, enter any PIP-installable Python dependencies your `probability.py` requires.
If you click on "more parameters", you'll find exactly that - they are [documented elsewhere](./docs/parameters.md).
Finally, create your job by clicking the "Create job" button.
5. Start your job by clicking the corresponding button in the job table.
6. Monitor the progress of your job and the log output on the dashboard, which is accessible via the job table, too.
7. Once your job finishes, both the job table and the dashboard will show a "download" button. Clicking on it will download an archive of all the samples.
8. Unpack the downloaded sample archive and use the [sample concatenation script](./chainsail_helpers/scripts/concatenate_samples.py) to concatenate the samples.
9. [Send us feedback](mailto:support@chainsail.io) on whether Chainsail worked for you and how we can improve it :-)
