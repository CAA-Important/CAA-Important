/*
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 *    GA_Stacking.java
 *    Copyright (C) 1999-2012 University of Waikato, Hamilton, New Zealand
 *
 */
//Adjust for classifier array
package weka.classifiers.meta;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.ArrayList;

import java.util.Collections;
import java.util.Enumeration;
import java.util.List;
import java.util.Random;
import java.util.Vector;
import java.util.concurrent.Executors;

import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.RandomizableParallelMultipleClassifiersCombiner;
import weka.classifiers.misc.InputMappedClassifier;
import weka.classifiers.rules.ZeroR;
import weka.core.*;
import weka.core.Capabilities.Capability;
import weka.core.TechnicalInformation.Field;
import weka.core.TechnicalInformation.Type;

import io.jenetics.BitChromosome;
import io.jenetics.BitGene;
import io.jenetics.Genotype;
import io.jenetics.engine.Engine;
import io.jenetics.engine.EvolutionResult;
import io.jenetics.engine.Limits;
import io.jenetics.util.Factory;

/**
 <!-- globalinfo-start -->
 * Combines several classifiers using the stacking method. Can do classification or regression.<br/>
 * <br/>
 * For more information, see<br/>
 * <br/>
 * David H. Wolpert (1992). Stacked generalization. Neural Networks. 5:241-259.
 * <p/>
 <!-- globalinfo-end -->
 *
 <!-- technical-bibtex-start -->
 * BibTeX:
 * <pre>
 * &#64;article{Wolpert1992,
 *    author = {David H. Wolpert},
 *    journal = {Neural Networks},
 *    pages = {241-259},
 *    publisher = {Pergamon Press},
 *    title = {Stacked generalization},
 *    volume = {5},
 *    year = {1992}
 * }
 * </pre>
 * <p/>
 <!-- technical-bibtex-end -->
 *
 <!-- options-start -->
 * Valid options are: <p/>
 * 
 * <pre> -M &lt;scheme specification&gt;
 *  Full name of meta classifier, followed by options.
 *  (default: "weka.classifiers.rules.Zero")</pre>
 * 
 * <pre> -X &lt;number of folds&gt;
 *  Sets the number of cross-validation folds.</pre>
 * 
 * <pre> -S &lt;num&gt;
 *  Random number seed.
 *  (default 1)</pre>
 * 
 * <pre> -B &lt;classifier specification&gt;
 *  Full class name of classifier to include, followed
 *  by scheme options. May be specified multiple times.
 *  (default: "weka.classifiers.rules.ZeroR")</pre>
 * 
 * <pre> -D
 *  If set, classifier is run in debug mode and
 *  may output additional info to the console</pre>
 * 
 <!-- options-end -->
 *
 * @author Eibe Frank (eibe@cs.waikato.ac.nz)
 * @version $Revision: 12205 $ 
 */
