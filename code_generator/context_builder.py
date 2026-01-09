import numpy as np
from generic_helper import GenericHelper


class DetailedContextBuilder:
    def __init__(self, utilities, patterns):
        self.utilities = utilities
        self.patterns = patterns
        self.openai_client = GenericHelper.get_openai_client()
    
    def cosine_similarity(self, vec1, vec2):
        """
        calculate cosine similarity between two vectors
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def identify_domain(self, request):
        """Identify which domain request is about"""
        request_lower = request.lower()

        domain_keywords = {
            's3': ['s3', 'aws', 'bucket', 'upload', 'download', 'storage', 'file storage'],
            'database': ['database', 'db', 'query', 'sql', 'postgres', 'mysql', 'connection']
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                return domain
        
        return None
    
    def find_relevant_utilities(self, request, top_k=10):
        """vector search for relevant utilities"""
        response = self.openai_client.embeddings.create(
            model='text-embedding-3-small',
            input=request
        )
        query_embedding = response.data[0].embedding

        # calculate similarities
        similarities = list()
        for utility in self.utilities:
            sim = self.cosine_similarity(query_embedding, utility['embedding'])
            similarities.append(utility, sim)
        
        # sort by similarity
        similarities.sort(key=lambda x:x[1], reverse=True)

        # Add relevance score to utilities
        relevant = list()
        for utility, score in similarities[:top_k]:
            utility_copy = utility.copy()
            utility_copy['relevance_score'] = score
            relevant.append(utility_copy)
        
        return relevant

    def build_context(self, request, relevant_utilities):
        """
        build detailed context with full implementations
        """
        domain = self.identify_domain(request)
        context = "<company_codebase>\n\n"
        # add domain specific pattern first, if exists
        if domain and domain in self.patterns:
            context += self.build_pattern_section(domain, self.patterns[domain])
        
        # add relevant utilities with full details
        context += self.build_utilities_section(relevant_utilities, max_full_details=5)
        context += "<company_codebase>\n\n"
        return context, domain

    def build_pattern_section(self, domain_name, pattern):
        """
        Build section for domain specific pattern
        """
        section = f"""
        {'='*70}
        PRIMARY PATTERN FOR {domain_name.upper()}
        {'='*70}
        This is your company's standard way to handle {domain_name}.
        **Main Utility:** {pattern['main_utility']}
        **Type:** {pattern['type']}
        **Location:** `{pattern['file']}`
        **Import:** `from {pattern['import_path']} import {pattern['main_utility']}`
        **Purpose:** 
        {pattern['docstring']}
        **How to Initialize:**
        ```python
        {pattern['initialization']}
        ```
        **Use case:**
        {pattern['use_case']}
        """

        if pattern.get('methods'):
            section += f"**Available Methods:** {', '.join(pattern['methods'])}\n"
        
        section += f"""** FULL IMPLEMENTATION: **
        ```python
        {pattern['full_code']}
        ```
        **IMPORTANT:** Read the implementation above carefully!
        - Check what ELSE this utility does besides its main purpose
        - Decide if these extra features (logging, metrics, retry, etc.) match your needs
        - If user wants "simple" or "testing", this might do TOO MUCH
        - If user wants "production", these extra features are BENEFICIAL
        """
        return section

    def build_utilities_section(self, utilities, max_full_details=5):
        """
        Build section with utility details
        """
        section = f"""
        {'='*50}
        OTHER RELEVANT UTILITIES
        {'='*50}

        These utilities might also be relevant. Read implementations to decide if they fit.

        """
        for i, utility in enumerate(utilities, 1):
            if i <= max_full_details:
                # Full details for top n utilities
                section += self.build_full_utility_detail(utility, i)
            else:
                section += self.build_utility_summary(utility, i)
            
        return section

    def build_full_utility_detail(self, utility, index):
        detail = f"""
        {'-'*50}
        ## {index}. {utility['name']} ({utility['type'].upper()}) - Relevance: {utility['relevance_score']:.2f}
        {'-'*50}
        **Location:** {utility['file']}
        **Import:** `from {utility['import_path']} import {utility['name']}`
        **Lines of code:** {utility['line_count']}
        """
        if utility['docstring']:
            detail += f"**Documentation:** {utility['docstring']}"
        
        # for classes, show method breakdown
        if utility['type'] == 'class' and utility.get('method_details'):
            detail += "**Methods:** \n"
            for method in utility['method_details']:
                method_type = ""
                if method.get('is_static'):
                    method_type = " [staticmethod]"
                elif method.get('is_classmethod'):
                    method_type = " [classmethod]"
                
                args_str = ', '.join(method['args'])
                detail += f"  - {method['name']}({args_str}){method_type}\n"
                if method['docstring']:
                    detail += f"  {method['docstring']}\n"
            detail += "\n"
        detail += f"""**FULL IMPLEMENTATION**:
        ```python
        {utility['code']}
        ```
        **Decision checklist:**
        - Does this match what user needs ? 
        - What else does this do besides the main purpose ? 
        - Are the extra features helpful or problematic for this usecase ? 
        - If the user wants simple, does this have too many features ? 
        - If the user wants production, does this have enough features ? 
        """
        return detail 


    def build_utility_summary(self, utility, index):
        summary = f"""
        ## {index}. {utility['name']} - Relevance: {utility['relevance_score']:.2f}

        **Type:** {utility['type']}
        **Import:** `from {utility['import_path']} import {utility['name']}`
        **Description:** {utility['docstring'] or 'No Documentation'}
        """

        if utility['type'] == 'class' and utility.get('methods'):
            summary += f"**Methods:** {', '.join(utility['methods'])}"
        
        summary += f"""*Full implementation details not shown to save tokens. 
        If you need to use this utility, let me know and I will provide the complete code."""

        return summary

    