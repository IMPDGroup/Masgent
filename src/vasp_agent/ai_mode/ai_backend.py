import os, sys
import asyncio
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai import Agent

import vasp_agent.ai_mode.ai_tools as ai_tools

def ask_for_api_key():
    key = input('Enter your OpenAI API key: ').strip()
    if not key:
        print('\nAPI key cannot be empty. Exiting...\n')
        sys.exit(1)

    # Store temporarily for this session
    os.environ['OPENAI_API_KEY'] = key

    # Optional: write to .env so user never needs to type again
    save = input('\nSave this key to .env file for future? (y/n): ').strip().lower()
    if save == 'y':
        with open('.env', 'w') as f:
            f.write(f'OPENAI_API_KEY={key}\n')
        print('\nAPI key saved to .env file.')
        
    print('\nAPI key loaded. Ask anything...\n')

def print_help():
    print('\nVASP-Agent AI usage:')
    print('  Chat with the AI by typing your questions or using specific commands.\n')
    print('Available commands:')
    print('  cli                → Switch to CLI mode')
    print('  help               → Show this help message')
    print('  exit               → Exit the program\n')

async def chat_stream(agent, user_input, history):
    async with agent.run_stream(user_prompt=user_input, message_history=history) as result:
        async for message in result.stream_text(delta=True):
            print(message)
        print('\n')
        return list(result.all_messages())

async def ai_mode(agent):
    history = []
    
    try:
        while True:
            user_input = input('VASP-Agent AI > ').strip().lower()

            if not user_input:
                continue
            
            if user_input in {'exit'}:
                return 'exit-mode'
            elif user_input in {'cli'}:
                return 'cli-mode'
            elif user_input in {'help'}:
                print_help()
            else:
                try:
                    history = await chat_stream(agent, user_input, history)
                except Exception as e:
                    print(f'[Error]: {e}')

    except (KeyboardInterrupt, EOFError):
        print('\nExiting VASP-Agent. Goodbye!\n')
        sys.exit(0)

def main():
    load_dotenv(dotenv_path='.env')

    if 'OPENAI_API_KEY' not in os.environ:
        ask_for_api_key()
    else:
        print('API key found in environment. Ask anything...\n')

    model = OpenAIChatModel(model_name='gpt-5-nano')

    agent = Agent(
        model=model,
        system_prompt='You are a experienced VASP expert assisting users with VASP-related tasks. Provide clear and concise answers to help users effectively.',
        tools=[ai_tools.read_file, ai_tools.list_files, ai_tools.rename_file],
        )
    
    mode = asyncio.run(ai_mode(agent))
    return mode

if __name__ == '__main__':
    main()