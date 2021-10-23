#prog_languages
keywords = [[]]*6
i = 0;
keywords[0] = '''Python	Java	JavaScript	C	Ruby	Shell	C++	C#	.NET	HTML	NodeJS	AngularJS		
'''.split()
keywords[1] = '''SDK	GIT	SCM	Kubernetes	Serverless	IaaC	Microservices	Docker	Ensemble	Safe	Puppet	CICD	Lambda	SQS
'''.split()
keywords[2] = 'SQL NoSQL DynamoDB'.split()
keywords[3] = 'AWS GCP Azure ELK EKS'.split()
keywords[4] = 'NIST	CIS 	ISO	GDPR'.split()
keywords[5] = 'CEH	CISSP	CISA 	CISM	CompTIA Security+'.split()
for words in keywords:
    for w in words:
        print(w)