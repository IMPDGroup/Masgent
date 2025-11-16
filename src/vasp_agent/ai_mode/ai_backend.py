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

    system_prompt = '''
You are a VASP expert assistant.

You have access to multiple tools for generating or manipulating VASP-related files such as
POSCAR, INCAR, KPOINTS, POTCAR, structures, supercells, magnetic configurations, and more.

When the user asks for something that can be handled by one of your tools, ALWAYS call that tool.
If the user omits a parameter, infer physically reasonable values before calling any tool.
Do not call the tool with missing values.

If a tool execution returns an error, analyze the error, correct the parameters,
and immediately call the tool again.

After a tool runs, OUTPUT ONLY THE CONTENT OF THE "message" FIELD
from the tool's return value.
Do NOT output the entire dictionary.
Do NOT output "status".
Do NOT output JSON.
Do NOT add explanations, apologies, summaries, or extra text.
Output ONLY the message string.

If a tool returns nothing, output a single short confirmation: "Completed."

If the user asks a conceptual, explanatory, or theoretical question for which no tool applies,
respond normally without calling a tool.

If the user asks something ambiguous or underspecified, ask for clarification.
    '''

    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[
            ai_tools.generate_poscar,
            ai_tools.generate_vasp_inputs_from_poscar,
            ],
        )
    
    mode = asyncio.run(ai_mode(agent))
    return mode

if __name__ == '__main__':
    main()