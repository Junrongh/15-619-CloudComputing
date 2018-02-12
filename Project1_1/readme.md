##		Project 1 Big Data Analytics

###		EC2 info

AMI Detail:

	Ubuntu, username = ubuntu
		
Public DNS:
	
	ec2-54-167-36-132.compute-1.amazonaws.com
		
Public IP:
	
	54.167.36.132
			
Login & Copy:

	$ ssh -i 15619Project1.pem ubuntu@54.167.36.132
	
	$ scp -i 15619Project1.pem -r Project1 ubuntu@54.167.36.132:


<div class="panel panel-default writeup_section" data-sequence="5">
    <div class="panel-body writeuppanel">
        <h2>Data Pre-processing</h2>

<p>Pre-processing the initial data so that it is in the proper form is crucial before you can even begin analyzing it to gain any insights. <strong>Never assume that the dataset is perfectly clean and well formed.</strong> The phrase "garbage in, garbage out," points out that if your input data is malformed, you should not expect to gain insight. The phrase is also particularly applicable to data mining, machine learning or any data analysis project. Thus, the representation and quality of data must be ascertained and ensured before analyzing the data.</p>

<p>Your first task this week is to transform and filter out rows from the logs based on the following rules below.</p>

<ol>
<li><p><strong>Handle dirty data</strong>: Removing malformed data is always the very first step in data pre-processing. Some lines don't have the four columns as expected. You should filter out these lines, for example:</p>

<pre><code>en  506 0
</code></pre>

<p><strong>In data processing, you need to make sure that your code must not crash when given malformed data.</strong></p></li>
<li><p><strong>URL normalization and percent-encoding</strong>: According to <a href="https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax">RFC 3986</a>, URLs should be normalized and special characters will be converted by <a href="https://en.wikipedia.org/wiki/Percent-encoding#Percent-encoding_reserved_characters">percent-encoding</a>.</p>

<p>For example, user talk created by <code>K6ka</code> with the title</p>

<pre><code>User talk:K6ka
</code></pre>

<p>actually matches this URL:</p>

<pre><code>https://en.wikipedia.org/wiki/User_talk%3AK6ka
</code></pre>

<p>Although <code>%</code> percent encoded titles are expected in URLs, decoded titles are expected in pageview logs. Due to arbitrary user behavior and third-party usage, various titles pointing to the same page still exist for some pages, such as <code>Special%3ASearch</code> and <code>Special:Search</code>. As a result, we need to map all these titles to the same original title <code>Special:Search</code>. We will accomplish this by making use of percent decoding.</p>

<p>However, the definition and solution of percent encoding for Wikipedia is slightly different from the widely used definition, and you may find that most percent decoders will break with our dataset. The reason for this is that there are many <code>%</code> symbols which are not followed by hex chars, such as <code>1%_rule_(Internet_culture)</code>. Most percent decoders can only be used in <strong>perfectly encoded character sequences</strong> where <code>%</code> has been encoded into <code>%25</code>.</p>

<p><strong>Once again, please do not assume that the dataset is in perfect format or encoding.</strong> Developers of The Wikimedia Foundation are using their own decoder with the following two differences in contrast with the common URL decoder.</p>

<ul>
<li>They keep percent signs that are not followed by hexadecimal digits.</li>
<li>They do not convert plus-signs to spaces.</li>
</ul>

<p>We don't want you to reinvent the wheel, hence, we offer you code snippets in <a href="https://cmucc-datasets.s3.amazonaws.com/wikipediatraf/percent-decoder/PercentDecoder.java">Java</a>, <a href="https://cmucc-datasets.s3.amazonaws.com/wikipediatraf/percent-decoder/percent_decoder.py">Python 2</a> and <a href="https://cmucc-datasets.s3.amazonaws.com/wikipediatraf/percent-decoder/percent_decoder_py3.py">Python 3</a>. You are allowed to copy and adapt the percent-decoder code snippet into your code without citing it in the references file.</p>

<p>Use them wisely. If you wish to use Bash, it will help if you use piping with the Java/Python snippets.</p>

