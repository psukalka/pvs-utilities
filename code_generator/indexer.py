import ast
from pathlib import Path
from generic_helper import GenericHelper


class CodebaseIndexer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.openai_client = GenericHelper.get_openai_client()

    def get_source(self, file_path):
        source = None
        encodings = ['utf-8'] #, 'utf-8-sig', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as fp:
                    source = fp.read()
                break # on success
            except (UnicodeDecodeError, LookupError):
                continue
        if not source:
            print(f"Could not decode file: {file_path} with any encoding")
        return source

    def extract_tree(self, source):
        try:
            tree = ast.parse(source)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []
        return tree

    def index_file(self, file_path):
        """
        Extract the utilities from the codebase
        """
        utilities = []
        try:
            source = self.get_source(file_path)
            tree = self.extract_tree(source)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    utilities.append(self.extract_class(node, source, file_path))
                elif isinstance(node, ast.FunctionDef):
                    utilities.append(self.extract_function(node, source, file_path))
            return utilities
        except Exception as ex:
            print(f"Failed in indexing file: {file_path} with error: {ex}")
            return []

    def extract_class(self, node, source, file_path):
        """
        Extract class with all its methods
        """
        method_details = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_details.append({
                    'name': item.name,
                    'args': [arg.arg for arg in item.args.args],
                    'docstring': ast.get_docstring(item) or '',
                    'is_static': any(isinstance(dec, ast.Name) and dec.id == "staticmethod" for dec in item.decorator_list),
                    'is_classmethod': any(isinstance(dec, ast.Name) and dec.id == "classmethod" for dec in item.decorator_list)
                })
        
        full_code = ast.get_source_segment(source, node)
        return {
            "type": "class",
            "name": node.name,
            "method_details": method_details,
            "methods": [m['name'] for m in method_details],
            "file": str(file_path),
            "docstring": ast.get_docstring(node) or '',
            "code": full_code,
            "code_summary": f"{full_code[:200]}..." if len(full_code) > 200 else full_code,
            "import_path": self.file_to_import_path(file_path),
            "line_count": len(full_code.split('\n'))
        }

    def extract_function(self, node, source, file_path):
        full_code = ast.get_source_segment(source, node)
        return {
            'type': 'function',
            'name': node.name,
            'file': str(file_path),
            'args': [arg.arg for arg in node.args.args],
            'docstring': ast.get_docstring(node) or '',
            'code': full_code,
            'code_summary': f'{full_code[:200]}...' if len(full_code) > 200 else full_code,
            'import_path': self.file_to_import_path(file_path),
            'line_count': len(full_code.split('\n'))
        }


    def file_to_import_path(self, file_path):
        path = Path(file_path)
        parts = list(path.parts)

        for i in range(len(parts) -1, -1, -1):
            parent = Path(*parts[:i+1])
            if (parent / "__init__.py").exists():
                import_parts = parts[i:]
                break
        else:
            import_parts = parts[-3:] if len(parts) >= 3 else parts
        
        import_path = '.'.join(import_parts).replace('.py', '')
        return import_path

    def index_codebase(self, force_reindex=False):
        """
        Index entire codebase with caching
        """
        all_utilities = list()
        files_processed = 0
        patterns = [
            '**/managers/**/*.py',
            '**/helpers/*.py'
        ]
        for pattern in patterns:
            for file_path in self.repo_path.glob(pattern):
                if any(skip in str(file_path) for skip in ['__pycache__', 'migrations', 'test_']):
                    continue
                utilities = self.index_file(file_path)
                all_utilities.extend(utilities)
                files_processed += 1
                if files_processed % 10 == 0:
                    print(f"Processed: {files_processed} files ...")
        print(f"Indexed {files_processed} files. Found {len(all_utilities)} utilities")

        print(f"Generating embeddings ...")
        for i, utility in enumerate(all_utilities):
            description = self.create_embedding_text(utility)
            # response = self.openai_client.embeddings.create(
            #     model='text-embedding-3-small',
            #     input=description
            # )
            # utility['embedding'] = response.data[0].embedding
            if (i+1) % 50 == 0:
                print(f"Skipped: {i+1}/{len(all_utilities)} embeddings ...")
        print(f"embeddings complete")
        return all_utilities

    def create_embedding_text(self, utility):
        text_parts = [
            f"{utility['name']}",
            utility['docstring']
        ]
        if utility['type'] == 'class':
            text_parts.append(f"Methods: {', '.join(utility['methods'])}")
            for method in utility['method_details']:
                if method['docstring']:
                    text_parts.append(f"{method['name']}: {method['docstring']}")
        
        text_parts.append(utility['code_summary'])
        return '\n'.join(filter(None, text_parts))

if __name__ == '__main__':
    indexer = CodebaseIndexer("C:\\workspaces\\kukufm-py\\kukufm-py\\")
    indexer.index_codebase()