public class Missing_Member_RR_GA_Stacking 
  extends RandomizableParallelMultipleClassifiersCombiner
  implements TechnicalInformationHandler{

  /** for serialization */
  static final long serialVersionUID = 5134738557155845452L;
  
  /** The meta classifier */
  protected Classifier m_MetaClassifier = new ZeroR();
 
  /** Format for meta data */
  protected Instances m_MetaFormat = null;

  /** Format for base data */
  protected Instances m_BaseFormat = null;

  /** Set the number of folds for the cross-validation */
  protected int m_NumFolds = 10;
  
  //Static variables for use by Jenetics, the genetic algorithm library
  
  protected static Missing_Member_RR_GA_Stacking statGA;
  
  protected static Instances statNewData;
  
  protected static Instances statm_MetaFormat = null;
  
  protected static int statm_NumFolds;
  
  protected static Random statRandom;
  
  protected static Instances statTestData;
  
  protected static Instances statMetaTestData;
  
  protected static Instances m_metaData;
  
  protected static ArrayList<Double> stat_best_accuracies = new ArrayList<Double>();
  
  protected static ArrayList<Genotype<BitGene>> stat_strings = new ArrayList<Genotype<BitGene>>();
  
  protected int numGens = 30;
  
  protected int numThreads = 2;
  
  //Arraylists to hold sub-ensembles and their information
  
  protected static ArrayList<String> configs = new ArrayList<String>();
  
  protected static ArrayList<Stacking> subEnsembles = new ArrayList<Stacking>();
  
  protected static ArrayList<Double> accuracies = new ArrayList<Double>();
  
  protected static ArrayList<Double> memberAccuracies = new ArrayList<Double>();
  
  
  protected static Stacking Stack = new Stacking();
  
  //Variable to keep track of whether training is occurring or not
  protected boolean training;
  
  //Variable to keep track of which classifier should be removed
  protected int toRemove = 0;
  
  
  public int getnumGens() {
	  return numGens;
  }
  
  public void setNumGens(int newNumGens) {
	  if(newNumGens >= 1) {
		  numGens = newNumGens;
	  }
  }
  
  public int getNumThreads() {
	  return numThreads;
  }
  
  public void setNumThreads(int newNumThreads) {
	  numThreads = newNumThreads;
  }
  
  /**
   * Returns a string describing classifier
   * @return a description suitable for
   * displaying in the explorer/experimenter gui
   */
  public String globalInfo() {

    return "Combines several classifiers using the stacking method.  "
      + "Determines best combination of classifiers using genetic algorithms.  "
      + "Can do classification or regression.\n\n"
      + "For more information, see\n\n"
      + getTechnicalInformation().toString();
  }

  /**
   * Returns an instance of a TechnicalInformation object, containing 
   * detailed information about the technical background of this class,
   * e.g., paper reference or book this class is based on.
   * 
   * @return the technical information about this class
   */
  public TechnicalInformation getTechnicalInformation() {
    TechnicalInformation 	result;
    
    result = new TechnicalInformation(Type.ARTICLE);
    result.setValue(Field.AUTHOR, "David H. Wolpert");
    result.setValue(Field.YEAR, "1992");
    result.setValue(Field.TITLE, "Stacked generalization");
    result.setValue(Field.JOURNAL, "Neural Networks");
    result.setValue(Field.VOLUME, "5");
    result.setValue(Field.PAGES, "241-259");
    result.setValue(Field.PUBLISHER, "Pergamon Press");
    
    return result;
  }
  
  /**
   * Returns an enumeration describing the available options.
   *
   * @return an enumeration of all the available options.
   */
  public Enumeration<Option> listOptions() {
    
    Vector<Option> newVector = new Vector<Option>(2);
    newVector.addElement(new Option(
	      metaOption(),
	      "M", 0, "-M <scheme specification>"));
    newVector.addElement(new Option(
	      "\tSets the number of cross-validation folds.",
	      "X", 1, "-X <number of folds>"));

    newVector.addAll(Collections.list(super.listOptions()));
    
    if (getMetaClassifier() instanceof OptionHandler) {
      newVector.addElement(new Option(
        "",
        "", 0, "\nOptions specific to meta classifier "
          + getMetaClassifier().getClass().getName() + ":"));
      newVector.addAll(Collections.list(((OptionHandler)getMetaClassifier()).listOptions()));
    }
    return newVector.elements();
  }

  /**
   * String describing option for setting meta classifier
   * 
   * @return the string describing the option
   */
  protected String metaOption() {

    return "\tFull name of meta classifier, followed by options.\n" +
      "\t(default: \"weka.classifiers.rules.Zero\")";
  }

  /**
   * Parses a given list of options. <p/>
   *
   <!-- options-start -->
   * Valid options are: <p/>
   * 
   * <pre> -M &lt;scheme specification&gt;
   *  Full name of meta classifier, followed by options.
   *  (default: "weka.classifiers.rules.Zero")</pre>
   * 
   * <pre> -X &lt;number of folds&gt;
   *  Sets the number of cross-validation folds.</pre>
   * 
   * <pre> -S &lt;num&gt;
   *  Random number seed.
   *  (default 1)</pre>
   * 
   * <pre> -B &lt;classifier specification&gt;
   *  Full class name of classifier to include, followed
   *  by scheme options. May be specified multiple times.
   *  (default: "weka.classifiers.rules.ZeroR")</pre>
   * 
   * <pre> -D
   *  If set, classifier is run in debug mode and
   *  may output additional info to the console</pre>
   * 
   <!-- options-end -->
   *
   * @param options the list of options as an array of strings
   * @throws Exception if an option is not supported
   */
  public void setOptions(String[] options) throws Exception {

    String numFoldsString = Utils.getOption('X', options);
    if (numFoldsString.length() != 0) {
      setNumFolds(Integer.parseInt(numFoldsString));
    } else {
      setNumFolds(10);
    }
    processMetaOptions(options);
    super.setOptions(options);
  }

  /**
   * Process options setting meta classifier.
   * 
   * @param options the options to parse
   * @throws Exception if the parsing fails
   */
  protected void processMetaOptions(String[] options) throws Exception {

    String classifierString = Utils.getOption('M', options);
    String [] classifierSpec = Utils.splitOptions(classifierString);
    String classifierName;
    if (classifierSpec.length == 0) {
      classifierName = "weka.classifiers.rules.ZeroR";
    } else {
      classifierName = classifierSpec[0];
      classifierSpec[0] = "";
    }
    setMetaClassifier(AbstractClassifier.forName(classifierName, classifierSpec));
  }

  /**
   * Gets the current settings of the Classifier.
   *
   * @return an array of strings suitable for passing to setOptions
   */
  public String [] getOptions() {

    String [] superOptions = super.getOptions();
    String [] options = new String [superOptions.length + 4];

    int current = 0;
    options[current++] = "-X"; options[current++] = "" + getNumFolds();
    options[current++] = "-M";
    options[current++] = getMetaClassifier().getClass().getName() + " "
      + Utils.joinOptions(((OptionHandler)getMetaClassifier()).getOptions());

    System.arraycopy(superOptions, 0, options, current, 
		     superOptions.length);
    return options;
  }
  
  /**
   * Returns the tip text for this property
   * @return tip text for this property suitable for
   * displaying in the explorer/experimenter gui
   */
  public String numFoldsTipText() {
    return "The number of folds used for cross-validation.";
  }

  /** 
   * Gets the number of folds for the cross-validation.
   *
   * @return the number of folds for the cross-validation
   */
  public int getNumFolds() {

    return m_NumFolds;
  }

  /**
   * Sets the number of folds for the cross-validation.
   *
   * @param numFolds the number of folds for the cross-validation
   * @throws Exception if parameter illegal
   */
  public void setNumFolds(int numFolds) throws Exception {
    
    if (numFolds < 0) {
      throw new IllegalArgumentException("Stacking: Number of cross-validation " +
					 "folds must be positive.");
    }
    m_NumFolds = numFolds;
  }
  
  /**
   * Returns the tip text for this property
   * @return tip text for this property suitable for
   * displaying in the explorer/experimenter gui
   */
  public String metaClassifierTipText() {
    return "The meta classifiers to be used.";
  }

  /**
   * Adds meta classifier
   *
   * @param classifier the classifier with all options set.
   */
  public void setMetaClassifier(Classifier classifier) {

    m_MetaClassifier = classifier;
  }
  
  /**
   * Gets the meta classifier.
   *
   * @return the meta classifier
   */
  public Classifier getMetaClassifier() {
    
    return m_MetaClassifier;
  }

  /**
   * Returns combined capabilities of the base classifiers, i.e., the
   * capabilities all of them have in common.
   *
   * @return      the capabilities of the base classifiers
   */
  public Capabilities getCapabilities() {
    Capabilities      result;
    
    result = super.getCapabilities();
    result.setMinimumNumberInstances(getNumFolds());

    return result;
  }
  
  /**
   * Buildclassifier selects a classifier from the set of classifiers
   * by minimising error on the training data.
   *
   * @param data the training data to be used for generating the
   * boosted classifier.
   * @throws Exception if the classifier could not be built successfully
   */
  public void buildClassifier(Instances data) throws Exception {
	  
	training = true;

    if (m_MetaClassifier == null) {
      throw new IllegalArgumentException("No meta classifier has been set");
    }

    // can classifier handle the data?
    getCapabilities().testWithFail(data);
    
    // remove instances with missing class
    Instances newData = new Instances(data);
    m_BaseFormat = new Instances(data, 0);
    newData.deleteWithMissingClass();
    
    //Split data for eval testing
    Random dataRandomizer = new Random(m_Seed);
    Instances newerData = new Instances(newData);
    newerData.randomize(dataRandomizer);
    newerData.stratify(3);
    
    Instances trainData = newerData.trainCV(3, 0);
    statTestData = newerData.testCV(3, 0);
    
    Random random = new Random(m_Seed);
    trainData.randomize(random);
    if (trainData.classAttribute().isNominal()) {
    	trainData.stratify(m_NumFolds);
    }

    // Create meta level
    generateMetaLevel(trainData, random, data);
    
    Evaluation judgeMembers = new Evaluation(statTestData);
    
    buildClassifiers(trainData);
    
    for(int i = 0; i < m_Classifiers.length; i++) {
    	judgeMembers.evaluateModel(m_Classifiers[i], statTestData);
    	double theAcc = 1 - judgeMembers.relativeAbsoluteError() / 100;
    	memberAccuracies.add(theAcc);
    }
  
    // restart the executor pool because at the end of processing
    // a set of classifiers it gets shutdown to prevent the program
    // executing as a server
    super.buildClassifier(newData); //newData?
    
    // Rebuild all the base classifiers on the full training data
    buildClassifiers(newData);
    
    //If program reaches this point, training has completed
    training = false;
    
  }

  /**
   * Generates the meta data
   * 
   * @param newData the data to work on
   * @param random the random number generator to use for cross-validation
   * @throws Exception if generation fails
   */
  
  //Put together final configuration
  //Testing round 1?
  protected void generateMetaLevel(Instances newData, Random random, Instances data) throws Exception  {
	//Setup static variables for Jenetics
	Instances metaData = metaFormat(newData);
	m_metaData = metaData;
	m_MetaFormat = new Instances(metaData, 0);
	statNewData = newData;
	statm_MetaFormat = m_MetaFormat;
	statm_NumFolds = m_NumFolds;
	statRandom = random;
	
	//Setting up genetic algorithm engine
    Factory<Genotype<BitGene>> bcGene = Genotype.of(BitChromosome.of(m_Classifiers.length, 0.5));
    Engine<BitGene, Double> engine = Engine.builder(Missing_Member_RR_GA_Stacking::eval, bcGene).executor(Executors.newFixedThreadPool(numThreads)).build();
    Genotype<BitGene> result = null;
    

      
      

      statGA = this;
      //Run genetic algorithm engine and get best result
      result = engine.stream().limit(io.jenetics.engine.Limits.bySteadyFitness(5)).limit(io.jenetics.engine.Limits.byFixedGeneration(numGens)).collect(EvolutionResult.toBestGenotype());
      //stat_best_accuracies.add(eval(result));
      //stat_strings.add(result);
    

    
   //result = stat_strings.get(stat_best_accuracies.indexOf(Collections.max(stat_best_accuracies)));
    
    
    
    
    
    //Put together final stacked ensemble
	String binary = result.toString().replace("|", "");
	//System.out.println(binary);
	
	int totClassLength = m_Classifiers.length;
	  
	  Stacking stack = new Stacking();
	  
	  ArrayList<Classifier> classifiers = new ArrayList<Classifier>();
	    
	    for(int i = 0; i < m_Classifiers.length; i++) {
	    	classifiers.add(m_Classifiers[i]);
	    }
	    
	    Classifier[] classArr = new Classifier[classifiers.size()];
	    
	    classifiers.toArray(classArr);
	    
	    stack.setClassifiers(classArr);
	    
	    
	    
	    stack.setMetaClassifier(m_MetaClassifier);
	    
	    
	    stack.setNumFolds(m_NumFolds);
	    
	    stack.buildClassifier(data);
	    
	    //This code can be used to see how many sub-ensembles were found
	    //System.out.println(configs.size());
	    
	    Stack = stack;
  
  }
  
  //Genetic algorithm performance evaluation function as required by Jenetics
  protected static double eval(Genotype<BitGene> gt){
	    
	    try {
			return evalExtend(gt, (Missing_Member_RR_GA_Stacking)weka.classifiers.AbstractClassifier.makeCopy(statGA), statNewData, statTestData, statMetaTestData, (Stacking)weka.classifiers.AbstractClassifier.makeCopy(Stack));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return 0.0;
		}
  }
  
  //Extended eval function to allow for use of additional parameters, since Jenetics does not allow for that
  protected static double evalExtend(Genotype<BitGene> gt, Missing_Member_RR_GA_Stacking ga, Instances newData, Instances test, Instances metaTest, Stacking stack) throws Exception {
	  String binary = gt.toString().replace("|", "");
	  binary = binary.substring(1, binary.length() - 2);
	  //System.out.println(binary);
	  Classifier[] temp = ga.m_Classifiers;
	  
	  //Setup the sub-ensemble
	  
	  ArrayList<Classifier> classifiers = new ArrayList<Classifier>();
	    
	    for(int i = 0; i < ga.m_Classifiers.length; i++) {
	    	if(binary.charAt(i) == '1') {
	    		classifiers.add(weka.classifiers.AbstractClassifier.makeCopy(ga.m_Classifiers[i]));
	    	}
	    }
	    
	    if(classifiers.size() == 0) {
	    	classifiers.add(weka.classifiers.AbstractClassifier.makeCopy(ga.m_Classifiers[0]));
	    }
	    
	    Classifier[] classArr = new Classifier[classifiers.size()];
	    
	    classifiers.toArray(classArr);
	    
	    stack.setClassifiers(classArr);
	    

	    
	    
	    stack.setMetaClassifier(weka.classifiers.AbstractClassifier.makeCopy(ga.m_MetaClassifier));
	    
	    stack.setNumFolds(ga.m_NumFolds);
	    
	    //This section is used to get the accuracies of the sub-ensembles
	    
	    //int thePlace = 0;
	    
	    stack.buildClassifier(newData);
	    
	    //thePlace++;
	    
	    Evaluation makeWeight = new Evaluation(test);
	    
	    //thePlace++;
	    
	    makeWeight.evaluateModel(stack, test);
	    
	    //thePlace++;
	    
	    
	    ga.m_Classifiers = temp;
	    
	    double toReturn = 1 - makeWeight.relativeAbsoluteError() / 100;
	    
	    //Record sub-ensemble information
	    if(!(configs.contains(binary))) {
	    	configs.add(binary);
	    	accuracies.add(toReturn);
	    	subEnsembles.add(stack);
	    }
	    
	    return(toReturn);
	    
  }
  
  
  
  

  /**
   * Returns class probabilities.
   *
   * @param instance the instance to be classified
   * @return the distribution
   * @throws Exception if instance could not be classified
   * successfully
   */
  @SuppressWarnings("finally")
public double[] distributionForInstance(Instance instance) throws Exception {	  
	String missingString = "";
	
	for(int i = 0; i < m_Classifiers.length; i++) {
		//If it's training time or member is not missing, mark it with a "1"
		//Otherwise, mark it with a "0"
		if(training || (i != toRemove)) {
			missingString = missingString + "1";
		}
		else {
			missingString = missingString + "0";
		}
	}
	
	//If training, perform as normal
	if(training) {
		return Stack.distributionForInstance(instance);
	}
	
	//If not training, update next classifier to be removed
	toRemove = (toRemove + 1) % m_Classifiers.length;
	
	//Attempt to get the best known sub-ensemble whose members are all available
	Stacking test = findBestSub(missingString);
	if(test != null) {
		return test.distributionForInstance(instance);
	}
	//If unable to find best known sub-ensemble, use best available member instead
	  int position = 0;
	  double highestAcc = -1.0;
	  for(int i = 0; i < m_Classifiers.length; i++) {
		  if(Character.compare(missingString.charAt(i), '0') == 0) {
			  continue;
		  }
		  if(memberAccuracies.get(i) > highestAcc) {
			  position = i;
			  highestAcc = memberAccuracies.get(i);
		  }
	  }
	  return m_Classifiers[position].distributionForInstance(instance);
    
  }
  
  public Stacking findBestSub(String restriction) {
	  //Function for finding best available sub-ensemble
	  int position = 0;
	  double highestAcc = -1.0;
	  for(int i = 0; i < configs.size(); i++) {
		 boolean acceptable = true;
		 String currentConfig = configs.get(i);
		 for(int j = 0; j < m_Classifiers.length; j++) {
			 char charR = restriction.charAt(j);
			 char charCC = currentConfig.charAt(j);
			 if(Character.compare(charR, '0') == 0) {
				 if(Character.compare(charCC, '1') == 0) {
					 acceptable = false;
					 break;
				 }
			 }
		 }
		 if(!acceptable) {
			 continue;
		 }
		 if(accuracies.get(i) > highestAcc) {
			 position = i;
			 highestAcc = accuracies.get(i);
		 }
	  }
	  //System.out.println(position);
	  //System.out.println(configs.get(position));
	  //System.out.println("");
	  
	  if(position < 0) {
		  return null;
	  }

	  return subEnsembles.get(position);
  }

  /**
   * Output a representation of this classifier
   * 
   * @return a string representation of the classifier
   */
  public String toString() {

	    if (m_Classifiers.length == 0) {
	      return "Stacking: No base schemes entered.";
	    }
	    if (m_MetaClassifier == null) {
	      return "Stacking: No meta scheme selected.";
	    }
	    if (m_MetaFormat == null) {
	      return "Stacking: No model built yet.";
	    }
	    String result = "Stacking\n\nBase classifiers\n\n";
	    for (int i = 0; i < m_Classifiers.length; i++) {
	      result += getClassifier(i).toString() +"\n\n";
	    }
	   
	    result += "\n\nMeta classifier\n\n";
	    result += m_MetaClassifier.toString();

	    return result;
	  }

  /**
   * Makes the format for the level-1 data.
   *
   * @param instances the level-0 format
   * @return the format for the meta data
   * @throws Exception if the format generation fails
   */
  protected Instances metaFormat(Instances instances) throws Exception {
	    ArrayList<Attribute> attributes = new ArrayList<Attribute>();
	    Instances metaFormat;

	    for (int k = 0; k < m_Classifiers.length; k++) {
	      Classifier classifier = (Classifier) getClassifier(k);
	      String name = classifier.getClass().getName() + "-" + (k+1);
	      if (m_BaseFormat.classAttribute().isNumeric()) {
		attributes.add(new Attribute(name));
	      } else {
		for (int j = 0; j < m_BaseFormat.classAttribute().numValues(); j++) {
		  attributes.add(
		      new Attribute(
			  name + ":" + m_BaseFormat.classAttribute().value(j)));
		}
	      }
	    }
	    attributes.add((Attribute) m_BaseFormat.classAttribute().copy());
	    metaFormat = new Instances("Meta format", attributes, 0);
	    metaFormat.setClassIndex(metaFormat.numAttributes() - 1);
	    return metaFormat;
	  }

  
  @Override
  public void preExecution() throws Exception {
    super.preExecution();
    if (getMetaClassifier() instanceof CommandlineRunnable) {
      ((CommandlineRunnable) getMetaClassifier()).preExecution();
    }
  }

  @Override
  public void postExecution() throws Exception {
    super.postExecution();
    if (getMetaClassifier() instanceof CommandlineRunnable) {
      ((CommandlineRunnable) getMetaClassifier()).postExecution();
    }
  }

  /**
   * Returns the revision string.
   * 
   * @return		the revision
   */
  public String getRevision() {
    return RevisionUtils.extract("$Revision: 12205 $");
  }
  
  
  

  /**
   * Main method for testing this class.
   *
   * @param argv should contain the following arguments:
   * -t training file [-T test file] [-c class index]
   */
  public static void main(String [] argv) {
    runClassifier(new Missing_Member_RR_GA_Stacking(), argv);
  }
}