<p>Note that URL normalization usually requires other steps besides percent-encoding. In this project, we will ask you to only complete percent-encoding. Additionally, bear in mind that you can reorder the rules if you wish in your code, as long as handling dirty data and percent decoding are considered as the prerequisites for other rules. Note that the <a href="http://www.degraeve.com/reference/urlencoding.php">URL Encoded Characters</a> include tabs and spaces which will change the number of columns in the records after percent-decoding. Think twice about which rule you should apply first in your data filter.</p></li>
<li><p><strong>Desktop/mobile Wikipedia sites</strong>: We will focus on English Desktop/Mobile Wikipedia pages, keep the rows only if the first column is exactly <code>en</code> or <code>en.m</code> (<strong>case sensitive</strong>) and exclude all others.</p></li>
<li><p><strong>Wikipedia namespaces</strong>: There are many special pages in Wikipedia that are not actually Wikipedia articles. Remove these pages. A Wikipedia namespace is a set of Wikipedia pages whose names begin with a particular reserved word recognized by the MediaWiki software (followed by a colon).</p>

<p>For example, in the user namespace, all titles begin with "User:". In the case of the article (or main) namespace, in which encyclopedia articles appear, the reserved word and colon are <strong>absent</strong>. The details for namespaces are as follows for your reference, and in this project we will only focus on namespace 0 (Main/Article):</p>

<p><img src="https://s3.amazonaws.com/15619public/webcontent/wiki-rules.png" alt="" /></p>

<h4><strong>Figure 2</strong>: List of Wikimedia namespaces (<a href="https://en.wikipedia.org/wiki/Wikipedia:Namespace">Source</a>)</h4>

<p>Disambiguation pages, templates, navboxes, user pages, discussion pages, file pages, category pages, help pages, and Wikipedia policy pages are not articles. Keep pages only if they belong to namespace 0 (Main/Article) and those grouped into other namespaces should be excluded.</p>

<p>We offer you a <a href="https://en.wikipedia.org/w/api.php?action=query&amp;meta=siteinfo&amp;siprop=namespaces&amp;format=json">JSON file listing all the namespaces</a> which need to be excluded, as well as <a href="https://en.wikipedia.org/w/api.php?action=query&amp;meta=siteinfo&amp;siprop=namespaces">a readable version</a>.</p>

<p>Instead of typing the namespaces by yourself, you should parse the JSON 
file with code to get all the namespaces (except for <code>namespace 0</code>). <strong>Having a strong understanding of working with JSON will help you a lot in later projects!</strong> You may notice that there are attributes about case sensitivity in the JSON file, please ignore them and follow our own rules.</p>

<ul>
<li>If you are using Java, you may use <strong><a href="https://github.com/FasterXML/jackson">Jackson</a> or <a href="https://github.com/google/gson">Google Gson</a></strong>. We do not recommend downloading the lib jars manually to compile the source code with <code>javac -cp</code>, because this approach is error-prone and not maintainable. Besides, please note that we will exclude any file with its size larger than 5MB upon submissions. Maven is the tool widely used in our course to manage Java dependencies. If you are new to Maven, please read Maven primer first where a template is also available for you to start. If you get errors such as <code>Could not find or load main class</code> or <code>java.io.FileNotFoundException</code>, we expect you to debug the errors on your own.</li>
<li>If you are using Python, you may use the <strong>json</strong> module in the standard library.</li>
<li>You are also allowed to use other libraries of your choice. </li>
</ul>

<p>Note:</p>

<ul>
<li>In order to improve the performance when we test your code, you should use a <strong>separate</strong> java/python/bash file to parse the JSON file and generate a blacklist to be used in your data filter code.</li>
<li>You can then manually copy the blacklist from your JSON parser to your code which filters the data.</li>
<li>Do not parse the namespace JSON repetitively each time the data filter program processes a new record. The filter will also be used in the next project with Hadoop streaming on a much larger dataset.</li>
<li>Use attribute-value pairs with attribute <code>*</code> instead of <code>canonical</code>.</li>
<li>When you submit your code, do not forget to submit the code to parse the JSON file as a proof of your work.</li>
</ul>

<p>Page titles may contain spaces visually, but their URLs will replace spaces with underscores and this rule also applies to our pageview data. </p>

<p>Note that the standard namespace blacklist is <strong>case insensitive</strong>. You are expected to generate a prefix blacklist similar to this:</p>

<pre><code>media:
special:
talk:
user:
user_talk:  # instead of "User talk:"
wikipedia:
wikipedia_talk:
... # some title prefixes omitted
gadget_definition_talk:
</code></pre>

