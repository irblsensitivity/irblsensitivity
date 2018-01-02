# -*- coding: utf-8 -*-
from __future__ import print_function
from commons import Subjects
from repository import GitInflator

urls={
	'HBASE':u'https://github.com/apache/hbase.git',
	'HIVE':u'https://github.com/apache/hive.git',
	'CAMEL':u'https://github.com/apache/camel.git',

	'MATH':u'https://github.com/apache/commons-math.git',
	'LANG':u'https://github.com/apache/commons-lang.git',
	'IO':u'https://github.com/apache/commons-io.git',
	'COLLECTIONS':u'https://github.com/apache/commons-collections.git',
	'CODEC':u'https://github.com/apache/commons-codec.git',
	'WEAVER':u'https://github.com/apache/commons-weaver.git',
	'CONFIGURATION':u'https://github.com/apache/commons-configuration.git',
	'CSV':u'https://github.com/apache/commons-csv.git',
	'COMPRESS':u'https://github.com/apache/commons-compress.git',
	'CRYPTO':u'https://github.com/apache/commons-crypto.git',

	'ENTESB':u'https://github.com/jboss-fuse/fuse.git',
	'JBMETA':u'https://github.com/jboss/metadata.git',

	'ELY':u'https://github.com/wildfly-security/wildfly-elytron.git',
	'SWARM':u'https://github.com/wildfly-swarm/wildfly-swarm.git',
	'WFARQ':u'https://github.com/wildfly/wildfly-arquillian.git',
	'WFCORE':u'https://github.com/wildfly/wildfly-core.git',
	'WFLY':u'https://github.com/wildfly/wildfly.git',
	'WFMP':u'https://github.com/wildfly/wildfly-maven-plugin.git',

	'ANDROID':u'https://github.com/spring-projects/spring-android',
	'AMQP':u'https://github.com/spring-projects/spring-amqp',
	'BATCH':u'https://github.com/spring-projects/spring-batch',
	'BATCHADM':u'https://github.com/spring-projects/spring-batch-admin',
	'DATACMNS':u'https://github.com/spring-projects/spring-data-commons',
	'DATAJPA':u'https://github.com/spring-projects/spring-data-jpa',
	'DATAMONGO':u'https://github.com/spring-projects/spring-data-mongodb',
	'DATAGRAPH':u'https://github.com/spring-projects/spring-data-neo4j',
	'DATAREDIS':u'https://github.com/spring-projects/spring-data-redis',
	'DATAREST':u'https://github.com/spring-projects/spring-data-rest',
	'LDAP':u'https://github.com/spring-projects/spring-ldap',
	'MOBILE':u'https://github.com/spring-projects/spring-mobile',
	'ROO':u'https://github.com/spring-projects/spring-roo',
	'SECOAUTH':u'https://github.com/spring-projects/spring-security-oauth',
	'SHL':u'https://github.com/spring-projects/spring-shell',
	'SOCIAL':u'https://github.com/spring-projects/spring-social',
	'SOCIALFB':u'https://github.com/spring-projects/spring-social-facebook',
	'SOCIALLI':u'https://github.com/spring-projects/spring-social-linkedin',
	'SOCIALTW':u'https://github.com/spring-projects/spring-social-twitter',
    'SPR':u'https://github.com/spring-projects/spring-framework',
	'SWF':u'https://github.com/spring-projects/spring-webflow',
	'SWS':u'https://github.com/spring-projects/spring-ws',
	'SGF':u'https://github.com/spring-projects/spring-data-gemfire',
	'SHDP':u'https://github.com/spring-projects/spring-hadoop',
	'SEC':u'https://github.com/spring-projects/spring-security',
	#'SOCIALGH':u'https://github.com/spring-projects/spring-social-github',
}

# Make works
import os, stat
def del_rw(action, name, exc):
	os.chmod(name, stat.S_IWRITE)
	os.remove(name)

def make():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			git = GitInflator(project, urls[project], S.getPath_base(group, project))
			git.inflate(S.versions[project])  # The items in versions is git tag name map with each version.

import shutil
def clear():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			target = S.getPath_source(group, project)
			try:
				shutil.rmtree(target, onerror=del_rw)
				print(u'removed: %s' % target)
			except Exception as e:
				print(u'failed to remove : %s' %target)

#clear()
make()

