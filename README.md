# Overview
This repository is for the paper titled "Sensitivity Analysis of IR-based Bug Localization Techniques" 

### Repository Description
 - **analysis** : The data for "scripts > Experiments > analysis" scripts.
 - **techniques** : Previous techniques, we made it to output common result.
    * releases : The executable files for techniques
 - **scripts** : Python scripts used for the paper
    * repository : Scripts to prepare the resources to execute each technique
    * results : Scripts to collect the execution results of each technique and export to Excel
    * analysis : Scripts to analysis for the result of each technique and features extracted from resources. We apply Mann-Whitney U test, Pearson correlation and so on.
    * combine_features : Scripts to extract features from data combining bug report and source code
    * features : Scripts to extract features from bug report and source code
    * commons : Scripts to managing subjects
    * utils : Common utils
 - **packing.sh** : Shell script to pack resource data per each subject
 - **unpacking.sh** : Shell script to unpack resource data per each subject

### Understand Features
We use the results from the Understnad Tool when extracting the metric for the source code. If you don't have a license of the Understand Tool, download the archive file [understand_features](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKRURZc3hvUWxseTA), and unzip it into the features directory. To know the detail use this archive, see the replication section.     
        
### Download Subjects ( Bug and Source Repository )
We use the 46 subjects below. 