<p>You are required to generate the blacklist in the format above to show your learning of JSON parsing. However, with the blacklist ready, you are free to transform and use the blacklist in your own approach.</p>

<p>As we mentioned, some titles use <code>%3A</code> or <code>%3a</code> instead of <code>:</code> due to percent encoding. Before you apply this blacklist, such titles should have already been percent decoded into <code>:</code>.</p>

<p>Blacklist filtering can take less effort if you make use of built-in functions in Python or helper utility libraries in Java. For example:</p>

<pre><code>any(title.startswith(prefix) for prefix in prefixes) # python
StringUtils.startsWithAny(title, prefixes);          # java with Apache Commons Lang library
</code></pre>

<p>You may need to change the code above to make it case insensitive. </p></li>
<li><p><strong>Wikipedia article title limitation</strong>: Wikipedia policy states that if any article starts with an English letter, the letter must be capitalized. For example, the English Wikipedia article for <code>iPad</code> actually matches this URL:</p>

<pre><code>https://en.wikipedia.org/wiki/IPad
</code></pre>

<p>Filter out all page titles that start with lowercase English characters. You may notice that some page titles don't start with English letters but digits, symbols, lowercase characters in other languages, etc., <strong>DO NOT</strong> filter them.</p>

<p><strong>Be cautious and read the documentation whenever you want to use any built-in utility in your chosen language</strong>, for example, read the Javadoc carefully if you want to use <code>Character#isLowerCase(char ch)</code>.</p></li>
<li><p><strong>Miscellaneous filename extensions</strong>: Despite having already filtered pages in <code>File:</code> or <code>Media:</code> namespace, you may still get files instead of articles.</p>

<ul>
<li><p>Media file names are case-sensitive, for example, <code>picture.jpg</code> and <code>picture.JPG</code> are not identical files. Nevertheless, we should use <strong>case insensitive</strong> matching to filter all the media files, ending with any of these suffixes: <code>png, gif, jpg, jpeg, tiff, tif, xcf, mid, ogg, ogv, svg, djvu, oga, flac, opus, wav, webm</code></p></li>
<li><p>A favicon (short for favorite icon), is a file containing one or more small icons. Browsers that provide favicon support typically display a page's favicon in the browser's address bar (sometimes in the history as well) and next to the page's name in a list of bookmarks. Originally, the favicon was a file called favicon.ico placed in the root directory (e.g., http://en.wikipedia.org/favicon.ico) of a web site. Therefore, we should exclude any files with <code>.ico</code> suffix.</p></li>
<li><p>The robots exclusion standard, also known as the robots exclusion protocol or simply <code>robots.txt</code>, is a standard used by websites to communicate with web crawlers and other web robots. The standard specifies how to inform the web robot about which areas of the website should not be processed or scanned. Robots are often used by search engines to categorize web sites. Exclude any files with the <code>.txt</code> suffix.</p></li>
</ul>

<p>Here is the filename extension blacklist (<strong>case-insensitive</strong>):</p>

<pre><code>.png
.gif
.jpg
.jpeg
.tiff
.tif
.xcf
.mid
.ogg
.ogv
.svg
.djvu
.oga
.flac
.opus
.wav
.webm
.ico
.txt
</code></pre></li>
<li><p><strong>Wikipedia Disambiguation</strong>: <a href="https://en.wikipedia.org/wiki/Wikipedia:Disambiguation">Disambiguation</a> in Wikipedia is the process of resolving conflicts when one article title can have different meanings in different fields or scenarios.</p>

<p>For example, the word "<a href="https://en.wikipedia.org/wiki/CPU_(disambiguation)">CPU</a> " can refer to a computer's central processing unit, a human enzyme, software updates in Oracle products such as the Oracle Database and Java and others.</p>

<p>Filter all disambiguation pages with the suffix <code>_(disambiguation)</code>(<strong>case insensitive</strong>), suffixes like <code>_%28disambiguation%29</code> should have already been decoded at this point. Don't filter any page with a specific topic such as <code>Numb_(Linkin_Park_song)</code>.</p></li>
<li><p><strong>Special pages</strong>: Finally, there are some special pages to exclude as well. Page titles that are exactly (<strong>case sensitive</strong>) in the following list should be excluded:</p>

<pre><code>404.php
Main_Page
-
</code></pre>

