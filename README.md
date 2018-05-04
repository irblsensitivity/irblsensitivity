# Overview
This repository shares data and code used for paper titled "IR-based Bug Localization: Reproducibility Study on thePerformance of State-of-the-Art Approaches" 


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
If you don't have a license of the Understand tool, download the archive file [understand_features](https://sourceforge.net/projects/irblsensitivity/files/understand_features.tar.gz), and extract it into the features directory. 
To apply this archive, You can find in the replication section.     
        
### Subjects ( Bug and Source Code Repository )
We used the 5 old subjects and the 46 new subjects in the below table.
The subjects classified into 6 groups to manage them (The Previous group is old subjects). 
Each of the archive contains bug reports, bug report repositories that we made, cloned git repository and metadata of them that we made. 


| Group                  | Subject | Archive       | Git Repository                           |
|:-----------------------|:--------|:-----------------------|:-----------------------------------------|
| Apache | CAMEL | [CAMEL.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/CAMEL.tar) | [https://github.com/apache/camel.git](https://github.com/apache/camel.git) |
| Apache | HBASE | [HBASE.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/HBASE.tar) | [https://github.com/apache/hbase.git](https://github.com/apache/hbase.git) |
| Apache | HIVE | [HIVE.tar](https://sourceforge.net/projects/irblsensitivity/files/Apache/HIVE.tar) | [https://github.com/apache/hive.git](https://github.com/apache/hive.git) |
| Commons | CODEC | [CODEC.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CODEC.tar) | [https://github.com/apache/commons-codec.git](https://github.com/apache/commons-codec.git) |
| Commons | COLLECTIONS | [COLLECTIONS.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/COLLECTIONS.tar) | [https://github.com/apache/commons-collections.git](https://github.com/apache/commons-collections.git) |
| Commons | COMPRESS | [COMPRESS.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/COMPRESS.tar) | [https://github.com/apache/commons-compress.git](https://github.com/apache/commons-compress.git) |
| Commons | CONFIGURATION | [CONFIGURATION.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CONFIGURATION.tar) | [https://github.com/apache/commons-configuration.git](https://github.com/apache/commons-configuration.git) |
| Commons | CRYPTO | [CRYPTO.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CRYPTO.tar) | [https://github.com/apache/commons-crypto.git](https://github.com/apache/commons-crypto.git) |
| Commons | CSV | [CSV.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/CSV.tar) | [https://github.com/apache/commons-csv.git](https://github.com/apache/commons-csv.git) |
| Commons | IO | [IO.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/IO.tar) | [https://github.com/apache/commons-io.git](https://github.com/apache/commons-io.git) |
| Commons | LANG | [LANG.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/LANG.tar) | [https://github.com/apache/commons-lang.git](https://github.com/apache/commons-lang.git) |
| Commons | MATH | [MATH.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/MATH.tar) | [https://github.com/apache/commons-math.git](https://github.com/apache/commons-math.git) |
| Commons | WEAVER | [WEAVER.tar](https://sourceforge.net/projects/irblsensitivity/files/Commons/WEAVER.tar) | [https://github.com/apache/commons-weaver.git](https://github.com/apache/commons-weaver.git) |
| JBoss | ENTESB | [ENTESB.tar](https://sourceforge.net/projects/irblsensitivity/files/JBoss/ENTESB.tar) | [https://github.com/jboss-fuse/fuse.git](https://github.com/jboss-fuse/fuse.git) |
| JBoss | JBMETA | [JBMETA.tar](https://sourceforge.net/projects/irblsensitivity/files/JBoss/JBMETA.tar) | [https://github.com/jboss/metadata.git](https://github.com/jboss/metadata.git) |
| Wildfly | ELY | [ELY.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/ELY.tar) | [https://github.com/wildfly-security/wildfly-elytron.git](https://github.com/wildfly-security/wildfly-elytron.git) |
| Wildfly | SWARM | [SWARM.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/SWARM.tar) | [https://github.com/wildfly-swarm/wildfly-swarm.git](https://github.com/wildfly-swarm/wildfly-swarm.git) |
| Wildfly | WFARQ | [WFARQ.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFARQ.tar) | [https://github.com/wildfly/wildfly-arquillian.git](https://github.com/wildfly/wildfly-arquillian.git) |
| Wildfly | WFCORE | [WFCORE.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFCORE.tar) | [https://github.com/wildfly/wildfly-core.git](https://github.com/wildfly/wildfly-core.git) |
| Wildfly | WFLY | [WFLY.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFLY.tar) | [https://github.com/wildfly/wildfly.git](https://github.com/wildfly/wildfly.git) |
| Wildfly | WFMP | [WFMP.tar](https://sourceforge.net/projects/irblsensitivity/files/Wildfly/WFMP.tar) | [https://github.com/wildfly/wildfly-maven-plugin.git](https://github.com/wildfly/wildfly-maven-plugin.git) |
| Spring | AMQP | [AMQP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/AMQP.tar) | [https://github.com/spring-projects/spring-amqp](https://github.com/spring-projects/spring-amqp) |
| Spring | ANDROID | [ANDROID.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/ANDROID.tar) | [https://github.com/spring-projects/spring-android](https://github.com/spring-projects/spring-android) |
| Spring | BATCH | [BATCH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/BATCH.tar) | [https://github.com/spring-projects/spring-batch](https://github.com/spring-projects/spring-batch) |
| Spring | BATCHADM | [BATCHADM.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/BATCHADM.tar) | [https://github.com/spring-projects/spring-batch-admin](https://github.com/spring-projects/spring-batch-admin) |
| Spring | DATACMNS | [DATACMNS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATACMNS.tar) | [https://github.com/spring-projects/spring-data-commons](https://github.com/spring-projects/spring-data-commons) |
| Spring | DATAGRAPH | [DATAGRAPH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAGRAPH.tar) | [https://github.com/spring-projects/spring-data-neo4j](https://github.com/spring-projects/spring-data-neo4j) |
| Spring | DATAJPA | [DATAJPA.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAJPA.tar) | [https://github.com/spring-projects/spring-data-jpa](https://github.com/spring-projects/spring-data-jpa) |
| Spring | DATAMONGO | [DATAMONGO.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAMONGO.tar) | [https://github.com/spring-projects/spring-data-mongodb](https://github.com/spring-projects/spring-data-mongodb) |
| Spring | DATAREDIS | [DATAREDIS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAREDIS.tar) | [https://github.com/spring-projects/spring-data-redis](https://github.com/spring-projects/spring-data-redis) |
| Spring | DATAREST | [DATAREST.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/DATAREST.tar) | [https://github.com/spring-projects/spring-data-rest](https://github.com/spring-projects/spring-data-rest) |
| Spring | LDAP | [LDAP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/LDAP.tar) | [https://github.com/spring-projects/spring-ldap](https://github.com/spring-projects/spring-ldap) |
| Spring | MOBILE | [MOBILE.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/MOBILE.tar) | [https://github.com/spring-projects/spring-mobile](https://github.com/spring-projects/spring-mobile) |
| Spring | ROO | [ROO.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/ROO.tar) | [https://github.com/spring-projects/spring-roo](https://github.com/spring-projects/spring-roo) |
| Spring | SEC | [SEC.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SEC.tar) | [https://github.com/spring-projects/spring-security](https://github.com/spring-projects/spring-security) |
| Spring | SECOAUTH | [SECOAUTH.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SECOAUTH.tar) | [https://github.com/spring-projects/spring-security-oauth](https://github.com/spring-projects/spring-security-oauth) |
| Spring | SGF | [SGF.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SGF.tar) | [https://github.com/spring-projects/spring-data-gemfire](https://github.com/spring-projects/spring-data-gemfire) |
| Spring | SHDP | [SHDP.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SHDP.tar) | [https://github.com/spring-projects/spring-hadoop](https://github.com/spring-projects/spring-hadoop) |
| Spring | SHL | [SHL.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SHL.tar) | [https://github.com/spring-projects/spring-shell](https://github.com/spring-projects/spring-shell) |
| Spring | SOCIAL | [SOCIAL.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIAL.tar) | [https://github.com/spring-projects/spring-social](https://github.com/spring-projects/spring-social) |
| Spring | SOCIALFB | [SOCIALFB.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALFB.tar) | [https://github.com/spring-projects/spring-social-facebook](https://github.com/spring-projects/spring-social-facebook) |
| Spring | SOCIALLI | [SOCIALLI.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALLI.tar) | [https://github.com/spring-projects/spring-social-linkedin](https://github.com/spring-projects/spring-social-linkedin) |
| Spring | SOCIALTW | [SOCIALTW.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SOCIALTW.tar) | [https://github.com/spring-projects/spring-social-twitter](https://github.com/spring-projects/spring-social-twitter) |
| Spring | SPR | [SPR.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SPR.tar) | [https://github.com/spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) |
| Spring | SWF | [SWF.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SWF.tar) | [https://github.com/spring-projects/spring-webflow](https://github.com/spring-projects/spring-webflow) |
| Spring | SWS | [SWS.tar](https://sourceforge.net/projects/irblsensitivity/files/Spring/SWS.tar) | [https://github.com/spring-projects/spring-ws](https://github.com/spring-projects/spring-ws) |
| Previous | AspectJ | [AspectJ.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/AspectJ.tar) | [https://github.com/eclipse/org.aspectj](https://github.com/eclipse/org.aspectj) |
| Previous | JDT | [JDT.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/JDT.tar) | [https://github.com/eclipse/eclipse.jdt.core](https://github.com/eclipse/eclipse.jdt.core) |
| Previous | PDE | [PDE.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/PDE.tar) | [https://github.com/eclipse/eclipse.pde.ui](https://github.com/eclipse/eclipse.pde.ui) |
| Previous | SWT | [SWT.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/SWT.tar) | [https://github.com/eclipse/eclipse.platform.swt](https://github.com/eclipse/eclipse.platform.swt) |
| Previous | ZXing | [ZXing.tar](https://sourceforge.net/projects/irblsensitivity/files/Previous/ZXing.tar) | [https://github.com/zxing/zxing](https://github.com/zxing/zxing) |



# Replication
All the experiments are executed in Ubuntu 16.04 LTS.

### Install indri
- To execute BLUiR and AmaLgam, you need to install indri.
- Since there are compile problems, we chose indri-5.6 version.
- In the installing process, please memorize the path in the first line in the "make install" log. <br />
(In my case, /usr/local/bin.  This is the installed path of indri)
- And then, Change Settings.txt file.
- Commands to install indri
> // Install g++ and make for indri <br />
> $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test <br />
> $ sudo apt-get update <br />
> $ sudo apt-get install g++ <br />
> $ sudo apt-get install make <br />
> $ sudo apt-get install --reinstall zlibc zlib1g zlib1g-dev <br />
> <br />
> // download and install indri (If you faced an error in the compiling, please try with another version.)<br />
> $ wget https://downloads.sourceforge.net/project/lemur/lemur/indri-5.6/indri-5.6.tar.gz <br />
> $ tar -xzf indri-5.6.tar.gz <br />
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
> $ vi Settings.txt <br />
> &nbsp; &nbsp; indripath=/usr/local/bin/ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<-- edit this value as a the first log of "make install" <br />
>

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


### Install python libraries
> // install python dependencies <br />
> $ pip install numpy scipy matplotlib pytz GitPython bs4 xlswriter nltk <br />
> $ python -m nltk.downloader all &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; // NLTK Data download. Reference : http://www.nltk.org/data.html <br />


### Preparing resources 
* Clone the repository by using the following command. (We cloned into the "IRBL" directory.)
> $ sudo apt-get update <br />
> $ sudo apt-get install git <br />
> $ git clone https://github.com/irblsensitivity/irblsensitivity.git IRBL <br />
    
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
    - In the file scripts/commons/Subject.py, there are variables that stores a resource PATH information as a string.
    - The variables are Subjects.root, Subjects.root_result, and Subjects.root_feature.
    - You should change the variables according to cloned path of this repository.

* Inflate the source codes.
    - We used multiple versions of source code for the experiment. 
    - The script, launcher_GitInflator.py clones a git repositories and inflates it into the multiple versions which are used in the experiment.
    - Since the provided archives have only a git repository, you need to inflate also.
    - The version information that needs to inflate exists in the Python script and provided archives.
    - The information for the inflation are in the provided scripts and archives. See a file versions.txt in any subject's data directory.
> IRBL$ cd scripts <br />
> IRBL/scripts$ python launcher_GitInflator.py <br />
    
* Build bug repositories
    - We need to build a repository for the bug reports with pre-crawled bug reports.
    - We are already providing the result of this works in provided subject's archives.
    
> IRBL/scripts$ python launcher_repoMaker.py <br />
> IRBL/scripts$ python launcher_DupRepo.py <br />
    
* Update count information of bug and source codes.
    - The script of Counting.py makes a count information for bug and source code. 
> IRBL/scripts$ python Counting.py <br />
    

### Feature Extraction
* To build data for analysis, you should extract features from bug reports and source codes.
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
       $ tar -xzf understand_features.tar.gz -C IRBL/features <br />


> IRBL/scripts$ python features/BugFeatures.py <br />
> IRBL/scripts$ python features/BugCorpus.py <br />
> IRBL/scripts$ python features/SourceFeatures.py <br />
> IRBL/scripts$ python features/SourceCorpus.py <br />
> IRBL/scripts$ python features/MethodFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryBugFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryCodeFeatures.py <br />
> IRBL/scripts$ python combine_features/SummaryDuplicatesBugFeatures.py <br />

### Execute Techniques
* To get the result of each technique, you can use scripts/launcher_Tool.py.
* Preparing step
    - You need to set the PATHs and JavaOptions in the launcher_Tool.py file.
    - Open the file, launcher_Tool.py and check the following variables 
    - ProgramPATH: Set the directory path which contains the release files of the IRBL techniques. (ex. u'~/IRBL/techniques/releases/')
    - OutputPATH: Set the result path to save output of each technique (ex. u'~/IRBL/expresults/')
    - JavaOptions: Set the java command options. (ex. '-Xms512m -Xmx4000m')
    - JavaOptions_Locus: Set the java options for Locus. Because Locus need a large memory, we separated the option. (ex. '-Xms512m -Xmx4000m')
* The script executes 6 techniques for all subjects.
* The script basically works for the multiple versions of bug repository and each of the related source codes.
* Options
    - -w <work name>: \[necessary\] With this option, users can set the ID for each experiment, and each ID is also used as a directory name to store the execution results of each Technique. Additionally, if the name starts with "Old", this script works for the previous data, otherwise works for the new data.
    - -g <group name>: A specific group. With this option, the script works for the subjects in the specified group. 
    - -p <subject name>: A specific subject. To use this option, you should specify the group name. 
    - -t <technique name>: A specific technique. With this option, the script makes results of specified technique.
    - -v <version name>: A specific version. With this option, the script works for the specified version of source code.
    - -s: Single version mode, With this option, the script works for the only latest source code.
    - -m: With this option, the bug repositories created by combining the text of duplicate bug report pairs are used instead of the normal one.


* Examples
> IRBL/scripts$ python launcher_Tool.py -w NewData <br />
> IRBL/scripts$ python launcher_Tool.py -w NewDataSingle -s <br />
> IRBL/scripts$ python launcher_Tool.py -w NewData_Locus -t Locus <br />
> IRBL/scripts$ python launcher_Tool.py -w NewData_CAMLE -g Apache -p CAMEL <br />


# Previous Techniques Load on Eclipse
We changed previous techniques on Eclipse. But we didn't include eclipse environment files (.metadata folder, .project and .classpath file) in each previous techniques folders.
 
 So, If you want to load these techniques on Eclipse, please follow next sequence.
 
 - Open Eclipse
 - Make a 'techniques' folder into workplace of Eclipse. Then .metadata folder will be created in 'techniques' folder.
 - On the 'Package Explorer' panel, Open context menu by clicking right mouse button.
 - Select 'Import', Then a pop-up windows will be placed.
 - Except BLUiR project,  choose 'General > Projects from Folder or Archive' item and click 'Next' button.
 - Designate project folder in 'techniques' and click 'Finish' button.
 - Then, the project will be loaded and be shown in the Package Explorer.
 - BLUiR is made as Maven project. So, You should import with 'Maven > Existing Maven Project'. And then, just choose project folder. You don't need to change any other options.
 - Especially BLIA project, need to add library JUnit.


