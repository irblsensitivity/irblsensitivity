/**
 * Copyright (c) 2014 by Software Engineering Lab. of Sungkyunkwan University. All Rights Reserved.
 * 
 * Permission to use, copy, modify, and distribute this software and its documentation for
 * educational, research, and not-for-profit purposes, without fee and without a signed licensing agreement,
 * is hereby granted, provided that the above copyright notice appears in all copies, modifications, and distributions.
 */
package edu.skku.selab.blp.blia.indexer;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import edu.skku.selab.blp.Property;
import edu.skku.selab.blp.db.dao.DbUtil;
import edu.skku.selab.blp.db.dao.SourceFileDAO;

/**
 * @author Klaus Changsun Youm(klausyoum@skku.edu)
 *
 */
public class StructuredSourceFileCorpusCreatorTest {

	/**
	 * @throws java.lang.Exception
	 */
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception {
		double alpha = 0.2;
		double beta = 0.2;
		int pastDays = 20;
		
		Property prop = Property.loadInstance(Property.ZXING);
		prop.alpha = alpha;
		prop.beta = beta;
		prop.pastDays = pastDays;

		DbUtil dbUtil = new DbUtil();
		String dbName = Property.getInstance().productName;
		boolean commitDataIncluded = false;
		dbUtil.openConnetion(dbName);
		dbUtil.initializeAllData(commitDataIncluded);
		dbUtil.closeConnection();
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void verifyCreate() throws Exception {
		StructuredSourceFileCorpusCreator structuredSourceFileCorpusCreator = new StructuredSourceFileCorpusCreator();
		String version = SourceFileDAO.DEFAULT_VERSION_STRING;
		structuredSourceFileCorpusCreator.create(version);
	}

}
