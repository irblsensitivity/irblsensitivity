# Overview
This repository shares data and code used for paper titled "Sensitivity Analysis of IR-based Bug Localization Techniques". 


### Repository Description
 - **analysis**: The data for "scripts > Experiments > analysis" scripts.
 - **techniques**: Previous techniques, we made it to output common result.
    * releases: The executable files for each technique.
 - **scripts**: Python scripts used for the paper.
    * repository: Scripts to prepare the resources to execute each technique.
    * results: Scripts to collect the execution results of each technique and export to Excel.
    * analysis: Scripts to analysis for the result of each technique and features extracted from resources. <br /> 
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;We applied Mann-Whitney U test, Pearson correlation and so on.
    * combine_features: Scripts to extract features from data combining bug report and source code.
    * features: Scripts to extract features from bug report and source code.
    * commons: Scripts to managing subjects and common functions.
    * utils: Personal libraries for experiments.
 - **packing.sh**: Shell script to pack resource data per each subject.
 - **unpacking.sh**: Shell script to unpack resource data per each subject.

### Understand Features
We used the results from the [Understnad](https://scitools.com/) tool to extract the metrics for the target code. 
If you don't have a license of the Understand tool, download the archive file [understand_features](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKRURZc3hvUWxseTA), and extract it into the features directory. 
To apply this archive, You can find in the replication section.     
        
### Subjects ( Bug and Source Code Repository )
We used the 46 subjects below the table. 
The subjects classified into 5 groups to manage them. 
Each of the archive contains bug reports, bug report repositories that we made, cloned git repository and metadata of them that we made. 


| Group                  | Subject | Archive       | Git Repository                           |
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
All the experiments are executed in Ubuntu 16.04 LTS.

### Install indri
- To execute BLUiR and AmaLgam, you need to install indri.
- Since there are compile problems, we chose indri-5.6 version. (if you can compile the upper version, I think that is better)
- In the installing process, please memorize the path in the first line in the "make install" log. <br />
(In my case, /usr/local/bin.  This is the installed path of indri)
- And then, Change Settings.txt file.
- Command to install indri
> // Install g++ and make for indri <br />
> $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test <br />
> $ sudo apt-get update <br />
> $ sudo apt-get install g++ <br />
> $ sudo apt-get install make <br />
> $ sudo apt-get install --reinstall zlibc zlib1g zlib1g-dev <br />
> <br />
> // download and install indri <br />
> $ wget https://downloads.sourceforge.net/project/lemur/lemur/indri-5.6/indri-5.6.tar.gz <br />
> $ tar -xvf indri-5.6.tar.gz <br />
> $ cd indri-5.6 <br />
> $ ./configure <br />
> $ make <br />
> $ make install <br />
>    /usr/bin/install -c -m 755 -d /usr/local/bin <br />
>    /usr/bin/install -c -m 755 -d /usr/local/include <br />
>    /usr/bin/install -c -m 755 -d /usr/local/include/indri <br />
>    ... <br />
>    ... <br />
>    /usr/bin/install -c -m 644 Makefile.app /usr/local/share/indri <br />
>  <br />
> // changeSettings.txt file <br />
> $ cd ~/irblsensitivity/techniques/releases &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;// We assume you cloned our repository to  <br />
> $ vi Settings.txt
>    indripath=/usr/local/bin/ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<-- edit this value as a the first log of "make install" <br />

### Install java and python
* We used java 8 and python 2.7
* If you have java and python in your computer, please skip this section.
> // install java <br />
> $ sudo apt-get install python-software-properties <br />
> $ sudo add-apt-repository ppa:webupd8team/java <br />
> $ sudo apt-get update <br />
> $ sudo apt-get install oracle-java8-installer <br />
>  <br />
> // install python <br />
> $ sudo add-apt-repository ppa:fkrull/deadsnakes <br />
> $ sudo apt-get update <br />
> $ sudo apt-get install python2.7 python <br />
> $ sudo apt-get install python-pip <br />
>  <br />


### Install python libraries
> // install python dependencies <br />
> $ pip install numpy scipy matplotlib pytz GitPython bs4 xlswriter nltk <br />
> $ python -m nltk.downloader all &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; // NLTK Data download. Reference : http://www.nltk.org/data.html <br />


### Preparing resources 
* Clone the repository by using the following command. (We cloned the "IRBL" directory.)
> <br />
> $ sudo apt-get update <br />
> $ sudo apt-get install git <br />
> $ git clone https://github.com/irblsensitivity/irblsensitivity.git IRBL <br />
> <br />
    
* Download subjects' archives.
    - Download all subjects from the Subjects table and save them in the cloned repository path 
    - In our case, we save it to the IRBL/_archives directory.
    - Each subject must be stored in the group directory to which it belongs.
    - Finally, unpacking all archives by using the unpacking.sh script.
> $ cd IRBL <br />
> IRBL$ mkdir _archives <br />
> IRBL$ cd _archives <br />
> IRBL/_archives$ mkdir Apache <br /> 
> IRBL/_archives$ cd Apache <br />
> IRBL/_archives/Apache$ wget -O CAMEL.tar "https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKdEZZZnJrWmZxWjg" <br />
> ....work recursively.... <br />
> IRBL$ mkdir data <br />
> IRBL$ ./unpacking.sh _archives data <br />

    
* Update PATH information.
    - In the file scripts/commons/Subject.py, there is a resource PATH information as a string.
    - The variables are Subjects.root, Subjects.root_result, and Subjects.root_feature.
    - You should change the variables according to cloned path of IRBL repository.

* Inflate the source codes.
    - We used multiple versions of source code for the experiment.
    - Because the provided subjects have an only git repository, you need to checkout and copy it for each version that is used in our experiment.
    - The information that needs to inflate versions exists in the source code and provided subject archives.
    See a file versions.txt in any subject's data folder.
> <br />
> IRBL$ cd scripts <br />
> IRBL/scripts$ python launch_GitInflator.py <br />
> <br />
    
    
* Make bug repositories
    - We need to build repository files from crawled bug reports.
    - We are already providing the result of this works in provided subject's archives.
    
> <br />
> IRBL/scripts$ python launcher_repoMaker.py <br />
> IRBL/scripts$ python launcher_DupRepo.py <br />
> <br />
    
* Update count information of bug and source codes.
    - The script of Counting.py makes a count information for bug and source code. 
> <br />
> IRBL/scripts$ python Counting.py <br />
> <br />
    

### Feature Extraction
* To make data for analysis, you should extract features from bug reports and source codes.
* Use the scripts in scripts/features and scripts/combined_features.
* They should be executed in the following order.
    - BugFeatures--> BugCorpus 
    - SourceFeatures --> SourceCorpus --> MethodFeatures
    - SummaryBugFeatures --> SummaryCodeFeatures --> SummaryDuplicatesBugFeatures
* When you execute SourceFeatures, you need Understand tool. 
  If you don't have a license of Understand or want to use provided data, 
  please do following steps. 
    - Download the file to a directory you want. ([understand_features](https://drive.google.com/uc?export=download&id=0B78iVP5pcTfKRURZc3hvUWxseTA))<br />
    - Extract the compressed archive into the directory, "features".<br />
      This "features" directory should be same as Subjects.root_feature <br />
       $ tar xzf understand_features.tar.gz -C IRBL/features <br />


> <br />
> IRBL/scripts$ python features/BugFeatures.py <br />
> IRBL/scripts$ python features/BugCorpus.py <br />
> IRBL/scripts$ python features/SourceFeatures.py <br />
> IRBL/scripts$ python features/SourceCorpus.py <br />
> IRBL/scripts$ python features/MethodFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryBugFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryCodeFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryDuplicatesBugFeatures.py <br />
> <br />

### Execute Techniques
* Preparing
    - You need to set the PATH information and JavaOptions in the launcher_Tool.py file.
    - Open the file and check the following variables 
    - ProgramPATH: Set the release files of techniques (ex. u'~/IRBL/techniques/releases/')
	- OutputPATH: Set the result path to save output of each technique (ex. u'~/IRBL/expresults/')
	- JavaOptions: Set the java command options. (ex. '-Xms512m -Xmx4000m')
	- JavaOptions_Locus: Set the java options for Locus. Because Locus need a large memory, we separate the option. (ex. '-Xms512m -Xmx4000m')
* To get the result of each technique, you can use scripts/launcher_Tool.py.
* The script execute 6 techniques for all subjects.
* The script basically works with multiple versions of source code and bug repository. 
* Options
    - -w <work name>: \[nessessary\] The directory name that stores the results of technique. If the name starts with "Old", this script works with previous data,  otherwise works with new data.
    - -g <group name>: The specific group. When you use this option, the script works with subjects in the specified group. 
    - -p <subject name>: The specific subject. To use this option, you should specify the group name according to this subject. 
    - -t <technique name>: The specific technique. When you use this option, the script makes results of specified technique.
    - -v <version name>: The specific version. When you use this option, the script works with the specified version of source code.
    - -s: Single version mode, If this option used, the script works with only latest source code.
    - -d: If this option is specified, the script works with latest source code and each version of bug repository. This option is for the single version mode.
    - -m: If this option is specified, Use merged repository of duplicated bug.
* Examples
> <br />
> IRBL/scripts$ python launcher_Tool.py -w NewData
> IRBL/scripts$ python launcher_Tool.py -w NewDataSingle -s
> IRBL/scripts$ python launcher_Tool.py -w NewData_Locus -t Locus
> IRBL/scripts$ python launcher_Tool.py -w NewData_CAMLE -g Apache -p CAMEL
> <br />
    