<ul>
<li><code>Main_Page</code> is the main entrance of the Wikipedia site.</li>
<li><code>404.php</code> is caused when a user attempts to follow a broken or dead link.</li>
<li><code>-</code> is a single hyphen-minus character, why does this get many accesses every hour? If you read the Java source code of <a href="https://github.com/wikimedia/analytics-refinery-source/blob/master/refinery-core/src/main/java/org/wikimedia/analytics/refinery/core/PageviewDefinition.java">Pageview</a> and you will find the clue: <code>-</code> is used whenever any unknown project or article is encountered.</li>
</ul></li>
</ol>

<p><strong>Output format</strong>: Output the remaining articles in the following format:</p>

<pre><code>  [page_title]\t[count_views]
</code></pre>

<p>Where <code>\t</code> is a <em>tab</em>.</p>

<p>For example:</p>

<pre><code>  Carnegie_Mellon_University  34
</code></pre>

<p>Name the output file exactly <code>output</code>, and follow these rules strictly:</p>

<ul>
<li><strong>If there are records from both desktop and mobile sites for the same page title, sum the accesses into one record.</strong></li>
<li>Sort the output in <strong>descending numerical order</strong> of the number of accesses</li>
<li>Break ties by ascending <strong>lexicographical</strong> order (based on the Unicode value of each character in the strings) of page titles. You can find the <a href="https://en.wikipedia.org/wiki/Help:Alphabetical_order">Order of Common Characters</a> offered by the Wikipedia Manual. You can just use <code>String.compareTo(String anotherString)</code> in Java or <code>sorted()</code> in Python, while some tricks are needed if you want to use <code>sort</code> in Bash, more specifically, please figure out the usage of <code>LC_ALL=en_US.UTF-8</code> and <code>LC_ALL=C</code>.</li>
</ul>

<p>To get a full understanding of the big picture, <strong>please continue reading the writeup and finish the "Data Analysis" section before you start coding.</strong></p>

<p><div class="panel panel-danger"> <div class="panel-heading">Danger</div> <div class="panel-body"> </p>

<h2>Be cautious about implicit reliance on your environment</h2>

<p>Your code should work well and its behaviors should be consistent on different systems. You are allowed write and test the code on your own laptop first. <strong>To help you learn best practices, we will test your code in a different environment.</strong></p>

<p><strong>If your code seems to run well locally but behaves differently upon submission, read this panel carefully before you create posts on Piazza.</strong></p>

<p>Failing to realize the potential difference among development, testing and production environments can lead to pitfalls. If your code behaves well in your development environment, it does not guarantee that your code will work perfectly in other environments.</p>

<p>You should make your code independent from unpredictable/uncontrollable external environments. Please pay attention to <strong>encoding-aware I/O operations, newlines and locale</strong> in your code and always <strong>handle them explicitly instead of relying on the system default setting</strong>. Besides, watch out for <strong>versions and absolute/relative paths</strong>. All the following topics can be pitfalls of this project.</p>

<h3>Locale</h3>

<p>On POSIX platforms such as Linux, locale identifiers are defined in this format:</p>

<pre><code>    [language[_territory][.codeset][@modifier]].
</code></pre>

<p>You can get the locale setting on your machine with command <code>locale</code>.</p>

<p>Locale on a Linux system can determine the default encoding in locale-aware programs. In addition, locale is also an important topic in Internationalization/Localization, which will make a difference in date, time, number, currency and so on. In this project, we will explore how the default encoding may change the behavior of programs and the practice to make the programs independent from the system default encoding.</p>

<h3>Encoding-aware I/O</h3>

<p>Let us start with File I/O.</p>

<pre><code>BufferedWriter bw = new BufferedWriter(new FileWriter(OUTPUT));
</code></pre>

<p>This seems good, and it will work correctly on your own laptop in most cases.</p>

<p>If you run <a href="http://findbugs.sourceforge.net/">Findbugs</a> upon this snippet, you will get this SEVERE warning:</p>

<pre><code>Reliance on default encoding

Found a call to a method which will perform a byte to String (or String to byte) conversion, and will assume that the default platform encoding is suitable. This will cause the application behavior to vary between platforms. Use an alternative API and specify a charset name or Charset object explicitly.
</code></pre>

<p>Similarly, the following snippet in python 2/3 relies on the value returned by <code>locale.getpreferredencoding(False)</code>:</p>

