from context_builder import DetailedContextBuilder
from generic_helper import GenericHelper

class CompanyCodeGenerator(object):
    """Generates code that follows company pattern"""

    def __init__(self, utilities, patterns):
        self.utilities = utilities
        self.patterns = patterns
        self.context_builder = DetailedContextBuilder(utilities, patterns)
        self.anthropic_client = GenericHelper.get_anthropic_client()

    def generate(self, request, explain_reasoning=True):
        """Generate code for the request"""

        print(f"Request: {request}\n")

        # Find relevant utilities
        relevant_utilities = self.context_builder.find_relevant_utilities(request, top_k=10)

        print(f"Found {len(relevant_utilities)} relevant utilities")
        for i, util in enumerate(relevant_utilities[:5], 1):
            print(f"    {i}. {util['name']} (score: {util['relevance_score']:.2f})")

        print(f"Building context...")
        context, domain = self.context_builder.build_context(request, relevant_utilities)

        if domain:
            print(f"Identified domain: {domain}")

        system_prompt = self.create_system_prompt()

        user_prompt = f"""{context}
        <task>
        {request}
        </task>
        Generate production ready code that follows the company's patterns shown above.
        {'CRITICAL: Explain your reasoning first' if explain_reasoning else ''}
        {'- Which utilities are you using and why?' if explain_reasoning else ''}
        {'- Which utilities are you not using and why?' if explain_reasoning else ''}
        {'- What did you learn from reading the implementations?' if explain_reasoning else ''}
        {'- How does your code follow company pattern' if explain_reasoning else ''}

        Then provide the complete code with:
        1. All necessary imports
        2. Proper error handling
        3. Docstrings
        4. Type hints (if company uses them)
        5. Comments explaining key decisions
        """

        print(f"Generating code with claude")
        response = self.anthropic_client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=4000,
            system=system_prompt,
            messages=[{
                'role': 'user',
                'content': user_prompt
            }]
        )

        generated_code = response.content[0].text
        return {
            'code': generated_code,
            'domain': domain,
            'utilities_found': len(relevant_utilities),
            'top_utilities': [u['name'] for u in relevant_utilities[:5]],
            'context_size': len(context)
        }

    def create_system_prompt(self):
        return """You are a senior software engineer at this company. You have deep knowledge of company's codebase and coding standards.
        Your job is to generate production-ready code that follows company patterns, reuses existing utilities if exist and create new if none fits requirements.
        CRITICAL DECISION MAKING PROCESS:
        1. READ IMPLEMENTATIONS CAREFULLY
            - You have access to full implementations, not just signatures
            - Read what each utility actually does, not just its name
            - Check for side effects: logging, metrics, retries, alerts, etc.
            
        2. MATCH REQUIREMENTS TO IMPLEMENTATIONS:
            - User wants "simple" --> avoid utilities with extra features
            - User wants "production" --> use utilities with monitoring / logging
            - User wants "testing" --> avoid production utilities with side effects
            - User is explicit about the needs --> follow them exactly 
            
        3. DECISION CRITERIA:
            Use existing utilities when:
                - Implementations matches requirements exactly
                - Extra features are beneficial for use case
                - It follows company patterns
            
            Don't use these utilities when:
                - User wants simpler version
                - Extra features would cause problems
                - It's designed for different use case (prod vs test)
                
            Write new code when:
                - No existing utility fits
                - Existing ones do too much
                - User explicitly wants different approach
                
        4. ALWAYS EXPLAIN YOUR REASONING:
            Before showing code, explain:
                - "I'm using X because ..." 
                - "I'm NOT using Y because it includes Z which would..."
                - "I'm writing new code because existing utilities..."

        5. **JUST BECAUSE IT EXISTS DOESN'T MEAN USE IT**
                - Evaluate each utility against the specific requirements
                - Sometimes writing simpler code is better than using complex utility
                - Production utilities aren't suitable for testing
                - Testing utilities aren't suitable for production

        CODING STANDARDS:
                - Include all necessary imports (use company import paths shown in context)
                - Add comprehensive docstrings
                - Include error handling
                - Add comments explaining non-obvious decisions
                - Follow PEP 8 style guidelines
                - Use type hints if company codebase uses them

        Remember: Your goal is to write the BEST code for the situation, not just to maximize utility reuse."""