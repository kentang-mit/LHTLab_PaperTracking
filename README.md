# LHTLab_PaperTracking
A paper tracking system which collects paper from CVPR,ICCV,ICML,ICLR,NIPS and arXiv and displays the results on web.

Dependencies:
Python 2.7 and Scrapy 1.5.0(for crawlers), MySQL 5.7(for data storage), NodeJS 8.11.0(for front-end display)

To get started:
First, create a MySQL database named `academic`
Then, run 6 crawlers under dlpapercollector folder respectively. You can change some parameters to collect more/less papers from arXiv.
Finally, cd web and run
```bash
node app
```
You can see the results in http://localhost:3000. To show papers other than the person-reid topic, please modify SQLs in `app.js` by yourself.

All rights reserved by LHT's Lab, SJTU.