<pre><code>with open(fname, "r") as f:
</code></pre>

<p>This bug can be easily ignored when you only run and test your code in your own development environment, in which the default encoding will be set to UTF-8. However, if the production environment has another default encoding, your code will produce unexpected output. If you see weird output like <code>????</code>, <a href="https://en.wikipedia.org/wiki/Specials_(Unicode_block)#Replacement_character">replacement characters</a> or empty boxes in the future, check your encoding! Many traditional encodings will change unsupported code points into question marks, such as ISO-8859-1, a.k.a. Latin-1. Failing to deal with encoding when handling input can cause more severe failure, as the program may crash. For example, processing UTF-8 encoded input as ASCII in Python 3 may cause <code>UnicodeEncodeError: 'ascii' codec can't encode character: ordinal not in range(128)</code>.</p>

<p>You must set encoding explicitly when your program converts an input stream of bytes to strings, and when your program converts strings to an output stream of bytes. <strong>You CANNOT pass all the test cases if you fail to make your program encoding-aware.</strong></p>

<p>Here are examples to handle encoding in an explicit fashion:</p>

<pre><code>For example, in Java 8:

    BufferedReader br = new BufferedReader(
            new InputStreamReader(new FileInputStream(INPUT), StandardCharsets.UTF_8));
    PrintWriter printWriter = new PrintWriter(new File(OUTPUT), "UTF-8");
    Stream&lt;String&gt; stream = Files.lines(
            Paths.get(OUTPUT), StandardCharsets.UTF_8)

In Python 3:

    # for more information, read https://docs.python.org/3/howto/unicode.html
    with open(fname, "rt", encoding='utf-8') as f:

In Python 2.7:

    # for more information, read https://docs.python.org/2/howto/unicode.html
    with io.open(fname, "wt", encoding='utf-8') as f:
</code></pre>

<p>Okay, let's try another example! Will the following code produce the same output in multiple environments?</p>

<pre><code>System.out.println(str);
</code></pre>

<p>No! Even <code>System.out</code>, as a <code>PrintStream</code>, is system dependent! To help you overcome this hurdle and pass all the tasks in this project, we offer you a best practice here:</p>

<pre><code>Scanner in = new Scanner(
        new BufferedInputStream(System.in), "UTF-8");
PrintWriter out = new PrintWriter(
        new OutputStreamWriter(System.out, "UTF-8"), true);
</code></pre>

<p>If you cannot get a full score upon submission and you wonder if it is caused by encoding, you may test your program on your instance by running your program with different locales:</p>

<pre><code> LC_ALL=en_US.UTF-8 ./your_program  # `locale charmap` will return `UTF-8`
 LC_ALL=C ./your_program            # `locale charmap` will return `ANSI_X3.4-1968` (ascii)
</code></pre>

<p>Encoding-awareness covers not only I/O but also the source code. If there are UTF-8 characters in the source code, including the comments, the Java compiler can break if the system default encoding does not support UTF-8. You should set the source code encoding using <code>javac -encoding utf8 *.java</code> or use the <a href="https://stackoverflow.com/questions/3017695/how-to-configure-encoding-in-maven">Maven approach</a>. Although the source code encoding in Python is independent from system default encoding and Python 3 supports UTF-8 by default, Python 2 will default to ASCII and you must follow this <a href="https://www.python.org/dev/peps/pep-0263/#defining-the-encoding">Python Enhancement Proposal</a> to define a source code encoding in Python 2.</p>

<p>If you are passionate about mining insight from data, keep in mind that encoding-unaware data processing may fail to produce the expected output <strong>silently</strong>. If you are enthusiastic about API design, please make your library encoding-aware. Even in one of the most widely-used utility projects, <a href="http://commons.apache.org/">Apache Commons</a>, the contributors feel the pain caused by encoding reliance. <a href="https://commons.apache.org/proper/commons-io/index.html">Apache Commons IO</a>, after 12 years since the initial release and more than 4 years since the encoding reliance was reported, the library finally deprecates all the encoding-unaware methods in the <a href="https://commons.apache.org/proper/commons-io/upgradeto2_5.html">2.5</a> release. Encodings can be more vital when working with web applications and databases, bear this in mind when you work on the team project in the future.</p>

