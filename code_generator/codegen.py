from indexer import CodebaseIndexer
from pattern_analyzer import CompanyPatternAnalyzer
from company_code_generator import CompanyCodeGenerator

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Company code generator that follows company patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        python codegen.py "Create S3 Downloader"
        python codegen.py "Add payment verification method"
        python codegen.py "Create database connection pooler" --reindex
        python codegen.py --interactive
        """
    )

    parser.add_argument('request', nargs='*', help='Code generation request')
    parser.add_argument('--repo', default='.', help='Path to repository')
    parser.add_argument('--reindex', action='store_true', help='Force indexing of codebase')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--output', '-o', help='Output file with generated code')
    parser.add_argument('--no-reasoning', action='store_true', help='Skip reasoning')

    args = parser.parse_args()

    print(f"Company code generator \n\n")
    indexer = CodebaseIndexer(args.repo)
    utilities = indexer.index_codebase(force_reindex=args.reindex)

    analyzer = CompanyPatternAnalyzer(utilities)
    patterns = analyzer.analyze_patterns()

    generator = CompanyCodeGenerator(utilities, patterns)

    if args.interactive:
        interactive_mode(generator, args)
        return

    if not args.request:
        parser.print_help()
        return
    
    request = ' '.join(args.request)
    result = generator.generate(request, explain_reasoning=not args.no_reasoning)

    print('-'*50)
    print(result['code'])
    print('-'*50)

    print('\n Generation Stats:')
    print(f"   Domain: {result['domain'] or 'General'}")
    print(f"   Utilities found: {result['utilities_found']}")
    print(f"   Top matches: {', '.join(result['top_utilities'])}")
    print(f"   Context size: {result['context_size']:,} characters")
    
    # Save to file
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result['code'])
        print(f"\n💾 Saved to {args.output}")

def interactive_mode(generator, args):
    """Interactive code generation mode"""
    
    print("\n" + "="*70)
    print("🎯 INTERACTIVE MODE")
    print("="*70)
    print("\nType your code requests (or 'quit' to exit)")
    print("Commands:")
    print("  quit/exit/q - Exit")
    print("  save <filename> - Save last generated code")
    print("  clear - Clear screen")
    print("\n" + "="*70 + "\n")
    
    last_result = None
    
    while True:
        try:
            request = input("\n📝 Request: ").strip()
            
            if not request:
                continue
            
            # Handle commands
            if request.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if request.lower() == 'clear':
                os.system('clear' if os.name != 'nt' else 'cls')
                continue
            
            if request.lower().startswith('save '):
                if last_result:
                    filename = request[5:].strip()
                    with open(filename, 'w') as f:
                        f.write(last_result['code'])
                    print(f"💾 Saved to {filename}")
                else:
                    print("❌ No code to save. Generate something first!")
                continue
            
            # Generate code
            result = generator.generate(request, explain_reasoning=not args.no_reasoning)
            last_result = result
            
            # Display
            print("\n" + "="*70)
            print(result['code'])
            print("="*70)
            
            # Ask if satisfied
            satisfied = input("\n✅ Satisfied with this code? (y/n/edit): ").strip().lower()
            
            if satisfied == 'n':
                refinement = input("What would you like to change?: ")
                request_refined = f"{request}. Additionally: {refinement}"
                result = generator.generate(request_refined, explain_reasoning=not args.no_reasoning)
                last_result = result
                print("\n" + "="*70)
                print(result['code'])
                print("="*70)
            
            elif satisfied == 'edit':
                print("\nWhat aspect would you like to adjust?")
                print("1. Make simpler")
                print("2. Add more features")
                print("3. Use different utility")
                print("4. Add tests")
                print("5. Custom edit")
                
                choice = input("Choice (1-5): ").strip()
                
                edits = {
                    '1': f"{request}. Make it simpler with fewer dependencies.",
                    '2': f"{request}. Add more features like error handling, logging, and retry logic.",
                    '3': f"{request}. Use a different utility from the codebase.",
                    '4': f"{request}. Also include unit tests.",
                }
                
                if choice in edits:
                    request_refined = edits[choice]
                elif choice == '5':
                    custom = input("Describe edit: ")
                    request_refined = f"{request}. {custom}"
                else:
                    continue
                
                result = generator.generate(request_refined, explain_reasoning=not args.no_reasoning)
                last_result = result
                print("\n" + "="*70)
                print(result['code'])
                print("="*70)
            
            # Save option
            save = input("\n💾 Save to file? (y/filename/n): ").strip()
            if save.lower() == 'y':
                filename = input("Filename: ")
                with open(filename, 'w') as f:
                    f.write(result['code'])
                print(f"✅ Saved to {filename}")
            elif save.lower() not in ['n', '']:
                with open(save, 'w') as f:
                    f.write(result['code'])
                print(f"✅ Saved to {save}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