| Group                  | Subject | Repository Download    | Git Repository                           |
|:-----------------------|:--------|:-----------------------|:-----------------------------------------|
| Apache | CAMEL | [CAMEL.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdEZZZnJrWmZxWjg) | [https://github.com/apache/camel.git](https://github.com/apache/camel.git) |
| Apache | HBASE | [HBASE.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKSlZHQWhJRl96Z1U) | [https://github.com/apache/hbase.git](https://github.com/apache/hbase.git) |
| Apache | HIVE | [HIVE.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKLTF1N01Zd3UtTWs) | [https://github.com/apache/hive.git](https://github.com/apache/hive.git) |
| Commons | CODEC | [CODEC.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKeVh5UjF4NXRJQU0) | [https://github.com/apache/commons-codec.git](https://github.com/apache/commons-codec.git) |
| Commons | COLLECTIONS | [COLLECTIONS.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKTWRmTFIxUEN4dWM) | [https://github.com/apache/commons-collections.git](https://github.com/apache/commons-collections.git) |
| Commons | COMPRESS | [COMPRESS.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdXlFUEY2NkQxbUk) | [https://github.com/apache/commons-compress.git](https://github.com/apache/commons-compress.git) |
| Commons | CONFIGURATION | [CONFIGURATION.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKQTVSRWdGQmdHVzQ) | [https://github.com/apache/commons-configuration.git](https://github.com/apache/commons-configuration.git) |
| Commons | CRYPTO | [CRYPTO.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdkZiZTlCRl8xUEE) | [https://github.com/apache/commons-crypto.git](https://github.com/apache/commons-crypto.git) |
| Commons | CSV | [CSV.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKSlk4aEZZUzFSVDA) | [https://github.com/apache/commons-csv.git](https://github.com/apache/commons-csv.git) |
| Commons | IO | [IO.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKVkMtN0ZEcWhaNlU) | [https://github.com/apache/commons-io.git](https://github.com/apache/commons-io.git) |
| Commons | LANG | [LANG.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKMVJKZEllUGVBZVU) | [https://github.com/apache/commons-lang.git](https://github.com/apache/commons-lang.git) |
| Commons | MATH | [MATH.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKYzU1MWo2cWMxZHc) | [https://github.com/apache/commons-math.git](https://github.com/apache/commons-math.git) |
| Commons | WEAVER | [WEAVER.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKN085ZGtJTVJ1emc) | [https://github.com/apache/commons-weaver.git](https://github.com/apache/commons-weaver.git) |
| JBoss | ENTESB | [ENTESB.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKUjc0QjZHTXpxdDA) | [https://github.com/jboss-fuse/fuse.git](https://github.com/jboss-fuse/fuse.git) |
| JBoss | JBMETA | [JBMETA.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKcW9lc212Umw2Vmc) | [https://github.com/jboss/metadata.git](https://github.com/jboss/metadata.git) |
| Wildfly | ELY | [ELY.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKbGNqRWZXa0M1MFU) | [https://github.com/wildfly-security/wildfly-elytron.git](https://github.com/wildfly-security/wildfly-elytron.git) |
| Wildfly | SWARM | [SWARM.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKZk82TWFrUERFckU) | [https://github.com/wildfly-swarm/wildfly-swarm.git](https://github.com/wildfly-swarm/wildfly-swarm.git) |
| Wildfly | WFARQ | [WFARQ.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKYTBoUU12cGFlckk) | [https://github.com/wildfly/wildfly-arquillian.git](https://github.com/wildfly/wildfly-arquillian.git) |
| Wildfly | WFCORE | [WFCORE.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKNDhzSzY4bU8yejg) | [https://github.com/wildfly/wildfly-core.git](https://github.com/wildfly/wildfly-core.git) |
| Wildfly | WFLY | [WFLY.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKTTllanRER3JqQVU) | [https://github.com/wildfly/wildfly.git](https://github.com/wildfly/wildfly.git) |
| Wildfly | WFMP | [WFMP.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKX05GNllYdkFmdHM) | [https://github.com/wildfly/wildfly-maven-plugin.git](https://github.com/wildfly/wildfly-maven-plugin.git) |
| Spring | AMQP | [AMQP.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKeWRaaXV3dzNnazg) | [https://github.com/spring-projects/spring-amqp](https://github.com/spring-projects/spring-amqp) |
| Spring | ANDROID | [ANDROID.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKNS1mUXYtSWZiVG8) | [https://github.com/spring-projects/spring-android](https://github.com/spring-projects/spring-android) |
| Spring | BATCH | [BATCH.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKX0oyLTI0LWUtY2c) | [https://github.com/spring-projects/spring-batch](https://github.com/spring-projects/spring-batch) |
| Spring | BATCHADM | [BATCHADM.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKZ2VwYndrdVlMUlU) | [https://github.com/spring-projects/spring-batch-admin](https://github.com/spring-projects/spring-batch-admin) |
| Spring | DATACMNS | [DATACMNS.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKSGlld1g2ck91eG8) | [https://github.com/spring-projects/spring-data-commons](https://github.com/spring-projects/spring-data-commons) |
| Spring | DATAGRAPH | [DATAGRAPH.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKVC16TXA3S1lqbWc) | [https://github.com/spring-projects/spring-data-neo4j](https://github.com/spring-projects/spring-data-neo4j) |
| Spring | DATAJPA | [DATAJPA.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKS29vYUFrTHRmVE0) | [https://github.com/spring-projects/spring-data-jpa](https://github.com/spring-projects/spring-data-jpa) |
| Spring | DATAMONGO | [DATAMONGO.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKTkoxb043RkdrSTg) | [https://github.com/spring-projects/spring-data-mongodb](https://github.com/spring-projects/spring-data-mongodb) |
| Spring | DATAREDIS | [DATAREDIS.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKQUc1T1VyOHVHUEE) | [https://github.com/spring-projects/spring-data-redis](https://github.com/spring-projects/spring-data-redis) |
| Spring | DATAREST | [DATAREST.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKbUU3aWI2QkdOdGM) | [https://github.com/spring-projects/spring-data-rest](https://github.com/spring-projects/spring-data-rest) |
| Spring | LDAP | [LDAP.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKcTRGd1k2VmoxWUE) | [https://github.com/spring-projects/spring-ldap](https://github.com/spring-projects/spring-ldap) |
| Spring | MOBILE | [MOBILE.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKNWpuMXUzY2lpRVk) | [https://github.com/spring-projects/spring-mobile](https://github.com/spring-projects/spring-mobile) |
| Spring | ROO | [ROO.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKZEZfUUNlcmtIYjA) | [https://github.com/spring-projects/spring-roo](https://github.com/spring-projects/spring-roo) |
| Spring | SEC | [SEC.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKRnNzQ1hDS1JUcGs) | [https://github.com/spring-projects/spring-security](https://github.com/spring-projects/spring-security) |
| Spring | SECOAUTH | [SECOAUTH.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKX2V4Q1Q3czhhbkE) | [https://github.com/spring-projects/spring-security-oauth](https://github.com/spring-projects/spring-security-oauth) |
| Spring | SGF | [SGF.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKYzZ6Y1FydjNuQWs) | [https://github.com/spring-projects/spring-data-gemfire](https://github.com/spring-projects/spring-data-gemfire) |
| Spring | SHDP | [SHDP.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKQk1sZ0RtVGVVejg) | [https://github.com/spring-projects/spring-hadoop](https://github.com/spring-projects/spring-hadoop) |
| Spring | SHL | [SHL.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKZWhKbm9SWC1NRFk) | [https://github.com/spring-projects/spring-shell](https://github.com/spring-projects/spring-shell) |
| Spring | SOCIAL | [SOCIAL.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKajNvYndiQno1Qnc) | [https://github.com/spring-projects/spring-social](https://github.com/spring-projects/spring-social) |
| Spring | SOCIALFB | [SOCIALFB.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKVmZsc2kxQnNXdUE) | [https://github.com/spring-projects/spring-social-facebook](https://github.com/spring-projects/spring-social-facebook) |
| Spring | SOCIALLI | [SOCIALLI.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKVDBLbFNlMzdCc3c) | [https://github.com/spring-projects/spring-social-linkedin](https://github.com/spring-projects/spring-social-linkedin) |
| Spring | SOCIALTW | [SOCIALTW.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKd1g0SzVFazRzZzA) | [https://github.com/spring-projects/spring-social-twitter](https://github.com/spring-projects/spring-social-twitter) |
| Spring | SPR | [SPR.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKYmlsbkpkVjltN0E) | [https://github.com/spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) |
| Spring | SWF | [SWF.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKM3VKQVFqakJKUUk) | [https://github.com/spring-projects/spring-webflow](https://github.com/spring-projects/spring-webflow) |
| Spring | SWS | [SWS.tar](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKYUxaUnpWT2FnVlE) | [https://github.com/spring-projects/spring-ws](https://github.com/spring-projects/spring-ws) |
 


# Replication

### Install indri
- To execute BLUiR and AmaLgam, you need to install indri following commands.
- I selected indri-5.6 version because upper versions couldn't compile. (if you can compile the upper version, I think that is better)
- The end of the installation, memorize the path in the first line in the "make install" log. (In my case, /usr/local/bin.  This is installed indri path)
- And then, Change Settings.txt file.


    // Install g++ and make for indri
    $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    $ sudo apt-get update
    $ sudo apt-get install g++
    $ sudo apt-get install make
    $ sudo apt-get install --reinstall zlibc zlib1g zlib1g-dev
    
    // download and install indri
    $ wget https://downloads.sourceforge.net/project/lemur/lemur/indri-5.6/indri-5.6.tar.gz
    $ tar -xvf indri-5.6.tar.gz
    $ cd indri-5.6
    $ ./configure
    $ make
    $ make install
       /usr/bin/install -c -m 755 -d /usr/local/bin
       /usr/bin/install -c -m 755 -d /usr/local/include
       /usr/bin/install -c -m 755 -d /usr/local/include/indri
       ...
       ...
       /usr/bin/install -c -m 644 Makefile.app /usr/local/share/indri
    
    // changeSettings.txt file
    $ cd ~/irblsensitivity/techniques/releases      # We assume you cloned our repository to 
    $ vi Settings.txt
       indripath=/usr/local/bin/   <-- edit this value as a the first log of "make install"

### Install java and python
* I used java8 and python2.7
* If your system have already installed, skip this part after only checking the python dependencies


    // install java
    $ sudo apt-get install python-software-properties
    $ sudo add-apt-repository ppa:webupd8team/java
    $ sudo apt-get update
    $ sudo apt-get install oracle-java8-installer
    
    // install python
    $ sudo add-apt-repository ppa:fkrull/deadsnakes
    $ sudo apt-get update
    $ sudo apt-get install python2.7 python
    $ sudo apt-get install python-pip
    
    // install python dependencies
    $ pip install numpy scipy matplotlib pytz GitPython bs4 xlswriter nltk
    $ python -m nltk.downloader all     // NLTK Data download. Reference : http://www.nltk.org/data.html


### Preparing resources 
* Clone this repositoy


    $ git clone https://github.com/irblsensitivity/irblsensitivity.git IRBL
    
    
* Download subjects from the table in section of Download Subjects and save them to in the cloned repository path (In my case, save it to _archives directory).

    
    $ git clone https://github.com/irblsensitivity/irblsensitivity.git IRBL
    $ cd IRBL
    IRBL$ mkdir _archives
    IRBL$ cd _archives
    IRBL/_archives$ mkdir Apache 
    IRBL/_archives$ cd Apache
    IRBL/_archives/Apache$ wget -O CAMEL.tar "https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdEZZZnJrWmZxWjg"
    ....work recursively....
    IRBL$ mkdir data
    IRBL$ ./unpacking.sh _archives data

    
* Update PATH information
    - In the Subject.py file, There are  

* Inflating the source codes
    - We used multiple version of source code for experiment.
    - Because the provided subjects has only git repository, you need to check out and copy for each version that is used in experiment.

    
    IRBL$ cd scripts
    IRBL/scripts$ python launch_GitInflator.py
    
    IRBL/_archives/Apache$ wget -O CAMEL.tar "https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdEZZZnJrWmZxWjg"
    ....work recursively....
    IRBL$ mkdir data
    IRBL$ ./unpacking.sh _archives data
    
    
* Make bug repository
    - The works already done in provided subjects.
* Update count information of bug and source codes



### Feature Extraction
features : BugFeatures--> BugCorpus --> SourceFeatures --> SourceCorpus --> MethodFeatures
combine_features : SummaryBugFeatures --> SummaryCodeFeatures --> SummaryDuplicatesBugFeatures