<blockquote>
  <p>"It does not make sense to have a string without knowing what encoding it uses." -- Joel Spolsky</p>
</blockquote>

<h3>Newline (EOL)</h3>

<p>Believe it or not, <code>System.out.println(str)</code> has yet another problem. Try your code on both Linux and Windows platforms, and compare the md5sum of the standard output -- and they will be different.</p>

<p>A newline, also known as end of line (EOL), is a special character or sequence of characters signifying the end of a line of text and the start of a new line. The actual codes representing a newline vary across operating systems, which can be a problem when exchanging text files between systems with different newline representations.</p>

<p>Systems based on ASCII or a compatible character set use either LF (Line feed, '\n'), CR (Carriage return, '\r'), or CR followed by LF (CR+LF, '\r\n'). Unix and Unix-like systems, e.g. Linux, Mac OS X, etc., use '\n' while Windows use '\r\n'.</p>

<p>You may edit your code on your own laptop during your development and testing phases, however, keep in mind if you are a Windows user, the code may seem "visually" correct but will behave differently on a Unix or Unix-like System. <strong>Make sure you set the EOL to UNIX format in your editor, especially when you write bash scripts locally, or your scripts might break when you upload the script or you "copy &amp; paste" the code to the remote instance.</strong> You may use <code>cat -e filename</code> to make sure there is no CR (Carriage return, '\r') in your code (there will be <code>^M</code> at the end of each line if CR exists).</p>

<p>It is also recommended to always handle newlines explicitly in your code.</p>

<pre><code>For example, in Java 8:

    //OS-dependent code
    printWriter.println(entry.getKey() + "\t" + entry.getValue());
    printWriter.printf("%s\t%s%n", entry.getKey(), entry.getValue());
    printWriter.print(entry.getKey() + "\t" + entry.getValue() + System.lineSeparator());
    //System.lineSeparator() can be replaced with System.getProperty("line.separator");

    //OS-independent code with identical output in various operating systems
    printWriter.print(entry.getKey() + "\t" + entry.getValue() + "\n");

In Python 3:

    # OS-dependent code
    output = open('output', 'wt', encoding='utf-8')
    output.write(line + '\n')
    # Python automatically translates "\n" to the proper newline of the current OS.
    # it will be converted to "\r\n" in Windows

    # OS-independent code
    output = open('output', 'wt', encoding='utf-8', newline='\n')
    output.write(line + '\n')
</code></pre>

<h3>Versions &amp; Compatibility</h3>

<h4>Bash</h4>

<p>If you want to use <code>awk</code> to do regex/string operations ignoring case, <code>IGNORECASE</code> seems to be a good idea. It can be set to a non-zero value.</p>

<pre><code> awk 'BEGIN{IGNORECASE = 1;}...' FILENAME
</code></pre>

<p>The command will work well on our student AMI, but it will break on Mac OS X. Because <code>IGNORECASE</code> is implemented in GNU Awk (a.k.a. <code>gawk</code>) but not in Mac's <code>awk</code>. Alternatively, <code>tolower()</code> is supported by both versions.</p>

<p>Similarly, the BSD <code>grep</code> on Mac is different from the GNU <code>grep</code> on our student AMI. There is also no <code>wget</code> installed on Mac OS X and an "imperfect substitute" is <code>curl -O</code>. Consider using <a href="https://brew.sh/">Homebrew</a> if you need to install GNU tools on a Mac platform.</p>

<p>Whenever using tools among different systems, remember that there can always be various versions. For example, a lot of popular Unix-like tools have their <a href="http://directory.fsf.org/wiki/GNU">GNU versions</a>. Remember to check the versions first before you start using tools and choose more compatible solutions if possible.</p>

<h4>Python</h4>

<p>If you are a Python user, specify your Python version explicitly.</p>

<p>Use either <code>python2</code> or <code>python3</code> to run python, do not use <code>python</code> and rely on the default one in the system environment. This also applies to the usage of <code>pip2</code> and <code>pip3</code> over <code>pip</code>. Alternatively, set the proper <a href="https://en.wikipedia.org/wiki/Shebang_(Unix)">shebang</a> line to specify the interpreter to use and run your script as an executable, such as <code>./script.py</code>. If you decide to use shebang, be extremely careful because some shebang lines can still break in different system environments, such as <code>#!/usr/bin/python3</code> because the python installation path may vary across platforms. <code>#!/usr/bin/env python3</code> is the best way to define the shebang for portability.</p>

