class CompanyPatternAnalyzer:
    def __init__(self, utilities):
        self.utilities = utilities

    def analyze_patterns(self):
        patterns = {
            's3': self.find_domain_patterns(['s3', 'aws', 'bucket', 'storage']),
            'database': self.find_domain_patterns(['database', 'db', 'connection', 'postgres', 'mysql'])
        }

    def find_main_utility(self, utilities):
        # Priority manager > class > function
        managers = [u for u in utilities if 'manager' in u['name'].lower() and u['type'] == 'class']
        if managers:
            return [0]
        
        classes = [u for u in utilities if u['type'] == 'class']
        if classes:
            return classes[0]
        
        return utilities[0] if utilities else None

    def find_domain_patterns(self, keywords):
        matching_utilities = []
        for utility in self.utilities:
            text = f"{utility['name']} {utility['docstring']}".lower()
            if any(keyword in text for keyword in keywords):
                matching_utilities.append(utility)
        
        if not matching_utilities:
            return None

        main_utility = self.find_main_utility(matching_utilities)
        if not main_utility:
            return None

        pattern = {
            'main_utility': main_utility['name'],
            'type': main_utility['type'],
            'import_path': main_utility['import_path'],
            'file': main_utility['file'],
            'docstring': main_utility['docstring'],
            'full_code': main_utility['code'],
            'methods': main_utility.get('methods', []),
            'initialization': self.infer_initialization(main_utility),
            'use_case': self.infer_use_case(main_utility),
            'all_related': [u['name'] for u in matching_utilities]
        }

        return pattern

    def infer_initialization(self, utility):
        if utility['type'] == 'function':
            args = ', '.join(utility['args'])
            return f"{utility['name']}({args})"
        
        code = utility['code'].lower()
        if 'get_client' in code:
            return f"{utility['name']}.get_client()"
        elif 'get_connection' in code:
            return f"{utility['name']}.get_connection()"
        elif 'get_instance' in code or 'instance' in code:
            return f"{utility['name']}.get_instance()"
        else:
            return f"{utility['name']}()"

    def infer_use_case(self, utility):
        code = utility['name'].lower()
        docstring = utility['docstring'].lower()
        
        indicators = list()

        if 'production' in docstring:
            indicators.append("Production use")
        if 'test' in code or 'mock' in code:
            indicators.append("Test use")
        if 'logging' in code and 'metrics' in code:
            indicators.append("Includes logging and monitoring")
        if 'retry' in code or 'backoff' in code:
            indicators.append("Has retry logic")
        if 'cache' in code:
            indicators.append("Includes caching")
        return ', '.join(indicators) if indicators else "General Purpose"