<h4>Java</h4>

<p>When you are trying to run a class compiled with Java 8 into a lower JRE, you will get "Unsupported major.minor version Error". We are using Java 8, GNU Awk and GNU grep in our course.</p>

<p>If you are in doubt about any versioning issue of tools/languages/libraries we support, please create a private post on Piazza.</p>

<h3>Absolute/Relative Paths</h3>

<p><strong>DO NOT</strong> write code like the example below because your code won't be able to execute anywhere other than the absolute path.</p>

<pre><code> python3 /home/&lt;andrewId&gt;/Project1_1/script.py
</code></pre>

<p>Replace any absolute path with a relative one!</p>

<h3>Conclusion</h3>

<p>To sum up, you should always pay attention to the potential causes of implicit reliance in your implementation, and it will help you a lot during <strong>this project, this semester, and hopefully in your career</strong>.</p>

<p></div></div></p>

        
    </div>
</div>




<div class="panel panel-default writeup_section" data-sequence="7">
    <div class="panel-body writeuppanel">
        <h2>Data Analysis</h2>

<p>After filtering the data, you are expected to analyze your results and answer a set of questions, which are present in the file <code>/home/&lt;andrewId&gt;/Project1_1/runner.sh</code> on your instance. To complete this module, do the following:</p>

<ol>
<li><p>Go to the project folder located at <code>/home/&lt;andrewId&gt;/Project1_1</code></p></li>
<li><p>The project folder consists of the following files: the runner script <code>runner.sh</code>, <code>submitter</code> to submit your solutions and <code>reference</code> to cite the links and students you get help from, and other data files for you to work on. You have permissions to edit the <code>runner.sh</code> and <code>references</code> files.</p></li>
<li><p>Edit the script <code>runner.sh</code> to include the commands/code used to answer the questions. We recommend using bash scripting, but it is not required.</p>

<p>Do not move any of the provided files.</p>

<p>If you are using any external scripts, ensure that you are calling the correct scripts from <code>runner.sh</code>. Please ensure that you are placing all your code in the same folder and also assume that the dataset is present in the current folder.</p>

<p>When you need to access the dataset in your code assume that it is present in the working directory (i.e., do not use any absolute or relative paths for accessing the dataset -- we will auto-grade it later in a single jailed environment).</p></li>
<li><p>Edit the text file <code>references</code> to include all the links that you referred to for completing this project. Also, include the Andrew IDs of all students who you might have discussed general ideas with when working on this project in the same file. This is extremely important.</p>

<p>We analyze many aspects of your AWS and TheProject.Zone usage, as well as automated code similarity detection tools.</p>

<p><strong>NOTE</strong>: Citing resources and having big picture discussions with other students does not excuse cheating. <strong>You are not allowed to look at or discuss code with another person. Similarly, you are not allowed to use any code snippet from anyone or anywhere on the Internet</strong>.</p>

<p>When in doubt, please post privately on Piazza.</p></li>
<li><p>You can run and check your answers by typing <code>./runner.sh</code> from the Project1_1 folder.</p>

<p>Running this script should print out the answers to all the questions you have answered. Please ensure that the answers are printing correctly before you submit your answers.</p>

<p>Do not print hardcoded answers in <code>runner.sh</code>. We will run your code on other log files for verification and grading.</p>

<p>If you want to focus on one question and get a readable unescaped answer, we offer you <code>./runner.sh -r &lt;question_id&gt;</code> from the Project1_1 folder to run one single question. Type <code>./runner.sh -h</code> to get the usage example.</p></li>
<li><p>Once you have completed all the questions, you can submit the answers to the evaluation system using the <code>submitter</code> executable. Run the executable using the command <code>./submitter</code> from the auto-grader folder.</p>

<p>Remember that your submission password can be found by clicking on the button on the top of this page. <strong>Make sure you open port 80 for incoming HTTP traffic before you proceed.</strong></p>

<p>Type <code>./submitter -h</code> to get the usage example.</p></li>
<li><p>After running the <code>./submitter</code> command, a website will be created with answers and values which are specific to your submission. Once your details are validated, these pages will be read by our load generators within a few minutes, at which point, you will see the feedback and scores in your submission table.</p>

<p>The load generators also read your code and save them to our repository, where they will be strictly analyzed for similarities with submissions from other students in the past and present, as well as with code from the internet.</p>

<p>There is no limit on the number of submissions allowed before the project deadline. However, submissions must be separated by at least 60 seconds.</p>

<p>Make sure not to exceed the budget specified for this project module.</p></li>
</ol>

<p><div class="panel panel-info"> <div class="panel-heading">Information</div> <div class="panel-body"> </p>

<h4>Progressively Solve Data Science Problems with Jupyter Notebook</h4>

<p>We <strong>strongly</strong> recommend that you use <code>awk</code>, <code>grep</code> and Python Data Analysis Library to solve the data analysis questions in <code>runner.sh</code>. Please finish the Jupyter Notebook primer and the self-study interactive notebooks in the Azure Notebooks library <a href="https://notebooks.azure.com/CloudComputingCourse/libraries/cloud-computing-course">15-319/15-619: Cloud Computing Course</a>, and you will be able to solve most questions quickly.</p>

<p>We have created the virtual environment at <code>/home/ubuntu/virtualenv/</code> on your instance with Pandas and Jupyter pre-installed, please use the following commands to run the server:</p>

<pre><code>source /home/ubuntu/virtualenv/bin/activate
jupyter notebook --no-browser
</code></pre>

<p>You can now follow the guide in the "Remote Server Using SSH Tunneling" section in the Jupyter Notebook primer to build the connection.</p>

<p>When programming on Jupyter, please keep in mind that memory is very limited on a <code>t2.micro</code> machine, you should be aware of the memory usage, for example:</p>

<ol>
<li>You should not read the whole dataset <code>pageviews-20161109-000000.gz</code> into memory.</li>
<li>You should not store duplicate filtered <code>output</code> in memory. Load it once and reuse it.</li>
<li>If you get any out-of-memory error, restarting the kernel will fix it.</li>
</ol>

<p></div></div></p>

<h4>Notes</h4>

<p>When submitting, please make sure the following source code is in your Project1_1 folder:</p>

<ul>
<li>Code to extract the namespace blacklist from the JSON file used in <code>json()</code> in <code>runner.sh</code>.</li>
<li>Code to convert <code>pageviews-20161109-000000.gz</code> to <code>output</code> used in <code>filter()</code> in <code>runner.sh</code>.</li>
<li>Code to use the <code>output</code> file to generate the answers in each data analysis question.</li>
<li>Make sure that the source code is present (*.sh, *.java, *.py, etc.).</li>
<li>Your code should demonstrate good style and discipline. Every time you write code, remember that someone else is going to read it. Make your code readable, self-explanatory and standardized, which will avoid many potential bugs. <strong>Hard to read code of poor quality will lead to a loss of points during manual grading.</strong></li>
<li><strong>Lack of comments, especially among complicate code, will lead to a loss of points during manual grading.</strong></li>
</ul>

<p>Performance matters when processing big data, hence, the data filter program should not have a large overhead because the overhead will get amplified as the data size scales. </p>

<p>For example, although the Pandas library is the recommended tool in the data analysis task (since the filtered output is no longer that large), <strong>DO NOT use Pandas in the data filter program.</strong>  The powerful features provided by Pandas is at the expensive cost of time and memory, which is not suitable for large dataset. We will explore the Spark Framework in Project 4 which enables you to process and analyze big data in a similar flavor as Pandas.</p>

<p><div class="panel panel-danger"> <div class="panel-heading">Danger</div> <div class="panel-body"> </p>

<p>You are required to make your program efficient and get rid of any overhead, otherwise it will cause a "Grading timeout" with a 0 score.</p>

<ol>
<li>Do not compile java code in <code>filter()</code>.</li>
<li>Do not use Pandas in the data filter program.</li>
</ol>

<p>Besides, we block most internet connections during the grading. </p>

<ol>
<li>Do not use any Maven remote repositories other than the <em>Maven central repository</em>.</li>
<li>Do not send any HTTP/HTTPS requests in your code.</li>
</ol>

<p>If you get a "Grading timeout", do not simply resubmit without changing your code as the result will be the same. </p>

<p></div></div></p>

<p>Once again, if your submitted code does not produce the same results as the ones on your local computer, consider the topics mentioned in "Be cautious about implicit reliance on your environment".</p>

        
    </div>
</div>